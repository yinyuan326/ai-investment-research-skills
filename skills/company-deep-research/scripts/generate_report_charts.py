#!/usr/bin/env python3
"""Generate consistent research-report charts from a JSON specification."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


COLORS = ["#17324D", "#2E638C", "#6E96B5", "#B58A4A", "#7A3E65", "#4C7A68"]
GRID = "#D9E1E7"
TEXT = "#24313D"
MUTED = "#667684"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="JSON chart specification")
    parser.add_argument("--output-dir", type=Path, default=Path("charts"))
    parser.add_argument("--font", type=Path, help="Optional CJK font path")
    return parser.parse_args()


def select_font(override: Path | None) -> font_manager.FontProperties:
    candidates = [
        override,
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
        Path("C:/Windows/Fonts/msyh.ttc"),
    ]
    for candidate in candidates:
        if candidate and candidate.expanduser().is_file():
            return font_manager.FontProperties(fname=str(candidate.expanduser()))
    return font_manager.FontProperties(family="DejaVu Sans")


def validate_output(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9._-]+\.png", name):
        raise ValueError(f"invalid output filename: {name}")
    return name


def validate_series(chart: dict, x: list[str]) -> list[dict]:
    series = chart.get("series")
    if not isinstance(series, list) or not series:
        raise ValueError("line/bar/stacked_bar charts require non-empty series")
    for item in series:
        values = item.get("values")
        if not isinstance(values, list) or len(values) != len(x):
            raise ValueError("each series must have one numeric value per x label")
        item["values"] = [float(value) for value in values]
    return series


def style_axis(ax, chart: dict, font: font_manager.FontProperties) -> None:
    ax.set_title(chart.get("title", ""), loc="left", fontsize=14, color=TEXT, pad=14, fontproperties=font)
    if chart.get("subtitle"):
        ax.text(0, 1.01, chart["subtitle"], transform=ax.transAxes, fontsize=8.5, color=MUTED, fontproperties=font)
    ax.set_ylabel(chart.get("y_label", ""), color=MUTED, fontproperties=font)
    ax.set_xlabel(chart.get("x_label", ""), color=MUTED, fontproperties=font)
    ax.grid(axis="y", color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8.5)
    for label in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        label.set_fontproperties(font)


def line_chart(ax, chart: dict, font: font_manager.FontProperties) -> None:
    x = [str(value) for value in chart.get("x", [])]
    series = validate_series(chart, x)
    positions = np.arange(len(x))
    for index, item in enumerate(series):
        ax.plot(
            positions,
            item["values"],
            marker="o",
            linewidth=2.2,
            markersize=4.5,
            label=item.get("name", f"Series {index + 1}"),
            color=item.get("color", COLORS[index % len(COLORS)]),
        )
    ax.set_xticks(positions, x)
    style_axis(ax, chart, font)


def bar_chart(ax, chart: dict, font: font_manager.FontProperties, stacked: bool) -> None:
    x = [str(value) for value in chart.get("x", [])]
    series = validate_series(chart, x)
    positions = np.arange(len(x))
    if stacked:
        bottom = np.zeros(len(x))
        for index, item in enumerate(series):
            values = np.array(item["values"])
            ax.bar(
                positions,
                values,
                bottom=bottom,
                width=0.62,
                label=item.get("name", f"Series {index + 1}"),
                color=item.get("color", COLORS[index % len(COLORS)]),
            )
            bottom += values
    else:
        width = min(0.72 / len(series), 0.28)
        offset = (len(series) - 1) * width / 2
        for index, item in enumerate(series):
            ax.bar(
                positions - offset + index * width,
                item["values"],
                width=width * 0.9,
                label=item.get("name", f"Series {index + 1}"),
                color=item.get("color", COLORS[index % len(COLORS)]),
            )
    ax.set_xticks(positions, x)
    style_axis(ax, chart, font)


def heatmap_chart(ax, chart: dict, font: font_manager.FontProperties) -> None:
    x = [str(value) for value in chart.get("x", [])]
    y = [str(value) for value in chart.get("y", [])]
    values = np.array(chart.get("values", []), dtype=float)
    if values.shape != (len(y), len(x)):
        raise ValueError("heatmap values must match y rows and x columns")
    image = ax.imshow(values, cmap=chart.get("cmap", "Blues"), aspect="auto")
    ax.set_xticks(np.arange(len(x)), x)
    ax.set_yticks(np.arange(len(y)), y)
    number_format = chart.get("number_format", ".1f")
    threshold = (float(values.min()) + float(values.max())) / 2
    for row in range(len(y)):
        for col in range(len(x)):
            color = "white" if values[row, col] > threshold else TEXT
            ax.text(col, row, format(values[row, col], number_format), ha="center", va="center", color=color, fontsize=8.5, fontproperties=font)
    ax.set_title(chart.get("title", ""), loc="left", fontsize=14, color=TEXT, pad=14, fontproperties=font)
    ax.set_xlabel(chart.get("x_label", ""), color=MUTED, fontproperties=font)
    ax.set_ylabel(chart.get("y_label", ""), color=MUTED, fontproperties=font)
    ax.tick_params(length=0, colors=MUTED)
    for label in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        label.set_fontproperties(font)
    plt.colorbar(image, ax=ax, fraction=0.035, pad=0.03)


def render_chart(chart: dict, output_dir: Path, font: font_manager.FontProperties) -> Path:
    chart_type = chart.get("type")
    output = output_dir / validate_output(chart.get("output", ""))
    width = float(chart.get("width", 8.6))
    height = float(chart.get("height", 4.8))
    fig, ax = plt.subplots(figsize=(width, height), facecolor="white")

    if chart_type == "line":
        line_chart(ax, chart, font)
    elif chart_type == "bar":
        bar_chart(ax, chart, font, stacked=False)
    elif chart_type == "stacked_bar":
        bar_chart(ax, chart, font, stacked=True)
    elif chart_type == "heatmap":
        heatmap_chart(ax, chart, font)
    else:
        raise ValueError(f"unsupported chart type: {chart_type}")

    if chart_type != "heatmap" and chart.get("series"):
        legend = ax.legend(frameon=False, loc=chart.get("legend_location", "best"), prop=font)
        for text in legend.get_texts():
            text.set_color(TEXT)

    source = chart.get("source")
    if source:
        fig.text(0.01, 0.01, f"Source: {source}", fontsize=7.5, color=MUTED, fontproperties=font)
    fig.tight_layout(rect=(0, 0.04 if source else 0, 1, 1))
    fig.savefig(output, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output


def main() -> None:
    args = parse_args()
    if not args.spec.is_file():
        raise SystemExit(f"spec file not found: {args.spec}")
    data = json.loads(args.spec.read_text(encoding="utf-8"))
    charts = data.get("charts")
    if not isinstance(charts, list) or not charts:
        raise SystemExit("spec must contain a non-empty 'charts' list")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    font = select_font(args.font)
    for chart in charts:
        try:
            output = render_chart(chart, args.output_dir, font)
        except (TypeError, ValueError, KeyError) as exc:
            raise SystemExit(f"invalid chart specification: {exc}") from exc
        print(f"Rendered {output}")


if __name__ == "__main__":
    main()
