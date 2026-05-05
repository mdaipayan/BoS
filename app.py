import streamlit as st

# --- CSS INJECTION FOR ACADEMIC STYLING ---
st.markdown("""
<style>
    .syllabus-body { font-family: 'Times New Roman', serif; color: black; }
    .main-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    .main-table td, .main-table th { border: 1px solid black; padding: 10px; font-size: 14px; }
    
    .bg-orange { background-color: #F9CB9C; font-weight: bold; text-align: center; font-size: 18px; }
    .bg-purple { background-color: #D9D2E9; font-weight: bold; }
    .bg-green { background-color: #D9EAD3; font-weight: bold; }
    .bold-label { font-weight: bold; background-color: #f2f2f2; }
</style>
""", unsafe_allow_html=True)

st.title("Syllabus Generator: Civil Engineering")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("1. Metadata")
    subject = st.text_input("Subject Name", "FLUID MECHANICS")
    code = st.text_input("Subject Code", "PCCCE5T001")
    credits = st.text_input("Credits", "03")
    
    st.header("2. Content Units")
    u1 = st.text_area("Unit I", "Fluid Properties & Statics...")
    u2 = st.text_area("Unit II", "Fluid Kinematics...")

# --- PAGE LOGIC (TABS) ---
tab1, tab2, tab3 = st.tabs(["Page 1: Header & Objectives", "Page 2: Detailed Units", "Page 3: Refs & Signatures"])

with tab1:
    st.markdown(f"""
    <div class="syllabus-body">
        <table class="main-table">
            <tr class="bg-orange"><td colspan="4">{subject}</td></tr>
            <tr>
                <td class="bold-label">Total Credits</td><td>{credits}</td>
                <td class="bold-label">Subject Code</td><td>{code}</td>
            </tr>
            <tr>
                <td class="bold-label">Teaching Scheme</td><td colspan="3" class="bold-label">Examination Scheme</td>
            </tr>
            <tr>
                <td>Lecture: 02 Hrs/Week<br>Tutorial: 01 Hrs/Week</td>
                <td>Internal: 40 Marks<br>External: 60 Marks</td>
                <td colspan="2">Total Marks: 100<br>Duration: 03 Hours</td>
            </tr>
            <tr class="bg-purple"><td colspan="4">Course Objectives</td></tr>
            <tr><td colspan="4">1. To understand fluid properties.<br>2. To analyze fluid statics and buoyancy.</td></tr>
            <tr class="bg-green"><td colspan="4">Course Outcomes</td></tr>
            <tr><td colspan="4">CO1: Determine metacentric height.<br>CO2: Apply Bernoulli’s theorem.</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown(f"""
    <div class="syllabus-body">
        <table class="main-table">
            <tr class="bg-purple"><td style="width:20%">Unit</td><td>Detailed Content</td></tr>
            <tr><td><b>Unit I</b></td><td>{u1}</td></tr>
            <tr><td><b>Unit II</b></td><td>{u2}</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="syllabus-body">
        <h3>Textbooks:</h3>
        <p>1. R.K. Bansal, Fluid Mechanics, Laxmi Pub.</p>
        <br><br>
        <table class="main-table" style="text-align:center;">
            <tr>
                <td style="height:80px; vertical-align:bottom;">BOS Chairperson</td>
                <td style="vertical-align:bottom;">Dean (Academic)</td>
                <td style="vertical-align:bottom;">Principal</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
