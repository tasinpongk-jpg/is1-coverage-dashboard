"""Build a multipart/mixed MIME message with attachment, send via himalaya SMTP.

Himalaya v2.0 has no inline MML processing (skill docs are misleading);
you have to provide a pre-compiled RFC 5322 message. The himalaya
message send subcommand accepts a file or stdin containing the raw
message (with headers + body + MIME parts).
"""
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
import mimetypes
import subprocess
import sys
from pathlib import Path

ATTACHMENTS = [
    Path("C:/Users/Tasinpong/projects/is1-coverage-dashboard/6M26-deck.pptx"),
    Path("C:/Users/Tasinpong/projects/is1-coverage-dashboard/6M26-deck-mockup.html"),
]

BODY = """Hi,

Deck rebuilt — 18 slides. Only F1 and F4 show confirmed numbers
from the control CSV; the other 12 segments show explicit "รอข้อมูล"
placeholder slides per spec rule (no fake numbers).

Files:
  6M26-deck.pptx (61 KB) - 18 slides editable
  6M26-deck-mockup.html (26 KB) - same content in HTML for browser view

18 slides:
  1. Cover (CONFIRMED: F1, F4; PENDING: 12 segments)
  2. Sector Overview (only F1 + F4 confirmed; 12 segments amber)
  3. F1 - CONFIRMED with full data + Top 5 + analyst view
  4. F4 - CONFIRMED with full data + Top 5 + analyst view
  5-16. PENDING slides for F2, F3, F5-F9, P1-P5
        (รอข้อมูล placeholder, no fake numbers)
  17. Outlook & Investment Implications (general themes only)
  18. Methodology & Data Status

Per spec rule: "Do NOT estimate, interpolate, or carry forward a
prior-period figure to fill a gap - leave it blank." Hence the 12
pending slides. Once fill_from_control.py runs against the real CSV,
those slides will populate with real data.

Confirmed numbers:
  F1 โปรตีนจากสัตว์ครบวงจร: 386,480 mb (-3.2% YoY)
  F4 เครื่องดื่มแบรนด์: 43,279 mb (-2.0% YoY)

Other 12 segments need fill_from_control.py before they have numbers.

3 locations:
  - C:\\Users\\Tasinpong\\projects\\is1-coverage-dashboard\\
  - OneDrive Deliverables (synced)
  - This email

- Hermes
"""

msg = EmailMessage()
msg["From"] = "jarvis4champ@gmail.com"
msg["To"] = "tasinpong.k@gmail.com"
msg["Subject"] = "6M26 deck corrected - F1+F4 confirmed, 12 segments marked 'รอข้อมูล'"
msg["Date"] = formatdate(localtime=True)
msg["Message-ID"] = make_msgid(domain="hermes.local")
msg.set_content(BODY)

for ATTACHMENT in ATTACHMENTS:
    if not ATTACHMENT.is_file():
        print(f"WARNING: {ATTACHMENT} not found, skipping", file=sys.stderr)
        continue
    ctype, encoding = mimetypes.guess_type(ATTACHMENT.name)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    msg.add_attachment(
        ATTACHMENT.read_bytes(),
        maintype=maintype,
        subtype=subtype,
        filename=ATTACHMENT.name,
    )

raw = msg.as_bytes()
print(f"Built MIME message: {len(raw)} bytes, {len(msg.as_string())} chars")
print(f"Attachments: {len(ATTACHMENTS)} files")
for a in ATTACHMENTS:
    print(f"  - {a.name}: {a.stat().st_size:,} bytes")

# Write to a Windows-native path that himalaya can find (bash /tmp resolves
# to /tmp under git-bash, but himalaya wants a real file on the Windows fs)
import os
out_dir = os.environ.get("USERPROFILE") or os.path.expanduser("~")
out_path = Path(out_dir) / "q2-harvest-email.mime"
out_path.write_bytes(raw)
print(f"Wrote {out_path}")

# Send via himalaya — v2 requires `--` separator before the MESSAGE arg
result = subprocess.run(
    ["himalaya", "message", "send", "--", str(out_path)],
    capture_output=True,
    text=True,
    timeout=60,
)
print(f"stdout: {result.stdout}")
print(f"stderr: {result.stderr}")
print(f"exit: {result.returncode}")
sys.exit(result.returncode)