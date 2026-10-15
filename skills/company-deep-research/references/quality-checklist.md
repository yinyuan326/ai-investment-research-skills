# Institutional report quality checklist

Score each of the 30 items as 0 (missing), 1 (partial), or 2 (complete). A formal public-company report has a maximum of 60 and should score at least 52/60, with no zero on a critical item marked `*`. For a private-company report, mark genuinely inapplicable items N/A, explain why, and require at least 87% of applicable points.

## A. Decision usefulness

1. `*` The entity, cutoff date/time, audience, horizon, currency, and decision question are explicit.
2. `*` The opening page states stance, confidence, valuation context, bull case, bear case, catalysts, and thesis breakers.
3. The current price or implied valuation is connected to the operating outcomes required to justify it.
4. The report states what evidence would change the conclusion and the next evidence to monitor.
5. The conclusion follows from the evidence and model rather than from narrative momentum.

## B. Evidence integrity

6. `*` Every decision-critical factual claim has a nearby citation or evidence-matrix entry.
7. Filing claims include document date and page number where available; volatile web data include observation/access time.
8. Primary and authoritative sources are used where reasonably available.
9. Material management claims are attributed, independently corroborated where possible, and confidence-adjusted where not.
10. Conflicting evidence, source incentives, definition differences, and material limitations are disclosed.

## C. Industry, business, and competition

11. `*` Market boundaries and the demand unit are defined; TAM is not treated as obtainable revenue.
12. `*` A bottom-up bridge links industry demand to company volume, price, revenue, margin, and capacity constraints.
13. Technical or operating advantages are linked to measurable customer and economic consequences.
14. Named competitors and substitutes are compared on consistent quantitative and qualitative dimensions.
15. Customer qualification, pricing, backlog or order quality, concentration, supply dependencies, and route-to-market are addressed.

## D. Financial analysis and forecast model

16. `*` At least three historical fiscal years plus the latest interim period use consistent units, periods, currency, and definitions.
17. Historical earnings are normalized for material one-offs, minority interests, dilution, and accounting differences.
18. `*` At least three forecast years are driven by segment volume/adoption, price/mix, margin, capex, and working-capital assumptions.
19. Segment forecasts reconcile to consolidated revenue, earnings, cash flow, net debt, diluted shares, and per-share outcomes.
20. Cash conversion, working-capital days, maintenance/growth capex, funding needs, covenants, and ROIC/returns are addressed where material.

## E. Valuation, uncertainty, and challenge

21. `*` Equity value, enterprise value, net debt, minority claims, non-operating assets, and diluted shares reconcile correctly.
22. `*` At least two independent primary valuation methods are used and their differences are explained.
23. Reverse valuation identifies the growth, margin, reinvestment, timing, and terminal assumptions embedded in the current price.
24. Bear, base, and bull scenarios reconcile to the operating model and valuation; sensitivities expose the key drivers.
25. The strongest contrary case is presented fairly; risks have mechanisms, model impacts, indicators, and falsification conditions.

## F. Presentation and delivery

26. The report uses `[事实]`, `[公司口径]`, `[计算]`, and `[判断]` consistently and avoids false precision.
27. Tables and at least four decision-useful visuals clarify trends, demand bridges, forecast drivers, and valuation rather than decorate the report.
28. The evidence matrix, open-diligence questions, definitions, assumptions, and calculations are complete enough to reproduce the conclusion.
29. No placeholder, broken citation, stale price, inconsistent period, unsupported recommendation, or arithmetic discrepancy remains.
30. `*` The PDF has embedded fonts, readable charts and tables, working links, correct page numbers, and no clipping, overlap, blank glyphs, or unexpected blank pages.

## Required checks

Run:

```bash
python3 scripts/report_audit.py path/to/report.md --mode public-formal
```

Then manually score all 30 items. Automatic checks are necessary but cannot validate source credibility, forecast judgment, model correctness, or investment reasoning.
