# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Fixed / Hardened
- Homoglyph & confusable bypass: the gate now scans NFKD-folded, quote/∩-
  normalized text (math-alpha, fullwidth, curly-quote B″, ∩-vs-⋂ all caught).
- Zero-width characters are stripped before hashing and rejected outright.
- Non-`.md` files under `questions/` are now rejected (were silently ignored).
- The gate fails on a missing or empty `questions/` directory (was fail-open).
- Positive checks now parse structure instead of matching substrings: a real
  level-1 heading, real frontmatter `spdx:`/`content_hash:`, and the `## ∞0' —`
  return heading are all required.
- The two-character shard path is now verified, not just the filename stem.
- Author/by-line/email attribution is rejected (the commons has no authors).

### Changed
- Forbidden markers, Codex hash, and SPDX id extracted to `membrane-spec.json`
  (shared with `Idk-commons`), with a pinned-SHA sync test.
- `normalize_question` → `normalize_heading` (it normalizes an H1, not a file).

### Added
- Test suite (`tests/`), SHA-pinned multi-version CI, README terminology,
  `SECURITY.md`, `CONTRIBUTING.md`, and standard community files.
