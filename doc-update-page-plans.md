# STEP Series Documentation — Page-by-Page Update Plans

**Companion to:** `doc-update-ground-plan.md`
**Convention:** Each page lists Add / Change / Remove / Fix items. "Fix" covers
typos, grammar, terminology alignment, and link corrections.

Items marked [v2.1.0] should include a version admonition in the text.
Items marked [TERM] are terminology glossary alignment.

---

## 0. All Pages (global pass)

Apply after individual page updates are complete:

- [ ] Fix: "sensers" → "sensors" anywhere it appears
- [ ] Fix: "Electromagnet brake" → "Electromagnetic brake" in titles/body
- [ ] Fix: All internal links — verify language (EN links on EN pages, JA on JA)
- [ ] Fix: First mention of "OSC" on each page should expand to "OSC (Open Sound Control)"
- [ ] Fix: Consistent capitalization: "PowerSTEP01" (not "powerSTEP01"), "microSD" (not "micro SD")
- [ ] Fix: "configTool" references → specify which tool (browser config tool or old STEP400/800 tool)
- [ ] Fix: "STEP400/800" section title → "STEP Series" (top-level only)
- [ ] Add: Where a page references a specific firmware version, use consistent admonition format

---

## 1. Getting Started (currently "Tutorial")

**Rename:** "Tutorial" → "Getting Started"

- [ ] Change: Review flow — does it walk a new user from unboxing to first motor movement?
- [ ] Fix: Any references to "config.txt" should note that long filenames are now supported [v2.1.0]
- [ ] Add: Mention the browser config tool as an alternative to manual SD editing [v2.1.0]
- [ ] Fix: [TERM] alignment pass

**Note:** This page is likely fine content-wise. The rename is the main change.

---

## 2. Connections and Settings

### 2.1 Power Supply and Motor

- [ ] Fix: Grammar/clarity pass (the current page is well-structured but has some awkward phrasing)
- [ ] Fix: [TERM] "motor driver" → "driver IC" where referring to the chip specifically
- [ ] Change: Nothing substantive expected — flag any errors found during review

### 2.2 Sensors and Switches (currently "Sensor and Switch")

**Rename:** "Sensor and Switch" → "Sensors and Switches"

- [ ] Fix: [TERM] alignment pass
- [ ] Fix: Verify HOME/LIMIT sensor terminology is consistent with OSC command reference pages

### 2.3 Network and DIP Switch (currently "Network and the DIP switch")

**Rename:** Drop "the" — "Network and DIP Switch"

- [ ] Fix: References to "configTool" — clarify which tool
- [ ] Fix: Grammar/clarity pass

### 2.4 Configuration with microSD Card (currently "Setup with a microSD card")

**Rename:** "Setup with a microSD card" → "Configuration with microSD Card"

Major updates needed:

- [ ] Change: Remove the statement "the file extension is changed to .txt instead of .json because it can only contain three characters for the extension" — this is no longer true [v2.1.0]
- [ ] Add: [v2.1.0] Long filename support — config files can now use descriptive names like `STEP400_venue-A.json`
- [ ] Add: [v2.1.0] File discovery priority: firmware looks for `config.txt` first (backward compatibility), then falls back to the alphabetically first `.json` file on the card
- [ ] Add: [v2.1.0] SD library changed from Arduino SD to SdFat v2
- [ ] Change: Update the config tool reference — the page currently describes only the old per-product HTML tools. Add reference to the new browser config tool. Keep old tool links but note they are for firmware <2.1.0.
- [ ] Add: [v2.1.0] `/saveConfig` OSC command can save running config to SD without removing the card
- [ ] Fix: The sentence "Copy this file to the top level of the microSD card" — clarify that the file goes in the root directory
- [ ] Fix: [TERM] "micro SD" → "microSD" throughout

### 2.5 Configuration with Browser Tool [NEW PAGE]

Write from scratch. Content outline:

- [ ] Add: Introduction — what the tool does (read, edit, save board config via USB)
- [ ] Add: Requirements — Chrome or Edge browser (Web Serial API), USB cable
- [ ] Add: Connecting — click Connect, select serial port, config loads automatically
- [ ] Add: Editing — sections are collapsible panels, per-axis parameters as columns
- [ ] Add: Saving to SD — saves running config back to the board's SD card
- [ ] Add: Offline mode — load/save JSON files without serial connection (for pre-staging configs)
- [ ] Add: Filename support — editable config name field, firmware discovers by priority
- [ ] Add: Status monitoring — real-time motor status polling
- [ ] Add: Troubleshooting — browser compatibility (no Firefox/Safari), connection issues
- [ ] Add: Link to hosted tool URL (TBD: `/tools/step-config/` or similar)
- [ ] Add: Link to microSD card page for config file format details
- [ ] Add: Note about old config tools — link to STEP400/STEP800 tools for firmware <2.1.0
- [ ] Add: Note this requires firmware v2.1.0 or later

### 2.6 Example Parameters for Sample Motors (currently "Example parameter values for example steppers")

**Rename:** Shorten title

- [ ] Change: Remove the instruction "the name must be changed to config.txt when copying to microSD" — update to explain that any `.json` filename works with firmware v2.1.0+, and `config.txt` remains required for older firmware [v2.1.0]
- [ ] Fix: Grammar/clarity pass
- [ ] Fix: [TERM] alignment

---

## 3. Functional Descriptions

### 3.1 Voltage Mode and Current Mode

- [ ] Fix: Grammar/clarity pass
- [ ] Fix: [TERM] "STEP 400" → "STEP400" (if space found)
- [ ] Change: Nothing major expected unless errors are found during review

### 3.2 Speed Profile and Motion Types (currently "Speed profile and types of motor motion")

**Rename:** Shorten title

- [ ] Fix: Grammar/clarity pass
- [ ] Fix: [TERM] alignment

### 3.3 Homing and Position Management

- [ ] Fix: Current text has some awkward phrasing ("the sensor state have not changed" → "the sensor state has not changed")
- [ ] Fix: "configTool" → specify which tool
- [ ] Fix: [TERM] alignment

### 3.4 Servo Mode

- [ ] Fix: Grammar/clarity pass
- [ ] Fix: [TERM] alignment

---

## 4. OSC Command Reference

### 4.0 OSC Command Reference (index page)

- [ ] Fix: Current intro text has useful info about argument types — review for accuracy
- [ ] Fix: "with of without notification" → "with or without notification" (if this text appears on this page)
- [ ] Add: Link to the new "Command List (Quick Reference)" page at the top

### 4.1 Command List (Quick Reference) [NEW PAGE]

Write from scratch. Content:

- [ ] Add: Introduction — purpose of this page, how to use it
- [ ] Add: Table of ALL commands organized by category (see ground plan section C3)
- [ ] Add: Categories: System & network, Configuration & reporting, Motor driver setup, Voltage/current mode, Speed & acceleration, Motion commands, Combined (multi-motor), Homing & switches, Position, Servo mode, Electromagnetic brake, Status queries
- [ ] Add: Each row: Command name (linked to detail page), Direction (→ send / ← receive), Arguments summary, STEP400 ✓/✗, STEP800 ✓/✗
- [ ] Add: Commands may appear in multiple categories
- [ ] Add: Version badges for commands added in specific versions (e.g., `/saveConfig` → "v2.1.0")
- [ ] Add: Note at top: "For detailed descriptions, click the command name to go to the relevant page"

**Source:** Cross-reference `oscListeners.h` declarations against all existing doc pages.

### 4.2 Automatically Sent Messages from the Device

- [ ] Fix: Grammar/clarity pass — "with of without notification" → "with or without notification"
- [ ] Fix: [TERM] alignment
- [ ] Change: Verify completeness against firmware — are all auto-sent messages documented?

### 4.3 System Settings

- [ ] Add: [v2.1.0] `/saveConfig` command — new command, saves running configuration to SD card. No arguments. Returns confirmation message. Requires SD card to be present.
- [ ] Change: [v2.1.0] `/getConfigName` — document the new 5th argument `configFilename` (the on-disk filename, distinct from the user-editable `configName`)
- [ ] Fix: Grammar/clarity pass
- [ ] Fix: [TERM] alignment

### 4.4 Motor Driver Settings

- [ ] Fix: Grammar/clarity pass
- [ ] Fix: "Switches the micro stepping mode" → "Sets the microstepping mode"
- [ ] Fix: [TERM] alignment
- [ ] Change: Verify all commands from the firmware audit are documented:
  - setMicrostepMode, getMicrostepMode ✓
  - setHomeSwMode, getHomeSwMode ✓
  - setLimitSwMode, getLimitSwMode ✓
  - getHomingStatus — verify documented here or in Homing page
  - setStallThreshold, getStallThreshold ✓
  - setOverCurrentThreshold, getOverCurrentThreshold ✓
  - setLowSpeedOptimizeThreshold, getLowSpeedOptimizeThreshold ✓
  - enableLowSpeedOptimize ✓
  - setBemfParam, getBemfParam — verify documented here or in Voltage/Current page

### 4.5 Alarm Settings

- [ ] Fix: "ULVO" → "UVLO" (typo appears in current text: "When ULVO occurs")
- [ ] Fix: "with of without notification" → "with or without notification"
- [ ] Fix: "the motor state will automatically enters" → "the motor state will automatically enter"
- [ ] Fix: "On the Bridge shutdown" → "On bridge shutdown" (article consistency)
- [ ] Fix: [TERM] alignment
- [ ] Change: Verify all enable* report commands are documented

### 4.6 Voltage and Current Mode Settings

- [ ] Add: Individual KVAL setter commands (currently undocumented):
  - `/setHoldKval (int)motorID (int)holdKVAL` — Sets only the hold KVAL
  - `/setRunKval (int)motorID (int)runKVAL` — Sets only the run KVAL
  - `/setAccKval (int)motorID (int)accKVAL` — Sets only the acceleration KVAL
  - `/setDecKval (int)motorID (int)decKVAL` — Sets only the deceleration KVAL
  - Add note: "See also `/setKval` to set all four at once."
- [ ] Add: Individual TVAL setter commands (currently undocumented, PowerSTEP01 only):
  - `/setHoldTval (int)motorID (int)holdTVAL`
  - `/setRunTval (int)motorID (int)runTVAL`
  - `/setAccTval (int)motorID (int)accTVAL`
  - `/setDecTval (int)motorID (int)decTVAL`
  - Add note: "See also `/setTval` to set all four at once."
- [ ] Fix: "In STEP 400, the TVAL is as follows" → [TERM] fix spacing
- [ ] Fix: "setDecKVAL" argument in `/setKval` listing — verify correct naming
- [ ] Fix: [TERM] alignment
- [ ] Fix: Grammar/clarity pass

### 4.7 Speed Profile

- [ ] Add: Raw variant commands (currently undocumented):
  - `/setSpeedProfileRaw (int)motorID (int)acc (int)dec (int)maxSpeed` — Sets speed profile using raw register values
  - `/setMaxSpeedRaw (int)motorID (int)maxSpeed`
  - `/setMinSpeedRaw (int)motorID (int)minSpeed`
  - `/setFullstepSpeedRaw (int)motorID (int)fullstepSpeed`
  - `/setAccRaw (int)motorID (int)acc`
  - `/setDecRaw (int)motorID (int)dec`
  - `/getSpeedProfileRaw (int)motorID` — returns raw register values
  - Add note: "Raw commands set/get the driver IC register values directly without unit conversion. For most users, the standard commands (in steps/s and steps/s²) are recommended."
- [ ] Fix: Grammar/clarity pass
- [ ] Fix: [TERM] alignment

### 4.8 Homing

- [ ] Fix: "/setHomingDirectionand" → "/setHomingDirection and" (missing space)
- [ ] Fix: "from setReleaseSwTimeout command" → "from the /setReleaseSwTimeout command" (add article and slash)
- [ ] Fix: [v2.1.0] Note the `goUntilTimeout` typo fix — old STEP400 configs had `goUnitlTimeout` which was silently ignored. Fixed in v2.1.0.
- [ ] Fix: Grammar/clarity pass throughout
- [ ] Fix: [TERM] alignment

### 4.9 HOME and LIMIT Sensors (currently "HOME and LIMIT sensers")

**Rename:** Fix typo "sensers" → "Sensors"

- [ ] Fix: [TERM] alignment
- [ ] Fix: Grammar/clarity pass

### 4.10 Position Management

- [ ] Fix: "Returns the current position of all motors at once. /getPosition 255 returns individual messages for each motors but this command returns single message with a position list." — grammar cleanup
- [ ] Fix: [TERM] alignment
- [ ] Change: Verify setElPos / getElPos are documented (they're in the firmware)

### 4.11 Motor Control

- [ ] Fix: "the motor reached to the specified speed" → "the motor reaches the specified speed"
- [ ] Fix: "until reaches to the specified step counts" → "until it reaches the specified step count"
- [ ] Fix: "In motion start condition" — clarify what this means (prerequisite? state?)
- [ ] Add: Raw motion variant commands (currently undocumented):
  - `/runRaw (int)motorID (int)speed` — raw register value for speed
  - `/goUntilRaw (int)motorID (int)action (int)dir (int)speed` — raw speed value
  - `/combinedRunRaw speed1 ... speedN` — combined raw run
  - Add note: "Raw commands use driver IC register values directly."
- [ ] Fix: [TERM] alignment
- [ ] Fix: Grammar/clarity pass

### 4.12 Electromagnetic Brake (currently "Electromagnet brake")

**Rename:** "Electromagnet brake" → "Electromagnetic Brake"

- [ ] Fix: [TERM] alignment
- [ ] Fix: Grammar/clarity pass
- [ ] Change: Verify activate/free commands are documented

### 4.13 Servo Mode (OSC reference)

- [ ] Fix: Grammar/clarity pass
- [ ] Fix: [TERM] alignment
- [ ] Change: Verify setTargetPositionList is documented

---

## 5. Differences Between STEP400 and STEP800

**Move:** From top level into "Technical Information" section.

- [ ] Change: Update the command list to include any newly documented commands (individual KVAL/TVAL setters, raw variants) and note which are STEP400-only
- [ ] Fix: "setDecTVAL" in `/setTval` argument list — verify consistency
- [ ] Fix: [TERM] alignment
- [ ] Fix: Grammar/clarity pass
- [ ] Add: Note that STEP100/STEP200 share characteristics with STEP400/STEP800 respectively (same driver ICs)

---

## 6. Technical Information

### 6.1 Firmware Update (currently "The firmware update")

**Rename:** Drop "The"

- [ ] Fix: Grammar/clarity pass
- [ ] Add: [v2.1.0] Note that v2.1.0 is the latest version, link to GitHub Releases
- [ ] Fix: [TERM] alignment

### 6.2 Compiling the Firmware (currently "Compiling the Arduino sketch")

**Rename:** "Compiling the Arduino sketch" → "Compiling the Firmware"

- [ ] Change: [v2.1.0] Note that the Arduino IDE sketch folder is no longer included in the repo; download pre-built `.ino` from GitHub Releases instead
- [ ] Change: [v2.1.0] Update dependency list — `greiman/SdFat` v2 replaces `arduino-libraries/SD`
- [ ] Change: Emphasize PlatformIO as the primary build method (it already is, but make this clearer)
- [ ] Fix: [TERM] alignment
- [ ] Fix: Grammar/clarity pass

### 6.3 USB Serial Diagnosis (currently "Diagnosis via USB serial port")

**Rename:** Shorten title

- [ ] Add: [v2.1.0] New serial commands:
  - `G` — Get config as JSON (used by browser config tool)
  - `T` — Get real-time motor/board status as JSON
  - `{...}` — Write config JSON to SD card
  - `R` — Reboot the board
  - `F<filename>` — Set the config filename for next save
- [ ] Add: Note that these commands are used by the browser config tool but can also be used directly from any serial terminal
- [ ] Fix: [TERM] alignment
- [ ] Fix: Grammar/clarity pass

### 6.4 Differences Between STEP400 and STEP800 [MOVED]

(See section 5 above)

### 6.5 Firmware Changelog [NEW PAGE]

Write from scratch:

- [ ] Add: v2.1.0 changes (from v2.1.0-release-notes.md)
- [ ] Add: v2.0.0 changes (from GitHub Releases / Discussion #38)
- [ ] Add: Earlier version history if available
- [ ] Add: Links to GitHub Releases for each version
- [ ] Add: Migration notes between versions (especially v2.0.0 → v2.1.0 config changes)

---

## 7. Hardware Pages

### 7.1 Hardware – STEP400
### 7.2 Hardware – STEP800

- [ ] Fix: [TERM] alignment
- [ ] Fix: Grammar/clarity pass
- [ ] Change: No substantive updates expected unless errors found

---

## Implementation Notes

### Priority order

1. **New pages first** — Browser config tool, Command list, Firmware changelog (highest user impact)
2. **Major updates** — microSD card, System settings, Voltage/current mode, Speed profile (v2.1.0 content)
3. **Undocumented commands** — individual KVAL/TVAL, raw variants (completeness)
4. **Renames and fixes** — terminology, grammar, links (quality)

### EN/JA handling

- Write EN version first for each page
- Kanta reviews EN, then creates/updates JA independently
- Some pages may have JA-specific phrasing issues — flag during EN review

### Handoff to Claude Code

Each page update can be a separate Claude Code task:
- Provide the page's current Markdown file + this update plan
- Claude Code produces the updated Markdown
- Kanta reviews diff and merges

### Tracking

Use this document as a checklist. Mark items `[x]` as they are completed.
