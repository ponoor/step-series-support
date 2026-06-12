# CLAUDE.md — STEP Series Documentation Update

## Overview

This task updates the Markdown documentation in `docs/` of the `ponoor/step-series-support` repo. All changes are to Markdown files only. EN and JA versions exist in parallel — **update EN files only**. Kanta handles JA separately.

**Reference documents** (in repo root):
- `doc-update-ground-plan.md` — structural decisions, terminology glossary, command audit
- `doc-update-page-plans.md` — per-page checklist of what to add/change/fix

Read both before starting any batch. They are authoritative.

**How to use this file:** Run one batch per session. Start with the batch number you're told (e.g., "Run Batch 2"). If not specified, check which batches are already complete and run the next one.

**Batch completion marker:** After finishing a batch, create or append to `docs/UPDATE_PROGRESS.md`:
```
## Batch N — Complete
- Date: YYYY-MM-DD
- Files modified: (list)
- Notes: (any issues found)
```

---

## Batch 1: Global Mechanical Fixes

**Goal:** Terminology alignment, filename consistency, and formatting normalization across ALL doc files.

**Check before starting:** This should be the first batch. If `docs/UPDATE_PROGRESS.md` exists and shows Batch 1 complete, skip to Batch 2.

### 1.1 Terminology replacements

Apply these substitutions across all `.md` files in `docs/`. Use case-sensitive matching where indicated.

| Find | Replace | Notes |
|------|---------|-------|
| `sensers` | `sensors` | Case-insensitive |
| `Electromagnet brake` | `Electromagnetic brake` | In titles and body text |
| `STEP 400` | `STEP400` | With space → no space |
| `STEP 800` | `STEP800` | With space → no space |
| `ULVO` | `UVLO` | Typo in alarm settings |
| `powerSTEP01` | `PowerSTEP01` | Capitalization |
| `Powerstep01` | `PowerSTEP01` | Capitalization |
| `micro SD` | `microSD` | No space, lowercase m |
| `micro sd` | `microSD` | |
| `SD card` | `SD card` | Keep as-is (this is correct) |
| `Arduino sketch` | `firmware` | Only when referring to the compiled binary, NOT in the title "Compiling the Arduino sketch" (that's renamed in Batch 4) |

### 1.2 Grammar fixes (targeted)

These are specific known errors. Search and fix:

| Find (approximate) | Fix |
|---------------------|-----|
| `with of without` | `with or without` |
| `the motor reached to the` | `the motor reaches the` |
| `until reaches to the specified step counts` | `until it reaches the specified step count` |
| `the motor state will automatically enters` | `the motor state will automatically enter` |
| `/setHomingDirectionand` | `/setHomingDirection and` |
| `from setReleaseSwTimeout command` | `from the /setReleaseSwTimeout command` |
| `the sensor state have not changed` | `the sensor state has not changed` |
| `Returns the current position of all motors at once. /getPosition 255 returns individual messages for each motors` | Fix: "each motors" → "each motor" |
| `In motion start condition` | Clarify to: "This command can only be executed when the motor is stopped." (or similar, based on context) |

### 1.3 First-mention OSC expansion

On each page that uses "OSC" in the body text, ensure the first mention reads "OSC (Open Sound Control)". Do NOT expand in command names like `/setKval`.

### 1.4 configTool references

Find all mentions of "configTool" or "the configTool" or "the Configuration Tool" and make them specific:
- If referring to the old HTML tools → "the STEP400/STEP800 configuration tool"
- If referring generically → "the configuration tool" (lowercase)
- Do NOT update to reference the new browser tool yet — that happens in Batch 3

### 1.5 Commit

Commit all changes as a single commit: `docs: global terminology and grammar fixes`

---

## Batch 2: OSC Command Reference Pages

**Goal:** Update all pages under `docs/osc-command-reference/` (or equivalent path), add undocumented commands, write the new Command List page.

**Check before starting:** Verify Batch 1 is complete by checking `docs/UPDATE_PROGRESS.md`.

### 2.1 Find the OSC reference files

List the files under the OSC command reference directory. The path may be `docs/osc-command-reference/` or nested differently. Identify files corresponding to:
- Automatically sent messages
- System settings
- Motor driver settings
- Alarm settings
- Voltage and current mode settings
- Speed profile
- Homing
- HOME and LIMIT sensors
- Position management
- Motor control
- Electromagnetic brake
- Servo mode
- Differences between STEP400 and STEP800

### 2.2 System settings page

Add the following new command:

```markdown
## /saveConfig

Saves the current running configuration to the SD card.

| | |
|---|---|
| Command | `/saveConfig` |
| Argument | None |
| Response | None |
| Timing | Always |

Writes the current in-memory configuration to the SD card as a JSON file.
The filename used is the one previously set, or the filename from which the
config was originally loaded.

> **Added in firmware v2.1.0**

```

Update `/getConfigName`:

Add documentation for the 5th argument in the response:

```markdown
The response has been extended with a 5th argument:

/configName (string)configName (int)sdInitOk (int)configFileFound
  (int)configFileLoaded (string)configFilename

- `configFilename`: The filename of the configuration file on the SD card
  (e.g., `config.txt` or `STEP400_venue-A.json`). This is the on-disk
  filename, distinct from `configName` which is the user-editable label.
```

Add version admonition:
```markdown
> **Changed in firmware v2.1.0:** Added `configFilename` as 5th argument.
```

### 2.3 Voltage and current mode settings page

Add individual KVAL commands after the existing `/setKval` entry:

```markdown
## /setHoldKval
Sets only the hold KVAL value.

| | |
|---|---|
| Command | `/setHoldKval (int)motorID (int)holdKVAL` |
| Argument | motorID 1-4/1-8, holdKVAL 0-255 |
| Response | None |
| Timing | Always |

See also: `/setKval` to set all four KVAL values at once.

## /setRunKval
Sets only the run KVAL value.
(same structure)

## /setAccKval
Sets only the acceleration KVAL value.
(same structure)

## /setDecKval
Sets only the deceleration KVAL value.
(same structure)
```

Add the same pattern for individual TVAL commands (PowerSTEP01 / STEP400 only):
`/setHoldTval`, `/setRunTval`, `/setAccTval`, `/setDecTval`

### 2.4 Speed profile page

Add raw variant commands in a new subsection at the end:

```markdown
## Raw register value commands

The following commands set or get speed profile parameters using raw driver IC
register values without unit conversion. For most users, the standard commands
(in steps/s and steps/s²) are recommended. These are for advanced use cases
where direct register control is needed.

### /setSpeedProfileRaw
(document with same table structure as /setSpeedProfile)

### /setMaxSpeedRaw
### /setMinSpeedRaw
### /setFullstepSpeedRaw
### /setAccRaw
### /setDecRaw
### /getSpeedProfileRaw
```

### 2.5 Motor control page

Add raw motion commands:

```markdown
## Raw register value commands

### /runRaw
### /goUntilRaw
### /combinedRunRaw
```

Same documentation pattern as the standard versions, noting they use raw register values.

### 2.6 Homing page

Add version admonition about the typo fix:

```markdown
> **Fixed in firmware v2.1.0:** The STEP400 configuration template previously
> contained a typo `goUnitlTimeout` (note the swapped letters). The firmware
> always read the correctly spelled `goUntilTimeout`, so this value was silently
> ignored on STEP400 configs, always falling back to the default (10000 ms).
> This has been corrected in v2.1.0.
```

### 2.7 Other OSC reference pages

Apply grammar/clarity fixes and terminology alignment from `doc-update-page-plans.md` sections 4.2, 4.4, 4.5, 4.9, 4.10, 4.12, 4.13.

### 2.8 Differences between STEP400 and STEP800

- Add newly documented commands to the appropriate sections (individual KVAL/TVAL → STEP400 only for TVAL, both for KVAL)
- Move this file to be a child of the Technical Information section (adjust any parent/hierarchy metadata if front matter supports it)

### 2.9 Write new Command List page

Create a new file for the quick reference table. Organize by category per `doc-update-ground-plan.md` section C3. Derive the complete list from the finished reference pages — scan all the pages updated above and compile every command into the table.

Table format per category:
```markdown
## System & Network

| Command | Direction | Arguments | STEP400 | STEP800 |
|---------|-----------|-----------|:-------:|:-------:|
| [/setDestIp](system-settings.md) | → | (int)destIp0 ... | ✓ | ✓ |
| [/saveConfig](system-settings.md) | → | — | ✓ | ✓ |
```

Commands may appear in multiple category tables.

### 2.10 Commit

One commit for all OSC reference changes: `docs: update OSC command reference — add undocumented commands, v2.1.0 changes, grammar fixes`

---

## Batch 3: Settings Pages and Browser Tool

**Goal:** Update config-related pages, write the new browser config tool page.

**Check before starting:** Verify Batches 1-2 are complete.

### 3.1 Configuration with microSD card

Apply all changes from `doc-update-page-plans.md` section 2.4:
- Remove the outdated 3-character extension limitation text
- Add long filename support info with [v2.1.0] admonition
- Add file discovery priority explanation
- Add `/saveConfig` cross-reference
- Update config tool references to mention the new browser tool
- Fix "Copy this file to the top level" → clarify root directory

### 3.2 Example parameters page

- Update the `config.txt` naming requirement: any `.json` filename works with v2.1.0+
- Add backward compatibility note for older firmware

### 3.3 Network and DIP switch

- Update configTool references to be specific

### 3.4 Write new browser config tool page

Create a new file. Content outline (see `doc-update-page-plans.md` section 2.5 for full checklist):

Structure:
1. Introduction — what the tool does, firmware requirement (v2.1.0+)
2. Requirements — Chrome or Edge, USB cable
3. Connecting to the board — step by step with Connect button
4. Reading and editing configuration — describe the form layout
5. Saving to the board — save workflow, filename support
6. Offline mode — load/save JSON without serial connection
7. Status monitoring — real-time motor status display
8. Troubleshooting — browser compatibility, connection issues
9. Previous configuration tools — links to old STEP400/STEP800 tools with note about firmware versions

Keep the page concise and task-oriented. Link to the microSD card page for config file format details rather than duplicating.

### 3.5 Commit

`docs: update configuration pages, add browser config tool documentation`

---

## Batch 4: Technical Info, Functional Descriptions, Final Pass

**Goal:** Remaining pages, new changelog, and final quality pass.

**Check before starting:** Verify Batches 1-3 are complete.

### 4.1 Compiling the firmware page

- Rename title in the document (heading and front matter if present)
- Add note about Arduino IDE folder removal from repo — download from GitHub Releases
- Update dependency list: SdFat v2 replaces arduino-libraries/SD
- Emphasize PlatformIO as primary build method

### 4.2 USB serial diagnosis page

- Add new serial commands table (G, T, {, R, F) with descriptions
- Note these are used by the browser config tool but work from any serial terminal

### 4.3 Write firmware changelog page

Create new file. Structure:

```markdown
# Firmware Changelog

## v2.1.0
(content from v2.1.0-release-notes.md, condensed)

## v2.0.0
(content from GitHub Discussion #38 / release notes, condensed)

## Earlier versions
(brief notes if information is available, otherwise note that
detailed changelogs were not maintained for versions before v2.0.0)
```

Link to GitHub Releases for each version.

### 4.4 Functional description pages

Grammar and clarity pass on:
- Voltage mode and current mode
- Speed profile and motion types
- Homing and position management
- Servo mode

### 4.5 Hardware pages

Grammar/terminology pass on Hardware – STEP400 and Hardware – STEP800.

### 4.6 Getting Started page (Tutorial)

- Rename title
- Add mention of browser config tool as alternative to SD editing
- Quick grammar pass

### 4.7 Final link audit

Scan all files for internal links (`](../` or `](./` or absolute ponoor.com links).
Verify each link target exists and points to the correct language version.
Report any broken links in the UPDATE_PROGRESS.md entry.

### 4.8 Commit

`docs: update technical info, functional descriptions, add changelog, final pass`

---

## Reference: File Structure

The actual file paths in the repo may differ from the website URL structure.
At the start of each batch, run `find docs/ -name "*.md" | sort` to get the
actual layout and map it to the page names in this document.

## Reference: Version Admonition Format

Use this consistent format for all version notes:

```markdown
> **Added in firmware v2.1.0**
> Description of what was added.
```

```markdown
> **Changed in firmware v2.1.0**
> Description of what changed.
```

```markdown
> **Fixed in firmware v2.1.0**
> Description of what was fixed.
```
