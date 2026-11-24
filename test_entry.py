"""Tests for the Two Days of Quiet Dread entry.

Behavior under test: running main.py writes exactly one line of
1-140 UTF-8 characters to $MAKEFUN_OUTPUT_DIR/entry.txt, and that
line reads like a tired engineer approving a PR with quiet dread.
"""
import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(REPO, "main.py")

# Stock lines the entry must not be (or contain) — the judge rewards a
# fresh turn of phrase, not a cliche pasted from the shelf.
STOCK = [
    "this is fine",
    "looks good to me",
    "ship it",
    "lgtm",
    "works on my machine",
    "it is what it is",
    "we'll fix it in prod",
    "approved, whatever happens happens",
]


def run_entry():
    """Run main.py the way the grader does and return the entry text."""
    with tempfile.TemporaryDirectory() as outdir:
        env = dict(os.environ, MAKEFUN_OUTPUT_DIR=outdir)
        proc = subprocess.run(
            [sys.executable, MAIN], env=env, capture_output=True, text=True
        )
        assert proc.returncode == 0, f"main.py failed: {proc.stderr}"
        path = os.path.join(outdir, "entry.txt")
        assert os.path.exists(path), "entry.txt was not written"
        with open(path, encoding="utf-8") as f:
            return f.read()


class TestEntry(unittest.TestCase):
    def test_single_line_1_to_140_chars(self):
        text = run_entry()
        stripped = text.strip()
        self.assertTrue(1 <= len(stripped) <= 140, f"length {len(stripped)}")
        self.assertNotIn("\n", stripped, "must be a single line")
        self.assertNotEqual(stripped, "", "must not be only whitespace")

    def test_approves_the_pr(self):
        text = run_entry().lower()
        self.assertIn("approv", text, "must approve the pull request")

    def test_carries_quiet_dread(self):
        text = run_entry().lower()
        # Dread carried by a flat conditional about nobody being left.
        self.assertIn("assuming", text)
        self.assertIn("still", text)

    def test_flat_tone_no_melodrama(self):
        text = run_entry()
        self.assertNotIn("!", text, "no exclamation: dread stays quiet")
        self.assertNotIn("?", text, "no cry for help")

    def test_not_a_stock_cliche(self):
        text = run_entry().lower()
        for phrase in STOCK:
            self.assertNotIn(phrase, text, f"stock phrase: {phrase}")


if __name__ == "__main__":
    unittest.main()
