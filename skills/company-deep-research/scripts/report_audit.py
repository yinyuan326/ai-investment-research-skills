#!/usr/bin/env python3
"""Audit structural and substantive minimums in a Markdown company report."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CORE_CONCEPTS = {
    "decision summary": ("决策摘要", "decision summary", "executive summary"),
    "industry and demand": ("行业", "市场", "industry", "market"),
    "business model": ("商业模式", "单位经济", "business model", "unit economics"),
    "competition": ("竞争", "护城河", "competition", "competitive", "moat"),
    "financials": ("财务", "financial"),
    "valuation": ("估值", "valuation"),
    "risks": ("风险", "risk"),
    "scenarios": ("情景", "scenario"),
    "conclusion": ("结论", "conclusion"),
    "evidence": ("证据矩阵", "来源", "source", "evidence matrix"),
}


def contains_any(text: str, variants: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(variant.lower() in lowered for variant in variants)


def unique_years(pattern: str, text: str) -> set[str]:
    return set(re.findall(pattern, text, re.I))


def count_methods(text: str) -> tuple[int, list[str]]:
    methods = {
        "DCF": ("DCF", "现金流折现", "折现现金流"),
        "SOTP": ("SOTP", "分部估值", "sum of the parts"),
        "trading comparables": ("可比公司", "交易倍数", "trading comparables", "peer multiples"),
        "transactions": ("可比交易", "先例交易", "precedent transaction"),
        "asset value": ("资产价值", "重置成本", "清算价值", "asset value", "replacement cost"),
    }
    found = [name for name, variants in methods.items() if contains_any(text, variants)]
    return len(found), found


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument(
        "--mode",
        choices=("public-formal", "private-formal", "note"),
        default="public-formal",
    )
    args = parser.parse_args()

    if not args.report.is_file():
        raise SystemExit(f"report not found: {args.report}")
    text = args.report.read_text(encoding="utf-8")
    lowered = text.lower()
    failures: list[str] = []
    warnings: list[str] = []

    for concept, variants in CORE_CONCEPTS.items():
        if not contains_any(text, variants):
            failures.append(f"missing required concept: {concept}")

    placeholders = re.findall(r"\b(?:TODO|TBD|FIXME)\b|待补充|待确认|\[待[^]]+\]", text, re.I)
    if placeholders:
        failures.append(f"contains {len(placeholders)} unresolved placeholder(s)")

    links = re.findall(r"\[[^\]]+\]\(https?://[^)]+\)|https?://\S+", text)
    if args.mode != "note" and len(links) < 8:
        failures.append(f"only {len(links)} web source link(s); formal evidence coverage is too thin")
    elif len(links) < 12:
        warnings.append(f"only {len(links)} web source link(s); review evidence coverage")

    labels = ("[事实]", "[公司口径]", "[计算]", "[判断]")
    label_count = sum(text.count(label) for label in labels)
    if args.mode != "note" and label_count < 12:
        failures.append(f"only {label_count} claim labels; fact/judgment separation is too sparse")

    evidence_rows = re.findall(r"^\|\s*C\d{2,}\s*\|", text, re.M | re.I)
    if args.mode != "note" and len(evidence_rows) < 10:
        failures.append(f"only {len(evidence_rows)} evidence-matrix claim rows")
    elif len(evidence_rows) < 15:
        warnings.append(f"only {len(evidence_rows)} evidence-matrix claim rows; check coverage")

    page_citations = re.findall(r"(?:\bp\.?\s*\d+\b|第\s*\d+\s*页)", text, re.I)
    if args.mode != "note" and len(page_citations) < 5:
        warnings.append("fewer than five page-level citations found")

    if args.mode == "public-formal":
        actual_years = unique_years(r"\b(20\d{2})A\b", text)
        forecast_years = unique_years(r"\b(20\d{2})E\b|\b(20\d{2})年预测", text)
        forecast_years = {year for groups in forecast_years for year in (groups if isinstance(groups, tuple) else (groups,)) if year}
        if len(actual_years) < 3:
            failures.append(f"only {len(actual_years)} explicitly labeled actual fiscal years; require at least three")
        if len(forecast_years) < 3:
            failures.append(f"only {len(forecast_years)} explicit forecast years; require at least three")

        driver_groups = {
            "volume/adoption": ("销量", "产量", "采用率", "volume", "adoption"),
            "price/mix": ("价格", "均价", "产品结构", "price", "mix"),
            "margin": ("毛利率", "EBITDA率", "margin"),
            "capex": ("资本开支", "capex"),
            "working capital": ("营运资本", "周转天数", "working capital"),
        }
        missing_drivers = [name for name, variants in driver_groups.items() if not contains_any(text, variants)]
        if missing_drivers:
            failures.append("missing forecast driver coverage: " + ", ".join(missing_drivers))

        if not contains_any(text, ("需求桥", "需求到收入", "demand bridge", "industry-to-revenue")):
            failures.append("industry-demand-to-company-revenue bridge not identified")
        if not contains_any(text, ("自由现金流", "FCFF", "FCF", "free cash flow")):
            failures.append("free-cash-flow forecast or analysis not identified")
        if not contains_any(text, ("稀释股", "摊薄股", "diluted shares")):
            failures.append("diluted-share analysis not identified")
        if not contains_any(text, ("少数股东", "非控股权益", "minority interest", "non-controlling")):
            warnings.append("minority-interest treatment not identified")

        method_count, method_names = count_methods(text)
        if method_count < 2:
            failures.append(f"only {method_count} independent primary valuation method(s): {', '.join(method_names) or 'none'}")
        if not contains_any(text, ("反向估值", "隐含预期", "reverse valuation", "reverse expectations")):
            failures.append("reverse valuation / embedded-expectations test not identified")

        scenario_groups = (
            ("熊市", "悲观", "bear"),
            ("基准", "base"),
            ("牛市", "乐观", "bull"),
        )
        if not all(contains_any(text, variants) for variants in scenario_groups):
            failures.append("bear/base/bull scenario set is incomplete")

        images = re.findall(r"!\[[^\]]*\]\([^)]+\)", text)
        if len(images) < 4:
            failures.append(f"only {len(images)} embedded visual(s); formal public report requires four when data supports")

    elif args.mode == "private-formal":
        if not contains_any(text, ("融资", "稀释", "financing", "dilution")):
            failures.append("financing and dilution analysis not identified")
        if not contains_any(text, ("单位经济", "贡献毛利", "unit economics", "contribution margin")):
            failures.append("unit-economics analysis not identified")
        if not contains_any(text, ("退出", "回报", "IRR", "MOIC", "exit", "return")):
            failures.append("investor return or exit analysis not identified")

    if "企业价值" not in text and "enterprise value" not in lowered:
        warnings.append("enterprise-value terminology not found")
    if not contains_any(text, ("股权价值", "市值", "equity value", "market cap")):
        warnings.append("equity-value or market-cap terminology not found")

    print(f"Audit: {args.report}")
    print(f"Mode: {args.mode}")
    print(f"Evidence links: {len(links)}; claim labels: {label_count}; evidence rows: {len(evidence_rows)}; page citations: {len(page_citations)}")
    for item in failures:
        print(f"FAIL: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    if failures:
        raise SystemExit(1)
    if warnings:
        print("PASS WITH WARNINGS: manual review required")
    else:
        print("PASS: institutional minimum checks satisfied")


if __name__ == "__main__":
    main()
