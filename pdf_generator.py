"""
PDF Interview Guide Generator for Living Legacy.

Uses fpdf2 to produce a clean, professional PDF from the project data
and the curated question bank.
"""

import io
from collections import OrderedDict
from datetime import datetime

from fpdf import FPDF


def _safe(text: str) -> str:
    """Replace Unicode characters that Helvetica/latin-1 cannot encode."""
    replacements = {
        "\u2014": "--",   # em-dash
        "\u2013": "-",    # en-dash
        "\u2018": "'",    # left single quote
        "\u2019": "'",    # right single quote (apostrophe)
        "\u201c": '"',    # left double quote
        "\u201d": '"',    # right double quote
        "\u2026": "...",  # ellipsis
        "\u2022": "-",    # bullet
        "\u00a0": " ",    # non-breaking space
    }
    for char, repl in replacements.items():
        text = text.replace(char, repl)
    # Fallback: strip anything else outside latin-1
    return text.encode("latin-1", errors="replace").decode("latin-1")


class InterviewGuidePDF(FPDF):
    """Custom PDF with header / footer branding."""

    def __init__(self, subject_name: str, legacy_type: str):
        super().__init__()
        self.subject_name = _safe(subject_name)
        self.legacy_type = _safe(legacy_type)
        self.set_auto_page_break(auto=True, margin=25)

    # ── Header ──────────────────────────────────────────────────────────
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(90, 130, 150)
        self.cell(0, 8, "Living Legacy  |  Interview Guide", align="L")
        self.cell(
            0, 8,
            _safe(f"{self.subject_name}'s {self.legacy_type}"),
            align="R", new_x="LMARGIN", new_y="NEXT",
        )
        self.set_draw_color(90, 130, 150)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    # ── Footer ──────────────────────────────────────────────────────────
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def generate_interview_guide_pdf(
    project_data: dict,
    questions: OrderedDict,
    priority_map: dict | None = None,
) -> bytes:
    """
    Build a PDF interview guide and return it as raw bytes.

    Parameters
    ----------
    project_data : dict
        The project scope dict (from build_project_data).
    questions : OrderedDict
        { category: [question, ...] } -- curated & possibly user-edited.
    priority_map : dict | None
        Optional { question_text: priority_label } where priority_label
        is one of "Must Ask", "Nice to Have", "Optional".
        If None every question is treated equally.

    Returns
    -------
    bytes
        The PDF file content.
    """
    subject = _safe(project_data["subject"]["name"])
    legacy_type = _safe(project_data["legacy_type"])

    pdf = InterviewGuidePDF(subject_name=subject, legacy_type=legacy_type)
    pdf.alias_nb_pages()
    pdf.add_page()

    # ── Title page content ──────────────────────────────────────────────
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(46, 64, 87)  # #2E4057
    pdf.cell(0, 14, "Interview Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(74, 124, 143)  # #4A7C8F
    pdf.cell(0, 10, _safe(f"{subject}'s {legacy_type}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"Prepared on {datetime.now().strftime('%B %d, %Y')}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Audience & relationship summary
    audiences = ", ".join(project_data.get("target_audience", []))
    relationship = project_data["subject"].get("relationship", "")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, _safe(f"Target audience: {audiences}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, _safe(f"Captured by: {relationship}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    if project_data.get("audience_notes"):
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_x(10)
        pdf.multi_cell(0, 5, _safe(f"Audience notes: {project_data['audience_notes']}"), align="C")
        pdf.ln(4)

    # ── Tips box ────────────────────────────────────────────────────────
    pdf.add_page()
    _section_heading(pdf, "Tips for a Great Interview")
    tips = [
        "Find a quiet, comfortable place with minimal distractions.",
        "Let the storyteller speak freely. Follow the story, not just the script.",
        'Use follow-up prompts like: "Tell me more about that" or "How did that make you feel?"',
        "Silence is okay. Give them time to think and remember.",
        "Record the interview if possible (audio or video) in addition to taking notes.",
        "It's fine to skip questions or change the order. This guide is a starting point.",
        "If emotions come up, be patient and compassionate. Some stories need time.",
        "Focus on specific memories and details rather than generalities.",
        "Take breaks as needed. This doesn't have to happen in one sitting.",
    ]
    for tip in tips:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        pdf.set_x(15)
        pdf.multi_cell(0, 6, _safe(f"- {tip}"))
        pdf.ln(1)

    pdf.ln(4)

    # ── Priority legend (if priorities are provided) ────────────────────
    if priority_map:
        _section_heading(pdf, "Priority Legend")
        for label, desc in [
            ("MUST ASK", "Essential questions that form the core of the legacy."),
            ("NICE TO HAVE", "Valuable questions if time and energy allow."),
            ("OPTIONAL", "Bonus questions -- great if the conversation goes there naturally."),
        ]:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(46, 64, 87)
            pdf.cell(28, 6, f"[{label}]")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 6, _safe(desc), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)

    # ── Question sections ───────────────────────────────────────────────
    for category, q_list in questions.items():
        # Category heading
        pdf.add_page()
        _section_heading(pdf, _safe(category))

        for idx, question in enumerate(q_list, 1):
            priority = ""
            if priority_map and question in priority_map:
                priority = f"  [{priority_map[question].upper()}]"

            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(46, 64, 87)
            question_text = _safe(f"{idx}. {question}{priority}")
            pdf.set_x(10)
            pdf.multi_cell(0, 6, question_text)

            # Notes lines (light gray ruled lines for handwritten notes)
            pdf.set_draw_color(210, 210, 210)
            pdf.set_line_width(0.2)
            y_start = pdf.get_y() + 2
            for line_num in range(3):
                y = y_start + (line_num * 7)
                if y > 270:  # near bottom margin
                    pdf.add_page()
                    y = pdf.get_y() + 2
                    y_start = y - (line_num * 7)
                pdf.line(15, y, 195, y)
            pdf.set_y(y_start + 3 * 7 + 3)

    # ── Final page ──────────────────────────────────────────────────────
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(46, 64, 87)
    pdf.cell(0, 12, "Thank you for preserving what matters most.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.set_x(10)
    pdf.multi_cell(0, 6, _safe(
        "Every question is a doorway into a memory. "
        "Not every door needs to be opened today. "
        "Take your time, enjoy the conversation, and let the stories come."
    ), align="C")

    return bytes(pdf.output())


def generate_scope_summary_pdf(project_data: dict) -> bytes:
    """
    Build a one-page Project Brief PDF and return it as raw bytes.

    Parameters
    ----------
    project_data : dict
        The project scope dict (from build_project_data).

    Returns
    -------
    bytes
        The PDF file content.
    """
    subject = _safe(project_data["subject"]["name"])
    legacy_type = _safe(project_data["legacy_type"])
    legacy_desc = _safe(project_data.get("legacy_description", ""))

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    page_w = pdf.w - 20  # usable width (10mm margins each side)

    # ── Accent bar at top ────────────────────────────────────────────
    pdf.set_fill_color(46, 64, 87)  # #2E4057
    pdf.rect(0, 0, 210, 6, "F")
    pdf.set_fill_color(74, 124, 143)  # #4A7C8F
    pdf.rect(0, 6, 210, 2, "F")
    pdf.ln(14)

    # ── Title ────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(46, 64, 87)
    pdf.cell(0, 10, "Living Legacy Project Brief", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(74, 124, 143)
    pdf.cell(0, 8, _safe(f"{subject}'s {legacy_type}"),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Date generated
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(140, 140, 140)
    pdf.cell(0, 5, f"Generated {datetime.now().strftime('%B %d, %Y')}",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Thin divider
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.3)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(6)

    # ── Helper: section label + value ────────────────────────────────
    LABEL_COL_W = 45  # mm reserved for the label column

    def _field(label: str, value: str):
        safe_label = _safe(label)
        safe_value = _safe(value)

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(46, 64, 87)
        label_w = pdf.get_string_width(safe_label) + 2  # +2 for padding

        if label_w <= LABEL_COL_W:
            # Label fits in the fixed column → side-by-side layout
            pdf.cell(LABEL_COL_W, 6, safe_label)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(page_w - LABEL_COL_W, 6, safe_value)
        else:
            # Label is too long → stacked layout (label above, value indented)
            pdf.multi_cell(page_w, 6, safe_label)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(60, 60, 60)
            pdf.set_x(10 + LABEL_COL_W)  # indent the value
            pdf.multi_cell(page_w - LABEL_COL_W, 6, safe_value)
        pdf.ln(2)

    # ── Subject ──────────────────────────────────────────────────────
    _field("Subject:", subject)
    relationship = project_data["subject"].get("relationship", "")
    if relationship:
        _field("Relationship:", relationship)

    # ── Legacy Type ──────────────────────────────────────────────────
    _field("Legacy Type:", f"{legacy_type} -- {legacy_desc}")

    # ── Target Audience ──────────────────────────────────────────────
    audiences = project_data.get("target_audience", [])
    if audiences:
        _field("Target Audience:", ", ".join(audiences))
    audience_notes = project_data.get("audience_notes", "")
    if audience_notes:
        _field("Audience Notes:", audience_notes)

    # ── Key Themes / Focus Areas ─────────────────────────────────────
    # Collect theme selections from scoping_details (multiselect answers)
    themes = []
    for _q_text, answer in project_data.get("scoping_details", {}).items():
        if isinstance(answer, list):
            themes.extend(answer)
    if themes:
        _field("Key Themes:", ", ".join(themes))

    # ── Scoping Highlights (non-list answers) ────────────────────────
    for q_text, answer in project_data.get("scoping_details", {}).items():
        if isinstance(answer, str) and answer:
            _field(f"{q_text}:", answer)

    # ── Delivery Formats ─────────────────────────────────────────────
    formats = project_data.get("delivery_formats", [])
    if formats:
        _field("Delivery Format(s):", ", ".join(formats))

    # ── Timeline ─────────────────────────────────────────────────────
    timeline = project_data.get("timeline", "")
    if timeline:
        _field("Timeline:", timeline)

    # ── Additional Notes ─────────────────────────────────────────────
    notes = project_data.get("additional_notes", "")
    if notes:
        _field("Additional Notes:", notes)

    # ── Footer accent ────────────────────────────────────────────────
    pdf.ln(4)
    pdf.set_draw_color(74, 124, 143)
    pdf.set_line_width(0.3)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(140, 140, 140)
    pdf.cell(0, 5, "Living Legacy -- Preserving stories that matter.",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5,
             "Share this brief with family members or stakeholders "
             "to explain the project scope.",
             align="C", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())


def _section_heading(pdf: FPDF, title: str):
    """Draw a styled section heading."""
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(74, 124, 143)
    pdf.cell(0, 10, _safe(title), new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(74, 124, 143)
    pdf.set_line_width(0.6)
    pdf.line(10, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(6)
