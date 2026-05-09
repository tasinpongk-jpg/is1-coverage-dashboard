-- ~/.hammerspoon/init.lua  — meeting recorder toggle (Cmd+Shift+R)
--
-- Behavior: on toggle-on, ffmpeg starts recording the configured avfoundation
-- input device to ~/Meetings/live/<timestamp>-meet.wav. On toggle-off, ffmpeg
-- exits gracefully (SIGINT — never SIGKILL on BlackHole) and the file is moved
-- into ~/Meetings/inbox/. With no template suffix it processes as "generic";
-- rename to add `-set` or `-both` BEFORE launchd's debounce window if you want
-- the SET-style template, or ask Cowork to rename and re-trigger.

local recPid, recFile = nil, nil
local menubar = hs.menubar.new()
menubar:setTitle("●")
menubar:setTooltip("Idle")

-- Toggle source: ":0" mic only; ":2" Mic+BH aggregate (requires Audio MIDI Setup).
-- Run `ffmpeg -f avfoundation -list_devices true -i ""` to confirm the index.
local DEVICE = ":2"
local LIVE   = os.getenv("HOME") .. "/Meetings/live"
local INBOX  = os.getenv("HOME") .. "/Meetings/inbox"

local function outPath()
  hs.execute("mkdir -p '" .. LIVE .. "'")
  local stamp = os.date("%Y%m%d-%H%M%S")
  return LIVE .. "/" .. stamp .. "-meet.wav"
end

local function startRec()
  recFile = outPath()
  local cmd = string.format(
    "/opt/homebrew/bin/ffmpeg -y -f avfoundation -i '%s' " ..
    "-filter_complex '[0:a]pan=mono|c0=0.5*c0+0.5*c1+0.5*c2+0.5*c3[a]' " ..
    "-map '[a]' -ar 16000 -c:a pcm_s16le '%s' " ..
    "</dev/null >/tmp/ffrec.log 2>&1 & echo $!", DEVICE, recFile)
  recPid = tonumber(hs.execute(cmd):match("(%d+)"))
  menubar:setTitle("🔴 REC")
  menubar:setTooltip("Recording → " .. recFile)
  hs.alert.show("Recording started")
end

local function stopRec()
  if recPid then
    -- graceful stop; SIGKILL would corrupt BlackHole's output
    hs.execute("kill -INT " .. recPid)
    hs.timer.doAfter(2, function()
      hs.execute(string.format("mkdir -p '%s' && mv '%s' '%s/'",
                               INBOX, recFile, INBOX))
      hs.alert.show("Recording saved → inbox")
    end)
    recPid = nil
    menubar:setTitle("●")
    menubar:setTooltip("Idle")
  end
end

hs.hotkey.bind({"cmd", "shift"}, "R", function()
  if recPid then stopRec() else startRec() end
end)

hs.alert.show("Hammerspoon meeting-rec ready (⌘⇧R)")
