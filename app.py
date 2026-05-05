from __future__ import annotations

import streamlit as st

from syllabus_generator import SyllabusData, compile_pdf, render_latex


st.set_page_config(page_title="Syllabus Builder", layout="wide")
st.title("Syllabus Builder")
st.caption("Edit fields, generate LaTeX, and download a compiled PDF.")


def split_lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def split_units(value: str) -> list[tuple[str, str]]:
    units: list[tuple[str, str]] = []
    raw_blocks = [block.strip() for block in value.split("\n\n") if block.strip()]
    for block in raw_blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        heading = lines[0]
        body = " ".join(lines[1:]) if len(lines) > 1 else ""
        units.append((heading, body))
    return units


def block_from_units(units: list[tuple[str, str]]) -> str:
    return "\n\n".join(f"{heading}\n{body}" for heading, body in units)


def default_data() -> SyllabusData:
    return SyllabusData()


if "data" not in st.session_state:
    st.session_state.data = default_data()

data: SyllabusData = st.session_state.data

with st.sidebar:
    st.header("Actions")
    if st.button("Reset to default"):
        st.session_state.data = default_data()
        st.rerun()
    st.markdown("Designed for GitHub + Streamlit deployment.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Course Details")
    data.title = st.text_input("Course Title", value=data.title)
    meta1, meta2 = st.columns(2)
    with meta1:
        data.total_credits = st.text_input("Total Credits", value=data.total_credits)
        data.teaching_hours = st.text_input("Teaching Hours / Week", value=data.teaching_hours)
        data.tutorial_hours = st.text_input("Tutorial Hours / Week", value=data.tutorial_hours)
        data.practical_hours = st.text_input("Practical Hours / Week", value=data.practical_hours)
    with meta2:
        data.subject_code = st.text_input("Subject Code", value=data.subject_code)
        data.exam_duration = st.text_input("Exam Duration", value=data.exam_duration)
        data.internal_evaluation = st.text_input("Internal Evaluation", value=data.internal_evaluation)
        data.end_semester_evaluation = st.text_input("End Semester Evaluation", value=data.end_semester_evaluation)

    data.objectives = split_lines(
        st.text_area("Course Objectives", value="\n".join(data.objectives), height=140)
    )
    data.outcomes = split_lines(
        st.text_area("Course Outcomes", value="\n".join(data.outcomes), height=180)
    )
    data.units = split_units(
        st.text_area("Units", value=block_from_units(data.units), height=280)
    )
    data.textbooks = split_lines(
        st.text_area("Text Books", value="\n".join(data.textbooks), height=110)
    )

with col2:
    st.subheader("Lab Details")
    data.lab_title = st.text_input("Lab Title", value=data.lab_title)
    lab1, lab2 = st.columns(2)
    with lab1:
        data.lab_total_credits = st.text_input("Lab Credits", value=data.lab_total_credits)
        data.lab_teaching_hours = st.text_input("Lab Teaching Hours / Week", value=data.lab_teaching_hours)
        data.lab_tutorial_hours = st.text_input("Lab Tutorial Hours / Week", value=data.lab_tutorial_hours)
        data.lab_practical_hours = st.text_input("Lab Practical Hours / Week", value=data.lab_practical_hours)
    with lab2:
        data.lab_subject_code = st.text_input("Lab Subject Code", value=data.lab_subject_code)
        data.lab_exam_duration = st.text_input("Lab Exam Duration", value=data.lab_exam_duration)
        data.lab_internal_evaluation = st.text_input("Lab Internal Evaluation", value=data.lab_internal_evaluation)
        data.lab_end_semester_evaluation = st.text_input("Lab End Semester Evaluation", value=data.lab_end_semester_evaluation)

    data.lab_objectives = split_lines(
        st.text_area("Lab Objectives", value="\n".join(data.lab_objectives), height=140)
    )
    data.lab_outcomes = split_lines(
        st.text_area("Lab Outcomes", value="\n".join(data.lab_outcomes), height=180)
    )
    data.experiments_heading = st.text_input("Experiments Heading", value=data.experiments_heading)
    data.experiments = split_lines(
        st.text_area("Experiments", value="\n".join(data.experiments), height=180)
    )

st.subheader("Signatories")
sig1, sig2, sig3 = st.columns(3)
with sig1:
    data.bos_chairperson = st.text_input("Signature 1", value=data.bos_chairperson)
with sig2:
    data.dean_academic = st.text_input("Signature 2", value=data.dean_academic)
with sig3:
    data.principal = st.text_input("Signature 3", value=data.principal)

latex_content = render_latex(data)

preview_tab, latex_tab = st.tabs(["Preview Actions", "LaTeX Source"])

with preview_tab:
    st.write("Generate a fresh PDF from the edited syllabus fields.")
    if st.button("Generate PDF", type="primary"):
        try:
            pdf_bytes, tex_source = compile_pdf(latex_content)
            st.success("PDF generated successfully.")
            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name="syllabus.pdf",
                mime="application/pdf",
            )
            st.download_button(
                "Download LaTeX",
                data=tex_source,
                file_name="syllabus.tex",
                mime="text/plain",
            )
        except Exception as exc:
            st.error("PDF generation failed.")
            st.code(str(exc))

with latex_tab:
    st.text_area("Generated LaTeX", value=latex_content, height=500)
