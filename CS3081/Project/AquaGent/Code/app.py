
"""AquaGent - Bayesian Uncertainty + CSP"""

import csv
import io
from datetime import datetime

import streamlit as st

from src.decision import evaluate
from src.model import DURATIONS, Inputs, MATERIALS

st.set_page_config(
    page_title="AquaGent | Water Harvesting AI",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BAYES = {
    "prior_fog": 0.35,
    "sensor_sensitivity": 0.90,
    "sensor_specificity": 0.90,
    "min_fog_confidence": 0.75,
}

# --------------------------------------------------
# DESIGN - LIGHT THEME
# --------------------------------------------------

st.markdown("""
<style>
:root {
    color-scheme: light !important;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #f7fafc !important;
    color: #344054 !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        150deg,#f4fbfa,#f7f9fc 65%,#f6fafb
    ) !important;
}

.block-container {
    max-width: 1230px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}

/* Text visibility */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] *,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] strong,
label, label *, p, h1, h2, h3, h4 {
    color: #344054 !important;
}

h1, h2, h3 {
    letter-spacing: -.025em;
}

/* Main form */
[data-testid="stForm"] {
    background: #ffffff !important;
    padding: 1.3rem;
    border: 1px solid #dcebea;
    border-radius: 20px;
    box-shadow: 0 8px 28px #0d33400a;
}

/* Inputs */
input, textarea,
[data-baseweb="select"] > div,
[data-baseweb="input"] > div,
[data-testid="stNumberInput"] button {
    background-color: #f0f2f6 !important;
    color: #344054 !important;
    border-color: #e3e7ee !important;
}

[data-baseweb="select"] *,
[data-baseweb="input"] *,
[data-testid="stNumberInput"] *,
[data-testid="stSlider"] *,
[data-testid="stCheckbox"] *,
[data-testid="stRadio"] * {
    color: #344054 !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #dce8e9;
    border-radius: 16px;
    padding: 15px 18px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"] {
    color: #174553 !important;
}

[data-testid="stMetricValue"] {
    font-weight: 750;
}

/* Buttons */
.stButton button[kind="primary"],
[data-testid="stFormSubmitButton"] button[kind="primary"] {
    background: #e85b55 !important;
    border-color: #e85b55 !important;
    color: #ffffff !important;
    border-radius: 12px;
    font-weight: 700;
    min-height: 3rem;
}

.stButton button,
[data-testid="stDownloadButton"] button {
    border-radius: 12px;
}

.stButton button *,
[data-testid="stDownloadButton"] button * {
    color: inherit !important;
}

/* Hero */
.ag-hero {
    background: linear-gradient(
        115deg,#153342,#16646b 70%,#139f98
    );
    border-radius: 23px;
    padding: 30px 36px;
    color: white !important;
    margin-bottom: 24px;
    box-shadow: 0 16px 30px #0e57651c;
}

.ag-hero h1 {
    color: white !important;
    font-size: 2.55rem;
    margin: 0 0 8px;
}

.ag-hero p {
    color: #d6f3ef !important;
    margin: 0;
}

.ag-tags {
    display: flex;
    gap: 9px;
    flex-wrap: wrap;
    margin-top: 19px;
}

.ag-tags span {
    color: #ffffff !important;
    background: #ffffff20;
    border: 1px solid #ffffff30;
    border-radius: 20px;
    padding: 6px 12px;
    font-size: .8rem;
}

/* Sections */
.ag-section {
    font-weight: 750;
    font-size: 1.28rem;
    color: #173744 !important;
    margin: 27px 0 12px;
}

.ag-section span {
    display: inline-block;
    background: #dff2ef;
    padding: 8px 11px;
    border-radius: 10px;
    color: #087f79 !important;
    font-size: .82rem;
    margin-right: 10px;
}

/* Recommendation */
.ag-choice {
    background: #e6f5f2;
    border-left: 5px solid #11988e;
    border-radius: 13px;
    padding: 16px 20px;
    color: #134a46 !important;
    font-weight: 750;
    font-size: 1.1rem;
}

.small-note {
    color: #648087 !important;
    font-size: .82rem;
}

[data-testid="stDataFrame"] {
    background: #ffffff !important;
}

[data-testid="stExpander"] {
    border-color: #dce4e8 !important;
}

@media(max-width:700px) {
    .ag-hero {
        padding: 22px;
    }

    .ag-hero h1 {
        font-size: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "runs": [],
    "result": None,
    "run_index": None,
    "approval": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def heading(number, title):
    st.markdown(
        f'<div class="ag-section">'
        f'<span>{number}</span>{title}</div>',
        unsafe_allow_html=True
    )


def decide(value):
    index = st.session_state.run_index

    if index is not None and 0 <= index < len(st.session_state.runs):
        run = st.session_state.runs[index]

        if run["status"] == "SUCCESS":
            run["operator_decision"] = value
            st.session_state.approval = value


# HERO SECTION

st.markdown(
    """
    <div class="ag-hero">
        <h1>💧 AquaGent</h1>
        <p>
            Intelligent atmospheric water-harvesting
            decision support system.
        </p>
        <div class="ag-tags">
            <span>Bayesian Uncertainty</span>
            <span>Constraint Satisfaction (CSP)</span>
            <span>Raschel Mesh</span>
            <span>MOF-303</span>
            <span>Operator Review</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# ENVIRONMENT AND COLLECTOR INPUTS
# --------------------------------------------------

heading("01", "Environment & collector inputs")

with st.form("conditions"):

    weather, sensor, limits = st.columns(3, gap="large")

    with weather:
        st.markdown("**🌦️ Weather**")

        humidity = st.slider(
            "Relative humidity (%)",
            0, 100, 85
        )

        temperature = st.slider(
            "Temperature (°C)",
            -10, 55, 25
        )

        wind = st.slider(
            "Wind speed (m/s)",
            0.0, 15.0, 3.0, 0.5
        )

    with sensor:
        st.markdown("**📡 Sensors & safety**")

        fog = st.selectbox(
            "Fog sensor reading",
            ["Detected", "Not detected", "Missing"]
        )

        missing_humidity = st.checkbox(
            "Humidity sensor missing"
        )

        missing_temp = st.checkbox(
            "Temperature sensor missing"
        )

        safety = st.checkbox(
            "Plant safety checks passed",
            value=True
        )

    with limits:
        st.markdown("**⚡ Operating limits**")

        energy = st.number_input(
            "Available energy (demo kWh)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.5
        )

        hours = st.selectbox(
            "Maximum duration (hours)",
            list(DURATIONS),
            index=2
        )

    st.divider()

    st.markdown("**🔬 Collector specifications**")

    a, b, c, d = st.columns(4)

    with a:
        mesh_area = st.number_input(
            "Mesh area (m²)",
            min_value=0.1,
            value=2.0,
            step=0.5
        )

    with b:
        efficiency = st.number_input(
            "Mesh efficiency (0–1)",
            min_value=0.0,
            max_value=1.0,
            value=0.30,
            step=0.05
        )

    with c:
        lwc = st.number_input(
            "Fog LWC (g/m³)",
            min_value=0.0,
            value=0.20,
            step=0.05,
            help="Assumed liquid-water content of fog."
        )

    with d:
        mof_mass = st.number_input(
            "MOF-303 mass (kg)",
            min_value=0.1,
            value=1.0,
            step=0.5
        )

    submitted = st.form_submit_button(
        "✦ Analyze & recommend plan",
        type="primary",
        use_container_width=True
    )


# --------------------------------------------------
# RUN AI AGENT
# --------------------------------------------------

if submitted:

    reading = {
        "Detected": True,
        "Not detected": False,
        "Missing": None
    }[fog]

    data = Inputs(
        humidity=None if missing_humidity else humidity,
        temperature_c=None if missing_temp else temperature,
        fog_observed=reading,
        energy_budget_kwh=energy,
        max_hours=hours,
        safety_ok=safety,
        wind_m_s=wind,
        mesh_area_m2=mesh_area,
        mesh_efficiency=efficiency,
        fog_lwc_g_m3=lwc,
        mof_mass_kg=mof_mass,
        **BAYES
    )

    result = evaluate(data)

    st.session_state.result = result
    st.session_state.approval = None

    best = result.get("recommended") or {}

    run_no = len(st.session_state.runs) + 1

    st.session_state.runs.append({
        "run": run_no,
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "status": result["status"],
        "fog_probability": result["fog_probability"],
        "method": best.get("method", ""),
        "hours": best.get("hours", ""),
        "water_l_demo": best.get(
            "water_liters_demo", ""
        ),
        "energy_kwh_demo": best.get(
            "energy_kwh_demo", ""
        ),
        "operator_decision": (
            "PENDING"
            if result["status"] == "SUCCESS"
            else "N/A"
        ),
        "explanation": result.get("explanation", ""),
        "warnings": "; ".join(
            result.get("warnings", [])
        ),
        "excluded": "; ".join(
            f"{method}: {', '.join(reasons)}"
            for method, reasons
            in result.get("excluded", {}).items()
        ),
        "mesh_area_m2": mesh_area,
        "mesh_efficiency": efficiency,
        "fog_lwc_g_m3": lwc,
        "mof_mass_kg": mof_mass,
    })

    st.session_state.run_index = (
        len(st.session_state.runs) - 1
    )


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

result = st.session_state.result

if result is not None:

    heading("02", "Bayesian uncertainty analysis")

    probability = result.get("fog_probability")

    if probability is None:
        st.error(
            "Required input values are invalid or missing."
        )

    else:
        m, bar = st.columns([1, 2])

        with m:
            st.metric(
                "Estimated probability of fog",
                f"{probability * 100:.1f}%"
            )

        with bar:
            st.markdown("**Bayesian posterior**")
            st.progress(float(probability))

            st.caption(
                "Estimated from the fog sensor and "
                "fixed simulation assumptions."
            )

    for warning in result.get("warnings", []):
        st.warning(warning)

    heading("03", "AI recommendation & plan comparison")

    if result["status"] != "SUCCESS":

        if result["status"] == "SENSOR_WARNING":
            st.error(result["explanation"])
        else:
            st.warning(result["explanation"])

    else:

        best = result["recommended"]

        material = MATERIALS.get(
            best["method"], ""
        )

        st.markdown(
            f'<div class="ag-choice">'
            f'✓ {best["method"]} · {best["hours"]} hour(s)'
            f'<div class="small-note">{material}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        w, e, s = st.columns(3)

        w.metric(
            "Estimated water · demo",
            f'{best["water_liters_demo"]:.3f} L'
        )

        e.metric(
            "Energy · demo",
            f'{best["energy_kwh_demo"]:.2f} kWh'
        )

        s.metric(
            "Decision score · demo",
            f'{best["score_demo"]:.3f}'
        )

        st.write(
            "**Decision explanation:**",
            result["explanation"]
        )

        with st.expander(
            "Compare feasible CSP plans",
            expanded=True
        ):

            candidates = result.get("candidates", [])

            st.dataframe(
                candidates,
                hide_index=True,
                use_container_width=True
            )

            if candidates:

                chart = [
                    {
                        "Plan": f'{item["method"]} · {item["hours"]}h',
                        "Water (demo L)": item["water_liters_demo"]
                    }
                    for item in candidates
                ]

                st.bar_chart(
                    chart,
                    x="Plan",
                    y="Water (demo L)",
                    color="#078780"
                )

    if result.get("excluded"):

        with st.expander(
            "Why were methods excluded?",
            expanded=True
        ):

            for method, reasons in result["excluded"].items():
                st.warning(
                    f'{method}: '
                    f'{", ".join(reasons) or "No feasible assignment"}'
                )


    # --------------------------------------------------
    # OPERATOR REVIEW - FIXED
    # --------------------------------------------------

    heading("04", "Operator review")

    if result["status"] == "SUCCESS":

        yes, no = st.columns(2)

        with yes:
            if st.button(
                "✓ Approve recommendation",
                type="primary",
                use_container_width=True
            ):
                decide("APPROVED")
                st.rerun()

        with no:
            if st.button(
                "✕ Reject recommendation",
                use_container_width=True
            ):
                decide("REJECTED")
                st.rerun()

        if st.session_state.approval == "APPROVED":
            st.success("Operator decision: APPROVED")

        elif st.session_state.approval == "REJECTED":
            st.warning("Operator decision: REJECTED")

        else:
            st.info("Awaiting operator decision.")

    else:
        st.info(
            "No plan available for operator approval."
        )


# --------------------------------------------------
# PLANT DASHBOARD AND RUN HISTORY
# --------------------------------------------------

heading("05", "Plant dashboard & run history")

rows = st.session_state.runs

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total runs", len(rows))

m2.metric(
    "Recommended",
    sum(r["status"] == "SUCCESS" for r in rows)
)

m3.metric(
    "Sensor warnings",
    sum(r["status"] == "SENSOR_WARNING" for r in rows)
)

m4.metric(
    "No feasible plans",
    sum(r["status"] == "NO_FEASIBLE_METHOD" for r in rows)
)

if rows:

    display = []

    for r in reversed(rows):

        p = r["fog_probability"]

        display.append({
            "Run": r["run"],
            "Time": r["timestamp"],
            "Status": r["status"],
            "Fog probability": (
                f"{p * 100:.2f}%"
                if p is not None
                else "—"
            ),
            "Method": r["method"] or "—",
            "Hours": r["hours"] or "—",
            "Demo water (L)": r["water_l_demo"],
            "Demo energy (kWh)": r["energy_kwh_demo"],
            "Operator decision": r["operator_decision"]
        })

    st.dataframe(
        display,
        hide_index=True,
        use_container_width=True
    )

    with st.expander("Inspect run details"):

        number = st.selectbox(
            "Run number",
            [r["run"] for r in reversed(rows)]
        )

        chosen = next(
            r for r in rows
            if r["run"] == number
        )

        st.write(
            "**Explanation:**",
            chosen["explanation"]
        )

        st.write(
            "**Operator decision:**",
            chosen["operator_decision"]
        )

        if chosen["warnings"]:
            st.warning(chosen["warnings"])

        if chosen["excluded"]:
            st.info(chosen["excluded"])

    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=list(rows[0].keys())
    )

    writer.writeheader()
    writer.writerows(rows)

    left, right = st.columns(2)

    with left:
        st.download_button(
            "↓ Download history (CSV)",
            output.getvalue().encode("utf-8-sig"),
            file_name="aquagent_run_history.csv",
            mime="text/csv",
            use_container_width=True
        )

    with right:
        if st.button(
            "⌫ Clear run history",
            use_container_width=True
        ):
            st.session_state.runs = []
            st.session_state.result = None
            st.session_state.run_index = None
            st.session_state.approval = None
            st.rerun()

else:
    st.caption(
        "No experiments recorded yet. "
        "Run the AI agent to see results here."
    )


# --------------------------------------------------
# RESEARCH ASSUMPTIONS
# --------------------------------------------------

with st.expander("Research assumptions & model limitations"):

    st.caption(
        "This is a course simulation, not an operational control system. "
        "Fog LWC, mesh efficiency, sensor reliability, energy rates and "
        "operating thresholds are assumptions. MOF-303 yield is scaled "
        "from a published daily result; partial-cycle yield is not "
        "physically validated for Jeddah. Approval does not operate equipment."
    )
