# Public-company operating model

Use this framework for a formal listed-company report. The model may live in the Markdown report, a spreadsheet, or both, but its material inputs and outputs must be visible and reproducible.

## 1. Establish the perimeter

Record consolidated entities, material subsidiaries, associates, minority interests, discontinued operations, diluted securities, and reporting segments. Reconcile segment revenue and profit to consolidated totals before forecasting.

## 2. Build the historical base

Use at least three fiscal years and the latest interim period. Capture:

- revenue by material segment or product;
- volume, price/mix, capacity, utilization, and backlog where disclosed;
- gross profit, operating expenses, EBITDA/EBIT, tax, minority interests, and adjusted net income;
- operating cash flow, maintenance and growth capex, free cash flow, and net debt;
- receivable, inventory, payable, contract-liability, and cash-conversion metrics;
- diluted shares, stock compensation, options, convertibles, and other dilution.

Normalize one-offs explicitly. Never overwrite reported figures with adjusted figures.

## 3. Forecast segments from drivers

Use a separate driver block for every material segment:

| Segment | Driver | Latest A | Y1E | Y2E | Y3E | Source/rationale | Sensitivity |
|---|---|---:|---:|---:|---:|---|---|
| Example | Volume | | | | | | |
| Example | Price/mix | | | | | | |
| Example | Revenue | | | | | volume x price | |
| Example | Gross margin | | | | | yield/cost/mix | |
| Example | Capex | | | | | capacity plan | |

Use disclosed data where available. If a driver is undisclosed, use a bounded proxy and identify it as `[判断]`; do not back-solve a precise input merely to reach a desired result.

For capacity projects, model construction, qualification, ramp, yield, utilization, depreciation, working capital, and breakeven separately. Announced nameplate capacity is not saleable output.

## 4. Link to consolidated statements

At minimum calculate:

- `Revenue = sum(segment revenue)`
- `Gross profit = sum(segment revenue x segment gross margin)`
- `EBIT = gross profit - operating expenses - other operating costs`
- `NOPAT = EBIT x (1 - normalized tax rate)`
- `FCFF = NOPAT + D&A - capex - change in operating working capital`
- `Equity value = enterprise value - net debt - minority claims + non-operating assets`
- `Per-share value = equity value / diluted shares`

Explain material differences between EBITDA, EBIT, net income, operating cash flow, and free cash flow.

## 5. Forecast horizon and notation

Show at least three explicit forecast years for a formal report and preferably five when the investment thesis depends on a multi-year ramp. Label actual and estimate periods, for example `2025A`, `2026E`, and `2027E`. Do not mix quarterly annualization with audited annual figures without reconciliation.

## 6. Scenario architecture

Use one model architecture for bear, base, and bull cases. Change only identified drivers: volume/adoption, price/mix, yield/utilization, margin, capex, working capital, timing, funding, and valuation assumptions. Each scenario must produce revenue, earnings, cash flow, net debt, diluted shares, and value or return.

## 7. Integrity checks

Before delivery verify:

1. segment revenue sums to consolidated revenue;
2. margins and cash flows recalculate from displayed inputs;
3. capex and depreciation are plausible relative to capacity and assets;
4. working-capital assumptions reconcile to days or turnover;
5. minority interests and diluted shares are included once;
6. enterprise-to-equity bridge signs are correct;
7. scenario outputs reconcile to the same forecast model;
8. valuation does not use an earnings definition inconsistent with the selected multiple;
9. historical data matches cited filings;
10. every material assumption has a source, rationale, range, or explicit unknown label.
