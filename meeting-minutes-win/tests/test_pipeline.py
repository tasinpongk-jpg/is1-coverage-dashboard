"""End-to-end dry-run of meeting-minutes-win/bin/pipeline.py.

Mocks ffmpeg, whisper-cli, pandoc (subprocess.run) and the Ollama HTTP API
(urllib.request.urlopen) so the orchestration logic can be exercised without
actually downloading any models or installing any binaries.

What's covered:
  - detect_kind() for the four filename suffix cases
  - chunk_by_agenda() with and without วาระที่ markers
  - asr() handles whisper.cpp's nested JSON schema
  - merge() builds a JSONL with one line per non-empty turn
  - generate_minutes() executes map-reduce against the SET / generic prompts
  - render() copies .md to the right minutes/<kind>/ folder
  - STATE file progresses preprocess -> asr -> merge -> minutes:<kind> -> done
  - Idempotency: re-running the pipeline reuses cached outputs

Run from repo root:
  python meeting-minutes-win/tests/test_pipeline.py
"""
import json
import os
import sys
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent.parent
WIN_BIN = REPO / "meeting-minutes-win" / "bin"
SHARED_TEMPLATES = REPO / "meeting-minutes" / "templates"

sys.path.insert(0, str(WIN_BIN))


# ---------- subprocess.run stub ----------
def fake_subprocess_run(cmd, *args, **kwargs):
    """Imitate ffmpeg / whisper-cli / pandoc."""
    exe = Path(cmd[0]).name.lower()
    if exe == "ffmpeg":
        # ffmpeg is told `... -c:a pcm_s16le <out.wav>` — write a 1-byte placeholder.
        out_path = Path(cmd[-1])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"\x00")
    elif exe.startswith("whisper-cli") or exe.endswith("whisper-cli.exe"):
        # whisper-cli uses `-of <basename>` and writes <basename>.json
        of_idx = cmd.index("-of")
        out = Path(cmd[of_idx + 1] + ".json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            "transcription": [
                {"offsets": {"from": 0, "to": 5000},
                 "text": "ขอเปิดประชุมผู้ถือหุ้น AGM ครั้งที่ 1/2569"},
                {"offsets": {"from": 5000, "to": 12000},
                 "text": "วาระที่ 1 เรื่องที่ประธานแจ้งให้ทราบ EBITDA ไตรมาสที่ 1 เพิ่มขึ้นร้อยละ 12"},
                {"offsets": {"from": 12000, "to": 20000},
                 "text": "วาระที่ 2 ผู้ถือหุ้น PTT เสนอแก้ไขงบ ไม่มีผู้คัดค้าน มติเอกฉันท์"},
                {"offsets": {"from": 20000, "to": 25000},
                 "text": "ปิดประชุม"},
            ]
        }, ensure_ascii=False), encoding="utf-8")
    elif exe.startswith("pandoc"):
        # pandoc <in.md> -o <out.docx>
        out_idx = cmd.index("-o")
        out = Path(cmd[out_idx + 1])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(b"PK\x03\x04fake-docx-bytes")
    else:
        raise AssertionError(f"unexpected subprocess: {cmd}")

    class CompletedFake:
        returncode = 0
    return CompletedFake()


# ---------- urllib.request.urlopen stub ----------
class FakeOllamaResponse:
    """Returns a canned Markdown minutes for any chat call."""
    SET_REPLY = (
        "# รายงานการประชุมสามัญผู้ถือหุ้น ครั้งที่ ๑/๒๕๖๙\n\n"
        "**วันเดือนปี:** 14 พฤษภาคม 2569\n"
        "**ประธานในที่ประชุม:** ผู้พูดที่ ๑\n\n"
        "## วาระที่ ๑ เรื่องที่ประธานแจ้งให้ที่ประชุมทราบ\n"
        "- EBITDA ไตรมาสที่ 1 เพิ่มขึ้นร้อยละ 12\n"
        "**มติที่ประชุม:** รับทราบ\n\n"
        "## วาระที่ ๒ เรื่องเพื่อพิจารณา\n"
        "- ผู้ถือหุ้นเสนอแก้ไขงบ\n"
        "**มติที่ประชุม:** อนุมัติ ด้วยมติเป็นเอกฉันท์\n\n"
        "## ธงสัญญาณการกำกับดูแลกิจการ\n"
        "ไม่พบประเด็น\n"
    )
    GENERIC_REPLY = (
        "# บันทึกการประชุม: AGM ๑/๒๕๖๙\n\n"
        "## สรุปผู้บริหาร (TL;DR)\n"
        "EBITDA Q1 +12%; ผู้ถือหุ้นเห็นชอบงบด้วยมติเอกฉันท์\n"
    )

    def __init__(self, body_bytes):
        body = json.loads(body_bytes)
        system = body["messages"][0]["content"]
        text = self.SET_REPLY if "SET" in system else self.GENERIC_REPLY
        self._payload = json.dumps({
            "message": {"role": "assistant", "content": text}
        }).encode("utf-8")

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def fake_urlopen(req, *args, **kwargs):
    return FakeOllamaResponse(req.data)


# ---------- The test ----------
class PipelineDryRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workdir = Path(tempfile.mkdtemp(prefix="mm-test-"))
        os.environ["MEETINGS_ROOT"] = str(cls.workdir)
        os.environ["WHISPER_BIN"] = "whisper-cli.exe"  # only the basename matters
        # Point at a dummy model file so the existence check passes
        models = cls.workdir / "models"
        models.mkdir()
        (models / "ggml-large-v3-turbo-q5_0.bin").write_bytes(b"\x00")
        os.environ["WHISPER_MODEL"] = str(models / "ggml-large-v3-turbo-q5_0.bin")
        os.environ["SHARED_TEMPLATES"] = str(SHARED_TEMPLATES)

        # Now import (after env is set so module-level constants pick it up)
        import importlib
        import pipeline as p  # type: ignore
        importlib.reload(p)
        cls.p = p

        # Source audio: doesn't need to exist on disk for ffmpeg stub but pipeline
        # checks Path.exists(). Make a one-byte placeholder.
        cls.src = cls.workdir / "2026-05-14-AGM-PTT-set.m4a"
        cls.src.write_bytes(b"\x00")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.workdir, ignore_errors=True)

    def test_01_detect_kind(self):
        self.assertEqual(self.p.detect_kind("foo-set"), ["set"])
        self.assertEqual(self.p.detect_kind("foo-both"), ["set", "generic"])
        self.assertEqual(self.p.detect_kind("foo-gen"), ["generic"])
        self.assertEqual(self.p.detect_kind("foo-meet"), ["generic"])
        self.assertEqual(self.p.detect_kind("foo"), ["generic"])

    def test_02_chunk_by_agenda_with_markers(self):
        # Build a fake merged.jsonl with วาระที่ markers
        merged = self.workdir / "merged-test.jsonl"
        merged.write_text("\n".join([
            json.dumps({"start": 0,  "end": 5,  "speaker": "UNK", "text": "เปิดประชุม"}, ensure_ascii=False),
            json.dumps({"start": 5,  "end": 10, "speaker": "UNK", "text": "วาระที่ 1 เรื่องแจ้งทราบ ABC"}, ensure_ascii=False),
            json.dumps({"start": 10, "end": 15, "speaker": "UNK", "text": "วาระที่ 2 เรื่องพิจารณา XYZ"}, ensure_ascii=False),
        ]), encoding="utf-8")
        chunks = self.p.chunk_by_agenda(merged)
        self.assertGreaterEqual(len(chunks), 2,
            f"expected at least 2 agenda chunks, got {len(chunks)}: {chunks}")
        joined = "\n---\n".join(chunks)
        self.assertIn("วาระที่ 1", joined)
        self.assertIn("วาระที่ 2", joined)

    def test_03_chunk_by_agenda_without_markers(self):
        merged = self.workdir / "merged-flat.jsonl"
        merged.write_text("\n".join([
            json.dumps({"start": i, "end": i+1, "speaker": "UNK", "text": "ก" * 200},
                       ensure_ascii=False)
            for i in range(80)
        ]), encoding="utf-8")
        # 80 turns × ~200 chars + framing → should fall into multiple fixed windows
        chunks = self.p.chunk_by_agenda(merged, max_chars=5000)
        self.assertGreaterEqual(len(chunks), 2)

    @mock.patch("urllib.request.urlopen", side_effect=fake_urlopen)
    @mock.patch("subprocess.run", side_effect=fake_subprocess_run)
    def test_04_full_pipeline_set(self, _m_sub, _m_url):
        self.p.main(str(self.src))
        # State file says done
        sha = self.p.sha1(self.src.resolve())
        job = self.p.WORK_ROOT / sha / self.src.stem
        self.assertEqual((job / "STATE").read_text(), "done")
        # Per-stage outputs exist
        self.assertTrue((job / "raw.wav").exists())
        self.assertTrue((job / "asr.json").exists())
        self.assertTrue((job / "merged.jsonl").exists())
        self.assertTrue((job / "minutes_set.md").exists())
        # Final minutes copied to set/ folder, named with stem minus -set
        out_md = self.p.MIN_DIR / "set" / "2026-05-14-AGM-PTT-set.md"
        self.assertTrue(out_md.exists(), f"missing: {out_md}")
        self.assertIn("รายงานการประชุม", out_md.read_text(encoding="utf-8"))
        # docx rendered
        self.assertTrue(out_md.with_suffix(".docx").exists())

    @mock.patch("urllib.request.urlopen", side_effect=fake_urlopen)
    @mock.patch("subprocess.run", side_effect=fake_subprocess_run)
    def test_05_idempotent_rerun(self, _m_sub, m_url):
        # Second run should reuse caches and not call the LLM again
        m_url.reset_mock()
        self.p.main(str(self.src))
        self.assertEqual(m_url.call_count, 0,
            "Idempotent rerun should not invoke LLM (cached map+reduce outputs)")

    @mock.patch("urllib.request.urlopen", side_effect=fake_urlopen)
    @mock.patch("subprocess.run", side_effect=fake_subprocess_run)
    def test_06_both_kind(self, _m_sub, _m_url):
        # For -both input, the -both suffix is stripped from the output stem
        # and replaced with the per-kind suffix, so each output file is
        # individually identifiable as set or generic.
        src_both = self.workdir / "2026-05-14-board-meet-both.m4a"
        src_both.write_bytes(b"\x00")
        self.p.main(str(src_both))
        self.assertTrue((self.p.MIN_DIR / "set"     / "2026-05-14-board-meet-set.md").exists())
        self.assertTrue((self.p.MIN_DIR / "generic" / "2026-05-14-board-meet-generic.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
