# Valuation framework

## 1. Minimum standard

For a formal public-company report, use at least two independent primary valuation methods appropriate to the business and add a reverse-expectations test. Do not count two terminal multiples applied to the same earnings forecast as independent methods.

Select from:

- DCF or dividend/cash-flow valuation;
- sum of the parts (SOTP);
- trading comparables;
- precedent transactions;
- asset, replacement-cost, or liquidation value;
- probability-weighted milestone valuation for pre-revenue options.

Use reverse valuation to reveal what the current price requires, not as the only fair-value method.

## 2. DCF discipline

Forecast operating drivers and FCFF explicitly. State forecast horizon, WACC, terminal growth or exit multiple, tax, capex, working capital, net debt, minority interests, non-operating assets, diluted shares, and valuation date.

Use:

`FCFF = EBIT x (1 - tax) + D&A - capex - change in operating working capital`

`Terminal value = final forecast FCFF x (1 + g) / (WACC - g)`

Check that `WACC > g`. Explain why WACC and terminal growth fit the currency, geography, cyclicality, leverage, and maturity. Show WACC-versus-terminal-growth sensitivity and disclose how much enterprise value comes from the terminal value.

## 3. SOTP discipline

Use SOTP when segments differ materially in growth, margin, capital intensity, risk, maturity, or suitable peer set. For each segment state metric, forecast period, multiple or DCF basis, value range, ownership, and source. Deduct net debt, minority claims, holding-company costs, and other liabilities once; add non-operating assets once.

Do not give unproven options the same multiple as qualified, cash-generating businesses. Probability-weight or assign a bounded option value with explicit milestones.

## 4. Comparables discipline

Choose peers for economic similarity, not merely shared industry labels. Show:

- market-data date and currency;
- enterprise value, equity value, and diluted shares;
- revenue, EBITDA/EBIT, earnings, growth, margins, ROIC, and leverage;
- actual and forecast period consistency;
- accounting or business-model differences;
- median/range and the reason for any premium or discount.

Avoid comparing P/E across companies with materially different tax, leverage, minority interests, or loss-making segments without adjustment.

## 5. Reverse expectations

Solve for the volume, price, margin, reinvestment, timing, and terminal multiple required by the current enterprise or equity value. Compare those requirements with capacity, historical execution, industry demand, competitor economics, and funding constraints.

## 6. Reconciliation and conclusion

Present a valuation reconciliation:

| Method | Key inputs | Equity-value range | Per-share range | Weight/relevance | Main limitation |
|---|---|---:|---:|---|---|

Use a range rather than false precision. Explain why methods disagree and which evidence would move the range. Show upside/downside from the cutoff-date price, but do not present the result as personalized advice.

## 7. Mechanical helpers

Use `scripts/dcf_valuation.py` for a reproducible FCFF DCF and sensitivity table. Use `scripts/valuation_sensitivity.py` to test reverse EV/revenue and EV/EBITDA expectations. Independently check all inputs before interpreting outputs.
