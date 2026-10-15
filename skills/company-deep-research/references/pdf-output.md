# PDF and visualization workflow

## 1. Keep canonical and presentation deliverables

- Keep Markdown as the editable, auditable source.
- Use PDF as the presentation-ready artifact.
- Generate PDF only after evidence, model, valuation, and structural checks pass.
- Keep chart input data and generated images with the working files so visuals remain reproducible.

## 2. Create decision-useful visuals

For a formal report, include at least four visuals when reliable data exists:

1. historical and forecast operating or financial trend;
2. segment mix, industry-demand bridge, or capacity/ramp view;
3. valuation reconciliation or sensitivity;
4. catalysts, scenario outcomes, or risk heatmap.

Every chart must show title, unit, actual-versus-estimate periods, source or assumption note, and readable legend. Avoid dual axes unless necessary and clearly labeled. Never invent data to fill a chart.

The bundled chart helper accepts a JSON specification:

```bash
python3 scripts/generate_report_charts.py charts.json --output-dir charts
```

Each chart entry uses `type` (`line`, `bar`, `stacked_bar`, or `heatmap`), `output`, `title`, labels, source, and data. Example:

```json
{
  "charts": [
    {
      "type": "line",
      "output": "financial-trend.png",
      "title": "Revenue and free-cash-flow trend",
      "x": ["2024A", "2025A", "2026E", "2027E"],
      "y_label": "RMB mn",
      "series": [
        {"name": "Revenue", "values": [100, 120, 150, 190]},
        {"name": "FCFF", "values": [8, 10, 14, 20]}
      ],
      "source": "Filings and base-case model"
    }
  ]
}
```

Embed local charts in Markdown:

```markdown
![收入、利润与预测趋势（单位：亿元；2026E起为预测）](charts/financial-trend.png)
```

The PDF renderer resolves image paths relative to the Markdown file.

## 3. Render

```bash
python3 scripts/render_report_pdf.py path/to/report.md path/to/report.pdf
```

The renderer creates an A4 report with cover, contents, hierarchy, styled tables, local charts, clickable web links, headers, footers, and page numbers. It auto-detects and embeds a common system Chinese font. If detection fails, pass an embeddable `.ttf` or `.ttc` with `--font`.

`generate_report_charts.py` requires Matplotlib and NumPy. `render_report_pdf.py` requires ReportLab. Check the active interpreter and use the Codex workspace runtime or install only the missing packages in the active environment. If Matplotlib cannot write its default cache, set `MPLCONFIGDIR` to a writable temporary directory.

## 4. Verify portability and layout

Render the PDF with a standards-based renderer rather than relying only on the native preview application:

```bash
pdftoppm -png -r 130 report.pdf tmp/report-page
```

Inspect:

1. cover and contents;
2. one-page summary;
3. every page with a chart;
4. widest financial, competitor, forecast, and risk tables;
5. valuation and sensitivity pages;
6. final page and appendices.

Reject and regenerate for missing or blank Chinese glyphs, unembedded fonts, clipped text, overlapping rows, orphaned headings, unreadable legends, distorted charts, broken links, unexpected blank pages, or missing page numbers.

## 5. Delivery

- Use a descriptive filename containing company and cutoff year.
- Deliver Markdown and PDF with clear labels unless the user requests one format only.
- State cutoff date/time and preserve the investment-advice disclaimer.
- Do not delete the source, chart inputs, or calculation trail after rendering.
