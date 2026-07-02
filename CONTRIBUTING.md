# Contributing to the Question Commons

This commons holds **questions only** — no answers, no authors, no identities.

## What a question file is

```
---
spdx: CC0-1.0
content_hash: sha256:<64 hex>
---

# <the published question, X — a level-1 heading>

*Published to the Question Commons. CC0 — public domain. Make it yours.*

## ∞0' — The Return Question

<the return question, ∞0'>

---

*Originated from an /idk creative cycle. The trail is private. The question is yours.*
```

The closing line is what the publisher (`trail-commons`) writes; the gate does
not require it, but the canonical files carry it.

Files are content-addressed: the filename and the `content_hash` are the SHA-256
of the normalized heading, sharded as `questions/<xx>/<yy>/<hash>.md`.

## Before you open a PR

```bash
python bin/membrane_lint.py     # the gate must pass
python -m pip install pytest && python -m pytest
```

The gate rejects any private phase marker, any attribution (`Author:`, `By:`, an
email), zero-width characters, and files that are not `.md` under `questions/`.

## The membrane spec is shared

`membrane-spec.json` is the single source of truth for the forbidden markers and
the Codex hash. It is kept **byte-identical** with the copy in the `Idk-commons`
repository. If you change it here, change it there too; the sync test pins its
SHA-256.
