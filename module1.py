import streamlit as st
from fpdf import FPDF
from datetime import datetime

MODULE_TITLE = "Module 1: IS 3.1 — Balancing Equations"


# ---------------------------------------------------------------------------
# PDF GENERATION
# ---------------------------------------------------------------------------
def create_pdf(name, period, score, total, date_str, mc_results,
               q1_correct, q2_correct, q3_correct):
    pdf = FPDF()
    pdf.add_page()

    # ── Header bar ──────────────────────────────────────────────────────────
    pdf.set_fill_color(30, 60, 114)
    pdf.rect(0, 0, 210, 38, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 17)
    pdf.cell(0, 13, "Honors Chemistry — Semester 2 Review", ln=True, align="C")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, MODULE_TITLE, ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    # ── Student info box ────────────────────────────────────────────────────
    pdf.set_fill_color(240, 245, 255)
    y0 = pdf.get_y()
    pdf.rect(10, y0, 190, 32, "F")
    pdf.set_font("Arial", size=11)
    pdf.set_x(15)
    pdf.cell(95, 10, f"Student: {name}", ln=False)
    pdf.cell(95, 10, f"Period: {period}", ln=True)
    pdf.set_x(15)
    pdf.cell(95, 10, f"Date: {date_str}", ln=False)
    pct = (score / total) * 100
    grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"
    pdf.cell(95, 10, f"Letter Grade: {grade}", ln=True)
    pdf.ln(6)

    # ── Score banner ────────────────────────────────────────────────────────
    pdf.set_fill_color(30, 60, 114)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 15)
    pdf.cell(0, 13, f"FINAL SCORE:  {score} / {total}   ({pct:.1f}%)", ln=True, align="C", fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(7)

    # ── Section breakdown ───────────────────────────────────────────────────
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Score Breakdown:", ln=True)
    pdf.set_font("Arial", size=11)
    interactive_score = sum([q1_correct, q2_correct, q3_correct])
    mc_score = sum(1 for r in mc_results if r["correct"])
    pdf.set_x(15)
    pdf.cell(0, 8, f"  Interactive Balancing (Q1-3):  {interactive_score} / 3", ln=True)
    pdf.set_x(15)
    pdf.cell(0, 8, f"  Multiple Choice (Q4-20):       {mc_score} / 17", ln=True)
    pdf.ln(5)

    # ── Q1–3 feedback ───────────────────────────────────────────────────────
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Interactive Questions:", ln=True)
    pdf.set_font("Arial", size=10)

    items = [
        ("Q1 — Formation of Water",     q1_correct, "2H2 + O2 -> 2H2O"),
        ("Q2 — Combustion of Methane",  q2_correct, "CH4 + 2O2 -> CO2 + 2H2O"),
        ("Q3 — Reaction Type ID",       q3_correct, "Double Replacement & Decomposition"),
    ]
    for label, correct, answer in items:
        status = "CORRECT" if correct else "INCORRECT"
        if correct:
            pdf.set_text_color(39, 174, 96)
        else:
            pdf.set_text_color(192, 57, 43)
        pdf.set_font("Arial", "B", 10)
        pdf.set_x(15)
        pdf.cell(35, 7, f"  {status}", ln=False)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        suffix = "" if correct else f"  |  Correct: {answer}"
        pdf.cell(0, 7, f"{label}{suffix}", ln=True)

    pdf.ln(4)

    # ── MC feedback ─────────────────────────────────────────────────────────
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Multiple Choice Questions (Q4–20):", ln=True)

    for i, result in enumerate(mc_results):
        qnum = i + 4
        if result["correct"]:
            pdf.set_text_color(39, 174, 96)
            pdf.set_font("Arial", "B", 10)
            pdf.set_x(15)
            pdf.cell(30, 7, f"  Q{qnum}: CORRECT", ln=True)
        else:
            pdf.set_text_color(192, 57, 43)
            pdf.set_font("Arial", "B", 10)
            pdf.set_x(15)
            pdf.cell(30, 7, f"  Q{qnum}: INCORRECT", ln=False)
            pdf.set_text_color(80, 80, 80)
            pdf.set_font("Arial", size=9)
            chosen = result["chosen"] if result["chosen"] else "No answer"
            pdf.cell(0, 7, f"  You: {chosen}   |   Correct: {result['answer']}", ln=True)
        pdf.set_text_color(0, 0, 0)

    return pdf.output(dest="S").encode("latin-1")


# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(page_title=MODULE_TITLE, layout="centered", page_icon="⚖️")

# ---------------------------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* ── Global ── */
section.main > div { max-width: 880px; }

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

/* ── Progress bar ── */
.prog-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f8f9fa;
    border: 1px solid #e4e6ea;
    border-radius: 10px;
    padding: 11px 22px;
    margin-bottom: 22px;
    gap: 6px;
}
.prog-step { text-align: center; font-size: 0.8em; font-weight: 600; color: #aaa; flex: 1; }
.prog-step .num {
    width: 26px; height: 26px; border-radius: 50%;
    background: #dee2e6; color: #888;
    margin: 0 auto 4px; line-height: 26px;
    font-weight: 700; font-size: 0.9em;
}
.prog-step.active .num { background: #1e3c72; color: white; }
.prog-step.active      { color: #1e3c72; }
.prog-step.done   .num { background: #27ae60; color: white; }
.prog-step.done        { color: #27ae60; }
.prog-line { flex: 0.5; height: 2px; background: #dee2e6; border-radius: 2px; }

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
    padding: 20px 24px 6px;
    margin-bottom: 22px;
}

/* ── Callout boxes ── */
.callout { padding: 14px 18px; border-radius: 8px; margin: 14px 0; }
.callout-warn   { background: #fff9e6; border-left: 5px solid #f39c12; }
.callout-info   { background: #eaf4ff; border-left: 5px solid #2980b9; }
.callout h4 { margin: 0 0 7px; font-size: 1em; }
.callout p  { margin: 0; font-size: 0.94em; color: #333; line-height: 1.65; }

/* ── Atom diagram ── */
.atom-diagram {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: #fafbfc;
    border: 1px solid #e4e6ea;
    padding: 22px 18px;
    border-radius: 12px;
    margin: 16px 0 6px;
}
.atom-side { text-align: center; }
.atom-side h4 { margin: 0 0 9px; color: #2c3e50; font-size: 0.82em;
                text-transform: uppercase; letter-spacing: 1.2px; }
.atom-side .formula {
    font-size: 12px; background: #f1f3f5; padding: 3px 9px;
    border-radius: 5px; color: #333; font-family: monospace;
    margin-top: 7px; display: inline-block;
}
.atom-arrow { text-align: center; font-size: 2em; color: #aaa; line-height: 1; }
.atom-arrow small { display: block; font-size: 0.38em; color: #bbb; letter-spacing: 2px; margin-top: 3px; }

/* ── Reaction type cards ── */
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
    padding: 10px; margin-top: 12px;
}

/* ── Balance table ── */
.bal-tbl { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 0.94em; }
.bal-tbl th {
    background: #1e3c72; color: white;
    padding: 8px 14px; text-align: center;
}
.bal-tbl td { padding: 7px 14px; text-align: center; border-bottom: 1px solid #eee; }
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
    font-size: 0.93em;
}
.fb-bad {
    background: #fef8f8; border-left: 4px solid #e74c3c;
    padding: 9px 14px; border-radius: 0 6px 6px 0; margin: 4px 0;
    font-size: 0.93em;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="mod-header">
  <div class="badge">IS 3.1 &nbsp;·&nbsp; Honors Chemistry &nbsp;·&nbsp; Semester 2</div>
  <h1>Balancing Chemical Equations</h1>
  <p>Module 1 of 8 &nbsp;·&nbsp; Estimated time: 25–35 min &nbsp;·&nbsp; 20 points total</p>
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
  <h2>Chapter 3.1 — The Anatomy of Chemical Reactions</h2>
  <p>Read carefully — the interactive exercises and quiz are based on this material.</p>
</div>
<div class="tb-body">
""", unsafe_allow_html=True)

st.markdown("### The Law of Conservation of Mass")
st.write(
    "Proposed by **Antoine Lavoisier**, this law is the foundation of every chemical equation: "
    "**matter cannot be created or destroyed** in a chemical reaction. Atoms are only *rearranged* — "
    "every atom present in the reactants must also appear in the products. The total count of each "
    "element must therefore be identical on both sides of the reaction arrow."
)

st.markdown("""
<div class="atom-diagram">
  <div class="atom-side">
    <h4>Reactants</h4>
    <div style="font-size:36px; margin:10px 0;">🔵🔵 &nbsp;+&nbsp; 🔴🔴</div>
    <span class="formula">H₂ + Cl₂</span>
  </div>
  <div class="atom-arrow">➔<br><small>YIELDS</small></div>
  <div class="atom-side">
    <h4>Products</h4>
    <div style="font-size:36px; margin:10px 0;">🔵🔴 &nbsp;&nbsp;🔵🔴</div>
    <span class="formula">2 HCl</span>
  </div>
</div>
<p style="text-align:center; font-style:italic; color:#999; font-size:0.86em; margin-top:4px;">
Figure 1.1 — 2 blue (H) and 2 red (Cl) atoms appear on both sides. Nothing is created or destroyed.
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout callout-warn">
  <h4>🔑 Critical Rule — Coefficients vs. Subscripts</h4>
  <p>
    To balance an equation you may <strong>only change Coefficients</strong> — the large numbers placed
    <em>in front of</em> a formula (e.g., <strong style="color:#d35400; font-size:1.15em">2</strong>H₂O).<br><br>
    You must <strong>never change Subscripts</strong> — the small numbers <em>inside</em> a formula
    (e.g., H<strong style="color:#e74c3c">₂</strong>O). Changing a subscript changes the identity of the
    substance: H₂O is water, H₂O₂ is hydrogen peroxide — completely different compounds.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Balancing Strategy — Step by Step")
st.write(
    "**1.** Write the unbalanced equation with all correct formulas.  \n"
    "**2.** Count atoms of each element on both sides.  \n"
    "**3.** Balance metals first, then nonmetals, then H, and O last.  \n"
    "**4.** Adjust *coefficients only* until both sides match.  \n"
    "**5.** Double-check every element after any change.  \n"
    "**6.** Simplify — coefficients must be the smallest whole-number ratio."
)

st.markdown("""
<div class="callout callout-info">
  <h4>💡 Pro Tip — Handling Fractions</h4>
  <p>If balancing leaves you with a fractional coefficient (e.g., ½ O₂), multiply
  <em>every</em> coefficient in the entire equation by 2 to clear the fraction.
  All coefficients in a final answer must be whole numbers.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### The Five Major Reaction Types")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔗 Synthesis", "💥 Decomposition",
    "🔄 Single Replacement", "🔀 Double Replacement", "🔥 Combustion"
])

with tab1:
    st.markdown("""
    <div class="rxn-card">
      <h3>1. Synthesis (Combination)</h3>
      <p><b>General Pattern:</b> <code>A + B ➔ AB</code></p>
      <p><b>What happens:</b> Two or more simple substances join together to form a single, more complex
      product. Think of it as building blocks snapping together.</p>
      <p><b>Key clue:</b> Only <em>one</em> product is formed.</p>
      <p><b>Example 1 — Rusting of Iron:</b><br>
      <code>4Fe(s) + 3O₂(g) ➔ 2Fe₂O₃(s)</code></p>
      <p><b>Example 2 — Formation of Water:</b><br>
      <code>2H₂(g) + O₂(g) ➔ 2H₂O(l)</code></p>
      <div class="rxn-model">🟦 + 🟡 ➔ 🟦🟡</div>
    </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="rxn-card">
      <h3>2. Decomposition</h3>
      <p><b>General Pattern:</b> <code>AB ➔ A + B</code></p>
      <p><b>What happens:</b> The exact reverse of synthesis. A single complex compound breaks apart
      into two or more simpler substances. Energy input (heat, light, or electricity) is usually required.</p>
      <p><b>Key clue:</b> Only <em>one</em> reactant is present.</p>
      <p><b>Example 1 — Electrolysis of Water:</b><br>
      <code>2H₂O(l) ➔ 2H₂(g) + O₂(g)</code></p>
      <p><b>Example 2 — Heating Potassium Chlorate:</b><br>
      <code>2KClO₃(s) ➔ 2KCl(s) + 3O₂(g)</code></p>
      <div class="rxn-model">🟦🟡 ➔ 🟦 + 🟡</div>
    </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="rxn-card">
      <h3>3. Single Replacement</h3>
      <p><b>General Pattern:</b> <code>A + BC ➔ AC + B</code></p>
      <p><b>What happens:</b> A more reactive, uncombined element displaces a less reactive element
      from a compound. The displaced element is released on its own. Use the activity series to
      predict whether replacement will occur.</p>
      <p><b>Key clue:</b> One element appears alone on <em>both</em> sides — just different elements.</p>
      <p><b>Example 1 — Zinc in HCl:</b><br>
      <code>Zn(s) + 2HCl(aq) ➔ ZnCl₂(aq) + H₂(g)</code></p>
      <p><b>Example 2 — Halogen Displacement:</b><br>
      <code>2NaI(aq) + Br₂(l) ➔ 2NaBr(aq) + I₂(s)</code></p>
      <div class="rxn-model">🔴 + 🟦🟡 ➔ 🔴🟡 + 🟦</div>
    </div>""", unsafe_allow_html=True)

with tab4:
    st.markdown("""
    <div class="rxn-card">
      <h3>4. Double Replacement (Metathesis)</h3>
      <p><b>General Pattern:</b> <code>AB + CD ➔ AD + CB</code></p>
      <p><b>What happens:</b> The cations (positive ions) of two ionic compounds in aqueous solution
      swap partners. The reaction is driven by forming a precipitate, a gas, or water
      (acid-base neutralization).</p>
      <p><b>Key clue:</b> Two ionic compounds react and positive ions switch places — like a square dance.</p>
      <p><b>Example 1 — Precipitate Formation:</b><br>
      <code>Na₂SO₄(aq) + SrCl₂(aq) ➔ 2NaCl(aq) + SrSO₄(s)↓</code></p>
      <p><b>Example 2 — Neutralization:</b><br>
      <code>Ca(OH)₂(aq) + 2HCl(aq) ➔ CaCl₂(aq) + 2H₂O(l)</code></p>
      <div class="rxn-model">🔴🟡 + 🟦🟢 ➔ 🔴🟢 + 🟦🟡</div>
    </div>""", unsafe_allow_html=True)

with tab5:
    st.markdown("""
    <div class="rxn-card">
      <h3>5. Combustion</h3>
      <p><b>General Pattern:</b> <code>CₓHᵧ + O₂ ➔ CO₂ + H₂O</code></p>
      <p><b>What happens:</b> A hydrocarbon (compound of C and H) reacts rapidly with oxygen,
      releasing heat and light. The products are <em>always</em> CO₂ and H₂O for complete combustion —
      no exceptions.</p>
      <p><b>Key clue:</b> A carbon-hydrogen compound reacts with O₂. See CO₂ + H₂O as products? It's combustion.</p>
      <p><b>Example 1 — Burning Methane:</b><br>
      <code>CH₄(g) + 2O₂(g) ➔ CO₂(g) + 2H₂O(g)</code></p>
      <p><b>Example 2 — Burning Butane:</b><br>
      <code>2C₄H₁₀(g) + 13O₂(g) ➔ 8CO₂(g) + 10H₂O(g)</code></p>
      <div class="rxn-model">🪵 + 🌬️ ➔ ☁️ + 💧 + 🔥</div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close tb-body

st.divider()

# ---------------------------------------------------------------------------
# SECTION 3 — INTERACTIVE BALANCING (Q1–3)
# ---------------------------------------------------------------------------
st.subheader("③ Interactive Balancing Practice — Questions 1–3")
st.write(
    "Adjust the coefficients using the number inputs. "
    "The atom-count table updates live — all rows must turn **green** before the equation is balanced."
)

# ── Q1 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 1 — Formation of Water")
st.latex(r"\_\_ \, H_2 \;\; + \;\; \_\_ \, O_2 \;\; \longrightarrow \;\; \_\_ \, H_2O")

with st.expander("💡 Hint for Question 1"):
    st.write(
        "**Step 1 — Start with H:** Each H₂ has 2 H atoms; each H₂O also has 2 H atoms.  \n"
        "**Step 2 — Check O:** Each O₂ has 2 O atoms, but each H₂O has only 1 O atom.  \n"
        "**Step 3 — Fix the imbalance:** Putting 2 in front of H₂O gives 2 O on the right, "
        "matching O₂ on the left. Now check H — 2 H₂O needs 4 H atoms, so increase H₂ to 2.  \n"
        "**Answer:** 2H₂ + O₂ → 2H₂O"
    )

c1, c2, c3, c4, c5 = st.columns([2, 0.5, 2, 0.5, 2])
with c1: h2_c = st.number_input("H₂", min_value=1, max_value=20, value=1, step=1, key="h2")
with c2: st.markdown("<p style='text-align:center;font-size:1.5em;padding-top:28px'>+</p>", unsafe_allow_html=True)
with c3: o2_c = st.number_input("O₂", min_value=1, max_value=20, value=1, step=1, key="o2")
with c4: st.markdown("<p style='text-align:center;font-size:1.5em;padding-top:28px'>→</p>", unsafe_allow_html=True)
with c5: h2o_c = st.number_input("H₂O", min_value=1, max_value=20, value=1, step=1, key="h2o")

h_r1, h_p1 = h2_c * 2, h2o_c * 2
o_r1, o_p1 = o2_c * 2, h2o_c
q1_correct = (h_r1 == h_p1) and (o_r1 == o_p1)

hc1 = "ok" if h_r1 == h_p1 else "bad"
oc1 = "ok" if o_r1 == o_p1 else "bad"
st.markdown(f"""
<table class="bal-tbl">
  <tr><th>Element</th><th>Reactant Side</th><th>Product Side</th><th>Status</th></tr>
  <tr><td>H</td><td>{h_r1}</td><td>{h_p1}</td>
      <td class="{hc1}">{"✔ Balanced" if hc1=="ok" else "✘ Off"}</td></tr>
  <tr><td>O</td><td>{o_r1}</td><td>{o_p1}</td>
      <td class="{oc1}">{"✔ Balanced" if oc1=="ok" else "✘ Off"}</td></tr>
</table>""", unsafe_allow_html=True)

if q1_correct:
    st.success("✅ Perfectly balanced! **2H₂ + O₂ → 2H₂O**")

st.divider()

# ── Q2 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 2 — Combustion of Methane")
st.latex(r"\_\_ \, CH_4 \;\; + \;\; \_\_ \, O_2 \;\; \longrightarrow \;\; \_\_ \, CO_2 \;\; + \;\; \_\_ \, H_2O")

with st.expander("💡 Hint for Question 2"):
    st.write(
        "Use the **C → H → O** order (always balance O last).  \n"
        "**Step 1 (C):** 1 CH₄ gives 1 C atom. Match it with 1 CO₂.  \n"
        "**Step 2 (H):** 1 CH₄ gives 4 H atoms. Each H₂O holds 2 H → need 2 H₂O.  \n"
        "**Step 3 (O):** Right side: 1 CO₂ (2 O) + 2 H₂O (2 O) = 4 O total → 2 O₂ on the left.  \n"
        "**Answer:** CH₄ + 2O₂ → CO₂ + 2H₂O"
    )

c1, c2, c3, c4, c5, c6, c7 = st.columns([2, 0.4, 2, 0.4, 2, 0.4, 2])
with c1: ch4_c  = st.number_input("CH₄",  min_value=1, max_value=20, value=1, step=1, key="ch4")
with c2: st.markdown("<p style='text-align:center;font-size:1.5em;padding-top:28px'>+</p>", unsafe_allow_html=True)
with c3: mo2_c  = st.number_input("O₂ ",  min_value=1, max_value=20, value=1, step=1, key="mo2")
with c4: st.markdown("<p style='text-align:center;font-size:1.5em;padding-top:28px'>→</p>", unsafe_allow_html=True)
with c5: co2_c  = st.number_input("CO₂",  min_value=1, max_value=20, value=1, step=1, key="co2")
with c6: st.markdown("<p style='text-align:center;font-size:1.5em;padding-top:28px'>+</p>", unsafe_allow_html=True)
with c7: mh2o_c = st.number_input("H₂O ", min_value=1, max_value=20, value=1, step=1, key="mh2o")

c_r2, c_p2 = ch4_c,     co2_c
h_r2, h_p2 = ch4_c * 4, mh2o_c * 2
o_r2        = mo2_c * 2
o_p2        = co2_c * 2 + mh2o_c
q2_correct  = (c_r2 == c_p2) and (h_r2 == h_p2) and (o_r2 == o_p2)

cc2 = "ok" if c_r2 == c_p2 else "bad"
hc2 = "ok" if h_r2 == h_p2 else "bad"
oc2 = "ok" if o_r2 == o_p2 else "bad"
st.markdown(f"""
<table class="bal-tbl">
  <tr><th>Element</th><th>Reactant Side</th><th>Product Side</th><th>Status</th></tr>
  <tr><td>C</td><td>{c_r2}</td><td>{c_p2}</td>
      <td class="{cc2}">{"✔ Balanced" if cc2=="ok" else "✘ Off"}</td></tr>
  <tr><td>H</td><td>{h_r2}</td><td>{h_p2}</td>
      <td class="{hc2}">{"✔ Balanced" if hc2=="ok" else "✘ Off"}</td></tr>
  <tr><td>O</td><td>{o_r2}</td><td>{o_p2}</td>
      <td class="{oc2}">{"✔ Balanced" if oc2=="ok" else "✘ Off"}</td></tr>
</table>""", unsafe_allow_html=True)

if q2_correct:
    st.success("✅ Perfectly balanced! **CH₄ + 2O₂ → CO₂ + 2H₂O**")

st.divider()

# ── Q3 ──────────────────────────────────────────────────────────────────────
st.markdown("#### Question 3 — Identify the Reaction Type")
st.write("For each equation, select the correct reaction type from the dropdown.")

RXNTYPES = ["Select…", "Synthesis", "Decomposition",
            "Single Replacement", "Double Replacement", "Combustion"]

q3a = st.selectbox(
    "**Na₂SO₄(aq) + SrCl₂(aq) → 2NaCl(aq) + SrSO₄(s)**",
    RXNTYPES, key="q3a"
)
q3a_correct = q3a == "Double Replacement"
if q3a == "Double Replacement":
    st.success("Correct! Na⁺ and Sr²⁺ swap partners (NO₃⁻ ↔ SO₄²⁻) — that's the hallmark of double replacement.")
elif q3a != "Select…":
    st.warning("Not quite. Ask: what are the ions doing? Na⁺ and Sr²⁺ are switching anion partners.")

q3b = st.selectbox(
    "**2H₂O(l) → 2H₂(g) + O₂(g)**",
    RXNTYPES, key="q3b"
)
q3b_correct = q3b == "Decomposition"
if q3b == "Decomposition":
    st.success("Correct! One reactant breaking into simpler products — classic decomposition.")
elif q3b != "Select…":
    st.warning("Consider: how many reactants are there? A single compound splitting apart is always decomposition.")

q3_correct = q3a_correct and q3b_correct

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
        "q": "4. What type of reaction is:  Zn(s) + 2HCl(aq) → ZnCl₂(aq) + H₂(g) ?",
        "options": ["Synthesis", "Decomposition", "Single Replacement", "Double Replacement"],
        "a": "Single Replacement",
        "f": "Zinc (an uncombined element) displaces hydrogen from HCl. One element is alone on each side — that's single replacement.",
    },
    {
        "q": "5. What are the correct coefficients for:  __ Zn + __ HCl → __ ZnCl₂ + __ H₂ ?",
        "options": ["1, 2, 1, 1", "1, 1, 1, 1", "2, 2, 1, 1", "1, 2, 2, 1"],
        "a": "1, 2, 1, 1",
        "f": "Zn²⁺ needs 2 Cl⁻ → 2 HCl. Those 2 H atoms form H₂. Coefficients: 1 Zn, 2 HCl, 1 ZnCl₂, 1 H₂.",
    },
    {
        "q": "6. What type of reaction is:  S₈(s) + 24F₂(g) → 8SF₆(g) ?",
        "options": ["Synthesis", "Decomposition", "Combustion", "Single Replacement"],
        "a": "Synthesis",
        "f": "Two elemental reactants (S₈ and F₂) combine into a single product (SF₆). Multiple inputs → one output = synthesis.",
    },
    {
        "q": "7. What are the correct coefficients for:  __ S₈ + __ F₂ → __ SF₆ ?",
        "options": ["1, 24, 8", "1, 8, 8", "8, 1, 8", "1, 12, 4"],
        "a": "1, 24, 8",
        "f": "1 S₈ = 8 S atoms → 8 SF₆. Each SF₆ needs 6 F atoms: 8 × 6 = 48 F atoms → 24 F₂ molecules.",
    },
    {
        "q": "8. What type of reaction is:  4Fe(s) + 3O₂(g) → 2Fe₂O₃(s) ?",
        "options": ["Synthesis", "Decomposition", "Single Replacement", "Combustion"],
        "a": "Synthesis",
        "f": "Iron and oxygen (two simple elements) combine to form iron oxide (rust), a single more complex product.",
    },
    {
        "q": "9. What are the correct coefficients for:  __ Fe + __ O₂ → __ Fe₂O₃ ?",
        "options": ["4, 3, 2", "2, 3, 1", "4, 2, 3", "3, 4, 2"],
        "a": "4, 3, 2",
        "f": "2 Fe₂O₃ requires 4 Fe and 6 O atoms. Supply 6 O with 3 O₂. Check: 4 Fe = 4 Fe ✔, 6 O = 6 O ✔.",
    },
    {
        "q": "10. What type of reaction is:  C₄H₁₀(g) + O₂(g) → CO₂(g) + H₂O(g) ?",
        "options": ["Synthesis", "Double Replacement", "Combustion", "Decomposition"],
        "a": "Combustion",
        "f": "Hydrocarbon (C₄H₁₀) + O₂ → CO₂ + H₂O. That pattern is unmistakably combustion.",
    },
    {
        "q": "11. What are the correct coefficients for:  __ C₄H₁₀ + __ O₂ → __ CO₂ + __ H₂O ?",
        "options": ["2, 13, 8, 10", "1, 6.5, 4, 5", "2, 10, 8, 10", "1, 13, 4, 5"],
        "a": "2, 13, 8, 10",
        "f": "1 C₄H₁₀ gives 6.5 O₂ (a fraction). Multiply everything by 2: 2 C₄H₁₀ + 13 O₂ → 8 CO₂ + 10 H₂O.",
    },
    {
        "q": "12. What type of reaction is:  2MgO(s) → 2Mg(s) + O₂(g) ?",
        "options": ["Synthesis", "Decomposition", "Single Replacement", "Combustion"],
        "a": "Decomposition",
        "f": "MgO (one compound) breaks into Mg and O₂ (simpler substances). One reactant breaking down = decomposition.",
    },
    {
        "q": "13. What are the correct coefficients for:  __ MgO → __ Mg + __ O₂ ?",
        "options": ["2, 2, 1", "1, 1, 1", "2, 1, 2", "4, 4, 2"],
        "a": "2, 2, 1",
        "f": "O₂ needs 2 O atoms, so use 2 MgO. That also gives 2 Mg on each side. Check: 2 Mg = 2 Mg ✔, 2 O = 2 O ✔.",
    },
    {
        "q": "14. Predict the products of:  Fe(s) + HCl(aq) → _____  (Fe forms a +3 ion)",
        "options": ["FeCl + H", "FeCl₃ + H₂", "Fe₃Cl + H", "FeCl₂ + H₂"],
        "a": "FeCl₃ + H₂",
        "f": "Fe³⁺ requires 3 Cl⁻ to balance charge → FeCl₃. Released hydrogen is always diatomic → H₂.",
    },
    {
        "q": "15. Predict the products of:  Ca(OH)₂(aq) + HCl(aq) → _____",
        "options": ["CaCl₂ + H₂O", "CaH + ClOH", "CaCl + H₂O", "CaO + HCl"],
        "a": "CaCl₂ + H₂O",
        "f": "Acid-base neutralization (double replacement): Ca²⁺ + 2Cl⁻ → CaCl₂; OH⁻ + H⁺ → H₂O.",
    },
    {
        "q": "16. What are the correct coefficients for:  __ Ca(OH)₂ + __ HCl → __ CaCl₂ + __ H₂O ?",
        "options": ["1, 2, 1, 2", "1, 1, 1, 1", "2, 1, 2, 1", "1, 2, 2, 1"],
        "a": "1, 2, 1, 2",
        "f": "Ca(OH)₂ has 2 OH groups, each reacting with one HCl → 2 HCl needed, 2 H₂O formed. Ca + 2Cl → CaCl₂.",
    },
    {
        "q": "17. What type of reaction is:  2NaI(aq) + Br₂(l) → 2NaBr(aq) + I₂(s) ?",
        "options": ["Synthesis", "Single Replacement", "Double Replacement", "Decomposition"],
        "a": "Single Replacement",
        "f": "Br₂ (uncombined) displaces I⁻ from NaI; I₂ is released alone. One element switching partners = single replacement.",
    },
    {
        "q": "18. What are the correct coefficients for:  __ NaI + __ Br₂ → __ NaBr + __ I₂ ?",
        "options": ["2, 1, 2, 1", "1, 2, 1, 2", "1, 1, 1, 1", "2, 2, 2, 1"],
        "a": "2, 1, 2, 1",
        "f": "I₂ needs 2 I atoms → 2 NaI. That gives 2 Na → 2 NaBr. Br₂ provides 2 Br for 2 NaBr. ✔",
    },
    {
        "q": "19. What type of reaction is:  Pb(NO₃)₂(aq) + CuSO₄(aq) → PbSO₄(s) + Cu(NO₃)₂(aq) ?",
        "options": ["Synthesis", "Single Replacement", "Double Replacement", "Combustion"],
        "a": "Double Replacement",
        "f": "Pb²⁺ and Cu²⁺ swap their anion partners (NO₃⁻ and SO₄²⁻). Two ionic compounds exchanging = double replacement.",
    },
    {
        "q": "20. What are the correct coefficients for:  __ Pb(NO₃)₂ + __ CuSO₄ → __ PbSO₄ + __ Cu(NO₃)₂ ?",
        "options": ["1, 1, 1, 1", "2, 1, 2, 1", "1, 2, 1, 2", "2, 2, 2, 2"],
        "a": "1, 1, 1, 1",
        "f": "Both Pb²⁺ and Cu²⁺ are +2 ions, so the charge ratio is 1:1 throughout. This equation is already balanced!",
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
            st.markdown('<div class="fb-ok">✅ <b>Q1 — Formation of Water:</b> Correct!  2H₂ + O₂ → 2H₂O</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ <b>Q1 — Formation of Water:</b> Not balanced. Correct answer: <b>2H₂ + O₂ → 2H₂O</b></div>', unsafe_allow_html=True)

        if q2_correct:
            st.markdown('<div class="fb-ok">✅ <b>Q2 — Combustion of Methane:</b> Correct!  CH₄ + 2O₂ → CO₂ + 2H₂O</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ <b>Q2 — Combustion of Methane:</b> Not balanced. Correct answer: <b>CH₄ + 2O₂ → CO₂ + 2H₂O</b></div>', unsafe_allow_html=True)

        if q3_correct:
            st.markdown('<div class="fb-ok">✅ <b>Q3 — Reaction Types:</b> Both correct!</div>', unsafe_allow_html=True)
        else:
            wrong = []
            if not q3a_correct: wrong.append("Na₂SO₄ + SrCl₂ → Double Replacement")
            if not q3b_correct: wrong.append("2H₂O → Decomposition")
            st.markdown(f'<div class="fb-bad">❌ <b>Q3 — Reaction Types:</b> Missed: {", ".join(wrong)}</div>', unsafe_allow_html=True)

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

        if   pct >= 90: st.success("🏆 Outstanding! You have mastered balancing equations.")
        elif pct >= 80: st.success("🎯 Great work! Review any missed questions before the exam.")
        elif pct >= 70: st.warning("📚 Solid effort. Go back over the reaction types you missed.")
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
            file_name=f"{student_name.replace(' ', '_')}_Module1_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
