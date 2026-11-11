"""Publication guard: fail the test suite if private data reaches public text.

This is the automated version of "run a sensitive-data scan before publishing".
Forbidden strings are assembled from fragments so this file does not flag itself;
the file also excludes itself and .gitignore (an ignore list must name private
filenames by design).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".html", ".txt", ".cfg"}
EXCLUDED_FILES = {"test_public_privacy.py", ".gitignore"}
EXCLUDED_PARTS = {".git", "docs/avatars", "__pycache__", ".venv"}

# Fragments are joined only at runtime so the scanner cannot match its own source.
_PERSONAL = [
    "L" + "inda", "M" + "arc", "蒋" + "昊宇",
    "袁" + "睿", "庄" + "雯媛", "陈" + "伟宏",
]
_ORGANISATIONS = ["绿" + "云", "雷" + "迪森", "望" + "湖", "云" + "旅", "腾" + "讯"]
_INTERNAL = [
    "Work" + "Buddy", "current" + "_portfolio", "boll" + "_items",
    "Weekly" + "_strategy", "geopolitical" + "_events.json",
    "temporary" + "_strategy_watch", "automation-" + "1", "ashare" + "-factcheck",
    "@" + "skill", "反脆弱" + "周盘策略",
]

_SUBJECT_CODES = [
    "600" + "820", "601" + "899", "002" + "153", "603" + "277",
    "588" + "950", "516" + "150", "600" + "030", "601" + "318",
    "588" + "000", "000" + "538",
]

# Assemble regexes at runtime so no scanner can match its own source text.
_PATH_PATTERN = re.compile(
    "/" + "Users" + "/|" + "/" + "home" + "/|" + r"[A-Za-z]:\\"
)
_CREDENTIAL_PATTERN = re.compile(
    "gh" + "o_[A-Za-z0-9]{10}|"
    "s" + "k-[A-Za-z0-9]{16}|"
    "a" + "k_[A-Za-z0-9]{12}"
)

PATTERNS = {
    "local_absolute_path": _PATH_PATTERN,
    "credential": _CREDENTIAL_PATTERN,
    "real_subject_code": re.compile("|".join(map(re.escape, _SUBJECT_CODES))),
    "personal_name": re.compile("|".join(map(re.escape, _PERSONAL))),
    "private_organisation": re.compile("|".join(map(re.escape, _ORGANISATIONS))),
    "private_implementation": re.compile("|".join(map(re.escape, _INTERNAL))),
}


def public_text_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name in EXCLUDED_FILES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if any(part in rel for part in EXCLUDED_PARTS):
            continue
        yield path, rel


def scan():
    hits = []
    for path, rel in public_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                hits.append(f"{rel}:{line} [{label}]")
    return hits


class PublicPrivacyTests(unittest.TestCase):
    def test_no_private_data_in_public_text(self):
        self.assertEqual(scan(), [])

    def test_scanner_covers_the_new_docs(self):
        names = {rel for _, rel in public_text_files()}
        for expected in ("README.md", "PUBLIC_PROTOCOL.md", "docs/CASE-STUDIES.md"):
            self.assertIn(expected, names)

    def test_scanner_detects_a_planted_leak(self):
        """A guard that cannot fail is not a guard."""
        probe = ROOT / ".privacy_probe.tmp.md"
        try:
            probe.write_text("draft note " + "/" + "Us" + "ers/" + "someone/notes.md", encoding="utf-8")
            self.assertTrue(any("local_absolute_path" in hit for hit in scan()))
        finally:
            probe.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
