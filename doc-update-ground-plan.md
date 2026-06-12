# STEP Series Documentation — Ground Update Plan

**Date:** June 2026
**Scope:** All pages in the `docs/step-series/` section (EN + JA)
**Source of truth:** GitHub Markdown in `ponoor/step-series-support`
**Publish target:** ponoor.com via WordPress REST API

---

## A. Current Document Structure

Based on the ponoor.com sidebar:

```
STEP400/800
├── Tutorial
├── Connections and settings
│   ├── Power supply and Motor
│   ├── Sensor and Switch
│   ├── Network and the DIP switch
│   ├── Setup with a microSD card
│   └── Example parameter values for example steppers
├── Functional descriptions
│   ├── Voltage mode and current mode
│   ├── Speed profile and types of motor motion
│   ├── Homing and position management
│   └── Servo mode
├── OSC command reference
│   ├── Automatically sent messages from the device
│   ├── System settings
│   ├── Motor driver settings
│   ├── Alarm settings
│   ├── Voltage and current mode settings
│   ├── Speed profile
│   ├── Homing
│   ├── HOME and LIMIT sensors
│   ├── Position management
│   ├── Motor control
│   ├── Electromagnet brake
│   └── Servo mode
├── Differences between STEP400 and STEP800
└── Technical information
    ├── The firmware update
    ├── Compiling the Arduino sketch
    └── Diagnosis via USB serial port
```

---

## B. Proposed Updated Structure

Changes marked: [NEW], [UPDATED], [RENAMED], [MOVED]

```
STEP Series                                          [RENAMED from "STEP400/800"]
├── Getting started                                  [RENAMED from "Tutorial"]
├── Connections and settings
│   ├── Power supply and motor
│   ├── Sensors and switches                         [RENAMED: plural alignment]
│   ├── Network and DIP switch
│   ├── Configuration with microSD card              [UPDATED: long filename, discovery]
│   ├── Configuration with browser tool              [NEW: Web Serial config tool v2.0]
│   └── Example parameters for sample motors         [RENAMED: clarity]
├── Functional descriptions
│   ├── Voltage mode and current mode
│   ├── Speed profile and motion types               [RENAMED: shorter]
│   ├── Homing and position management
│   └── Servo mode
├── OSC command reference
│   ├── Command list (quick reference)               [NEW: single-page table of all commands]
│   ├── Automatically sent messages
│   ├── System settings                              [UPDATED: /saveConfig, /getConfigName]
│   ├── Motor driver settings
│   ├── Alarm settings
│   ├── Voltage and current mode settings             [UPDATED: individual KVAL commands]
│   ├── Speed profile
│   ├── Homing
│   ├── HOME and LIMIT sensors                        [RENAMED: typo fix "sensers"]
│   ├── Position management
│   ├── Motor control
│   ├── Electromagnetic brake                         [RENAMED: consistent spelling]
│   └── Servo mode
├── Technical information
│   ├── Firmware update
│   ├── Compiling the firmware                        [RENAMED: "Arduino sketch" is misleading now]
│   ├── USB serial diagnosis                          [RENAMED: shorter]
│   ├── Differences between STEP400 and STEP800       [MOVED from top level]
│   └── Firmware changelog                            [NEW: version history with links]
```

---

## C. Design Decisions

### C1. Naming consistency

**Problem:** Page titles and terminology drift across pages. Examples:
- "sensers" vs "sensors"
- "Electromagnet brake" vs "Electromagnetic brake"
- "The firmware update" (awkward article)
- "Compiling the Arduino sketch" (it's PlatformIO now)

**Decision:** Establish a terminology glossary and apply it across all pages. See section F.

### C2. Version-aware documentation

**Problem:** How to show what changed between firmware versions.

**Decision:** Use inline admonitions within existing pages, not separate per-version docs.

Format:
```markdown
> **Added in firmware v2.1.0**
> The `/saveConfig` command saves the running configuration to SD.
```

```markdown
> **Changed in firmware v2.1.0**
> The `/getConfigName` response now includes a 5th argument: `configFilename`.
```

This keeps all information about a command in one place while making version
differences scannable. A "Firmware changelog" page provides the reverse view
(what changed in each version).

### C3. OSC command quick reference table

**Problem:** Users must browse through many pages to discover available commands.

**Decision:** Add a single "Command list" page at the top of the OSC command reference
section. Organize commands by **functional category** (not by doc page), and allow
the same command to appear in multiple categories where it logically fits.

Proposed categories:
- **System & network** — setDestIp, getVersion, resetDevice, saveConfig, etc.
- **Configuration & reporting** — enableBusyReport, enableHizReport, setPositionReportInterval, etc.
- **Motor driver setup** — setMicrostepMode, setOverCurrentThreshold, setBemfParam, etc.
- **Voltage/current mode** — setKval, setTval, setVoltageMode, setCurrentMode, etc.
- **Speed & acceleration** — setSpeedProfile, setMaxSpeed, setAcc, etc.
- **Motion commands** — run, move, goTo, homing, softStop, hardStop, etc.
- **Combined (multi-motor)** — combinedRun, combinedGoTo, combinedSoftStop, etc.
- **Homing & switches** — getHomeSw, setHomingDirection, goUntil, releaseSw, etc.
- **Position** — getPosition, setPosition, resetPos, setMark, getMark, etc.
- **Servo mode** — enableServoMode, setTargetPosition, setServoParam, etc.
- **Electromagnetic brake** — enableElectromagnetBrake, setBrakeTransitionDuration, etc.
- **Status queries** — getStatus, getStatusList, getBusy, getDir, getHiZ, etc.

Each row shows: Command, Direction (send/receive), Arguments, STEP400, STEP800, and
a link to the detailed doc page. Commands that fit multiple categories appear in each.

### C4. Undocumented commands

**Problem:** Some commands exist in firmware but aren't in the docs. For example,
individual KVAL setters alongside the combined 4-KVAL setter.

**Decision:** Document all commands. For closely related command variants (e.g.,
`/setKVAL` sets all 4 at once, `/setHoldKVAL` sets one), keep them on the same
page (e.g., "Voltage and current mode settings") but group clearly:

```markdown
## KVAL settings

### /setKVAL (motorID, holdKVAL, runKVAL, accKVAL, decKVAL)
Sets all four KVAL values at once.

### /setHoldKVAL (motorID, holdKVAL)
Sets only the hold KVAL. (See also: /setKVAL to set all four at once.)

### /setRunKVAL (motorID, runKVAL)
...
```

No separate subpage needed — just expand the existing page with clear grouping.
The quick reference table makes the full list discoverable regardless of page length.

### C5. Browser configuration tool

**Problem:** New major feature needs documentation. Previous config tools also
need to be addressed.

**Decision:**
- **New page:** "Configuration with browser tool" under Connections and settings.
  Covers: requirements (Chrome/Edge), connecting via USB, reading/editing/saving
  config, offline mode (load/save JSON files), filename support.
- **URL for hosted tool:** `/tools/step-config/` (unified, not per-product).
  The old per-product tools at `/tools/step400-config/` and `/tools/step800-config/`
  should redirect or link to the new tool with a deprecation note.
- **Legacy tools:** Keep a brief note in a "Previous tools and legacy notes" page
  or at the bottom of the new config tool page. Don't delete the old tool pages
  immediately — users with old firmware may still need them.

### C6. Old config tools

**Decision:**
- Keep old tools at their current URLs and in the navigation
- Add a deprecation banner at the top of old tool pages: "For firmware v2.1.0+,
  use the new unified Configuration Tool."
- The new config tool page links to old tools for reference
- Add a brief note about old tools in the new config tool doc page

### C7. (Removed — Python library docs out of scope)

### C8. Cross-language links

**Problem:** Some pages link to the wrong language version (EN page linking to JA, etc.)

**Decision:** Audit all internal links during the page-by-page update. Use relative
paths within each language tree. The WPML plugin handles language switching at the
site level.

### C9. Section title "STEP400/800"

**Problem:** The top-level title "STEP400/800" excludes STEP100 and STEP200, which
use the same universal firmware.

**Decision:** Rename to "STEP Series" to be inclusive. Add a note that the docs cover
STEP100, STEP200, STEP400, and STEP800 with board-specific differences called out
inline.

---

## D. New Pages to Write

| Page | Location | Content summary |
|------|----------|----------------|
| Configuration with browser tool | Connections and settings | Web Serial workflow, offline mode, requirements |
| Command list (quick reference) | OSC command reference | Categorized table of all OSC commands with cross-listings |
| Firmware changelog | Technical information | Version history: v1.0→v2.0.0→v2.1.0, what changed |

---

## D2. OSC Command Audit (from `oscListeners.h`)

Full list of commands declared in the firmware, grouped by source code sections.
Commands marked **[UNDOC?]** need verification against existing doc pages.

### System / config commands
setDestIp, getVersion, getConfigName, setConfigName,
getConfigRegister, resetMotorDriver, reportError, getAdcVal, resetDevice,
**saveConfig** [NEW v2.1.0],
enableBusyReport, enableHizReport, enableHomeSwReport, enableLimitSwReport,
enableDirReport, enableMotorStatusReport, enableSwEventReport,
enableUvloReport, enableThermalStatusReport, enableOverCurrentReport,
enableStallReport, setPositionReportInterval, setPositionListReportInterval

### Status / query
getHomeSw, getLimitSw, getBusy, getDir, getHiZ, getUvlo,
getMotorStatus, getThermalStatus, getStatus, getStatusList

### Motor driver settings
setMicrostepMode, getMicrostepMode,
setHomeSwMode, getHomeSwMode, setLimitSwMode, getLimitSwMode,
getHomingStatus,
setStallThreshold, getStallThreshold,
setOverCurrentThreshold, getOverCurrentThreshold,
setLowSpeedOptimizeThreshold, getLowSpeedOptimizeThreshold, enableLowSpeedOptimize,
setBemfParam, getBemfParam,
setDecayModeParam, getDecayModeParam (PowerSTEP01 only)

### KVAL (voltage mode)
setKval (all 4 at once), **setHoldKval** [UNDOC?], **setRunKval** [UNDOC?],
**setAccKval** [UNDOC?], **setDecKval** [UNDOC?], getKval

### TVAL (current mode, PowerSTEP01 only)
setTval (all 4 at once), **setHoldTval** [UNDOC?], **setRunTval** [UNDOC?],
**setAccTval** [UNDOC?], **setDecTval** [UNDOC?], getTval, getTval_mA

### Speed profile
setSpeedProfile, setMaxSpeed, setMinSpeed, getMinSpeed,
setFullstepSpeed, getFullstepSpeed, setAcc, setDec,
**setSpeedProfileRaw** [UNDOC?], **setMaxSpeedRaw** [UNDOC?], **setMinSpeedRaw** [UNDOC?],
**setFullstepSpeedRaw** [UNDOC?], **setAccRaw** [UNDOC?], **setDecRaw** [UNDOC?],
getSpeed, getSpeedProfile, **getSpeedProfileRaw** [UNDOC?]

### Homing
setGoUntilTimeout, getGoUntilTimeout,
setReleaseSwTimeout, getReleaseSwTimeout,
setHomingDirection, getHomingDirection,
setHomingSpeed, getHomingSpeed,
setProhibitMotionOnHomeSw, getProhibitMotionOnHomeSw,
setProhibitMotionOnLimitSw, getProhibitMotionOnLimitSw

### Motor control / operational
getPosition, getPositionList, getMark,
run, **runRaw** [UNDOC?], move, goTo, goToDir,
homing, goUntil, **goUntilRaw** [UNDOC?], releaseSw, goHome, goMark,
setMark, setPosition, resetPos,
softStop, hardStop, softHiZ, hardHiZ

### Combined (all motors at once)
combinedRun, **combinedRunRaw** [UNDOC?], combinedMove, combinedGoTo, combinedGoToDir,
combinedSoftStop, combinedHardStop, combinedSoftHiZ, combinedHardHiZ

### Electromagnetic brake
enableElectromagnetBrake, setBrakeTransitionDuration, getBrakeTransitionDuration,
activate, free

### Servo mode
setTargetPosition, setTargetPositionList,
enableServoMode, setServoParam, getServoParam

### PowerSTEP01 voltage/current mode switching
setVoltageMode, setCurrentMode, setElPos, getElPos

---

## E. Existing Pages Needing Updates

| Page | What changes |
|------|-------------|
| Setup with a microSD card | Long filenames, `.json` discovery, `config.txt` priority, SdFat |
| System settings (OSC ref) | `/saveConfig` (new), `/getConfigName` 5th argument |
| Voltage and current mode settings | Individual KVAL commands: `/setHoldKval`, `/setRunKval`, `/setAccKval`, `/setDecKval`. Individual TVAL commands: `/setHoldTval`, `/setRunTval`, `/setAccTval`, `/setDecTval` |
| Speed profile (OSC ref) | Raw variants: `/setSpeedProfileRaw`, `/setMaxSpeedRaw`, `/setMinSpeedRaw`, `/setFullstepSpeedRaw`, `/setAccRaw`, `/setDecRaw`, `/getSpeedProfileRaw` |
| Motor control (OSC ref) | Raw variants: `/runRaw`, `/goUntilRaw`, `/combinedRunRaw` |
| Compiling the Arduino sketch | SdFat v2 dependency, PlatformIO emphasis, Arduino IDE folder removed from repo (download from GitHub Releases instead) |
| Diagnosis via USB serial port | New serial commands (G, T, {, R, F) for config tool |
| All OSC reference pages | Verify all commands against section D2 audit, terminology alignment |
| All pages | Terminology glossary (section F), link audit, version admonitions |

---

## F. Terminology Glossary (to be applied across all pages)

Establish consistent terms. Always use the left column:

| Use this | Not this |
|----------|----------|
| sensors | sensers |
| electromagnetic brake | electromagnet brake |
| firmware | Arduino sketch (when referring to the binary/build) |
| microSD card | SD card, micro SD, microsd |
| configuration file | config file (in prose; `config.txt` in code context is fine) |
| STEP Series | STEP400/800, step series |
| HOME sensor | home switch, HomeSw (in prose; `homeSwState` in code context is fine) |
| LIMIT sensor | limit switch, LimitSw (in prose) |
| driver IC | motor driver chip, stepper driver |
| PowerSTEP01 | powerSTEP01, Powerstep01 |
| Web Serial API | WebSerial, web serial |
| OSC (Open Sound Control) | OSC (first mention per page should expand the acronym) |

This glossary should be maintained as a file in the repo for reference during
future edits.

---

## G. Workflow

### Phase 1: Audit ✓ (partially complete)
- ✓ Extracted all OSC command declarations from `oscListeners.h`
- ✓ Identified likely undocumented commands (marked [UNDOC?] in section D2)
- TODO: Verify [UNDOC?] commands against existing doc pages (Claude Code task)
- TODO: Audit all internal links for language correctness (Claude Code task)

### Phase 2: Page-by-page update plans (Claude Chat)
- For each page in the structure above, produce a specific update plan
- Include: what to add, what to change, what to remove, terminology fixes
- Kanta reviews and approves each plan before implementation

### Phase 3: Implementation (Claude Code)
- Write/update Markdown files in the GitHub repo
- EN first, then JA (Kanta translates or reviews JA)
- Each page is a separate commit for easy review

### Phase 4: Publish
- Run the WP publish script to push updated Markdown to WordPress
- Verify rendering on ponoor.com
- Deploy new browser config tool to `/tools/step-config/`

### Phase 5: Post-publish
- Update README files in firmware and support repos if needed
- Add deprecation banners to old config tool pages on WordPress

---

## H. Out of Scope

- Python library docs (ReadTheDocs) — separate project
- Product pages (ponoor.com/products/) — separate concern
- Shop pages — not documentation
- Sphinx/RST files in the support repo — legacy, not maintained
- Hardware documentation (schematics, BOM) — separate from software docs
