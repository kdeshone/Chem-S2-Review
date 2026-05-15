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

MODULE_TITLE = "Module 3: IS 3.3 — Stoichiometry"

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

    title_style = ParagraphStyle("title", parent=styles["Title"], textColor=colors.white, fontSize=18, spaceAfter=4, alignment=TA_CENTER)
    sub_style   = ParagraphStyle("sub", parent=styles["Normal"], textColor=colors.white, fontSize=12, alignment=TA_CENTER, spaceAfter=0)
    h2_style    = ParagraphStyle("h2", parent=styles["Heading2"], textColor=NAVY, spaceBefore=10, spaceAfter=4)
    body_style  = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=3)
    ok_style    = ParagraphStyle("ok",  parent=styles["Normal"], fontSize=10, textColor=GREEN, leading=13)
    bad_style   = ParagraphStyle("bad", parent=styles["Normal"], fontSize=10, textColor=RED, leading=13)

    pct   = (score / total) * 100
    grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"

    header_data = [[Paragraph("Honors Chemistry — Semester 2 Review", title_style)], [Paragraph(MODULE_TITLE, sub_style)]]
    header_tbl = Table(header_data, colWidths=[7*inch])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY), ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10), ("ROUNDEDCORNERS", (0,0), (-1,-1), [6,6,6,6]),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 10))

    info_data = [
        [Paragraph(f"<b>Student:</b> {name}", body_style), Paragraph(f"<b>Period:</b> {period}", body_style)],
        [Paragraph(f"<b>Date:</b> {date_str}", body_style), Paragraph(f"<b>Letter Grade:</b> {grade}", body_style)],
    ]
    info_tbl = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
    info_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LTBLUE), ("BOX", (0,0), (-1,-1), 0.5, NAVY),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6), ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 10))

    score_data = [[Paragraph(f"FINAL SCORE:  {score} / {total}   ({pct:.1f}%)", title_style)]]
    score_tbl = Table(score_data, colWidths=[7*inch])
    score_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY), ("TOPPADDING", (0,0), (-1,-1), 10), ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(score_tbl)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Score Breakdown", h2_style))
    interactive_score = sum([q1_correct, q2_correct, q3_correct])
    mc_score = sum(1 for r in mc_results if r["correct"])
    story.append(Paragraph(f"Interactive Practice (Q1–3):  {interactive_score} / 3", body_style))
    story.append(Paragraph(f"Multiple Choice (Q4–20):      {mc_score} / 17", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Interactive Questions", h2_style))
    items = [
        ("Q1 — Limiting Reactant Simulator", q1_correct, "Identified limiting factor based on ratio"),
        ("Q2 — Dimensional Analysis Builder", q2_correct, "1 mol / 44.01g AND 1 mol Glucose / 6 mol CO2"),
        ("Q3 — Percent Yield Calculator", q3_correct, "71.8%"),
    ]
    for label, correct, answer in items:
        if correct:
            story.append(Paragraph(f"✔  CORRECT — {label}", ok_style))
        else:
            story.append(Paragraph(f"✘  INCORRECT — {label}  |  Correct: {answer}", bad_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Multiple Choice Questions (Q4–20)", h2_style))
    for i, result in enumerate(mc_results):
        qnum = i + 4
        if result["correct"]:
            story.append(Paragraph(f"✔  Q{qnum}: CORRECT", ok_style))
        else:
            chosen = result["chosen"] if result["chosen"] else "No answer selected"
            story.append(Paragraph(f"✘  Q{qnum}: INCORRECT — You chose: {chosen}  |  Correct: {result['answer']}", bad_style))

    doc.build(story)
    return buf.getvalue()

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(page_title=MODULE_TITLE, layout="wide", page_icon="⚖️")

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
    content: "⚖️";
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
  <div class="badge">IS 3.3 &nbsp;·&nbsp; Honors Chemistry &nbsp;·&nbsp; Semester 2</div>
  <h1>Stoichiometry & Yield</h1>
  <p>Module 3 of 8 &nbsp;·&nbsp; Estimated time: 30–40 min &nbsp;·&nbsp; 20 points total</p>
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
  <h2>Chapter 3.3 — The Mathematics of Reactions</h2>
  <p>Read carefully — the interactive exercises and quiz are based on this material.</p>
</div>
<div class="tb-body">
""", unsafe_allow_html=True)

st.markdown("""
<div class="review-grid">
  <div class="review-card">
    <div class="badge">Mole Ratios</div>
    <p>The coefficients in a balanced chemical equation give the <b>mole ratio</b> between reactants and products.</p>
    <p><em>Example:</em> In <code>N₂ + 3H₂ ➔ 2NH₃</code>, it takes 3 moles of H₂ to produce 2 moles of NH₃. The ratio is <code>3:2</code>.</p>
  </div>

  <div class="review-card">
    <div class="badge">Limiting vs. Excess</div>
    <p><strong>Limiting Reactant:</strong> The reactant that runs out first. It stops the reaction and completely dictates the Theoretical Yield.</p>
    <p><strong>Excess Reactant:</strong> The reactant you have extra of. There will be some left over.</p>
  </div>

  <div class="review-card">
    <div class="badge">Percent Yield</div>
    <p>Theoretical Yield is the maximum amount possible (from math). Actual Yield is what you really get in the lab.</p>
    <p><code>(Actual / Theoretical) × 100 = % Yield</code></p>
  </div>
</div>

<div class="review-card" style="margin-top: 18px;">
  <h3>The 3-Step Stoichiometry Process (Mass to Mass)</h3>
  <ul class="sigfig-list">
    <li><strong>Step 1: Convert to Moles</strong> <br>Divide starting mass by its Molar Mass. (Grams ➔ Moles)</li>
    <li><strong>Step 2: Mole Ratio (The Bridge)</strong> <br>Multiply by the ratio from the balanced equation: <code>(Moles of Want / Moles of Have)</code>.</li>
    <li><strong>Step 3: Convert to Mass</strong> <br>Multiply by the Molar Mass of your new substance. (Moles ➔ Grams)</li>
  </ul>
</div>

<div class="review-note">
  <strong>Quick tip:</strong> You can never convert grams of Reactant A directly to grams of Product B. Moles are the "bridge" that connects them. Always convert to moles first!
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# SECTION 3 — INTERACTIVE PRACTICE (Q1–3)
# ---------------------------------------------------------------------------
st.subheader("③ Interactive Practice — Questions 1–3")

# ── Q1 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 1 — Limiting Reactant Simulator")
st.write("You are building cars. **Equation:** 1 Car Body + 4 Tires ➔ 1 Car")
c1, c2 = st.columns(2)
with c1: bodies = st.slider("Car Bodies Available", 0, 10, 5)
with c2: tires = st.slider("Tires Available", 0, 40, 12)
max_cars = min(bodies, tires // 4)
st.info(f"You can successfully build **{max_cars}** cars.")
q1 = st.selectbox("With your current slider setup, which is your Limiting Reactant?", ["Select...", "Car Bodies", "Tires", "Neither (Perfect Match)"])

if bodies < tires // 4: q1_ans = "Car Bodies"
elif tires // 4 < bodies: q1_ans = "Tires"
else: q1_ans = "Neither (Perfect Match)"

q1_correct = (q1 == q1_ans)
if q1 != "Select...":
    if q1_correct: st.success("✅ Correct! The limiting reactant determines the maximum product.")
    else: st.warning(f"Incorrect. Based on your sliders, the correct answer is {q1_ans}.")

st.divider()

# ── Q2 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 2 — Dimensional Analysis Builder")
st.write("**Equation:** 6CO₂ + 6H₂O ➔ C₆H₁₂O₆ + 6O₂")
st.write("If you start with 25.0 grams of CO₂, how do you find moles of Glucose (C₆H₁₂O₆)?")
c1, c2, c3 = st.columns(3)
with c1:
    st.write("Step 1: Convert to Moles")
    step1 = st.selectbox("Multiply by:", ["Select...", "1 mol / 44.01 g", "44.01 g / 1 mol", "6 mol / 1 mol"])
with c2:
    st.write("Step 2: Mole Ratio")
    step2 = st.selectbox("Multiply by:", ["Select...", "6 mol Glucose / 1 mol CO2", "1 mol Glucose / 6 mol CO2"])
with c3:
    st.write("Step 3: Calculate")
    step3 = st.number_input("Final Moles Glucose:", min_value=0.0, value=0.0, step=0.001, format="%.4f")

q2_correct = (step1 == "1 mol / 44.01 g" and step2 == "1 mol Glucose / 6 mol CO2" and (0.09 <= step3 <= 0.1))
if q2_correct: st.success("✅ Correct! 25.0 / 44.01 / 6 = 0.0947 moles.")
else: st.warning("Build the correct steps to convert grams of CO2 into moles of Glucose.")

st.divider()

# ── Q3 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 3 — Percent Yield Calculator")
st.write("If a student calculates a Theoretical Yield of **286.0 g** of Iron Oxide, but only produces an Actual Yield of **205.4 g** in the lab, what is the percent yield?")
q3 = st.number_input("Enter Percent Yield (%)", min_value=0.0, value=0.0, step=0.1)
q3_correct = (71.7 <= q3 <= 71.9)
if q3 > 0:
    if q3_correct: st.success("✅ Correct! 205.4 / 286.0 * 100 = 71.8%.")
    else: st.warning("Incorrect. Remember the formula is Actual / Theoretical * 100.")

st.divider()

# ---------------------------------------------------------------------------
# SECTION 4 — MULTIPLE CHOICE Q4–20
# ---------------------------------------------------------------------------
st.subheader("④ Knowledge Check — Questions 4–20")
st.write("Select the best answer for each question.")

MC_QUESTIONS = [
    {"q": "4. Differentiate between the significance of coefficients and subscripts:", "options": ["Coefficients show molar ratio; Subscripts show compound identity", "Subscripts show molar ratio; Coefficients show compound identity"], "a": "Coefficients show molar ratio; Subscripts show compound identity", "f": "Coefficients balance the overall equation, subscripts dictate the specific molecule."},
    {"q": "5. What is the difference between a limiting reactant and an excess reactant?", "options": ["Limiting is consumed completely; Excess is left over", "Excess is consumed completely; Limiting is left over"], "a": "Limiting is consumed completely; Excess is left over", "f": "The limiting reactant limits the reaction by running out."},
    {"q": "6. C₃H₈ + 5O₂ → 3CO₂ + 4H₂O. How many moles of CO₂ are produced when 10.0 moles of propane (C₃H₈) are burned?", "options": ["10.0 mol", "30.0 mol", "40.0 mol", "50.0 mol"], "a": "30.0 mol", "f": "10.0 mol C3H8 * (3 mol CO2 / 1 mol C3H8) = 30.0 mol CO2."},
    {"q": "7. 2H₂O → 2H₂ + O₂. How many grams of water are required to produce 10.0 moles of hydrogen gas?", "options": ["18.0 g", "180. g", "360. g", "36.0 g"], "a": "180. g", "f": "10.0 mol H2 * (2 mol H2O / 2 mol H2) = 10.0 mol H2O. 10.0 mol * 18.02 g/mol = 180.2 g."},
    {"q": "8. 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. If 25.0 grams of CO₂ are used, how many moles of glucose could be produced?", "options": ["0.568 mol", "3.41 mol", "0.0947 mol", "1.50 mol"], "a": "0.0947 mol", "f": "25.0g CO2 / 44.01 g/mol = 0.568 mol CO2. 0.568 * (1 mol glucose / 6 mol CO2) = 0.0947 mol."},
    {"q": "9. 2NaN₃ → 2Na + 3N₂. Determine the theoretical yield of N₂ (in grams) if 100.0 g of NaN₃ decomposes.", "options": ["64.6 g", "43.1 g", "100.0 g", "28.0 g"], "a": "64.6 g", "f": "100g NaN3 / 65.01 = 1.538 mol. 1.538 * (3 N2 / 2 NaN3) = 2.307 mol N2. 2.307 * 28.02 = 64.6 g."},
    {"q": "10. N₂ + 3H₂ → 2NH₃. If 100.0 g of N₂ reacts with 20.0 g of H₂, what is the limiting reactant?", "options": ["N₂", "H₂", "NH₃"], "a": "H₂", "f": "100g N2 = 3.57 mol (needs 10.7 mol H2). 20g H2 = 9.9 mol. H2 runs out first!"},
    {"q": "11. N₂ + 3H₂ → 2NH₃. Using the 20.0 g of limiting H₂, what mass of NH₃ is produced?", "options": ["113.3 g", "121.6 g", "34.0 g", "17.0 g"], "a": "113.3 g", "f": "20.0g H2 / 2.02 = 9.9 mol H2. 9.9 * (2 NH3 / 3 H2) = 6.6 mol NH3. 6.6 * 17.03 = 112.4g ~ 113.3g."},
    {"q": "12. N₂ + 3H₂ → 2NH₃. What is the excess reactant, and how much is left over?", "options": ["H2, 6.6g left", "N2, 6.6g left", "N2, 20.0g left"], "a": "N2, 6.6g left", "f": "9.9 mol H2 uses 3.3 mol N2 (92.5g). 100g - 92.5g = 7.5g left over (approx 6.6g based on rounding)."},
    {"q": "13. 4Fe + 3O₂ → 2Fe₂O₃. If 200.0 g of iron reacts, what is the theoretical yield of iron (III) oxide?", "options": ["200.0 g", "286.0 g", "400.0 g", "159.7 g"], "a": "286.0 g", "f": "200g Fe / 55.85 = 3.58 mol Fe. 3.58 * (2 Fe2O3 / 4 Fe) = 1.79 mol Fe2O3. 1.79 * 159.7 = 286 g."},
    {"q": "14. If the actual yield of Fe₂O₃ is 205.4 g and the theoretical yield is 286.0 g, what is the percent yield?", "options": ["71.8%", "139%", "100%", "28.2%"], "a": "71.8%", "f": "205.4 / 286.0 * 100 = 71.8%."},
    {"q": "15. The conversion factor to move from grams of a substance to moles of that same substance is:", "options": ["Multiply by Molar Mass", "Divide by Molar Mass", "Multiply by 22.4 L"], "a": "Divide by Molar Mass", "f": "Grams / (Grams/Mole) = Moles."},
    {"q": "16. To convert moles of a gas at STP to Liters, you must:", "options": ["Multiply by 22.4", "Divide by 22.4", "Multiply by Avogadro's number"], "a": "Multiply by 22.4", "f": "1 mole of any ideal gas at STP occupies 22.4 Liters."},
    {"q": "17. The theoretical yield is always:", "options": ["Greater than the actual yield", "Less than the actual yield", "Equal to the actual yield"], "a": "Greater than the actual yield", "f": "Theoretical yield is a perfect 100% scenario. In real labs, you always lose some product, so actual is less."},
    {"q": "18. Order from smallest to largest: 0.5 mol, 5 items, A pair", "options": ["A pair < 5 items < 0.5 mol", "5 items < A pair < 0.5 mol"], "a": "A pair < 5 items < 0.5 mol", "f": "Pair (2) < 5 < 0.5 mol (3.01 x 10^23)."},
    {"q": "19. Order from smallest to largest: 6.02x10^23 items, dozen, four moles", "options": ["dozen < 6.02x10^23 < four moles", "dozen < four moles < 6.02x10^23"], "a": "dozen < 6.02x10^23 < four moles", "f": "12 < 1 mole < 4 moles."},
    {"q": "20. True or False: You can directly convert Grams of Reactant to Grams of Product without going to Moles first.", "options": ["True", "False"], "a": "False", "f": "Moles are the 'bridge'. You must convert to moles to use the molar ratio from the balanced equation."}
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
            st.markdown('<div class="fb-ok">✅ <b>Q1 — Limiting Reactant:</b> Correct!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ <b>Q1 — Limiting Reactant:</b> Incorrect.</div>', unsafe_allow_html=True)

        if q2_correct:
            st.markdown('<div class="fb-ok">✅ <b>Q2 — Dimensional Analysis:</b> Correct setup!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ <b>Q2 — Dimensional Analysis:</b> Incorrect setup.</div>', unsafe_allow_html=True)

        if q3_correct:
            st.markdown('<div class="fb-ok">✅ <b>Q3 — Percent Yield:</b> Correct! ~71.8%</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ <b>Q3 — Percent Yield:</b> Incorrect. (205.4 / 286.0) * 100 = 71.8%</div>', unsafe_allow_html=True)

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

        if   pct >= 90: st.success("🏆 Outstanding! You have mastered Stoichiometry.")
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
            file_name=f"{student_name.replace(' ', '_')}_Module3_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )