"""
PDF generator matching the exact Word doc theme:
- Font: Times New Roman throughout, 12pt body
- Margins: 1 inch on all sides
- Section header fills: #FAC090 (title), #CCC1D9 (objectives), #C2D69B (outcomes)
- Page 2: "FLUID MECHANICS" navy #002060, "COURSE CONTENT" purple #7030A0 14pt
- Signing authority box pinned to page footer on every page via canvas callback
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, Frame
from reportlab.platypus.frames import Frame as RLFrame

# ── Colours ───────────────────────────────────────────────────────────────────
BLACK       = colors.black
WHITE       = colors.white
PEACH       = colors.HexColor("#FAC090")
LAVENDER    = colors.HexColor("#CCC1D9")
LIGHT_GREEN = colors.HexColor("#C2D69B")
NAVY        = colors.HexColor("#002060")
PURPLE      = colors.HexColor("#7030A0")

# ── Margins & dimensions ──────────────────────────────────────────────────────
MARGIN      = 1 * inch                    # 1 inch all sides
PAGE_W      = A4[0] - 2 * MARGIN         # usable content width
PAGE_H      = A4[1]

FOOTER_H    = 1.1 * cm                   # height of the signing authority box
FOOTER_Y    = MARGIN - FOOTER_H - 0.15 * cm   # sits just inside the bottom margin

SIGNATORIES_DEFAULT = ["BOS Chairperson", "Dean (Academic)", "Principal"]


# ── Styles ────────────────────────────────────────────────────────────────────
def _s():
    base = getSampleStyleSheet()
    def ps(name, **kw):
        return ParagraphStyle(name, parent=base["Normal"], **kw)
    TNR = "Times-Roman"
    TNB = "Times-Bold"
    return {
        "body":    ps("BD",  fontSize=12, fontName=TNR, leading=15, alignment=TA_JUSTIFY),
        "bodyL":   ps("BDL", fontSize=12, fontName=TNR, leading=15, alignment=TA_LEFT),
        "cc":      ps("CC",  fontSize=12, fontName=TNR, leading=15, alignment=TA_CENTER),
        "hdrC":    ps("HC",  fontSize=12, fontName=TNB, leading=15, alignment=TA_CENTER),
        "hdrL":    ps("HL",  fontSize=12, fontName=TNB, leading=15, alignment=TA_LEFT),
        "hdrJ":    ps("HJ",  fontSize=12, fontName=TNB, leading=15, alignment=TA_JUSTIFY),
        "p2title": ps("P2T", fontSize=12, fontName=TNB, leading=15,
                      alignment=TA_CENTER, textColor=NAVY),
        "p2sub":   ps("P2S", fontSize=14, fontName=TNB, leading=17,
                      alignment=TA_CENTER, textColor=PURPLE),
    }


# ── Footer drawing callback ───────────────────────────────────────────────────
def _make_footer_cb(signatories):
    """Return an onPage callback that draws the signing authority box."""
    n   = len(signatories)
    col = PAGE_W / n
    x0  = MARGIN
    y0  = FOOTER_Y

    def draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Bold", 10)
        canvas.setStrokeColor(BLACK)
        canvas.setLineWidth(0.75)

        # Outer rectangle
        canvas.rect(x0, y0, PAGE_W, FOOTER_H)

        # Inner vertical dividers
        for i in range(1, n):
            canvas.line(x0 + i * col, y0, x0 + i * col, y0 + FOOTER_H)

        # Signatory text centred in each cell
        canvas.setFont("Times-Bold", 10)
        for i, sig in enumerate(signatories):
            cx = x0 + i * col + col / 2
            cy = y0 + FOOTER_H / 2 - 5   # vertically centred
            canvas.drawCentredString(cx, cy, sig)

        canvas.restoreState()

    return draw_footer


# ── Table style helper ────────────────────────────────────────────────────────
def _box(extra=None):
    cmds = [
        ("BOX",           (0, 0), (-1, -1), 0.75, BLACK),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5,  BLACK),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ]
    if extra:
        cmds.extend(extra)
    return TableStyle(cmds)


# ── Content tables ────────────────────────────────────────────────────────────
def _header_table(data, s):
    half = PAGE_W / 2
    rows = [
        [Paragraph(data.get("course_title", ""), s["hdrC"]), ""],
        [Paragraph(f"Total Credits  : {data.get('total_credits','')}", s["body"]),
         Paragraph(f"Subject Code  : {data.get('subject_code','')}", s["body"])],
        [Paragraph("Teaching Scheme", s["body"]),
         Paragraph("Examination Scheme", s["body"])],
        [Paragraph(f"Teaching Hrs /Week : {data.get('teaching_hrs','')}", s["body"]),
         Paragraph(f"Duration of End Semester Exam : {data.get('exam_duration','')}", s["body"])],
        [Paragraph(f"Tutorials Hrs/ Week : {data.get('tutorial_hrs','')}", s["body"]),
         Paragraph(f"Internal Evaluation                      : {data.get('internal_marks','')}", s["body"])],
        [Paragraph(f"Practical Hrs/ Week  : {data.get('practical_hrs','')}", s["body"]),
         Paragraph(f"End Semester Examination         : {data.get('ese_marks','')}", s["body"])],
    ]
    tbl = Table(rows, colWidths=[half, half])
    tbl.setStyle(_box([
        ("SPAN",       (0, 0), (1, 0)),
        ("BACKGROUND", (0, 0), (1, 0), PEACH),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl


def _objectives_table(objectives, s):
    num_w = 0.9 * cm
    txt_w = PAGE_W - num_w
    rows  = [[Paragraph("Course Objectives", s["hdrC"]), ""]]
    for i, obj in enumerate(objectives, 1):
        rows.append([Paragraph(str(i), s["cc"]), Paragraph(obj, s["body"])])
    tbl = Table(rows, colWidths=[num_w, txt_w])
    tbl.setStyle(_box([
        ("SPAN",       (0, 0), (1, 0)),
        ("BACKGROUND", (0, 0), (1, 0), LAVENDER),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl


def _outcomes_table(outcomes, s):
    co_w  = 1.3 * cm
    txt_w = PAGE_W - co_w
    rows  = [
        [Paragraph("Course Outcomes", s["hdrC"]), ""],
        [Paragraph("After completion of syllabus, students would be able to", s["hdrJ"]), ""],
    ]
    for co in outcomes:
        rows.append([
            Paragraph(co.get("label", ""), s["cc"]),
            Paragraph(co.get("desc", ""), s["body"]),
        ])
    tbl = Table(rows, colWidths=[co_w, txt_w])
    tbl.setStyle(_box([
        ("SPAN",       (0, 0), (1, 0)),
        ("BACKGROUND", (0, 0), (1, 0), LIGHT_GREEN),
        ("SPAN",       (0, 1), (1, 1)),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl


def _content_table(data, s):
    rows = [
        [Paragraph(data.get("course_title", "").upper(), s["p2title"])],
        [Paragraph("COURSE CONTENT", s["p2sub"])],
    ]
    for i, unit in enumerate(data.get("units", []), 1):
        cell = (
            f"<b>UNIT {_roman(i)}: {unit.get('title','')}</b><br/>"
            f"{unit.get('content','')}"
        )
        rows.append([Paragraph(cell, s["body"])])
    if data.get("textbooks"):
        tb = "<b>Text books:</b><br/>" + "<br/>".join(
            f"\u2022 {t}" for t in data["textbooks"])
        rows.append([Paragraph(tb, s["bodyL"])])
    if data.get("refbooks"):
        rb = "<b>Reference books:</b><br/>" + "<br/>".join(
            f"\u2022 {r}" for r in data["refbooks"])
        rows.append([Paragraph(rb, s["bodyL"])])
    tbl = Table(rows, colWidths=[PAGE_W])
    tbl.setStyle(_box([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return tbl


# ── Main ──────────────────────────────────────────────────────────────────────
def generate_syllabus_pdf(data: dict) -> bytes:
    buffer = io.BytesIO()

    signatories = data.get("signatories", SIGNATORIES_DEFAULT)
    footer_cb   = _make_footer_cb(signatories)

    # Content frame: full 1-inch margins; bottom margin is raised to leave
    # room for the pinned footer box (footer sits below the frame).
    frame = RLFrame(
        MARGIN, MARGIN,          # x, y (bottom-left of frame)
        PAGE_W,                  # width
        PAGE_H - 2 * MARGIN,    # height
        leftPadding=0, rightPadding=0,
        topPadding=0,  bottomPadding=0,
    )

    template = PageTemplate(id="main", frames=[frame], onPage=footer_cb)

    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        pageTemplates=[template],
    )

    s = _s()
    story = []

    # PAGE 1
    story.append(_header_table(data, s))
    story.append(Spacer(1, 8))
    story.append(_objectives_table(data.get("objectives", []), s))
    story.append(Spacer(1, 8))
    story.append(_outcomes_table(data.get("outcomes", []), s))

    # PAGE 2
    story.append(PageBreak())
    story.append(_content_table(data, s))

    doc.build(story)
    return buffer.getvalue()


def _roman(n: int) -> str:
    vals = [(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
    r = ""
    for v, sym in vals:
        while n >= v:
            r += sym; n -= v
    return r
