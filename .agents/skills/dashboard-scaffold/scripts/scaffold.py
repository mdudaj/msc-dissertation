#!/usr/bin/env python3
"""Placeholder generator for the dashboard-scaffold skill.

The scaffold is still stabilizing. This script documents the intended CLI and
fails closed until template assets are added.
"""

from __future__ import annotations

import argparse
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a minimal Django auth/dashboard scaffold.",
    )
    parser.add_argument("--target", default=".", help="Target repository path.")
    parser.add_argument("--product", required=True, help="Product name, e.g. Kisomo.")
    parser.add_argument(
        "--variant",
        choices=("operational", "educational-research", "executive-overview"),
        default="educational-research",
        help="Dashboard design variant.",
    )
    parser.add_argument("--primary", required=True, help="Primary theme color.")
    parser.add_argument("--secondary", required=True, help="Secondary theme color.")
    parser.add_argument("--accent", required=True, help="Accent theme color.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print intended action without writing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(
        "dashboard-scaffold generator is not active yet. "
        "Use SKILL.md and references/current-baseline.md for the current manual scaffold.",
        file=sys.stderr,
    )
    print(
        {
            "target": args.target,
            "product": args.product,
            "variant": args.variant,
            "primary": args.primary,
            "secondary": args.secondary,
            "accent": args.accent,
            "dry_run": args.dry_run,
        }
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
