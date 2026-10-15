#!/usr/bin/env python3
"""Calculate reverse EV/revenue and EV/EBITDA multiples from scenario inputs."""

from __future__ import annotations

import argparse


def positive_number(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("scenario values must be greater than zero")
    return number


def fmt(value: float) -> str:
    return f"{value:,.1f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a Markdown reverse-valuation sensitivity table."
    )
    parser.add_argument("--equity-value", required=True, type=positive_number)
    parser.add_argument(
        "--net-debt",
        required=True,
        type=float,
        help="Debt minus cash. Use a negative number for net cash.",
    )
    parser.add_argument("--revenue", required=True, nargs=3, type=positive_number)
    parser.add_argument("--ebitda", required=True, nargs=3, type=positive_number)
    parser.add_argument("--unit", default="USD mn")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    enterprise_value = args.equity_value + args.net_debt
    if enterprise_value <= 0:
        raise SystemExit("enterprise value must be greater than zero")

    labels = ("Bear", "Base", "Bull")
    print(f"Equity value: {fmt(args.equity_value)} {args.unit}")
    print(f"Net debt: {fmt(args.net_debt)} {args.unit}")
    print(f"Enterprise value: {fmt(enterprise_value)} {args.unit}")
    print()
    print("| Scenario | Revenue | EBITDA | EV/Revenue | EV/EBITDA | EBITDA margin |")
    print("|---|---:|---:|---:|---:|---:|")
    for label, revenue, ebitda in zip(labels, args.revenue, args.ebitda):
        print(
            f"| {label} | {fmt(revenue)} | {fmt(ebitda)} | "
            f"{enterprise_value / revenue:.1f}x | {enterprise_value / ebitda:.1f}x | "
            f"{ebitda / revenue:.1%} |"
        )


if __name__ == "__main__":
    main()
