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

MODULE_TITLE = "Module 4: IS 3.4 — Gases"

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
        ("Q1 — Boyle's Law Simulator", q1_correct, "Pressure Increases as Volume Decreases"),
        ("Q2 — Temperature Conversion", q2_correct, "298 K"),
        ("Q3 — Ideal Gas Law Calculator", q3_correct, "0.18 mol"),
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
st.set_page_config(page_title=MODULE_TITLE, layout="wide", page_icon="🎈")

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
    content: "🎈";
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
  <div class="badge">IS 3.4 &nbsp;·&nbsp; Honors Chemistry &nbsp;·&nbsp; Semester 2</div>
  <h1>Gases and Gas Laws</h1>
  <p>Module 4 of 8 &nbsp;·&nbsp; Estimated time: 30–40 min &nbsp;·&nbsp; 20 points total</p>
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
  <h2>Chapter 3.4 — Gas Laws & KMT</h2>
  <p>Read carefully — the interactive exercises and quiz are based on this material.</p>
</div>
<div class="tb-body">
""", unsafe_allow_html=True)

st.markdown("""
<div class="review-grid">
  <div class="review-card">
    <div class="badge">Kinetic Molecular Theory</div>
    <p>Gases consist of tiny particles that are very far apart. They are in continuous, rapid, random motion.</p>
    <p>Collisions between gas particles are perfectly <strong>elastic</strong>, meaning no kinetic energy is lost when they bounce.</p>
  </div>

  <div class="review-card">
    <div class="badge">Ideal Gas Law</div>
    <p><strong>PV = nRT</strong></p>
    <p>This law incorporates the moles (n) of gas. <b>R</b> is the ideal gas constant (0.0821 L·atm/mol·K).</p>
    <p>Gases best obey the ideal gas law at <strong>High Temps and Low Pressures</strong> because they are moving fast and spread far apart.</p>
  </div>

  <div class="review-card">
    <div class="badge">Dalton's Law</div>
    <p>Dalton's Law of Partial Pressures states that the total pressure of a gas mixture is simply the sum of all the individual partial pressures.</p>
    <p><code>P_total = P₁ + P₂ + P₃...</code></p>
  </div>
</div>

<div class="review-card" style="margin-top: 18px;">
  <h3>The Three Major Gas Relationships</h3>
  <ul class="sigfig-list">
    <li><strong>Boyle's Law (Pressure & Volume)</strong> <br><em>Inverse relationship.</em> If you squeeze a balloon (decrease volume), the pressure goes up.</li>
    <li><strong>Charles's Law (Volume & Temperature)</strong> <br><em>Direct relationship.</em> If you heat a balloon (increase temp), the volume expands.</li>
    <li><strong>Gay-Lussac's Law (Pressure & Temperature)</strong> <br><em>Direct relationship.</em> If you heat a rigid can of hairspray, the pressure builds up until it pops.</li>
  </ul>
</div>

<div class="review-note">
  <strong>Critical Rule:</strong> When calculating gas laws, temperature must <em>always</em> be in Kelvin to avoid dividing by zero or getting negative numbers! <br><br>
  Formula: <code>K = °C + 273</code>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# SECTION 3 — INTERACTIVE PRACTICE (Q1–3)
# ---------------------------------------------------------------------------
st.subheader("③ Interactive Practice — Questions 1–3")

# ── Q1 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 1 — Boyle's Law Simulator")
st.write("Imagine you have a sealed, flexible bottle. Move the slider to decrease the volume (squeeze it!).")
volume = st.slider("Bottle Volume (Liters)", min_value=0.5, max_value=5.0, value=5.0, step=0.1)
initial_pv = 5.0 * 1.0 
current_pressure = initial_pv / volume
st.info(f"**Current Pressure inside the bottle: {current_pressure:.2f} atm**")
st.progress(min(current_pressure / 10.0, 1.0))

q1 = st.radio("Based on your simulation, what happens to pressure when volume decreases?", ["Select...", "It Decreases", "It Increases", "It stays the same"], index=0)
q1_correct = (q1 == "It Increases")
if q1 != "Select...":
    if q1_correct: st.success("✅ Correct! This is Boyle's Law: an inverse relationship.")
    else: st.warning("Incorrect. Look at the pressure gauge as you slide the volume to the left.")

st.divider()

# ── Q2 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 2 — Temperature Conversions")
st.write("Gas laws require temperature to be in Kelvin. Use the formula: **K = °C + 273**")
celsius = st.slider("Select Celsius Temperature", -50, 100, 25)
st.write(f"Equation: K = {celsius} + 273 = **{celsius + 273} K**")

q2 = st.number_input("What is 25°C converted to Kelvin?", min_value=0, value=0)
q2_correct = (q2 == 298)
if q2 > 0:
    if q2_correct: st.success("✅ Correct! 25 + 273 = 298 K.")
    else: st.warning("Incorrect. Use the slider to find the Kelvin value for 25°C.")

st.divider()

# ── Q3 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 3 — Ideal Gas Law Calculator")
st.write("Calculate the number of moles of gas contained in a **3.0 L** vessel at **300. K** with a pressure of **1.50 atm**. (R = 0.0821)")
with st.expander("💡 Formula Reminder"): st.write("n = (P × V) / (R × T)")
q3 = st.number_input("Enter Moles (n):", min_value=0.0, value=0.0, step=0.01)
q3_correct = (0.17 <= q3 <= 0.19)
if q3 > 0:
    if q3_correct: st.success("✅ Correct! (1.50 * 3.0) / (0.0821 * 300) = 0.18 moles.")
    else: st.warning("Incorrect. Try plugging the numbers into the formula exactly as shown.")

st.divider()

# ---------------------------------------------------------------------------
# SECTION 4 — MULTIPLE CHOICE Q4–20
# ---------------------------------------------------------------------------
st.subheader("④ Knowledge Check — Questions 4–20")
st.write("Select the best answer for each question.")

MC_QUESTIONS = [
    {"q": "4. When a bottle is squeezed, the pressure increases and the volume:", "options": ["Increases", "Decreases", "Stays the same", "Fluctuates"], "a": "Decreases", "f": "Boyle's Law states that pressure and volume are inversely proportional."},
    {"q": "5. The volume of a hot air balloon will _____ as the temperature is raised.", "options": ["Increase", "Decrease", "Stay the same", "Pop instantly"], "a": "Increase", "f": "Charles's Law: Temperature and volume are directly proportional."},
    {"q": "6. If the temperature of a can of hairspray is increased, the pressure will:", "options": ["Increase", "Decrease", "Stay the same", "Vaporize"], "a": "Increase", "f": "Gay-Lussac's Law: Temperature and pressure are directly proportional."},
    {"q": "7. Gases best obey the ideal gas law at:", "options": ["Low temps, High pressures", "High temps, Low pressures", "Low temps, Low pressures", "High temps, High pressures"], "a": "High temps, Low pressures", "f": "High temps make them move fast; low pressures spread them far apart (minimizing attractions)."},
    {"q": "8. Convert 25°C to Kelvin.", "options": ["298 K", "-248 K", "25 K", "273 K"], "a": "298 K", "f": "Kelvin = °C + 273. 25 + 273 = 298 K."},
    {"q": "9. Convert 25 K to °C.", "options": ["298 °C", "-248 °C", "25 °C", "0 °C"], "a": "-248 °C", "f": "°C = K - 273. 25 - 273 = -248 °C."},
    {"q": "10. Combined gas law: A gas at 110 kPa and 30.0°C fills a 2.00 L container. If the temp is raised to 80.0°C and pressure is increased to 440 kPa, what is the new volume?", "options": ["0.58 L", "1.16 L", "4.00 L", "0.25 L"], "a": "0.58 L", "f": "P₁V₁/T₁ = P₂V₂/T₂. (110*2.00)/303 = (440*V₂)/353. Solving for V₂ gives 0.58 L."},
    {"q": "11. Combined gas law: What is the volume at STP of a 125.0 mL of a gas originally at 1.50 atm and 100.0°C?", "options": ["137 mL", "250 mL", "68 mL", "100 mL"], "a": "137 mL", "f": "(1.50 * 125.0)/373 = (1.0 * V₂)/273. Solving for V₂ gives 137 mL."},
    {"q": "12. Dalton's Law: John puts 1250 PSI of Oxygen, 780 PSI of Nitrogen and 550 PSI of Helium in a SCUBA tank. Total pressure?", "options": ["1250 PSI", "2580 PSI", "780 PSI", "2030 PSI"], "a": "2580 PSI", "f": "Dalton's Law states you simply add partial pressures: 1250 + 780 + 550 = 2580."},
    {"q": "13. Molar volume: H₂ + O₂ → H₂O (Unbalanced). How many liters of H₂ gas are required to produce 25.0 g of water at STP?", "options": ["31.1 L", "22.4 L", "15.5 L", "62.2 L"], "a": "31.1 L", "f": "Balance eq: 2H₂ + O₂ → 2H₂O. 25g/18.02 = 1.39 mol H₂O. Ratio is 2:2, so 1.39 mol H₂. 1.39 * 22.4 L/mol = 31.1 L."},
    {"q": "14. Ideal gas law: Calculate the number of moles of gas contained in a 3.0 L vessel at 300. K with a pressure of 1.50 atm.", "options": ["0.18 mol", "1.8 mol", "5.4 mol", "0.0821 mol"], "a": "0.18 mol", "f": "n = PV/RT = (1.50 * 3.0) / (0.0821 * 300) = 0.18 mol."},
    {"q": "15. What is the SI unit for pressure?", "options": ["Kilogram", "Pascal (or atm)", "Liter", "Kelvin"], "a": "Pascal (or atm)", "f": "Pressure is measured in Pascals, atmospheres (atm), or mm Hg."},
    {"q": "16. What is the standard temperature for gas law calculations?", "options": ["Celsius", "Fahrenheit", "Kelvin", "Joules"], "a": "Kelvin", "f": "Gas laws ALWAYS use Kelvin to avoid dividing by zero."},
    {"q": "17. What is the SI unit for volume?", "options": ["Grams", "Meters", "Liters", "Moles"], "a": "Liters", "f": "Volume for gases is typically measured in Liters (L) or milliliters (mL)."},
    {"q": "18. What are the standard values for STP (Standard Temperature and Pressure)?", "options": ["1 atm and 273 K", "1 atm and 298 K", "100 kPa and 0 K", "1 atm and 0 K"], "a": "1 atm and 273 K", "f": "STP is defined as 0 degrees Celsius (273 K) and 1 atmosphere of pressure."},
    {"q": "19. Which gas law describes an INVERSE relationship?", "options": ["Boyle's Law", "Charles's Law", "Gay-Lussac's Law", "Dalton's Law"], "a": "Boyle's Law", "f": "Boyle's is the only inverse law. If you squeeze it (less volume), pressure goes up."},
    {"q": "20. Which gas law describes a DIRECT relationship involving Volume and Temperature?", "options": ["Boyle's Law", "Charles's Law", "Dalton's Law", "Avogadro's Law"], "a": "Charles's Law", "f": "Charles's Law is direct. As heat goes up, volume goes up."}
]

user_mc_answers = {}
for i, q in enumerate(MC_QUESTIONS):
    st.markdown(f"**{q['q']}**")
    user_mc_answers[i] = st.radio("", q["options"], key=f"mcq_{i}", index=None, label_visibility="collapsed")
    st.write("")
st.divider()

# ---------------------------------------------------------------------------
# 5. GRADE & SUBMIT
# ---------------------------------------------------------------------------
st.subheader("⑤ Final Submission")
answered_mc   = sum(1 for v in user_mc_answers.values() if v is not None)
interactive_s = int(q1_correct) + int(q2_correct) + int(q3_correct)

col_a, col_b, col_c = st.columns(3)
with col_a: st.metric("Interactive (Q1–3)",  f"{interactive_s} / 3")
with col_b: st.metric("MC Answered (Q4–20)", f"{answered_mc} / 17")
with col_c: st.metric("Total Progress",       f"{interactive_s + answered_mc} / 20")

if st.button("📊 Grade & Generate Report", type="primary", use_container_width=True):
    if not student_name or not class_period: st.error("⚠️ Please enter your name and class period.")
    else:
        score = interactive_s
        mc_results = []
        st.markdown("### Question-by-Question Feedback")

        if q1_correct: st.markdown('<div class="fb-ok">✅ <b>Q1:</b> Correct!</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="fb-bad">❌ <b>Q1:</b> Incorrect.</div>', unsafe_allow_html=True)

        if q2_correct: st.markdown('<div class="fb-ok">✅ <b>Q2:</b> Correct!</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="fb-bad">❌ <b>Q2:</b> Incorrect. K = 25 + 273 = 298.</div>', unsafe_allow_html=True)

        if q3_correct: st.markdown('<div class="fb-ok">✅ <b>Q3:</b> Correct! 0.18 mol</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="fb-bad">❌ <b>Q3:</b> Incorrect. (1.50*3.0)/(0.0821*300) = 0.18.</div>', unsafe_allow_html=True)
        st.write("")

        for i, q in enumerate(MC_QUESTIONS):
            chosen = user_mc_answers[i]
            is_correct = chosen == q["a"]
            if is_correct: score += 1
            mc_results.append({"correct": is_correct, "chosen": chosen, "answer": q["a"]})
            qnum = i + 4
            if is_correct: st.markdown(f'<div class="fb-ok">✅ <b>Q{qnum}:</b> Correct! — {q["f"]}</div>', unsafe_allow_html=True)
            else: st.markdown(f'<div class="fb-bad">❌ <b>Q{qnum}:</b> Correct is <b>{q["a"]}</b> — {q["f"]}</div>', unsafe_allow_html=True)

        st.divider()
        pct = (score / 20) * 100
        grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"
        st.markdown(f"""<div class="score-box"><div class="sub">{student_name} · {class_period}</div>
          <div class="big">{score} / 20</div><div class="pct">{pct:.1f}% · Grade: {grade}</div></div>""", unsafe_allow_html=True)

        pdf_bytes = create_pdf(student_name, class_period, score, 20, datetime.now().strftime("%B %d, %Y"), mc_results, q1_correct, q2_correct, q3_correct)
        st.download_button(label="📄 Download Full Report (PDF)", data=pdf_bytes, file_name=f"{student_name.replace(' ', '_')}_Module4_Report.pdf", mime="application/pdf", use_container_width=True)