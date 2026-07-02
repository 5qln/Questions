"""Regression tests for the membrane gate (guards C5-C9, H8, H9, H11)."""
import hashlib
import json
from pathlib import Path

import membrane_lint as ml

REPO = Path(ml.__file__).resolve().parent.parent


def _flag_labels(text, relname="questions/xx/yy/f.md"):
    return " | ".join(ml.check(text, relname))


# ---- C9: structural positive checks ----
def test_hash_algorithm_fixture_is_stable():
    # Content-hash is the security-critical invariant; pin one known value.
    assert ml.content_hash("Does a path exist before the first walker, or only after?") \
        == "3a8757ae9e22b925b07cd70b80a68718cc8c6c3851205af0cb9dfab3a9eb10bd"


def test_level2_only_heading_has_no_X():
    text = "## ∞0' — The Return Question\n\nWho?\n"
    assert "no level-1 question heading" in _flag_labels(text)


def test_spdx_must_be_in_frontmatter_not_prose():
    text = "# Q?\n\nthe words spdx: CC0-1.0 in prose\n\n## ∞0' — R\n\nWho?\n"
    assert "missing SPDX dedication in frontmatter" in _flag_labels(text)


# ---- C5: homoglyph / confusable bypass is closed ----
def test_math_bold_alpha_is_caught():
    text = "# A question\n\n\U0001D6FC is here\n"      # 𝛼 (MATH BOLD SMALL ALPHA)
    assert "alpha" in _flag_labels(text)


def test_curly_quote_B_double_prime_is_caught():
    text = "# A question\n\nB\u2019\u2019 leaked\n"       # B'' with curly quotes
    assert "B''" in _flag_labels(text)


def test_intersection_lookalike_is_caught():
    text = "# A question\n\n\u03c6 \u2229 \u03a9\n"        # φ ∩ Ω  (∩ not ⋂)
    assert "φ ⋂ Ω" in _flag_labels(text)


# ---- C6: zero-width steganography channel ----
def test_zero_width_is_caught():
    text = "# A quest\u200bion\n\n## ∞0' — R\n\nWho?\n"
    assert "zero-width" in _flag_labels(text)


# ---- H8: no authors ----
def test_author_and_email_are_caught():
    assert "author attribution" in _flag_labels("# Q?\n\nAuthor: Jane Doe\n")
    assert "email" in _flag_labels("# Q?\n\nreach me at a@b.com\n")


# ---- C7: non-.md files under questions/ are rejected ----
def test_non_md_file_is_rejected(tmp_path):
    junk = tmp_path / "secret.json"
    junk.write_text('{"cycle": 40}', encoding="utf-8")
    assert ml.main([str(junk)]) == 1


# ---- a directory argument scans its contents (matches the no-arg scan) ----
def test_directory_argument_is_expanded(tmp_path):
    heading_text = "Does a directory hold questions, or only files?"
    want = ml.content_hash(heading_text)
    d = tmp_path / "questions" / want[:2] / want[2:4]
    d.mkdir(parents=True)
    (d / f"{want}.md").write_text(
        f"---\nspdx: CC0-1.0\ncontent_hash: sha256:{want}\n---\n\n"
        f"# {heading_text}\n\n*CC0*\n\n## ∞0' — The Return Question\n\nWho asks?\n",
        encoding="utf-8")
    assert ml.main([str(tmp_path / "questions")]) == 0
    # A stray non-.md inside the directory is still rejected.
    (d / "stray.json").write_text("{}", encoding="utf-8")
    assert ml.main([str(tmp_path / "questions")]) == 1


# ---- H11: shard path is verified ----
def test_wrong_shard_path_flagged():
    heading = "# A well-formed question about paths?"
    want = ml.content_hash(heading)
    body = (f"---\nspdx: CC0-1.0\ncontent_hash: sha256:{want}\n---\n\n"
            f"{heading}\n\n## ∞0' — R\n\nWho?\n")
    # placed at the WRONG shard
    labels = ml.check(body, f"questions/zz/99/{want}.md")
    assert "shard path does not match" in " | ".join(labels)


# ---- H11: an ancestor dir named "questions" must not break the shard check ----
def test_ancestor_dir_named_questions_does_not_break_shard():
    # Regression: when the repo is checked out into a directory literally named
    # "questions" (or any such ancestor), the shard check must still anchor to
    # the commons questions/ subdir, not the ancestor.
    heading_text = "Does the shard survive an ancestor of the same name?"
    want = ml.content_hash(heading_text)
    body = (f"---\nspdx: CC0-1.0\ncontent_hash: sha256:{want}\n---\n\n"
            f"# {heading_text}\n\n*CC0*\n\n## ∞0' — R\n\nWho?\n")
    relname = f"/home/user/questions/questions/{want[:2]}/{want[2:4]}/{want}.md"
    assert ml.check(body, relname) == []


# ---- clean happy path still passes end-to-end ----
def test_clean_crafted_file_passes(tmp_path):
    heading_text = "Is the map the territory when no one is walking?"
    want = ml.content_hash(heading_text)
    f = tmp_path / f"{want}.md"
    f.write_text(f"---\nspdx: CC0-1.0\ncontent_hash: sha256:{want}\n---\n\n"
                 f"# {heading_text}\n\n*CC0*\n\n## ∞0' — The Return Question\n\nWho asks?\n",
                 encoding="utf-8")
    assert ml.main([str(f)]) == 0


# ---- H9: the shared spec is intact and pinned (drift guard) ----
def test_spec_sha_is_pinned():
    spec_bytes = (REPO / "membrane-spec.json").read_bytes()
    got = hashlib.sha256(spec_bytes).hexdigest()
    # If you intentionally change the spec, update this pin AND the copy in Idk-commons.
    assert got == "10637382597e85eac82d30848a4582cee16cc6094b3a316f04f17f5b28d2e35b"


def test_codex_hash_matches_spec():
    spec = json.loads((REPO / "membrane-spec.json").read_text(encoding="utf-8"))
    assert ml.CODEX_HASH == spec["codex_hash"]
