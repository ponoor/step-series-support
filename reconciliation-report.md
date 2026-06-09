# Reconciliation Report: WordPress Export vs GitHub Docs

Generated: 2026-06-08

## Summary

| Category | Count |
| --- | --- |
| Matched pairs (identical content) | 0 |
| Pairs with formatting-only differences | ~55 |
| Pairs with substantive content differences | 3 |
| WP-only doc files (need adding to repo) | 3 |
| WP-only product sections (step100-200) | 8 files (en+ja) |
| GitHub-only files | 7 |

**Overall verdict:** WP is the more current source. Differences are mostly formatting (WP has extra blank lines between sections, spaces in table pipe cells, H1 titles at top of each page). Three files have genuine content changes where WP is newer.

---

## 1. Formatting-Only Differences (WP is canonical)

The vast majority of paired files differ only in whitespace and markdown style, not content:

- **WP adds blank lines** after headings and between table rows (more readable, matches modern Markdown)
- **WP uses spaced table cells**: `| Argument | Range |` vs GitHub's `|Argument|Range|`
- **WP includes H1 title** at top of each file (e.g., `# Alarm settings`); GitHub files omit H1 (relying on folder/nav structure)
- **WP uses `<url>` angle-bracket links** for bare URLs; GitHub uses plain URLs

These ~55 files should be replaced with the WP version (which adds the front matter and corrects formatting). No content review needed.

**Affected pairs (EN):** alarm-settings, automatically-sent-messages, brake, differences-between-step400-and-step800, home-and-limit-sensers, homing, motor-control, motor-driver-settings, position-management, servo-mode (osc-ref), speed-profile, system-settings, homing-and-position-management (func), servo-mode (func), speed-profile-and-type-of-motor-motions, voltage-mode-and-current-mode (func), network-and-dip-switch, power-supply-and-motor, sensor-and-switch, compile-the-arduino-sketch, diagnosis, firmware-update, hardware-step400, hardware-step800, tutorial, emb-step400/commands, emb-step400/connection, emb-step400/howtowork, emb-step400/specifications

**Affected pairs (JA):** Same list with `_jp.md` counterparts

---

## 2. Substantive Content Differences

### 2a. `setup-with-a-microsd-card` (EN and JA) — **WP is newer**

WP modified: `2021-09-09T15:24:33`

**WP adds:**
- New section `## Example config files` with link to `https://github.com/ponoor/step-series-support/tree/main/configGenerator`

**WP removes:**
- Stale paragraph referencing old URL `http://ponoor.com/tools/step400-config/` and `https://github.com/kanta/STEP400_prototype/tree/master/rev4/configTool`

**Recommendation:** Use WP version. The removed content references Kanta's personal prototype repo and is clearly stale.

GitHub files:
- `docs/connections-and-settings/setup-with-a-microsd-card_en.md`
- `docs/connections-and-settings/setup-with-a-microsd-card_jp.md`

---

### 2b. `voltage-and-current-mode-settings` (EN and JA) — **Decision needed**

WP modified: `2021-12-08T22:48:38` (EN), `2021-12-08T22:49:41` (JA)

**GitHub has but WP doesn't:**
Large HTML comment blocks containing deprecated commands:
- `<!-- /setHoldKval`, `/setRunKval`, `/setAccKval`, `/setDecKval` (Voltage mode deprecated aliases)
- `<!-- /setHoldTval`, `/setRunTval`, `/setAccTval`, `/setDecTval` (Current mode deprecated aliases)

These commands exist in GitHub wrapped in `<!-- ... -->` HTML comments. WP export has them removed entirely.

**Decision needed:** Should the deprecated commands be preserved in comments (GitHub approach — useful for historical reference) or removed (WP approach — cleaner)? If keeping comments, the WP version cannot simply replace the GitHub file.

GitHub files:
- `docs/osc-command-references/voltage-and-current-mode-settings_en.md`
- `docs/osc-command-references/voltage-and-current-mode-settings_jp.md`

---

## 3. WP-Only Files (need to be added to repo)

### 3a. `example-parameter-values-for-example-steppers` — **Add to repo**

WP modified: `2021-12-09T17:21:27` (EN), `2021-12-09T17:20:40` (JA)

- WP EN: `wp_export/en/docs/step-series/settings/example-parameter-values-for-example-steppers.md`
- WP JA: `wp_export/ja/docs/step-series/settings/example-parameter-values-for-example-steppers.md`

Proposed GitHub path:
- `docs/connections-and-settings/example-parameter-values-for-example-steppers_en.md`
- `docs/connections-and-settings/example-parameter-values-for-example-steppers_jp.md`

---

### 3b. `absolute-position-management` (JA only) — **Investigate**

WP modified: `2022-04-04T22:48:11`

- WP JA: `wp_export/ja/docs/step-series/osc-command-reference/absolute-position-management.md`
  - Title: `座標` (Coordinates)

There is a GitHub file `docs/osc-command-references/position-management_jp.md` — check if this is the same content under a different name, or genuinely missing content.

Note: The EN equivalent `position-management.md` exists in WP and maps to `position-management_en.md` in GitHub (formatting differences only). The JA WP file has a different slug (`absolute-position-management` vs `position-management`).

---

### 3c. `step100-200` section — **Add to repo (new product section)**

Both EN and JA versions exist in WP with no GitHub counterpart. This is a complete product documentation section for the STEP100/STEP200 family.

**EN files** (4 docs):
- `wp_export/en/docs/step100-200/get-the-materials.md`
- `wp_export/en/docs/step100-200/upload-the-sketch.md`
- `wp_export/en/docs/step100-200/usage.md`
- `wp_export/en/docs/step100-200/assemble.md` + subdocs (connections, step100, step200)

**JA files** (4 docs + subdocs):
- Same structure under `wp_export/ja/docs/step100-200/`

Proposed GitHub path: `docs/step100-200/` (new directory, parallel to existing sections)

---

## 4. GitHub-Only Files (review needed)

These exist in GitHub but have no WP counterpart. They appear to be overview/index pages that WP handles as category taxonomy pages.

| GitHub file | Content description | Recommendation |
| --- | --- | --- |
| `connections-and-settings/settings_en.md` | Index page listing links to 5 sub-documents in the section | Keep — useful as section overview in static docs |
| `connections-and-settings/settings_jp.md` | Japanese equivalent | Keep |
| `osc-command-references/osc-command-reference_en.md` | Explains OSC command structure, motor ID ranges, argument notation, timing, STEP400 vs STEP800 differences | Keep — important reference |
| `osc-command-references/osc-command-reference_jp.md` | Japanese equivalent | Keep |
| `functional-descriptions/osc-command-reference_en.md` | Brief overview of OSC command reference (appears to be a cross-reference/summary) | Keep or merge into section index |
| `functional-descriptions/osc-command-reference_jp.md` | Japanese equivalent | Keep or merge |
| `emb-step400/index_en.md` | Overview of electromagnetic brake feature, purpose, and STEP400 integration | Keep — no JA equivalent exists, may need JA translation |

---

## 5. WP Category/Index Files (not in scope for GitHub)

The following WP files are CMS category pages (auto-generated by WordPress) — they don't need GitHub equivalents as the folder structure serves the same purpose:

- `en/docs/step-series.md`
- `en/docs/step-series/osc-command-reference.md`
- `en/docs/step-series/functional-description.md`
- `en/docs/step-series/settings.md`
- `en/docs/step-series/technical-information.md`
- `en/docs/emb-step400.md`
- (Same for `ja/`)

---

## 6. Notes

- **`home-and-limit-sensers`**: The misspelling "sensers" (should be "sensors") exists in both WP and GitHub slug/filename. Fix consistently if desired, but requires a redirect on WordPress.
- **`motordriver-settings.md` (JA WP)**: WP JA uses `motordriver-settings` slug; GitHub JA uses `motor-driver-settings`. Confirmed they map to the same content (formatting differences only).
- **No shortcode artifacts** detected in the exported files — the WP export script handled conversion cleanly.
- **`goUnitlTimeout` typo** (known issue per CLAUDE.md): not found in the files checked — may be in config files rather than docs.

---

## Recommended Action Plan

1. **Replace** all formatting-only pairs (section 1) with WP versions — add front matter, use WP as source
2. **Decide** on `voltage-and-current-mode-settings`: keep HTML comments or remove
3. **Add** `example-parameter-values-for-example-steppers` (EN+JA) to `docs/connections-and-settings/`
4. **Investigate** `absolute-position-management` JA vs `position-management` JA — likely same content, different slug
5. **Add** `step100-200` section to `docs/step100-200/` (new directory)
6. **Keep** all GitHub-only overview/index files
