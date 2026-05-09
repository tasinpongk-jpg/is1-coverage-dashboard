# Audio routing setup (one-time)

The pipeline records the host Mac's microphone *and* whatever audio your
system is playing (Zoom, Teams, browser tab, Keynote). On macOS, capturing
both into a single ffmpeg input requires two virtual audio devices:
**Multi-Output** so you can still hear yourself + remote audio, and
**Aggregate** so ffmpeg sees one combined input.

This is GUI-only — Cowork cannot do it for you.

## Prerequisites

```bash
brew install --cask blackhole-2ch
sudo killall coreaudiod    # registers the kext without reboot
```

## Step 1 — Multi-Output Device

So you can still hear remote-meeting audio while BlackHole captures it.

1. Open **Audio MIDI Setup** (in `/Applications/Utilities/`).
2. Bottom-left **+** → **Create Multi-Output Device**.
3. Tick **MacBook Pro Speakers** (or your headphones output) AND
   **BlackHole 2ch**. Set both to **48000 Hz**.
4. **Master Device** = MacBook Pro Speakers. Tick **Drift Correction** on the
   BlackHole row (and only on BlackHole).
5. Right-click the new device in the sidebar → **Use This Device For Sound
   Output**.

When recording a video call, also set System Settings → Sound → Output to
this Multi-Output Device. Your meeting app can keep its own input/output
selection (set those to Microphone + Multi-Output if needed).

## Step 2 — Aggregate Device "Mic+BH"

So ffmpeg sees mic + system audio as one stream.

1. **+** → **Create Aggregate Device**.
2. Tick **MacBook Pro Microphone** AND **BlackHole 2ch**.
3. **Clock Source** = MacBook Pro Microphone. Tick **Drift Correction** on
   the BlackHole row.
4. Rename the device to `Mic+BH` (no spaces).

## Step 3 — Confirm avfoundation index

```bash
ffmpeg -f avfoundation -list_devices true -i "" 2>&1 | grep -E "Microphone|BlackHole|Mic\+BH"
```

You'll see something like:

```
[AVFoundation indev @ 0x...] AVFoundation audio devices:
[AVFoundation indev @ 0x...] [0] MacBook Pro Microphone
[AVFoundation indev @ 0x...] [1] BlackHole 2ch
[AVFoundation indev @ 0x...] [2] Mic+BH
```

Note the index of `Mic+BH` (commonly `2`). The Hammerspoon recorder hardcodes
`:2` — if yours differs, edit `~/.hammerspoon/init.lua`:

```lua
local DEVICE = ":2"   -- change this number
```

…and click the Hammerspoon menubar → **Reload Config**.

## Step 4 — Quick test

```bash
ffmpeg -y -f avfoundation -i ":2" \
  -filter_complex '[0:a]pan=mono|c0=0.5*c0+0.5*c1+0.5*c2+0.5*c3[a]' \
  -map '[a]' -ar 16000 -c:a pcm_s16le \
  -t 5 /tmp/test.wav
afplay /tmp/test.wav    # should hear yourself + any system audio you played
```

If the file is silent, check:
- TCC: System Settings → Privacy & Security → Microphone → Terminal allowed?
- Output: System Settings → Sound → Output set to Multi-Output Device?
- Sample rates: both subdevices at 48000 Hz?
- Drift correction: enabled on BlackHole rows in both devices?

## Common pitfalls

- **Recording is silent for the system-audio half.** You forgot to switch
  System Output to the Multi-Output Device. Apps default to "system output"
  for playback, and that's what BlackHole captures.
- **Recording is silent for the mic half.** You revoked Microphone permission
  for Terminal (or Hammerspoon, if you're using the hotkey).
- **Crackling / clock drift on long meetings.** Drift correction wasn't
  enabled on BlackHole. The drift accumulates on >30-min recordings.
- **Hammerspoon hotkey records 0 bytes.** Either Hammerspoon doesn't have
  Accessibility, or `DEVICE = ":2"` doesn't match your aggregate index.
