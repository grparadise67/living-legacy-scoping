"""
Living Legacy — Project Scoping Application
Guides users through selecting and scoping their legacy project.
"""

import json
import os
from collections import OrderedDict
from datetime import datetime

import streamlit as st
from legacy_data import (
    LEGACY_TYPES,
    AUDIENCE_OPTIONS,
    DELIVERY_FORMATS,
    TIMELINE_OPTIONS,
)
from question_bank import generate_questions
from pdf_generator import generate_interview_guide_pdf, generate_scope_summary_pdf

# ---------------------------------------------------------------------------
# Output directory for saved project files
# ---------------------------------------------------------------------------
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Living Legacy — Scope Your Story",
    page_icon="🌳",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .main-header h1 {
        color: #2E4057;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #5C7A99;
        font-size: 1.15rem;
    }
    .step-header {
        background: linear-gradient(135deg, #2E4057 0%, #4A7C8F 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
    }
    .legacy-card {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.4rem 0;
        transition: border-color 0.2s;
    }
    .legacy-card:hover {
        border-color: #4A7C8F;
    }
    .summary-box {
        background: #f0f7f4;
        border-left: 4px solid #4A7C8F;
        padding: 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    div[data-testid="stProgress"] > div > div > div {
        background-color: #4A7C8F;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "step": 1,
        "legacy_type": None,
        "scoping_answers": {},
        "audiences": [],
        "audience_detail": "",
        "delivery_formats": [],
        "subject_name": "",
        "subject_relationship": "",
        "timeline": "",
        "additional_notes": "",
        # Question bank state
        "generated_questions": OrderedDict(),
        "priority_map": {},
        "questions_generated": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

TOTAL_STEPS = 6


# ---------------------------------------------------------------------------
# Build project data dictionary from session state
# ---------------------------------------------------------------------------
def build_project_data() -> dict:
    """Assemble all session-state selections into a single dictionary."""
    lt = st.session_state.legacy_type
    lt_data = LEGACY_TYPES[lt]

    # Build a readable scoping section keyed by the question text
    scoping = {}
    for q in lt_data["follow_up_questions"]:
        answer = st.session_state.scoping_answers.get(q["key"], "")
        scoping[q["question"]] = answer

    return {
        "project_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "created_at": datetime.now().isoformat(),
        "legacy_type": lt,
        "legacy_description": lt_data["description"],
        "subject": {
            "name": st.session_state.subject_name,
            "relationship": st.session_state.subject_relationship,
        },
        "scoping_details": scoping,
        "target_audience": st.session_state.audiences,
        "audience_notes": st.session_state.audience_detail,
        "delivery_formats": st.session_state.delivery_formats,
        "timeline": st.session_state.timeline,
        "additional_notes": st.session_state.additional_notes,
    }


def save_project_json(data: dict) -> str:
    """Write the project data to a JSON file in the projects/ folder.
    Returns the absolute path of the saved file."""
    safe_name = data["subject"]["name"].replace(" ", "_")
    filename = f"legacy_{safe_name}_{data['project_id']}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath


def build_text_summary(data: dict) -> str:
    """Return a nicely formatted plain-text summary for download."""
    lines = []
    lines.append("=" * 60)
    lines.append("LIVING LEGACY — PROJECT SCOPE SUMMARY")
    lines.append("=" * 60)
    lines.append(f"Created: {data['created_at']}")
    lines.append(f"Project ID: {data['project_id']}")
    lines.append("")

    lines.append(f"LEGACY TYPE: {data['legacy_type']}")
    lines.append(f"  {data['legacy_description']}")
    lines.append("")

    lines.append("SUBJECT")
    lines.append(f"  Name: {data['subject']['name']}")
    lines.append(f"  Relationship: {data['subject']['relationship']}")
    lines.append("")

    lines.append("SCOPING DETAILS")
    for question, answer in data["scoping_details"].items():
        if isinstance(answer, list):
            answer = ", ".join(answer) if answer else "—"
        lines.append(f"  Q: {question}")
        lines.append(f"  A: {answer}")
        lines.append("")

    lines.append("TARGET AUDIENCE")
    lines.append(f"  {', '.join(data['target_audience'])}")
    if data["audience_notes"]:
        lines.append(f"  Notes: {data['audience_notes']}")
    lines.append("")

    lines.append("DELIVERY FORMAT(S)")
    lines.append(f"  {', '.join(data['delivery_formats'])}")
    lines.append("")

    lines.append(f"TIMELINE: {data['timeline']}")
    lines.append("")

    if data["additional_notes"]:
        lines.append("ADDITIONAL NOTES")
        lines.append(f"  {data['additional_notes']}")
        lines.append("")

    lines.append("=" * 60)
    lines.append("Thank you for preserving what matters most.")
    lines.append("=" * 60)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Progress indicator
# ---------------------------------------------------------------------------
def show_progress():
    step = st.session_state.step
    st.progress(step / TOTAL_STEPS)
    labels = [
        "Legacy Type",
        "Scope",
        "Audience",
        "Format",
        "Review",
        "Questions",
    ]
    cols = st.columns(TOTAL_STEPS)
    for i, (col, label) in enumerate(zip(cols, labels), 1):
        if i < step:
            col.markdown(f"<div style='text-align:center;color:#4A7C8F;font-size:0.78rem;'>✅ {label}</div>", unsafe_allow_html=True)
        elif i == step:
            col.markdown(f"<div style='text-align:center;color:#2E4057;font-weight:bold;font-size:0.78rem;'>● {label}</div>", unsafe_allow_html=True)
        else:
            col.markdown(f"<div style='text-align:center;color:#bbb;font-size:0.78rem;'>○ {label}</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1>🌳 Living Legacy</h1>
        <p>Every life has a story worth preserving.<br>
        Let's figure out the best way to capture yours.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

show_progress()

# =====================================================================
# STEP 1 — Choose Your Legacy Type
# =====================================================================
if st.session_state.step == 1:
    st.markdown('<div class="step-header"><h3>Step 1: What Kind of Legacy Would You Like to Create?</h3></div>', unsafe_allow_html=True)
    st.write("Select the option that best describes what you'd like to preserve. Don't worry — you can always adjust later.")

    for name, data in LEGACY_TYPES.items():
        with st.container():
            col_icon, col_text, col_btn = st.columns([0.8, 8, 2])
            with col_icon:
                st.markdown(f"<div style='font-size:2rem;text-align:center;padding-top:0.6rem;'>{data['icon']}</div>", unsafe_allow_html=True)
            with col_text:
                st.markdown(f"**{name}**")
                st.caption(data["description"])
            with col_btn:
                if st.button("Select", key=f"select_{name}", use_container_width=True):
                    st.session_state.legacy_type = name
                    st.session_state.step = 2
                    st.rerun()
        st.divider()


# =====================================================================
# STEP 2 — Scoping Questions
# =====================================================================
elif st.session_state.step == 2:
    lt = st.session_state.legacy_type
    data = LEGACY_TYPES[lt]

    st.markdown(f'<div class="step-header"><h3>Step 2: Let\'s Scope Your {data["icon"]} {lt}</h3></div>', unsafe_allow_html=True)
    st.write("These questions help us understand the depth and focus of your project.")

    answers = {}
    for q in data["follow_up_questions"]:
        st.markdown(f"**{q['question']}**")

        if q["type"] == "radio":
            answers[q["key"]] = st.radio(
                q["question"],
                q["options"],
                key=f"scope_{q['key']}",
                label_visibility="collapsed",
            )
        elif q["type"] == "multiselect":
            answers[q["key"]] = st.multiselect(
                q["question"],
                q["options"],
                key=f"scope_{q['key']}",
                label_visibility="collapsed",
            )
        elif q["type"] == "text":
            answers[q["key"]] = st.text_input(
                q["question"],
                key=f"scope_{q['key']}",
                placeholder=q.get("placeholder", ""),
                label_visibility="collapsed",
            )
        st.write("")  # spacing

    col_back, col_spacer, col_next = st.columns([2, 6, 2])
    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col_next:
        if st.button("Continue →", key="step2_next", use_container_width=True):
            st.session_state.scoping_answers = answers
            st.session_state.step = 3
            st.rerun()


# =====================================================================
# STEP 3 — Target Audience
# =====================================================================
elif st.session_state.step == 3:
    st.markdown('<div class="step-header"><h3>Step 3: Who Is This Legacy For?</h3></div>', unsafe_allow_html=True)
    st.write(
        "Understanding your audience helps us tailor the tone, depth, and format. "
        "Who do you most want to receive and experience this legacy?"
    )

    st.markdown("**Select all that apply:**")
    selected_audiences = []
    # Display in a 3-column grid
    cols = st.columns(3)
    for i, aud in enumerate(AUDIENCE_OPTIONS):
        with cols[i % 3]:
            checked = st.checkbox(
                f"{aud['icon']} {aud['label']}",
                key=f"aud_{aud['label']}",
                help=aud["description"],
            )
            if checked:
                selected_audiences.append(aud["label"])

    st.write("")
    st.markdown("**Who is the subject of this legacy?**")
    st.caption("Is this your own story, or are you capturing someone else's?")

    subject_relationship = st.radio(
        "Subject relationship",
        [
            "This is my own story",
            "I'm capturing a parent's story",
            "I'm capturing a grandparent's story",
            "I'm capturing a spouse/partner's story",
            "I'm capturing a friend's story",
            "I'm capturing someone else's story",
        ],
        key="subject_rel",
        label_visibility="collapsed",
    )

    subject_name = st.text_input(
        "What is the subject's first name? (The person whose story this is)",
        key="subject_name_input",
        placeholder="e.g., Margaret, Dad, Grandpa Joe",
    )

    st.write("")
    st.markdown("**Is there anything specific about your audience we should know?**")
    audience_detail = st.text_area(
        "Audience details",
        key="audience_detail_input",
        placeholder="e.g., My grandchildren are very young, so keep it simple and visual. / My colleagues would appreciate industry-specific detail.",
        label_visibility="collapsed",
        height=100,
    )

    col_back, col_spacer, col_next = st.columns([2, 6, 2])
    with col_back:
        if st.button("← Back", use_container_width=True, key="step3_back"):
            st.session_state.step = 2
            st.rerun()
    with col_next:
        if st.button("Continue →", key="step3_next", use_container_width=True):
            if not selected_audiences:
                st.error("Please select at least one audience.")
            elif not subject_name.strip():
                st.error("Please provide the subject's name.")
            else:
                st.session_state.audiences = selected_audiences
                st.session_state.audience_detail = audience_detail
                st.session_state.subject_name = subject_name
                st.session_state.subject_relationship = subject_relationship
                st.session_state.step = 4
                st.rerun()


# =====================================================================
# STEP 4 — Delivery Format & Timeline
# =====================================================================
elif st.session_state.step == 4:
    st.markdown('<div class="step-header"><h3>Step 4: Format & Timing</h3></div>', unsafe_allow_html=True)
    st.write("How would you like the finished legacy delivered, and when would you like to get started?")

    st.markdown("**Preferred format(s) — select all that interest you:**")
    selected_formats = []
    cols = st.columns(3)
    for i, fmt in enumerate(DELIVERY_FORMATS):
        with cols[i % 3]:
            checked = st.checkbox(
                f"{fmt['icon']} {fmt['label']}",
                key=f"fmt_{fmt['label']}",
                help=fmt["description"],
            )
            if checked:
                selected_formats.append(fmt["label"])

    st.write("")
    st.markdown("**When would you like to begin?**")
    timeline = st.radio(
        "Timeline",
        TIMELINE_OPTIONS,
        key="timeline_radio",
        label_visibility="collapsed",
    )

    st.write("")
    st.markdown("**Anything else we should know?**")
    additional_notes = st.text_area(
        "Additional notes",
        key="additional_notes_input",
        placeholder="e.g., I have boxes of old photos. / The subject has early-stage memory loss, so we should start soon. / I'd like this ready by Christmas.",
        label_visibility="collapsed",
        height=100,
    )

    col_back, col_spacer, col_next = st.columns([2, 6, 2])
    with col_back:
        if st.button("← Back", use_container_width=True, key="step4_back"):
            st.session_state.step = 3
            st.rerun()
    with col_next:
        if st.button("Review Summary →", key="step4_next", use_container_width=True):
            if not selected_formats:
                st.error("Please select at least one format.")
            else:
                st.session_state.delivery_formats = selected_formats
                st.session_state.timeline = timeline
                st.session_state.additional_notes = additional_notes
                st.session_state.step = 5
                st.rerun()


# =====================================================================
# STEP 5 — Summary / Confirmation
# =====================================================================
elif st.session_state.step == 5:
    st.markdown('<div class="step-header"><h3>Step 5: Your Living Legacy Project Summary</h3></div>', unsafe_allow_html=True)
    st.write("Here's everything you've told us. Review the details and confirm when you're ready.")

    lt = st.session_state.legacy_type
    lt_data = LEGACY_TYPES[lt]

    # --- Legacy type ---
    st.markdown(f"### {lt_data['icon']} Legacy Type: **{lt}**")
    st.caption(lt_data["description"])

    # --- Subject ---
    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
    st.markdown(f"**Subject:** {st.session_state.subject_name}")
    st.markdown(f"**Relationship:** {st.session_state.subject_relationship}")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Scoping answers ---
    st.markdown("#### Scoping Details")
    for q in lt_data["follow_up_questions"]:
        key = q["key"]
        answer = st.session_state.scoping_answers.get(key, "—")
        if isinstance(answer, list):
            answer = ", ".join(answer) if answer else "—"
        st.markdown(f"**{q['question']}**")
        st.write(f"> {answer}")

    # --- Audience ---
    st.markdown("#### Target Audience")
    audience_str = ", ".join(st.session_state.audiences)
    st.write(audience_str)
    if st.session_state.audience_detail:
        st.write(f"*Notes:* {st.session_state.audience_detail}")

    # --- Format & timeline ---
    st.markdown("#### Delivery & Timeline")
    formats_str = ", ".join(st.session_state.delivery_formats)
    st.write(f"**Format(s):** {formats_str}")
    st.write(f"**Timeline:** {st.session_state.timeline}")
    if st.session_state.additional_notes:
        st.write(f"**Additional notes:** {st.session_state.additional_notes}")

    st.divider()

    # ── Generate Project Brief PDF ─────────────────────────────────
    st.markdown("### 📋 Project Brief")
    st.write("Download a professional one-page summary to share with family members or stakeholders.")
    brief_data = build_project_data()
    brief_pdf_bytes = generate_scope_summary_pdf(brief_data)
    safe_brief_name = brief_data["subject"]["name"].replace(" ", "_")
    st.download_button(
        label="📄 Generate Project Brief (PDF)",
        data=brief_pdf_bytes,
        file_name=f"project_brief_{safe_brief_name}.pdf",
        mime="application/pdf",
        key="step5_brief_pdf",
    )

    st.divider()

    col_back, col_spacer, col_confirm = st.columns([2, 5, 3])
    with col_back:
        if st.button("← Edit Answers", use_container_width=True, key="step5_back"):
            st.session_state.step = 1
            st.rerun()
    with col_confirm:
        if st.button("Confirm → Build Interview Questions", type="primary", use_container_width=True, key="step5_confirm"):
            # Save project files
            project_data = build_project_data()
            saved_path = save_project_json(project_data)
            st.session_state["saved_project_data"] = project_data
            st.session_state["saved_project_path"] = saved_path

            # Generate the tailored question bank
            st.session_state.generated_questions = generate_questions(project_data)
            st.session_state.priority_map = {}
            st.session_state.questions_generated = True
            st.session_state.step = 6
            st.rerun()


# =====================================================================
# STEP 6 — Question Bank: Review, Edit, Prioritize, Export
# =====================================================================
elif st.session_state.step == 6:
    st.markdown(
        '<div class="step-header">'
        "<h3>Step 6: Your Personalized Interview Questions</h3>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.write(
        "We've generated a customized set of interview questions based on "
        "everything you told us. Review them below — you can **edit**, "
        "**delete**, **add your own**, and **set priorities** before "
        "exporting the final Interview Guide PDF."
    )

    # Rebuild project data for PDF (or use cached)
    if "saved_project_data" not in st.session_state:
        st.session_state["saved_project_data"] = build_project_data()
    project_data = st.session_state["saved_project_data"]

    questions: OrderedDict = st.session_state.generated_questions
    priority_map: dict = st.session_state.priority_map

    # ── Quick stats ─────────────────────────────────────────────────
    total_q = sum(len(qs) for qs in questions.values())
    stat1, stat2, stat3 = st.columns(3)
    stat1.metric("Categories", len(questions))
    stat2.metric("Total Questions", total_q)
    must_ask = sum(1 for v in priority_map.values() if v == "Must Ask")
    stat3.metric("Marked 'Must Ask'", must_ask)

    st.divider()

    # ── Category-by-category editing ────────────────────────────────
    updated_questions = OrderedDict()
    updated_priorities = {}

    for cat_idx, (category, q_list) in enumerate(questions.items()):
        with st.expander(f"**{category}** ({len(q_list)} questions)", expanded=(cat_idx == 0)):
            edited_list = []
            for q_idx, question in enumerate(q_list):
                q_key = f"q_{cat_idx}_{q_idx}"
                col_q, col_pri, col_del = st.columns([7, 2.5, 0.8])

                with col_q:
                    new_text = st.text_input(
                        f"Question {q_idx + 1}",
                        value=question,
                        key=f"edit_{q_key}",
                        label_visibility="collapsed",
                    )
                with col_pri:
                    current_pri = priority_map.get(question, "Nice to Have")
                    pri_options = ["Must Ask", "Nice to Have", "Optional"]
                    pri = st.selectbox(
                        "Priority",
                        pri_options,
                        index=pri_options.index(current_pri) if current_pri in pri_options else 1,
                        key=f"pri_{q_key}",
                        label_visibility="collapsed",
                    )
                with col_del:
                    delete = st.checkbox("🗑️", key=f"del_{q_key}", help="Remove this question")

                if not delete and new_text.strip():
                    edited_list.append(new_text.strip())
                    updated_priorities[new_text.strip()] = pri

            # Add new question for this category
            st.markdown("---")
            add_col, add_btn_col = st.columns([8, 2])
            with add_col:
                new_q = st.text_input(
                    "Add a question",
                    key=f"add_{cat_idx}",
                    placeholder="Type a new question and click Add…",
                    label_visibility="collapsed",
                )
            with add_btn_col:
                if st.button("➕ Add", key=f"addbtn_{cat_idx}", use_container_width=True):
                    if new_q.strip():
                        edited_list.append(new_q.strip())
                        updated_priorities[new_q.strip()] = "Nice to Have"

            if edited_list:
                updated_questions[category] = edited_list

    # ── Add an entirely new category ────────────────────────────────
    st.divider()
    st.markdown("**Add a New Category**")
    nc_col1, nc_col2, nc_col3 = st.columns([3, 6, 1.5])
    with nc_col1:
        new_cat_name = st.text_input("Category name", key="new_cat_name", placeholder="e.g., Hobbies & Pastimes", label_visibility="collapsed")
    with nc_col2:
        new_cat_q = st.text_input("First question", key="new_cat_q", placeholder="What question should start this category?", label_visibility="collapsed")
    with nc_col3:
        if st.button("➕ Add Category", key="add_cat_btn", use_container_width=True):
            if new_cat_name.strip() and new_cat_q.strip():
                updated_questions[new_cat_name.strip()] = [new_cat_q.strip()]
                updated_priorities[new_cat_q.strip()] = "Nice to Have"

    # Persist edits back to session state
    if updated_questions:
        st.session_state.generated_questions = updated_questions
        st.session_state.priority_map = updated_priorities

    # ── Export section ──────────────────────────────────────────────
    st.divider()
    st.markdown("### 📥 Export Your Interview Guide")
    st.write("Download your finalized question set as a ready-to-use Interview Guide.")

    export_col1, export_col2, export_col3 = st.columns(3)

    with export_col1:
        # PDF Interview Guide
        pdf_bytes = generate_interview_guide_pdf(
            project_data=project_data,
            questions=st.session_state.generated_questions,
            priority_map=st.session_state.priority_map,
        )
        safe_name = project_data["subject"]["name"].replace(" ", "_")
        st.download_button(
            label="📄 Download Interview Guide (PDF)",
            data=pdf_bytes,
            file_name=f"interview_guide_{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with export_col2:
        # JSON export of questions
        export_data = {
            "project_id": project_data.get("project_id", ""),
            "subject": project_data["subject"]["name"],
            "legacy_type": project_data["legacy_type"],
            "questions": dict(st.session_state.generated_questions),
            "priorities": st.session_state.priority_map,
        }
        st.download_button(
            label="💾 Download Questions (JSON)",
            data=json.dumps(export_data, indent=2, ensure_ascii=False),
            file_name=f"interview_questions_{safe_name}.json",
            mime="application/json",
            use_container_width=True,
        )

    with export_col3:
        # Project scope summary (text)
        text_summary = build_text_summary(project_data)
        st.download_button(
            label="📝 Download Project Scope (TXT)",
            data=text_summary,
            file_name=f"legacy_scope_{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.divider()

    # ── Navigation ──────────────────────────────────────────────────
    col_back6, col_spacer6, col_done6 = st.columns([2, 5, 3])
    with col_back6:
        if st.button("← Back to Review", use_container_width=True, key="step6_back"):
            st.session_state.step = 5
            st.rerun()
    with col_done6:
        if st.button("🎉 Finish", type="primary", use_container_width=True, key="step6_done"):
            st.balloons()
            st.success(
                f"**Your Living Legacy project is complete!**\n\n"
                f"Project saved to: `{st.session_state.get('saved_project_path', 'projects/')}`\n\n"
                f"You now have a personalized Interview Guide with "
                f"**{sum(len(qs) for qs in st.session_state.generated_questions.values())} questions** "
                f"across **{len(st.session_state.generated_questions)} categories** "
                f"ready to capture **{st.session_state.subject_name}'s** story. "
                f"Thank you for preserving what matters most. 🌳"
            )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption("Living Legacy — Preserving stories that matter. © 2026")
