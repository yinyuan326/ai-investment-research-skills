---
name: company-deep-research
description: Produce evidence-based institutional-quality company research in editable Markdown and polished PDF, with traceable sources, industry-to-revenue bridges, operating forecasts, valuation cross-checks, scenarios, risks, catalysts, and falsification conditions. Use for public-company investment reports, private-company or VC/PE diligence, commercial and technology diligence, competitor studies, investment-thesis testing, valuation work, PDF research reports, and updates to an existing company report.
---

# Company Deep Research

## Purpose

Turn a company and a decision question into a reproducible investment case. Treat the report as an evidence-and-model system, not a polished company profile. Separate facts, company claims, calculations, and judgments; connect industry demand to company economics; show what the current valuation requires; state what would invalidate the conclusion.

Default to Chinese unless the user requests another language. Do not reduce a formal report to a quick note merely because data collection or modeling is difficult.

## Route by assignment

- Use **formal public-company mode** for “深度研究”, “研报”, “投资价值”, listed-company diligence, or a requested PDF. Apply every public-company hard gate below.
- Use **formal private-company mode** for VC/PE or private-company diligence. Replace unavailable public-market forecasts with commercial, unit-economic, financing, dilution, and return scenarios; label unavailable information.
- Use **research-note mode** only when the user explicitly asks for a short answer, update, or limited question. State that it is not a full report.

## Required references

Read before research:

- `references/research-method.md` for evidence, triangulation, and analysis discipline.
- `references/report-template.md` for the decision-oriented report structure.
- `references/citation-standard.md` for source planning and page-level citations.
- `references/quality-checklist.md` before delivery.

Also read:

- `references/public-company-model.md` for a formal listed-company report.
- `references/valuation-framework.md` whenever valuation or investment return matters.
- `references/pdf-output.md` for a formal report or PDF.

## Formal public-company hard gates

Do not call a listed-company report complete unless it includes, or explicitly explains why reliable public data cannot support:

1. at least three historical fiscal years plus the latest interim period;
2. at least three explicit forecast years, separated from actual periods;
3. a segment or product driver model using volume/adoption, price/mix, margin, capex, and working-capital assumptions;
4. a bottom-up industry-demand-to-company-revenue bridge for the main growth thesis;
5. named competitors and substitutes compared on like-for-like quantitative and qualitative dimensions;
6. normalized earnings, cash conversion, capital intensity, dilution, minority interests, and funding needs;
7. at least two independent valuation methods appropriate to the company, plus reverse valuation of current expectations;
8. bear, base, and bull scenarios that reconcile to the operating model and valuation;
9. page-level citations for decision-critical filing claims and independent corroboration for material management claims;
10. at least four decision-useful visuals when sufficient data exists: operating/financial trend, segment or demand bridge, valuation/sensitivity, and catalyst/risk view.

Unknown values remain unknown or ranges. Never invent inputs to satisfy a gate. Explain the missing evidence and how it affects confidence.

## Workflow

### 1. Define the decision and research standard

Establish the investable entity, cutoff date and time, audience, horizon, geography, requested mode, currency, and decision question. For a public company, record the date-specific price, diluted share count, market capitalization, net debt, and enterprise value.

### 2. Build an issue tree and source plan

Prioritize questions that can change revenue, margins, cash flow, valuation, or risk. Create a claim ledger before drafting. Start with filings, regulator records, official statistics, technical documents, and procurement or contract evidence. Use secondary sources for context and contradiction, not as substitutes for available primary evidence.

### 3. Translate industry evidence into company economics

Define the value chain, profit pools, market boundaries, demand units, adoption constraints, and realistic obtainable market. Build a visible bridge:

`industry units × content or spend per unit × addressable share × company capture × price = company revenue`

Test the bridge against company capacity, utilization, customer qualification, supply constraints, and competitor response. Do not equate industry growth, announced capacity, pilots, or framework agreements with revenue.

### 4. Build the operating model before writing the conclusion

Follow `references/public-company-model.md`. Reconcile historical segment data to consolidated financials. Forecast each material segment from disclosed or bounded drivers. Link segment revenue to gross profit, operating expenses, taxes, capex, working capital, free cash flow, net debt, diluted shares, and per-share outcomes.

Keep actuals and estimates visibly distinct. Show formulas and assumption sources. Make scenarios coherent worlds, not arbitrary percentage changes.

### 5. Value and challenge the thesis

Follow `references/valuation-framework.md`. Use at least two independent primary valuation lenses and a reverse-expectations test when data permits. Reconcile equity value and enterprise value, explain terminal multiples or discount rates, and present sensitivity to the two or three assumptions that drive most of the result.

Run deterministic helpers where useful:

```bash
python3 scripts/valuation_sensitivity.py --equity-value 350 --net-debt -5 --revenue 18 25 35 --ebitda 2 6 12 --unit "RMB bn"
python3 scripts/dcf_valuation.py --fcff 1.2 1.8 2.6 3.4 4.2 --wacc 0.10 --terminal-growth 0.03 --net-debt 5 --shares 100 --unit "RMB mn"
```

Present the strongest bull and bear cases fairly. Identify observable thesis breakers and the next evidence most likely to change the view.

### 6. Write, visualize, and render

Use `references/report-template.md`. Write Markdown first as the canonical source. Generate decision-useful charts from audited inputs; `scripts/generate_report_charts.py` can create consistent line, bar, stacked-bar, and heatmap charts from JSON specifications. Embed local charts with normal Markdown image syntax.

For a formal report, deliver both `.md` and `.pdf` unless the user requests only one:

```bash
python3 scripts/render_report_pdf.py REPORT.md REPORT.pdf
```

### 7. Audit before delivery

1. score the report with `references/quality-checklist.md`;
2. run `python3 scripts/report_audit.py REPORT.md --mode public-formal` for a listed company, or the matching mode;
3. recalculate forecast, valuation, per-share, and sensitivity outputs;
4. verify that scenario values reconcile to the operating model;
5. render the PDF to images and inspect every page containing a chart or dense table, plus the cover, contents, summary, valuation, and final page;
6. fix failures; do not waive a critical gate silently.

## Output rules

- Lead with a one-page decision summary containing stance, confidence, fair-value or expectation range where supportable, upside/downside context, catalysts, and thesis breakers.
- Use `[事实]`, `[公司口径]`, `[计算]`, and `[判断]` consistently.
- Put citations next to claims; include document date, data period, and filing page for decision-critical facts.
- Distinguish reported, adjusted, forecast, and scenario figures. State units, currency, accounting period, and equity-versus-enterprise value.
- Quantify uncertainty with bounded ranges and sensitivities; never disguise missing evidence with precise numbers.
- Keep a complete evidence matrix and an open-diligence list.
- Do not present the report as personalized investment advice.

## Boundaries

Do not invent undisclosed customers, contracts, market shares, technical performance, segment economics, or private financials. Do not assume announced capacity equals qualified output, a framework contract equals committed revenue, or management guidance equals independently verified fact. When a formal gate cannot be met, state the missing evidence, use a bounded proxy only if defensible, lower confidence, and show how the conclusion changes.
