from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import List


@dataclass
class SyllabusData:
    title: str = "Fluid Mechanics"
    total_credits: str = "03"
    subject_code: str = "PCCCE5T001"
    teaching_hours: str = "02"
    tutorial_hours: str = "01"
    practical_hours: str = "00"
    exam_duration: str = "03 Hours"
    internal_evaluation: str = "40 Marks"
    end_semester_evaluation: str = "60 Marks"
    objectives: List[str] = field(default_factory=lambda: [
        "To impart fundamental knowledge of fluid properties, fluid statics, kinematics, dynamics, and the application of fluid mechanics in civil engineering systems.",
        "To apply theoretical concepts in analyzing fluid flow and selecting appropriate measurement techniques and model laws.",
    ])
    outcomes: List[str] = field(default_factory=lambda: [
        "Explain fluid properties and fundamental principles like buoyancy and stability of bodies.",
        "Analyze fluid pressure and compute hydrostatic forces on submerged surfaces.",
        "Apply continuity, Euler's, and Bernoulli's equations to solve fluid motion problems.",
        "Analyze and select flow measuring devices for pipelines, tanks, and open channels.",
        "Apply dimensional analysis and model laws in hydraulic model studies.",
        "Evaluate real-world civil engineering problems involving fluid flow using theoretical approaches.",
    ])
    units: List[tuple[str, str]] = field(default_factory=lambda: [
        (
            "UNIT I: Introduction and Archimedes Principle",
            "Introduction: Basic Concepts and Definitions, Distinction between a fluid and a solid; Density, Specific weight, Specific gravity, Kinematic and dynamic viscosity; variation of viscosity with temperature, Newton’s law of viscosity; Classification of fluids.\n\\noindent Fluid Statics: Fluid Pressure: Pressure at a point, Pascal’s law, Piezometer, U-Tube Manometer, Differential Manometer.",
        ),
        (
            "UNIT II: Fluid Kinematics",
            "Classification of flows, stream line, streak line, path line, continuity equation.",
        ),
        (
            "UNIT III: Fluid Dynamics",
            "Surface and body forces - Euler’s and Bernoulli’s equations for flow along a stream line, momentum equation and its applications.",
        ),
        (
            "UNIT IV: Boundary Layer Concepts",
            "Definition, thicknesses, characteristics along thin plate, laminar and turbulent boundary layers.",
        ),
        (
            "UNIT V: Flow Through Pipes",
            "Reynolds experiment, Darcy Weisbach equation, Minor losses in pipes, pipes in series and pipes in parallel, total energy line-hydraulic gradient line.",
        ),
    ])
    textbooks: List[str] = field(default_factory=lambda: [
        "R.K.Bansal, A Text Book of Fluid Mechanics and Hydraulic Machines, Laxmi  Pub.",
        "P.N. Modi & S.M. Set, Hydraulics, Fluid Mechanics and Hydraulic Machines, Standard Book House, Pub.",
    ])
    reference_books: List[str] = field(default_factory=lambda: [
        "F.M. White, Fluid Mechanics, Mc. Graw Hill, Pub.",
        "S. Ramamrutham, Hydraulics, Fluid Mechanics and Fluid Machines, Dhanpat Rai Publishing Co. Pub.",
    ])
    lab_table_title: str = "Fluid Mechanics"
    lab_section_title: str = "FLUID MECHANICS LAB"
    lab_total_credits: str = "03"
    lab_subject_code: str = "PCCCE5T001"
    lab_teaching_hours: str = "02"
    lab_tutorial_hours: str = "01"
    lab_practical_hours: str = "00"
    lab_exam_duration: str = "03 Hours"
    lab_internal_evaluation: str = "40 Marks"
    lab_end_semester_evaluation: str = "60 Marks"
    lab_objectives: List[str] = field(default_factory=lambda: [
        "To impart fundamental knowledge of fluid properties, fluid statics, kinematics, dynamics, and the application of fluid mechanics in civil engineering systems.",
        "To apply theoretical concepts in analyzing fluid flow and selecting appropriate measurement techniques and model laws.",
    ])
    lab_outcomes: List[str] = field(default_factory=lambda: [
        "Explain fluid properties and fundamental principles like buoyancy and stability of bodies.",
        "Analyze fluid pressure and compute hydrostatic forces on submerged surfaces.",
        "Apply continuity, Euler's, and Bernoulli's equations to solve fluid motion problems.",
        "Analyze and select flow measuring devices for pipelines, tanks, and open channels.",
        "Apply dimensional analysis and model laws in hydraulic model studies.",
        "Evaluate real-world civil engineering problems involving fluid flow using theoretical approaches.",
    ])
    experiments_heading: str = "Perform any 08 Experiments."
    experiments: List[str] = field(default_factory=lambda: [
        "Determination of Metacentric height and its importance.",
        "Verification of Bernoulli's Theorem.",
        "Calibration of Venturimeter.",
        "Calibration of Orifice meter.",
        "To determine the coefficient of discharge of Venturimeter.",
        "To determine the coefficient of discharge of Orifice meter.",
        "Calibration of Rectangular Notches/ V-Notches.",
        "Hydraulic Coefficients of an orifice.",
        "Hydraulic Coefficients of a Mouthpiece.",
        "Impact of jet apparatus.",
    ])
    bos_chairperson: str = "BOS Chairperson"
    dean_academic: str = "Dean (Academic)"
    principal: str = "Principal"


def _escape(text: str) -> str:
    replacements = {
        "\\": "\textbackslash{}",
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
        "{": "\\{",
        "}": "\\}",
        "~": "\\textasciitilde{}",
        "^": "\\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def _latex_lines(items: List[str], prefix: str) -> str:
    rows: List[str] = []
    for index, item in enumerate(items, start=1):
        clean = item.strip()
        if clean:
            rows.append(f"        {prefix}{index} & {_escape(clean)} \\\\")
            rows.append("        \\hline")
    return "\n".join(rows)


def _latex_enumerate(items: List[str]) -> str:
    rows: List[str] = []
    for item in items:
        clean = item.strip()
        if clean:
            rows.append(f"    \\item {_escape(clean)}")
    return "\n".join(rows)


def _latex_units(units: List[tuple[str, str]]) -> str:
    blocks: List[str] = []
    for heading, body in units:
        heading_clean = _escape(heading.strip())
        body_lines = []
        for line in body.splitlines():
            clean = line.strip()
            if not clean:
                continue
            if clean.startswith(r"\noindent"):
                body_lines.append(clean)
            else:
                body_lines.append(r"\noindent " + _escape(clean))
        blocks.append("\\subsection*{" + heading_clean + "}\n" + "\n".join(body_lines))
    return "\n\n".join(blocks)


def render_latex(data: SyllabusData) -> str:
    objectives = _latex_lines(data.objectives, "")
    outcomes = _latex_lines(data.outcomes, "CO")
    lab_objectives = _latex_lines(data.lab_objectives, "")
    lab_outcomes = _latex_lines(data.lab_outcomes, "CO")
    units = _latex_units(data.units)
    textbooks = _latex_enumerate(data.textbooks)
    reference_books = _latex_enumerate(data.reference_books)
    experiments = _latex_enumerate(data.experiments)

    return rf"""\documentclass[12pt, a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[margin=1in, bottom=1.5in]{{geometry}}
\usepackage[table]{{xcolor}}
\usepackage{{array}}
\usepackage{{enumitem}}
\usepackage{{titlesec}}
\usepackage{{fancyhdr}}
\usepackage{{tabularx}}
\usepackage{{enumitem}}
\usepackage{{titlesec}}

% Format Sections: 12pt, Bold, Centered (to match your current style)
\titleformat{{\section}}
  {{\normalfont\fontsize{{12}}{{14}}\bfseries\centering}}{{\thesection}}{{1em}}{{}}

  % Format Subsections: 12pt, Bold, Left-aligned
  \titleformat{{\subsection}}
    {{\normalfont\fontsize{{12}}{{14}}\bfseries}}{{\thesubsection}}{{1em}}{{}}

    % Adjust spacing around headers if they feel too tight
    \titlespacing*{{\section}}{{0pt}}{{12pt}}{{6pt}}
    \titlespacing*{{\subsection}}{{0pt}}{{10pt}}{{4pt}}

    % Color Definitions
    \definecolor{{headerblue}}{{RGB}}{{30, 50, 100}} 
    \definecolor{{tableorange}}{{RGB}}{{255, 218, 185}}
    \definecolor{{tablepurple}}{{RGB}}{{230, 210, 240}}

    % Color Definitions
    \definecolor{{headerblue}}{{RGB}}{{30, 50, 100}} 
    \definecolor{{outcomen-green}}{{RGB}}{{210, 230, 180}} % Matches the light green in the doc

    % Page Styling
    \pagestyle{{fancy}}
    \fancyhf{{}}
    \renewcommand{{\headrulewidth}}{{0pt}}
    \fancyfoot[C]{{
        \small
            \begin{{tabular}}{{|m{{0.3\textwidth}}|m{{0.3\textwidth}}|m{{0.3\textwidth}}|}}
                    \hline
                            & & \\
                                    & & \\
                                            \hline
                                                    \centering \textbf{{{_escape(data.bos_chairperson)}}} & \centering \textbf{{{_escape(data.dean_academic)}}} & \centering \textbf{{{_escape(data.principal)}}} \tabularnewline
                                                            \hline
                                                                \end{{tabular}}
                                                                }}

                                                                \begin{{document}}

                                                                % --- PAGE 1: COURSE DETAILS & OBJECTIVES ---
                                                                \begin{{center}}
                                                                    \renewcommand{{\arraystretch}}{{1.5}}
                                                                        \begin{{tabularx}}{{\textwidth}}{{|>{{\hsize=.85\hsize\linewidth=\hsize}}X|>{{\hsize=1.15\hsize\linewidth=\hsize}}X|}}
                                                                                \hline
                                                                                        \rowcolor{{tableorange}} \multicolumn{{2}}{{|c|}}{{\textbf{{{_escape(data.title)}}}}} \\
                                                                                                \hline
                                                                                                        Total Credits : {_escape(data.total_credits)} & Subject Code : {_escape(data.subject_code)} \\
                                                                                                                \hline
                                                                                                                        Teaching Scheme & Examination Scheme \\
                                                                                                                                \hline
                                                                                                                                        Teaching Hrs /Week : {_escape(data.teaching_hours)} & Duration of End Semester Exam : {_escape(data.exam_duration)} \\
                                                                                                                                                \hline
                                                                                                                                                        Tutorials Hrs/ Week : {_escape(data.tutorial_hours)} & Internal Evaluation \hspace{{2.4cm}}: {_escape(data.internal_evaluation)} \\
                                                                                                                                                                \hline
                                                                                                                                                                        Practical Hrs/ Week : {_escape(data.practical_hours)} & End Semester Examination \hspace{{1cm}}: {_escape(data.end_semester_evaluation)} \\
                                                                                                                                                                                \hline
                                                                                                                                                                                    \end{{tabularx}}
                                                                                                                                                                                    \end{{center}}

                                                                                                                                                                                    \vspace{{1cm}}

                                                                                                                                                                                    \begin{{center}}
                                                                                                                                                                                        \renewcommand{{\arraystretch}}{{1.5}}
                                                                                                                                                                                            \begin{{tabularx}}{{\textwidth}}{{|c|X|}}
                                                                                                                                                                                                    \hline
                                                                                                                                                                                                            \rowcolor{{tablepurple}} \multicolumn{{2}}{{|c|}}{{\textbf{{Course Objectives}}}} \\
                                                                                                                                                                                                                    \hline
{objectives}
                                                                                                                                                                                                                                                        \end{{tabularx}}
                                                                                                                                                                                                                                                        \end{{center}}

                                                                                                                                                                                                                                                        \vspace{{1cm}}
                                                                                                                                                                                                                                                        % --- COURSE OUTCOMES SECTION ---
                                                                                                                                                                                                                                                        \begin{{center}}
                                                                                                                                                                                                                                                            \renewcommand{{\arraystretch}}{{1.5}}
                                                                                                                                                                                                                                                                \begin{{tabularx}}{{\textwidth}}{{|c|X|}}
                                                                                                                                                                                                                                                                        \hline
                                                                                                                                                                                                                                                                                \rowcolor{{outcomen-green}} \multicolumn{{2}}{{|c|}}{{\textbf{{Course Outcomes}}}} \\
                                                                                                                                                                                                                                                                                        \hline
                                                                                                                                                                                                                                                                                                \multicolumn{{2}}{{|l|}}{{\textbf{{After completion of syllabus, students would be able to}}}} \\
                                                                                                                                                                                                                                                                                                        \hline
{outcomes}
                                                                                                                                                                                                                                                                                                                                        \end{{tabularx}}
                                                                                                                                                                                                                                                                                                                                        \end{{center}}

                                                                                                                                                                                                                                                                                                                                        \newpage

                                                                                                                                                                                                                                                                                                                                        % --- PAGE 2: UNITS I & II ---
                                                                                                                                                                                                                                                                                                                                        \section*{{\centering \color{{headerblue}} COURSE CONTENT}}

{units}

                                                                                                                                                                                                                                                                                                                                        \vspace{{0.5cm}}
                                                                                                                                                                                                                                                                                                                                        \noindent \textbf{{Text Books:}}
                                                                                                                                                                                                                                                                                                                                        \begin{{enumerate}}[label=\arabic*., leftmargin=*]
{textbooks}
                                                                                                                                                                                                                                                                                                                                        \end{{enumerate}}

                                                                                                                                                                                                                                                                                                                                        \noindent \textbf{{Reference Books:}}
                                                                                                                                                                                                                                                                                                                                        \begin{{enumerate}}[label=\arabic*., leftmargin=*]
{reference_books}
                                                                                                                                                                                                                                                                                                                                        \end{{enumerate}}

                                                                                                                                                                                                                                                                                                                                        \newpage

                                                                                                                                                                                                                                                                                                                                        % --- PAGE 1: LAB COURSE DETAILS & OBJECTIVES ---
                                                                                                                                                                                                                                                                                                                                        \begin{{center}}
                                                                                                                                                                                                                                                                                                                                            \renewcommand{{\arraystretch}}{{1.5}}
                                                                                                                                                                                                                                                                                                                                                \begin{{tabularx}}{{\textwidth}}{{|>{{\hsize=.85\hsize\linewidth=\hsize}}X|>{{\hsize=1.15\hsize\linewidth=\hsize}}X|}}
                                                                                                                                                                                                                                                                                                                                                        \hline
                                                                                                                                                                                                                                                                                                                                                                \rowcolor{{tableorange}} \multicolumn{{2}}{{|c|}}{{\textbf{{{_escape(data.lab_table_title)}}}}} \\
                                                                                                                                                                                                                                                                                                                                                                        \hline
                                                                                                                                                                                                                                                                                                                                                                                Total Credits : {_escape(data.lab_total_credits)} & Subject Code : {_escape(data.lab_subject_code)} \\
                                                                                                                                                                                                                                                                                                                                                                                        \hline
                                                                                                                                                                                                                                                                                                                                                                                                Teaching Scheme & Examination Scheme \\
                                                                                                                                                                                                                                                                                                                                                                                                        \hline
                                                                                                                                                                                                                                                                                                                                                                                                                Teaching Hrs /Week : {_escape(data.lab_teaching_hours)} & Duration of End Semester Exam : {_escape(data.lab_exam_duration)} \\
                                                                                                                                                                                                                                                                                                                                                                                                                        \hline
                                                                                                                                                                                                                                                                                                                                                                                                                                Tutorials Hrs/ Week : {_escape(data.lab_tutorial_hours)} & Internal Evaluation \hspace{{2.4cm}}: {_escape(data.lab_internal_evaluation)} \\
                                                                                                                                                                                                                                                                                                                                                                                                                                        \hline
                                                                                                                                                                                                                                                                                                                                                                                                                                                Practical Hrs/ Week : {_escape(data.lab_practical_hours)} & End Semester Examination \hspace{{1cm}}: {_escape(data.lab_end_semester_evaluation)} \\
                                                                                                                                                                                                                                                                                                                                                                                                                                                        \hline
                                                                                                                                                                                                                                                                                                                                                                                                                                                            \end{{tabularx}}

                                                                                                                                                                                                                                                                                                                                                                                                                                                            \end{{center}}

                                                                                                                                                                                                                                                                                                                                                                                                                                                            \vspace{{1cm}}

                                                                                                                                                                                                                                                                                                                                                                                                                                                            \begin{{center}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                \renewcommand{{\arraystretch}}{{1.5}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    \begin{{tabularx}}{{\textwidth}}{{|c|X|}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            \hline
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    \rowcolor{{tablepurple}} \multicolumn{{2}}{{|c|}}{{\textbf{{Course Objectives}}}} \\
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            \hline
{lab_objectives}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \end{{tabularx}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \end{{center}}

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \vspace{{1cm}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                % --- COURSE OUTCOMES SECTION ---
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \begin{{center}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    \renewcommand{{\arraystretch}}{{1.5}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        \begin{{tabularx}}{{\textwidth}}{{|c|X|}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \hline
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        \rowcolor{{outcomen-green}} \multicolumn{{2}}{{|c|}}{{\textbf{{Course Outcomes}}}} \\
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \hline
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        \multicolumn{{2}}{{|l|}}{{\textbf{{After completion of syllabus, students would be able to}}}} \\
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \hline
{lab_outcomes}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \end{{tabularx}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \end{{center}}

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \newpage
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                % --- PAGE 5: LAB COMPONENT ---
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \section*{{\centering \color{{headerblue}} {_escape(data.lab_section_title)}}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \noindent \textbf{{{_escape(data.experiments_heading)}}}

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \begin{{enumerate}}[label=\arabic*.]
{experiments}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \end{{enumerate}}

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                \end{{document}}
"""


def compile_pdf(latex_content: str, output_stem: str = "syllabus") -> tuple[bytes, str]:
    if shutil.which("latexmk") is None:
        raise RuntimeError("latexmk is not installed. Please install a TeX distribution with latexmk.")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tex_path = temp_path / f"{output_stem}.tex"
        tex_path.write_text(latex_content, encoding="utf-8")

        command = ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", tex_path.name]
        result = subprocess.run(command, cwd=temp_path, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            log = (result.stdout or "") + "\n" + (result.stderr or "")
            raise RuntimeError(log.strip())

        pdf_path = temp_path / f"{output_stem}.pdf"
        return pdf_path.read_bytes(), tex_path.read_text(encoding="utf-8")
