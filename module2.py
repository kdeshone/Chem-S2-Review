import streamlit as st
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

MODULE_TITLE = "Module 2: IS 3.2 — The Mole and Data Analysis"

NAVY  = colors.HexColor("#1e3c72")
GREEN = colors.HexColor("#27ae60")
RED   = colors.HexColor("#c0392b")
LTBLUE = colors.HexColor("#f0f5ff")

# ---------------------------------------------------------------------------
# PDF GENERATION
# ---------------------------------------------------------------------------
def create_pdf(name, period, score, total, date_str, mc_results,
               q1_correct, q2_correct, q3_correct):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch)
    styles = getSampleStyleSheet()
    story  = []

    # ── Styles ──────────────────────────────────────────────────────────────
    title_style = ParagraphStyle("title", parent=styles["Title"],
                                 textColor=colors.white, fontSize=18,
                                 spaceAfter=4, alignment=TA_CENTER)
    sub_style   = ParagraphStyle("sub", parent=styles["Normal"],
                                 textColor=colors.white, fontSize=12,
                                 alignment=TA_CENTER, spaceAfter=0)
    h2_style    = ParagraphStyle("h2", parent=styles["Heading2"],
                                 textColor=NAVY, spaceBefore=10, spaceAfter=4)
    body_style  = ParagraphStyle("body", parent=styles["Normal"],
                                 fontSize=10, leading=14, spaceAfter=3)
    ok_style    = ParagraphStyle("ok",  parent=styles["Normal"],
                                 fontSize=10, textColor=GREEN, leading=13)
    bad_style   = ParagraphStyle("bad", parent=styles["Normal"],
                                 fontSize=10, textColor=RED, leading=13)

    # ── Header table ────────────────────────────────────────────────────────
    pct   = (score / total) * 100
    grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"

    header_data = [[
        Paragraph("Honors Chemistry — Semester 2 Review", title_style),
    ], [
        Paragraph(MODULE_TITLE, sub_style),
    ]]
    header_tbl = Table(header_data, colWidths=[7*inch])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [6,6,6,6]),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 10))

    # ── Student info ────────────────────────────────────────────────────────
    info_data = [
        [Paragraph(f"<b>Student:</b> {name}", body_style),
         Paragraph(f"<b>Period:</b> {period}", body_style)],
        [Paragraph(f"<b>Date:</b> {date_str}", body_style),
         Paragraph(f"<b>Letter Grade:</b> {grade}", body_style)],
    ]
    info_tbl = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
    info_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LTBLUE),
        ("BOX",        (0,0), (-1,-1), 0.5, NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 10))

    # ── Score banner ────────────────────────────────────────────────────────
    score_data = [[
        Paragraph(f"FINAL SCORE:  {score} / {total}   ({pct:.1f}%)", title_style)
    ]]
    score_tbl = Table(score_data, colWidths=[7*inch])
    score_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(score_tbl)
    story.append(Spacer(1, 12))

    # ── Score breakdown ──────────────────────────────────────────────────────
    story.append(Paragraph("Score Breakdown", h2_style))
    interactive_score = sum([q1_correct, q2_correct, q3_correct])
    mc_score = sum(1 for r in mc_results if r["correct"])
    story.append(Paragraph(f"Interactive Practice (Q1–3):  {interactive_score} / 3", body_style))
    story.append(Paragraph(f"Multiple Choice (Q4–20):      {mc_score} / 17", body_style))
    story.append(Spacer(1, 8))

    # ── Interactive Q1–3 ────────────────────────────────────────────────────
    story.append(Paragraph("Interactive Questions", h2_style))
    items = [
        ("Q1 — Scientific Notation Builder", q1_correct, "1.5 x 10^3"),
        ("Q2 — Percent Error Calculation",   q2_correct, "5.0%"),
        ("Q3 — Molar Mass Calculation",      q3_correct, "386.9 g/mol"),
    ]
    for label, correct, answer in items:
        if correct:
            story.append(Paragraph(f"✔  CORRECT — {label}", ok_style))
        else:
            story.append(Paragraph(f"✘  INCORRECT — {label}  |  Correct: {answer}", bad_style))
    story.append(Spacer(1, 8))

    # ── MC Q4–20 ─────────────────────────────────────────────────────────────
    story.append(Paragraph("Multiple Choice Questions (Q4–20)", h2_style))

    for i, result in enumerate(mc_results):
        qnum = i + 4
        if result["correct"]:
            story.append(Paragraph(f"✔  Q{qnum}: CORRECT", ok_style))
        else:
            chosen = result["chosen"] if result["chosen"] else "No answer selected"
            story.append(Paragraph(
                f"✘  Q{qnum}: INCORRECT — You chose: {chosen}  |  Correct: {result['answer']}",
                bad_style
            ))

    doc.build(story)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(page_title=MODULE_TITLE, layout="wide", page_icon="🧮")

# ---------------------------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* ── Global ── */
section.main > div { max-width: none; }

/* ── Module header ── */
.mod-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 55%, #1565c0 100%);
    padding: 30px 32px 24px;
    border-radius: 14px;
    margin-bottom: 28px;
    box-shadow: 0 8px 24px rgba(30,60,114,0.22);
    position: relative;
    overflow: hidden;
}
.mod-header::after {
    content: "🧮";
    position: absolute; right: 28px; top: 18px;
    font-size: 64px; opacity: 0.12;
}
.mod-header .badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: white;
    padding: 3px 14px;
    border-radius: 20px;
    font-size: 0.78em;
    font-weight: 700;
    letter-spacing: 0.8px;
    margin-bottom: 10px;
}
.mod-header h1 { color: white !important; margin: 0 0 6px; font-size: 1.65em; }
.mod-header p  { color: rgba(255,255,255,0.82) !important; margin: 0; font-size: 0.97em; }

/* ── Textbook section ── */
.tb-head {
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    color: white !important;
    padding: 18px 24px;
    border-radius: 10px 10px 0 0;
}
.tb-head h2 { color: white !important; margin: 0 0 4px; font-size: 1.2em; }
.tb-head p  { color: rgba(255,255,255,0.83) !important; margin: 0; font-size: 0.93em; }
.tb-body {
    background: #fff;
    border: 1px solid #dee2e6;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 20px 24px 8px;
    margin-bottom: 22px;
}
.review-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 18px;
    margin-top: 16px;
}
.review-card {
    background: #ffffff;
    border: 1px solid #dce7f6;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 16px 32px rgba(30, 60, 114, 0.06);
}
.review-card h3 {
    margin: 0 0 10px;
    color: #1e3c72;
    font-size: 1.1em;
}
.review-card p {
    margin: 0 0 12px;
    color: #32415c;
    line-height: 1.7;
}
.review-card .badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #eef4ff;
    color: #1e3c72;
    padding: 8px 12px;
    border-radius: 999px;
    font-size: 0.9em;
    font-weight: 700;
    margin-bottom: 14px;
}
.review-note {
    margin-top: 18px;
    padding: 18px 20px;
    background: #f5f9ff;
    border-left: 4px solid #2980b9;
    border-radius: 14px;
    color: #1e3565;
    line-height: 1.75;
}
.sigfig-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 10px;
}
.sigfig-list li {
    background: #f6f9ff;
    border: 1px solid #d9e7f8;
    border-radius: 12px;
    padding: 14px 16px;
    color: #24324a;
}
.sigfig-list li strong {
    display: block;
    margin-bottom: 4px;
}

/* ── Callout boxes ── */
.callout { padding: 14px 18px; border-radius: 8px; margin: 14px 0; }
.callout-warn   { background: #fff9e6; border-left: 5px solid #f39c12; }
.callout-info   { background: #eaf4ff; border-left: 5px solid #2980b9; }
.callout h4 { margin: 0 0 7px; font-size: 1em; color: #333; }
.callout p  { margin: 0; font-size: 0.94em; color: #333; line-height: 1.65; }

/* ── Reaction type cards (Reused for Moles) ── */
.rxn-card {
    background: #fafbfc;
    border: 1px solid #e4e6ea;
    border-radius: 10px;
    padding: 18px 22px;
}
.rxn-card h3 { margin: 0 0 11px; color: #1e3c72; font-size: 1.08em; }
.rxn-card code {
    background: #eef2ff; padding: 2px 7px;
    border-radius: 4px; font-size: 0.93em; color: #2c3e50;
}
.rxn-model {
    background: white; border: 1px solid #dde;
    border-radius: 8px; text-align: center;
    font-size: 24px; letter-spacing: 4px;
    padding: 10px; margin-top: 12px; color: #333;
}

/* ── Balance table ── */
.bal-tbl { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 0.94em; }
.bal-tbl th {
    background: #1e3c72; color: white;
    padding: 8px 14px; text-align: center;
}
.bal-tbl td { padding: 7px 14px; text-align: center; border-bottom: 1px solid #eee; color: #333; }
.ok  { color: #27ae60; font-weight: 700; }
.bad { color: #e74c3c; font-weight: 700; }

/* ── Score display ── */
.score-box {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
    padding: 28px 24px;
    border-radius: 14px;
    text-align: center;
    margin: 18px 0;
    box-shadow: 0 6px 20px rgba(30,60,114,0.2);
}
.score-box .big  { font-size: 3em; font-weight: 800; margin: 6px 0; }
.score-box .sub  { font-size: 1.1em; opacity: 0.88; }
.score-box .pct  { font-size: 1.5em; font-weight: 700; margin-top: 4px; }

/* ── Feedback rows ── */
.fb-ok  {
    background: #f0faf4; border-left: 4px solid #27ae60;
    padding: 9px 14px; border-radius: 0 6px 6px 0; margin: 4px 0;
    font-size: 0.93em; color: #333;
}
.fb-bad {
    background: #fef8f8; border-left: 4px solid #e74c3c;
    padding: 9px 14px; border-radius: 0 6px 6px 0; margin: 4px 0;
    font-size: 0.93em; color: #333;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="mod-header">
  <div class="badge">IS 3.2 &nbsp;·&nbsp; Honors Chemistry &nbsp;·&nbsp; Semester 2</div>
  <h1>The Mole and Data Analysis</h1>
  <p>Module 2 of 8 &nbsp;·&nbsp; Estimated time: 30–40 min &nbsp;·&nbsp; 20 points total</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SECTION 1 — STUDENT INFO
# ---------------------------------------------------------------------------
st.subheader("① Student Information")
col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("First and Last Name", placeholder="e.g. Jane Smith")
with col2:
    class_period = st.selectbox(
        "Class Period",
        ["", "Period 1", "Period 2", "Period 3", "Period 4", "Period 5", "Period 6"],
    )

st.divider()

# ---------------------------------------------------------------------------
# SECTION 2 — CONCEPT REVIEW
# ---------------------------------------------------------------------------
st.subheader("② Concept Review")

st.markdown("""
<div class="tb-head">
  <h2>Chapter 3.2 — Measurements & The Mole</h2>
  <p>Read carefully — the interactive exercises and quiz are based on this material.</p>
</div>
<div class="tb-body">
""", unsafe_allow_html=True)

st.markdown("### Accuracy, Precision, and Significant Figures")
st.markdown("""
<div class="review-grid">
  <div class="review-card">
    <div class="badge">Accuracy vs. Precision</div>
    <p><strong>Accuracy</strong> measures how close your result is to the accepted or true value.</p>
    <p><strong>Precision</strong> measures how consistent repeated measurements are.</p>
    <p><em>Example:</em> Hitting the same spot on the target each time is precise; hitting the bullseye is accurate.</p>
  </div>

  <div class="review-card">
    <div class="badge">Percent Error</div>
    <p>Percent error shows how far an experimental value is from the accepted value in relative terms.</p>
    <p><code>| Measured - Actual | / Actual × 100</code></p>
    <p>Lower percent error means better accuracy.</p>
  </div>

  <div class="review-card">
    <div class="badge">Scientific Notation</div>
    <p>Used to write very large or very small numbers with one digit left of the decimal.</p>
    <p><code>1500 = 1.5 × 10³</code> and <code>0.001012 = 1.012 × 10⁻³</code></p>
    <p>Positive exponent: move decimal left. Negative exponent: move decimal right.</p>
  </div>
</div>

<div class="review-card" style="margin-top: 18px;">
  <h3>Significant Figures Rules</h3>
  <ul class="sigfig-list">
    <li><strong>Non-zero digits</strong> are always significant. <br><code>34</code> → 2 sig figs.</li>
    <li><strong>Embedded zeros</strong> are significant. <br><code>101</code> → 3 sig figs.</li>
    <li><strong>Leading zeros</strong> are never significant. <br><code>0.001012</code> → 4 sig figs.</li>
    <li><strong>Trailing zeros</strong> are significant only with a decimal. <br><code>3400.</code> → 4 sig figs; <code>3400</code> → 2 sig figs.</li>
  </ul>
</div>

<div class="review-note">
  <strong>Quick tip:</strong> When you calculate percent error, always compare the absolute difference to the accepted value and multiply by 100. Keep your final answer in the same precision as the measurement.
</div>
""", unsafe_allow_html=True)

st.markdown("### The Mole Concept")

tab1, tab2, tab3 = st.tabs([
    "📦 Avogadro's Number", "⚖️ Molar Mass", "🔬 Empirical vs Molecular"
])

with tab1:
    st.markdown("""
    <div class="rxn-card">
      <h3>1. Avogadro's Number</h3>
      <p><b>Value:</b> <code>6.02 × 10²³</code></p>
      <p><b>Description:</b> Just like a "dozen" means 12, a "mole" means 6.02 × 10²³ particles (atoms, molecules, or formula units).</p>
      <p><b>Conversion Factor:</b> To convert moles to particles, multiply by Avogadro's number. To convert particles to moles, divide by Avogadro's number.</p>
      <div class="rxn-model">1 Mole = 602,000,000,000,000,000,000,000 items</div>
      <div class="review-note" style="margin-top:14px; padding:14px 16px;">
        <strong>Worked example:</strong>
        <p style="margin: 8px 0 10px; color: #1e3565;"><strong>Problem:</strong> Convert <code>0.50 mol</code> of particles into the number of particles using Avogadro's number.</p>
        <ol style="margin: 0 0 0 18px; padding: 0; color: #1e3565;">
          <li>Start with the known quantity: <code>0.50 mol</code>.</li>
          <li>Multiply by Avogadro's number: <code>0.50 × 6.02 × 10²³</code>.</li>
          <li>Calculate the result: <code>3.01 × 10²³ particles</code>.</li>
          <li>Reverse the process to convert back: divide particles by Avogadro's number.</li>
          <li><code>3.01 × 10²³ ÷ 6.02 × 10²³ = 0.50 mol</code>.</li>
        </ol>
      </div>
    </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="rxn-card">
      <h3>2. Molar Mass</h3>
      <p><b>Units:</b> <code>g/mol</code></p>
      <p><b>Description:</b> The mass of exactly one mole of a substance. It is calculated by adding the atomic masses of all atoms in a compound's formula using the periodic table.</p>
      <p><b>Example (H₂O):</b> <br>H (1.01) × 2 = 2.02<br>O (16.00) × 1 = 16.00<br>Total = 18.02 g/mol</p>
      <div class="rxn-model">Mass of 1 Mole = Molar Mass (Periodic Table)</div>
      <div class="review-note" style="margin-top:14px; padding:14px 16px;">
        <strong>Worked example:</strong>
        <p style="margin: 8px 0 10px; color: #1e3565;"><strong>Problem:</strong> Find the molar mass of <code>CO₂</code>, then convert <code>22.0 g</code> of CO₂ to moles.</p>
        <ol style="margin: 0 0 0 18px; padding: 0; color: #1e3565;">
          <li>Write the formula: <code>CO₂</code>.</li>
          <li>Add atomic masses: C = 12.01, O = 16.00 × 2.</li>
          <li>Compute the total: <code>12.01 + 32.00 = 44.01 g/mol</code>.</li>
          <li>Use the mass-to-moles formula: <code>moles = mass ÷ molar mass</code>.</li>
          <li><code>22.0 g ÷ 44.01 g/mol = 0.50 mol</code>.</li>
        </ol>
      </div>
    </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="rxn-card">
      <h3>3. Empirical vs Molecular Formulas</h3>
      <p><b>Molecular Formula:</b> The actual number of atoms in a molecule (e.g., Benzene is <code>C₆H₆</code>).</p>
      <p><b>Empirical Formula:</b> The simplest, most reduced whole-number ratio of atoms in a compound.</p>
      <p><b>Example:</b> Since C₆H₆ can be divided by 6, its simplest ratio (Empirical Formula) is just <code>CH</code>.</p>
      <div class="rxn-model">C₄H₈ (Molecular) ➔ CH₂ (Empirical)</div>
      <div class="review-note" style="margin-top:14px; padding:14px 16px;">
        <strong>Worked example:</strong>
        <p style="margin: 8px 0 10px; color: #1e3565;"><strong>Problem:</strong> Determine the empirical formula for glucose, which has the molecular formula <code>C₆H₁₂O₆</code>.</p>
        <ol style="margin: 0 0 0 18px; padding: 0; color: #1e3565;">
          <li>Write the molecular formula: <code>C₆H₁₂O₆</code>.</li>
          <li>List the subscripts: C = 6, H = 12, O = 6.</li>
          <li>Find the greatest common divisor for all subscripts: <code>6</code>.</li>
          <li>Divide each subscript by 6: C → 1, H → 2, O → 1.</li>
          <li>Write the empirical formula: <code>CH₂O</code>.</li>
          <li>Check: this is the simplest whole-number ratio of atoms for glucose.</li>
        </ol>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close tb-body

st.divider()

# ---------------------------------------------------------------------------
# SECTION 3 — INTERACTIVE DATA ANALYSIS (Q1–3)
# ---------------------------------------------------------------------------
st.subheader("③ Interactive Practice — Questions 1–3")
st.write("Use the interactive tools below to solve the problems.")

# ── Q1 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 1 — Scientific Notation Builder")
st.write("Convert the number **1500** into scientific notation by adjusting the sliders.")

c1, c2 = st.columns(2)
with c1:
    base = st.slider("Base Number", min_value=1.0, max_value=9.9, value=5.0, step=0.1)
with c2:
    exponent = st.slider("Exponent (Power of 10)", min_value=-5, max_value=5, value=0, step=1)

st.info(f"**Your Answer:** {base} × 10^{exponent}")

q1_correct = (base == 1.5) and (exponent == 3)
if q1_correct:
    st.success("✅ Correct! 1.5 × 10³ is 1500.")
else:
    st.warning("Keep adjusting until your base and exponent equal 1500.")

st.divider()

# ── Q2 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 2 — Percent Error Calculation")
st.write(
    "A researcher measures the mass of a sample to be **5.51 g**. "
    "The actual mass of the sample is known to be **5.80 g**."
)
with st.expander("💡 Formula Reminder"):
    st.write("**| Measured - Actual | / Actual × 100**")

c1, c2, c3 = st.columns(3)
with c1:
    measured_in = st.number_input("Measured Value", value=0.00, step=0.01)
with c2:
    actual_in = st.number_input("Actual Value", value=0.00, step=0.01)
with c3:
    error_calc = st.number_input("Calculated % Error", value=0.0, step=0.1)

q2_correct = (measured_in == 5.51) and (actual_in == 5.80) and (4.9 <= error_calc <= 5.1)
if q2_correct:
    st.success("✅ Correct! |5.51 - 5.80| / 5.80 × 100 = 5.0%")
else:
    st.warning("Enter the values from the prompt and calculate the percent error.")

st.divider()

# ── Q3 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 3 — Molar Mass Calculation")
st.write("Calculate the molar mass of **Rb₂Cr₂O₇**. (Use whole numbers or one decimal place from the periodic table: Rb=85.5, Cr=52.0, O=16.0)")

c1, c2, c3 = st.columns(3)
with c1: 
    rb_mass = st.number_input("Mass of Rb atoms", min_value=0.0, value=0.0, step=1.0)
with c2: 
    cr_mass = st.number_input("Mass of Cr atoms", min_value=0.0, value=0.0, step=1.0)
with c3: 
    o_mass = st.number_input("Mass of O atoms", min_value=0.0, value=0.0, step=1.0)

total_mass = rb_mass + cr_mass + o_mass
st.info(f"**Total Calculated Molar Mass:** {total_mass:.1f} g/mol")

# Accepting a tight range to account for slight periodic table rounding variations
q3_correct = (386.0 <= total_mass <= 387.5) and (rb_mass > 0) and (cr_mass > 0) and (o_mass > 0)

if q3_correct:
    st.success("✅ Correct! (85.47 × 2) + (52.00 × 2) + (16.00 × 7) ≈ 386.9 g/mol")
else:
    st.warning("Multiply the atomic mass of each element by its subscript and add them together.")

st.divider()

# ---------------------------------------------------------------------------
# SECTION 4 — MULTIPLE CHOICE Q4–20
# ---------------------------------------------------------------------------
st.subheader("④ Knowledge Check — Questions 4–20")
st.write(
    "Select the best answer for each question. "
    "Detailed feedback will appear after you click **Grade & Generate Report**."
)

MC_QUESTIONS = [
    {
        "q": "4. Convert the following into scientific notation: 1500",
        "options": ["1.5 x 10^2", "15 x 10^2", "1.5 x 10^3", "1.5 x 10^-3"],
        "a": "1.5 x 10^3",
        "f": "Move the decimal 3 places to the left to get a base of 1.5. Left movement means a positive exponent.",
    },
    {
        "q": "5. Convert the following into scientific notation: 0.001012",
        "options": ["1.012 x 10^3", "1.012 x 10^-3", "10.12 x 10^-4", "1.012 x 10^-4"],
        "a": "1.012 x 10^-3",
        "f": "Move the decimal 3 places to the right. Right movement means a negative exponent.",
    },
    {
        "q": "6. Convert the following into decimal notation: 4.59 x 10^3",
        "options": ["459", "4590", "0.00459", "45900"],
        "a": "4590",
        "f": "A positive exponent of 3 means you move the decimal 3 places to the right.",
    },
    {
        "q": "7. Convert the following into decimal notation: 2.80 x 10^-4",
        "options": ["0.000280", "0.0000280", "28000", "0.00280"],
        "a": "0.000280",
        "f": "A negative exponent of -4 means you move the decimal 4 places to the left.",
    },
    {
        "q": "8. Indicate the number of significant figures in: 0.001012 L",
        "options": ["3", "4", "6", "7"],
        "a": "4",
        "f": "Leading zeros are NEVER significant. Only the digits '1012' count.",
    },
    {
        "q": "9. Indicate the number of significant figures in: 34 g",
        "options": ["1", "2", "3", "0"],
        "a": "2",
        "f": "Both digits (3 and 4) are non-zero, so they are both significant.",
    },
    {
        "q": "10. Round the following number to 2 significant figures: 0.826 mg",
        "options": ["0.82", "0.83", "0.8", "0.8260"],
        "a": "0.83",
        "f": "The first two sig figs are 8 and 2. The next digit is a 6, which rounds the 2 up to a 3.",
    },
    {
        "q": "11. Convert 850 cm to mm.",
        "options": ["85 mm", "8.5 mm", "8500 mm", "0.85 mm"],
        "a": "8500 mm",
        "f": "There are 10 millimeters in every centimeter. 850 * 10 = 8500.",
    },
    {
        "q": "12. Convert 2500 mg to kg.",
        "options": ["2.5 kg", "25 kg", "0.025 kg", "0.0025 kg"],
        "a": "0.0025 kg",
        "f": "Divide by 1,000 to get grams, then divide by 1,000 again to get kilograms (Total: divide by 1,000,000).",
    },
    {
        "q": "13. What is the SI base unit for length?",
        "options": ["Foot", "Centimeter", "Meter", "Kilometer"],
        "a": "Meter",
        "f": "The standard SI (metric) unit for measuring length is the meter.",
    },
    {
        "q": "14. What is the SI base unit for mass?",
        "options": ["Gram", "Kilogram", "Pound", "Ounce"],
        "a": "Kilogram",
        "f": "The standard SI (metric) unit for measuring mass is the kilogram.",
    },
    {
        "q": "15. A fridge's accepted temp is 38.0 F. The sensor reads: 37.8, 38.3, 38.1, 38.0, 37.6, 38.2, 38.0, 38.0, 37.4, 38.3. Is this precise?",
        "options": ["Yes, the values are very close together", "No, the values are scattered"],
        "a": "No, the values are scattered",
        "f": "Precision is about consistency. The values range from 37.4 to 38.3 (a 0.9 degree spread), making them imprecise.",
    },
    {
        "q": "16. What is the molar mass of Fe₂(CO₃)₃?",
        "options": ["115.8 g/mol", "291.7 g/mol", "350.5 g/mol", "172.9 g/mol"],
        "a": "291.7 g/mol",
        "f": "Fe (55.85 x 2) + C (12.01 x 3) + O (16.00 x 9) = 111.7 + 36.03 + 144 = 291.73 g/mol.",
    },
    {
        "q": "17. What is the molar mass of CoCl₂ • 6H₂O?",
        "options": ["237.9 g/mol", "129.8 g/mol", "18.0 g/mol", "147.8 g/mol"],
        "a": "237.9 g/mol",
        "f": "Add the mass of CoCl₂ (129.83) to the mass of 6 water molecules (6 x 18.02 = 108.12) = 237.95 g/mol.",
    },
    {
        "q": "18. How many moles of NH₃ contain 1.75 x 10²⁴ molecules?",
        "options": ["2.91 mol", "0.34 mol", "1.05 mol", "10.5 mol"],
        "a": "2.91 mol",
        "f": "Divide the number of molecules by Avogadro's number (6.02 x 10²³).",
    },
    {
        "q": "19. How many molecules are in 0.26 mol of CO₂?",
        "options": ["1.57 x 10²³", "4.31 x 10⁻²⁵", "2.31 x 10²⁴", "6.02 x 10²³"],
        "a": "1.57 x 10²³",
        "f": "Multiply the number of moles (0.26) by Avogadro's number (6.02 x 10²³).",
    },
    {
        "q": "20. What is the empirical formula for benzene (C₆H₆)?",
        "options": ["C₃H₃", "CH", "C₆H₆", "C₁₂H₁₂"],
        "a": "CH",
        "f": "An empirical formula is the simplest ratio. Both the 6s in C₆H₆ can be divided by 6, leaving just CH.",
    },
]

user_mc_answers = {}
for i, q in enumerate(MC_QUESTIONS):
    st.markdown(f"**{q['q']}**")
    user_mc_answers[i] = st.radio(
        "", q["options"], key=f"mcq_{i}", index=None, label_visibility="collapsed"
    )
    st.write("")

st.divider()

# ---------------------------------------------------------------------------
# SECTION 5 — GRADE & SUBMIT
# ---------------------------------------------------------------------------
st.subheader("⑤ Final Submission")

answered_mc   = sum(1 for v in user_mc_answers.values() if v is not None)
interactive_s = int(q1_correct) + int(q2_correct) + int(q3_correct)

col_a, col_b, col_c = st.columns(3)
with col_a: st.metric("Interactive (Q1–3)",  f"{interactive_s} / 3")
with col_b: st.metric("MC Answered (Q4–20)", f"{answered_mc} / 17")
with col_c: st.metric("Total Progress",       f"{interactive_s + answered_mc} / 20")

if st.button("📊 Grade & Generate Report", type="primary", use_container_width=True):
    if not student_name or not class_period:
        st.error("⚠️ Please enter your name and select a class period before grading.")
    else:
        score = interactive_s
        mc_results = []

        st.markdown("### Question-by-Question Feedback")

        # ── Interactive recap ────────────────────────────────────────────────
        if q1_correct:
            st.markdown('<div class="fb-ok">✅ <b>Q1 — Scientific Notation:</b> Correct!  1.5 x 10³</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ <b>Q1 — Scientific Notation:</b> Incorrect. Correct answer: <b>1.5 x 10³</b></div>', unsafe_allow_html=True)

        if q2_correct:
            st.markdown('<div class="fb-ok">✅ <b>Q2 — Percent Error:</b> Correct!  5.0%</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ <b>Q2 — Percent Error:</b> Incorrect. Correct answer: <b>5.0%</b></div>', unsafe_allow_html=True)

        if q3_correct:
            st.markdown('<div class="fb-ok">✅ <b>Q3 — Molar Mass:</b> Correct! ~386.9 g/mol</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ <b>Q3 — Molar Mass:</b> Incorrect. Correct answer: <b>~386.9 g/mol</b></div>', unsafe_allow_html=True)

        st.write("")

        # ── MC feedback ──────────────────────────────────────────────────────
        for i, q in enumerate(MC_QUESTIONS):
            chosen     = user_mc_answers[i]
            is_correct = chosen == q["a"]
            if is_correct:
                score += 1
            mc_results.append({"correct": is_correct, "chosen": chosen, "answer": q["a"]})

            qnum = i + 4
            if is_correct:
                st.markdown(
                    f'<div class="fb-ok">✅ <b>Q{qnum}:</b> Correct! — {q["f"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                display = chosen if chosen else "<em>No answer selected</em>"
                st.markdown(
                    f'<div class="fb-bad">❌ <b>Q{qnum}:</b> You chose <em>{display}</em>. '
                    f'Correct: <b>{q["a"]}</b> — {q["f"]}</div>',
                    unsafe_allow_html=True,
                )

        # ── Score banner ─────────────────────────────────────────────────────
        st.divider()
        pct   = (score / 20) * 100
        grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"
        st.markdown(f"""
        <div class="score-box">
          <div class="sub">{student_name} &nbsp;·&nbsp; {class_period}</div>
          <div class="big">{score} / 20</div>
          <div class="pct">{pct:.1f}% &nbsp;·&nbsp; Grade: {grade}</div>
        </div>""", unsafe_allow_html=True)

        if   pct >= 90: st.success("🏆 Outstanding! You have mastered data analysis and the mole.")
        elif pct >= 80: st.success("🎯 Great work! Review any missed questions before the exam.")
        elif pct >= 70: st.warning("📚 Solid effort. Go back over the concepts you missed.")
        else:           st.error("📖 Keep studying! Re-read the concept review and try again.")

        # ── PDF download ─────────────────────────────────────────────────────
        pdf_bytes = create_pdf(
            student_name, class_period, score, 20,
            datetime.now().strftime("%B %d, %Y"),
            mc_results, q1_correct, q2_correct, q3_correct,
        )
        st.download_button(
            label="📄 Download Full Report (PDF)",
            data=pdf_bytes,
            file_name=f"{student_name.replace(' ', '_')}_Module2_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )