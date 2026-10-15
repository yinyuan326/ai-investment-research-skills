#!/usr/bin/env python3
"""Calculate an FCFF DCF and a WACC/terminal-growth sensitivity table."""

from __future__ import annotations

import argparse


def positive(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return number


def rate(value: str) -> float:
    number = float(value)
    if not -0.5 < number < 1.0:
        raise argparse.ArgumentTypeError("rate must be expressed as a decimal")
    return number


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fcff", nargs="+", required=True, type=float)
    parser.add_argument("--wacc", required=True, type=rate)
    parser.add_argument("--terminal-growth", required=True, type=rate)
    parser.add_argument(
        "--net-debt",
        required=True,
        type=float,
        help="Debt minus cash; use a negative value for net cash.",
    )
    parser.add_argument("--shares", required=True, type=positive)
    parser.add_argument("--unit", default="RMB mn")
    parser.add_argument("--wacc-grid", nargs="*", type=rate)
    parser.add_argument("--growth-grid", nargs="*", type=rate)
    return parser.parse_args()


def dcf(fcff: list[float], wacc: float, growth: float) -> tuple[float, float, float]:
    if wacc <= growth:
        raise ValueError("WACC must be greater than terminal growth")
    if not fcff or any(value <= 0 for value in fcff):
        raise ValueError("all FCFF values must be greater than zero")

    present_value = sum(
        value / ((1 + wacc) ** year) for year, value in enumerate(fcff, start=1)
    )
    terminal_value = fcff[-1] * (1 + growth) / (wacc - growth)
    terminal_present_value = terminal_value / ((1 + wacc) ** len(fcff))
    enterprise_value = present_value + terminal_present_value
    return enterprise_value, terminal_present_value, present_value


def default_grid(center: float, offsets: tuple[float, ...]) -> list[float]:
    return [round(center + offset, 6) for offset in offsets]


def fmt(value: float) -> str:
    return f"{value:,.2f}"


def main() -> None:
    args = parse_args()
    try:
        enterprise_value, terminal_pv, explicit_pv = dcf(
            args.fcff, args.wacc, args.terminal_growth
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    equity_value = enterprise_value - args.net_debt
    per_share = equity_value / args.shares
    terminal_share = terminal_pv / enterprise_value

    print(f"Unit: {args.unit}")
    print(f"Forecast FCFF: {', '.join(fmt(value) for value in args.fcff)}")
    print(f"WACC: {args.wacc:.1%}")
    print(f"Terminal growth: {args.terminal_growth:.1%}")
    print(f"Explicit-period PV: {fmt(explicit_pv)}")
    print(f"Terminal-value PV: {fmt(terminal_pv)}")
    print(f"Terminal value / EV: {terminal_share:.1%}")
    print(f"Enterprise value: {fmt(enterprise_value)}")
    print(f"Net debt: {fmt(args.net_debt)}")
    print(f"Equity value: {fmt(equity_value)}")
    print(f"Diluted shares: {fmt(args.shares)}")
    print(f"Per-share value: {fmt(per_share)}")
    print()

    wacc_grid = args.wacc_grid or default_grid(args.wacc, (-0.02, -0.01, 0, 0.01, 0.02))
    growth_grid = args.growth_grid or default_grid(
        args.terminal_growth, (-0.01, -0.005, 0, 0.005, 0.01)
    )

    print("| Terminal growth / WACC | " + " | ".join(f"{w:.1%}" for w in wacc_grid) + " |")
    print("|---|" + "---:|" * len(wacc_grid))
    for growth in growth_grid:
        cells: list[str] = []
        for wacc in wacc_grid:
            if wacc <= growth:
                cells.append("n.m.")
                continue
            ev, _, _ = dcf(args.fcff, wacc, growth)
            cells.append(fmt((ev - args.net_debt) / args.shares))
        print(f"| {growth:.1%} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
