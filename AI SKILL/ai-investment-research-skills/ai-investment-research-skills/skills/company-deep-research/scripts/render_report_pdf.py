#!/usr/bin/env python3
"""Render an investor research report from Markdown to a polished Chinese PDF."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image as ReportImage,
    KeepTogether,
    ListFlowable,
    ListItem,
    LongTable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2E638C")
LIGHT_BLUE = colors.HexColor("#EAF1F7")
PALE = colors.HexColor("#F5F7F9")
TEXT = colors.HexColor("#24313D")
MUTED = colors.HexColor("#667684")
RULE = colors.HexColor("#CBD5DD")
WHITE = colors.white


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a Markdown investment report as an A4 PDF."
    )
    parser.add_argument("input", type=Path, help="Markdown source file")
    parser.add_argument("output", type=Path, help="Destination PDF file")
    parser.add_argument("--author", default="Independent Research")
    parser.add_argument(
        "--font",
        type=Path,
        help="Optional CJK TrueType/OpenType font path; common system fonts are auto-detected.",
    )
    return parser.parse_args()


def register_fonts(font_override: Path | None = None) -> Path:
    candidates = [
        font_override,
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ]
    font_path = None
    errors: list[str] = []
    for candidate in candidates:
        if not candidate or not candidate.expanduser().is_file():
            continue
        candidate = candidate.expanduser()
        try:
            pdfmetrics.registerFont(
                TTFont("ResearchCJK", str(candidate), subfontIndex=0)
            )
            font_path = candidate
            break
        except Exception as exc:
            errors.append(f"{candidate}: {exc}")
    if font_path is None:
        raise SystemExit(
            "No usable embeddable CJK font found. Pass one with --font /path/to/font.ttf. "
            + " | ".join(errors)
        )
    pdfmetrics.registerFontFamily(
        "ResearchCJK",
        normal="ResearchCJK",
        bold="ResearchCJK",
        italic="ResearchCJK",
        boldItalic="ResearchCJK",
    )
    return font_path


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="ResearchCJK",
            fontSize=25,
            leading=36,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=18,
            wordWrap="CJK",
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta",
            parent=base["BodyText"],
            fontName="ResearchCJK",
            fontSize=10.5,
            leading=19,
            textColor=MUTED,
            wordWrap="CJK",
        ),
        "toc_title": ParagraphStyle(
            "TocTitle",
            parent=base["Heading1"],
            fontName="ResearchCJK",
            fontSize=20,
            leading=27,
            textColor=NAVY,
            spaceAfter=16,
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "Heading1CJK",
            parent=base["Heading1"],
            fontName="ResearchCJK",
            fontSize=17,
            leading=24,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "Heading2CJK",
            parent=base["Heading2"],
            fontName="ResearchCJK",
            fontSize=13.5,
            leading=20,
            textColor=BLUE,
            spaceBefore=11,
            spaceAfter=6,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h3": ParagraphStyle(
            "Heading3CJK",
            parent=base["Heading3"],
            fontName="ResearchCJK",
            fontSize=11.5,
            leading=17,
            textColor=NAVY,
            spaceBefore=9,
            spaceAfter=4,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "BodyCJK",
            parent=base["BodyText"],
            fontName="ResearchCJK",
            fontSize=9.3,
            leading=15.5,
            textColor=TEXT,
            alignment=TA_JUSTIFY,
            spaceAfter=5,
            wordWrap="CJK",
            splitLongWords=True,
        ),
        "bullet": ParagraphStyle(
            "BulletCJK",
            parent=base["BodyText"],
            fontName="ResearchCJK",
            fontSize=9.1,
            leading=14.8,
            textColor=TEXT,
            leftIndent=15,
            bulletIndent=2,
            bulletFontName="Helvetica-Bold",
            bulletFontSize=8,
            bulletColor=BLUE,
            wordWrap="CJK",
        ),
        "quote": ParagraphStyle(
            "QuoteCJK",
            parent=base["BodyText"],
            fontName="ResearchCJK",
            fontSize=9.1,
            leading=15,
            textColor=MUTED,
            leftIndent=12,
            borderColor=BLUE,
            borderWidth=1.5,
            borderPadding=(4, 8, 4, 8),
            wordWrap="CJK",
        ),
        "table": ParagraphStyle(
            "TableCJK",
            parent=base["BodyText"],
            fontName="ResearchCJK",
            fontSize=7.1,
            leading=10.2,
            textColor=TEXT,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "table_header": ParagraphStyle(
            "TableHeaderCJK",
            parent=base["BodyText"],
            fontName="ResearchCJK",
            fontSize=7.2,
            leading=10.3,
            textColor=WHITE,
            alignment=TA_CENTER,
            wordWrap="CJK",
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.4,
            leading=10,
            textColor=TEXT,
            backColor=PALE,
            borderPadding=7,
        ),
        "caption": ParagraphStyle(
            "CaptionCJK",
            parent=base["BodyText"],
            fontName="ResearchCJK",
            fontSize=7.8,
            leading=11.5,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=8,
            wordWrap="CJK",
        ),
    }


def plain_text(value: str) -> str:
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("**", "").replace("`", "")
    return value.strip()


def inline_markup(value: str) -> str:
    links: list[tuple[str, str]] = []

    def save_link(match: re.Match[str]) -> str:
        links.append((match.group(1), match.group(2)))
        return f"@@LINK{len(links) - 1}@@"

    value = value.replace(r"\*", "*").replace(r"\_", "_")
    value = re.sub(r"\[([^]]+)\]\((https?://[^)]+)\)", save_link, value)
    value = html.escape(value, quote=False)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r"<font color='#6E3B67'>\1</font>", value)
    for label, color in (
        ("[事实]", "#176B52"),
        ("[公司口径]", "#8A5A13"),
        ("[计算]", "#2E638C"),
        ("[判断]", "#7A3E65"),
    ):
        value = value.replace(html.escape(label), f"<font color='{color}'><b>{label}</b></font>")
    for index, (label, url) in enumerate(links):
        link = (
            f"<link href='{html.escape(url, quote=True)}' color='#1F5C99'>"
            f"{html.escape(label)}</link>"
        )
        value = value.replace(f"@@LINK{index}@@", link)
    return value


def display_width(value: str) -> int:
    text = plain_text(value)
    return sum(2 if ord(char) > 127 else 1 for char in text)


def table_widths(rows: list[list[str]], available: float) -> list[float]:
    columns = len(rows[0])
    raw = []
    for col in range(columns):
        longest = max(display_width(row[col]) if col < len(row) else 1 for row in rows)
        raw.append(max(5.0, min(float(longest), 24.0)))
    total = sum(raw)
    widths = [available * item / total for item in raw]
    minimum = min(37.0, available / columns * 0.68)
    widths = [max(minimum, width) for width in widths]
    scale = available / sum(widths)
    return [width * scale for width in widths]


class ResearchDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, title: str, author: str) -> None:
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=19 * mm,
            bottomMargin=17 * mm,
            title=title,
            author=author,
            subject="Investor-grade company deep research report",
        )
        self.report_title = title
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="report-frame",
        )
        self.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=self._draw_page)])

    def _draw_page(self, canvas, doc) -> None:
        page = canvas.getPageNumber()
        canvas.saveState()
        if page == 1:
            canvas.setFillColor(NAVY)
            canvas.rect(0, A4[1] - 24 * mm, A4[0], 24 * mm, fill=1, stroke=0)
            canvas.setFillColor(BLUE)
            canvas.rect(A4[0] - 32 * mm, 0, 32 * mm, 7 * mm, fill=1, stroke=0)
        else:
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.45)
            canvas.line(self.leftMargin, A4[1] - 12 * mm, A4[0] - self.rightMargin, A4[1] - 12 * mm)
            canvas.setFont("ResearchCJK", 7.5)
            canvas.setFillColor(MUTED)
            header = plain_text(self.report_title)
            if len(header) > 38:
                header = header[:38] + "..."
            canvas.drawString(self.leftMargin, A4[1] - 9.2 * mm, header)
            canvas.drawRightString(A4[0] - self.rightMargin, 9 * mm, f"第 {page} 页")
            canvas.drawString(self.leftMargin, 9 * mm, "独立研究 · 非个性化投资建议")
        canvas.restoreState()

    def afterFlowable(self, flowable) -> None:
        level = getattr(flowable, "_toc_level", None)
        if level is None:
            return
        text = plain_text(flowable.getPlainText())
        key = f"heading-{self.seq.nextf('heading')}"
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level=level, closed=False)
        self.notify("TOCEntry", (level, text, self.page, key))


def extract_frontmatter(lines: list[str]) -> tuple[str, list[str], list[str]]:
    title = "公司深度研究报告"
    title_index = 0
    for index, line in enumerate(lines):
        if line.startswith("# "):
            title = plain_text(line[2:])
            title_index = index
            break
    metadata: list[str] = []
    body_start = title_index + 1
    for index in range(title_index + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped == "---":
            body_start = index + 1
            break
        if stripped:
            metadata.append(plain_text(stripped))
    return title, metadata, lines[body_start:]


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    rows: list[list[str]] = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|"):
        cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            rows.append(cells)
        index += 1
    width = max(len(row) for row in rows)
    return [row + [""] * (width - len(row)) for row in rows], index


def report_image(
    source: str,
    caption: str,
    base_dir: Path,
    styles: dict[str, ParagraphStyle],
) -> KeepTogether:
    source = source.strip().strip("<>")
    if re.match(r"https?://", source):
        raise SystemExit(
            f"remote Markdown image is not supported by the PDF renderer: {source}; "
            "download it locally and cite the source in the caption"
        )
    path = (base_dir / source).resolve() if not Path(source).is_absolute() else Path(source)
    if not path.is_file():
        raise SystemExit(f"Markdown image not found: {path}")
    image = ReportImage(str(path))
    max_width = A4[0] - 36 * mm
    max_height = 112 * mm
    scale = min(max_width / image.imageWidth, max_height / image.imageHeight, 1.0)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    items = [image]
    if caption:
        items.append(Paragraph(inline_markup(caption), styles["caption"]))
    else:
        items.append(Spacer(1, 6))
    return KeepTogether(items)


def markdown_story(
    markdown: str,
    styles: dict[str, ParagraphStyle],
    base_dir: Path,
) -> tuple[str, list]:
    lines = markdown.splitlines()
    title, metadata, body = extract_frontmatter(lines)
    story: list = [Spacer(1, 34 * mm)]
    title_parts = re.match(r"^(.+?[）)])\s*(.+)$", title)
    if title_parts:
        title_markup = inline_markup(title_parts.group(1)) + "<br/>" + inline_markup(title_parts.group(2))
    else:
        title_markup = inline_markup(title)
    story.append(Paragraph(title_markup, styles["cover_title"]))
    story.append(HRFlowable(width="34%", thickness=3, color=BLUE, hAlign="LEFT", spaceAfter=15))
    for item in metadata:
        story.append(Paragraph(inline_markup(item), styles["cover_meta"]))
    story.extend([Spacer(1, 12 * mm), Paragraph("证据驱动 · 情景估值 · 风险与证伪", styles["cover_meta"]), PageBreak()])

    story.append(Paragraph("目录", styles["toc_title"]))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOC1",
            fontName="ResearchCJK",
            fontSize=9.4,
            leading=15,
            textColor=NAVY,
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=3,
            wordWrap="CJK",
        ),
        ParagraphStyle(
            "TOC2",
            fontName="ResearchCJK",
            fontSize=8.2,
            leading=12.5,
            textColor=MUTED,
            leftIndent=12,
            firstLineIndent=0,
            wordWrap="CJK",
        ),
    ]
    story.extend([toc, PageBreak()])

    index = 0
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph_lines:
            value = " ".join(item.strip() for item in paragraph_lines)
            story.append(Paragraph(inline_markup(value), styles["body"]))
            paragraph_lines.clear()

    while index < len(body):
        line = body[index]
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            index += 1
            continue
        if stripped.startswith("```"):
            flush_paragraph()
            code: list[str] = []
            index += 1
            while index < len(body) and not body[index].strip().startswith("```"):
                code.append(body[index])
                index += 1
            story.append(Preformatted("\n".join(code), styles["code"]))
            index += 1
            continue
        image_match = re.match(r"^!\[([^]]*)\]\(([^)]+)\)\s*$", stripped)
        if image_match:
            flush_paragraph()
            story.append(
                report_image(
                    image_match.group(2),
                    image_match.group(1),
                    base_dir,
                    styles,
                )
            )
            index += 1
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            depth = len(heading.group(1))
            style_name = {1: "h1", 2: "h1", 3: "h2"}[depth]
            paragraph = Paragraph(inline_markup(heading.group(2)), styles[style_name])
            if depth <= 2:
                paragraph._toc_level = 0
            story.append(paragraph)
            index += 1
            continue
        if stripped == "---":
            flush_paragraph()
            story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceBefore=4, spaceAfter=6))
            index += 1
            continue
        if stripped.startswith("|") and index + 1 < len(body) and body[index + 1].strip().startswith("|"):
            flush_paragraph()
            rows, index = parse_table(body, index)
            if rows:
                rendered = []
                for row_index, row in enumerate(rows):
                    style = styles["table_header"] if row_index == 0 else styles["table"]
                    rendered.append([Paragraph(inline_markup(cell), style) for cell in row])
                table = LongTable(
                    rendered,
                    colWidths=table_widths(rows, A4[0] - 36 * mm),
                    repeatRows=1,
                    hAlign="LEFT",
                    splitByRow=1,
                )
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                            ("BACKGROUND", (0, 1), (-1, -1), WHITE),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
                            ("GRID", (0, 0), (-1, -1), 0.35, RULE),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
                            ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                        ]
                    )
                )
                story.extend([table, Spacer(1, 6)])
            continue
        if stripped.startswith(">"):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped.lstrip("> ")), styles["quote"]))
            index += 1
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        numbered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if bullet:
            flush_paragraph()
            while index < len(body):
                candidate = body[index].strip()
                match = re.match(r"^[-*]\s+(.+)$", candidate)
                if not match:
                    break
                story.append(
                    Paragraph(
                        inline_markup(match.group(1)),
                        styles["bullet"],
                        bulletText="-",
                    )
                )
                index += 1
            story.append(Spacer(1, 3))
            continue
        if numbered:
            flush_paragraph()
            items = []
            while index < len(body):
                candidate = body[index].strip()
                match = re.match(r"^\d+[.)]\s+(.+)$", candidate)
                if not match:
                    break
                items.append(
                    ListItem(
                        Paragraph(inline_markup(match.group(1)), styles["bullet"]),
                        leftIndent=12,
                    )
                )
                index += 1
            story.append(
                ListFlowable(
                    items,
                    bulletType="1",
                    start="1",
                    leftIndent=16,
                    bulletFontName="ResearchCJK",
                    bulletFontSize=8,
                    bulletColor=BLUE,
                    spaceAfter=5,
                )
            )
            continue
        paragraph_lines.append(line)
        index += 1

    flush_paragraph()
    return title, story


def main() -> None:
    args = parse_args()
    if not args.input.is_file():
        raise SystemExit(f"input file not found: {args.input}")
    if args.output.suffix.lower() != ".pdf":
        raise SystemExit("output path must end in .pdf")
    font_path = register_fonts(args.font)
    styles = make_styles()
    title, story = markdown_story(
        args.input.read_text(encoding="utf-8"),
        styles,
        args.input.resolve().parent,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc = ResearchDocTemplate(str(args.output), title=title, author=args.author)
    doc.multiBuild(story)
    print(f"Rendered {args.output} with font {font_path}")


if __name__ == "__main__":
    main()
