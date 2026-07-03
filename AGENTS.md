# AGENTS.md — working *on* the Question Commons

> For an AI agent modifying or maintaining **this repository**. The commons is
> the most sensitive of the three repos: everything here is **public, permanent,
> and CC0**. A mistake here cannot be recalled.

## What this repo is

`5qln/questions` is **the commons of record**: a public, CC0 collection of
**questions — and only questions**. Each file is one question that opened an
`/idk` cycle (**X**), paired with the question that cycle could not have asked
before it began (**∞0′**). No answers. No authors. No identities. One repo of
three; see [`SYSTEM.md`](https://github.com/5qln/Idk/blob/main/SYSTEM.md).

Questions arrive through [`Idk-commons`](https://github.com/5qln/Idk-commons)
(the transport), not by hand. Your job in this repo is to keep the gate honest
and the layout intact — not to author or edit questions.

## The hard rules

1. **Questions only. Nothing from the private trail.** No `α`, `{α′}`, `Z`, `∇`,
   `B″`, `φ ⋂ Ω`, no cycle number, no author, no date, no Codex seal. These are
   forbidden by pattern in the gate — do not add content that carries them, and
   never loosen the denylist.

2. **Never hand-edit a question's text.** A published question is CC0 and
   content-addressed: its filename is `sha256(normalize(X))`. Editing the text
   without renaming the file breaks the hash↔content invariant the gate enforces;
   editing at all rewrites something a human placed into the public domain. Leave
   question bodies alone.

3. **`membrane-spec.json` is byte-identical with `Idk-commons`.** It is a shared
   sealed contract. Any change lands in **both** repos in lockstep; the pinned
   SHA sync test guards against drift. Never edit one side alone.

4. **The commons fails closed.** `membrane_lint.py` refuses an empty or missing
   commons on purpose (guarding against silent deletion). Keep that behavior; a
   quiet commons is a first-class state, not an error to "fix" by removing the
   guard.

5. **Convergence is arrival, not conflict.** If two people surface the same
   question they land on the same file — that is the propagation signal the
   commons exists to reveal. Never treat a duplicate hash as a collision to
   resolve.

## Layout

| Path | What it is | Touch it when… |
| --- | --- | --- |
| `questions/<aa>/<bb>/<hash>.md` | one published question each (X + ∞0′, CC0) | **effectively never by hand** — arrives via transport |
| `membrane-spec.json` | shared sealed gate contract | only together with `Idk-commons` |
| `bin/membrane_lint.py` | CI gate, runs on every push/PR | changing structural form checks (mirror the tool) |
| `tests/` | lint tests | always, with any gate change |

## The file format a question must match

```markdown
---
spdx: CC0-1.0
content_hash: sha256:<64 hex chars>
---

# <the question>

*Published to the Question Commons. CC0 — public domain. Make it yours.*

## ∞0' — The Return Question

<the question that could not have been asked before>
```

The filename is the SHA-256 of the normalized question text, stored under a
two-level fan-out (`questions/<aa>/<bb>/`). Same normalization, same hash, same
path — that determinism is what makes convergence work.

## Before you finish

```bash
python3 bin/membrane_lint.py      # gate passes on the whole commons
python3 -m pytest -q              # lint tests pass
```

Confirm `membrane-spec.json` still matches `Idk-commons` byte-for-byte.

---

*The trail is private. The question is yours. Make it yours.*
