#!/usr/bin/env python3
"""Compatibility entry point for the public, research-only runner.

The public repository intentionally does not embed a venue-specific data client,
exposure loader, account integration, or credential. Use ``weekly_review.py`` for
the portable scaffold and implement any market adapter locally.
"""

from __future__ import annotations

from weekly_review import main


if __name__ == "__main__":
    raise SystemExit(main())
