
import streamlit as st

from src.decision import safe_recommend_method

st.set_page_config(
    page_title="Water Harvesting AI",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Water Harvesting AI")
st.subheader("Intelligent Water Collection Decision Support")

st.info(
    "Educational simulation using Rule-Based Logic, CSP, "
    "and experimental decision optimization. "
    "Water and energy estimates are not validated physical measurements."
)

st.divider()

# Input Section
st.header("🌤️ Weather & Sensor Inputs")

col1, col2 = st.columns(2)

with col1:
    humidity = st.slider(
        "Humidity (%)",
        min_value=0,
        max_value=100,
        value=85
    )

    fog_option = st.selectbox(
        "Fog Condition",
        ["Detected", "Not Detected", "Missing Reading"]
    )

with col2:
    energy = st.slider(
        "Available Energy (simulation units)",
        min_value=0,
        max_value=100,
        value=30
    )

    missing_humidity = st.checkbox(
        "Simulate Missing Humidity Reading"
    )

    invalid_humidity = st.checkbox(
        "Simulate Invalid Humidity Reading"
    )

# Convert inputs
if missing_humidity:
    humidity_value = None
elif invalid_humidity:
    humidity_value = 120
else:
    humidity_value = humidity

if fog_option == "Detected":
    fog_value = True
elif fog_option == "Not Detected":
    fog_value = False
else:
    fog_value = None

st.divider()

# AI Decision
if st.button("🧠 Run AI Agent", type="primary"):

    result = safe_recommend_method(
        humidity_value,
        fog_value,
        energy
    )

    st.header("AI Agent Results")

    status = result["status"]

    if status == "SENSOR_WARNING":
        st.error("Sensor Warning: Invalid or missing data")

        for warning in result["warnings"]:
            st.warning(warning)

    elif status == "NO_FEASIBLE_METHOD":
        st.warning(
            "No harvesting method satisfies the current constraints."
        )

    else:
        st.success(
            f"Recommended Method: {result['recommended']}"
        )

        st.write("**Decision Explanation:**")
        st.write(result["reason"])

        st.subheader("Available Methods Comparison")

        options = result["options"]
        
        all_methods = ["Fog Collector", "Special Material"]

        available = [
            item["method"] for item in options
        ]

        excluded = [
            method for method in all_methods
            if method not in available
        ]

        
        if excluded:
            from src.csp import explain_constraints

            st.subheader("Constraint Explanation")

            for method in excluded:
                reasons = explain_constraints(
                    method,
                    humidity_value,
                    fog_value,
                    energy
                )

                st.warning(
                    f"{method}: " + ", ".join(reasons)
                )



        st.dataframe(
            options,
            use_container_width=True,
            hide_index=True
        )

        chart_data = {
            item["method"]: item["water_liters"]
            for item in options
        }

        st.subheader("Estimated Water Yield Comparison")
        st.bar_chart(chart_data, y_label="Demo water units (L)")

    st.caption(
        "Final operational decisions require human review "
        "and scientifically validated equipment models."
    )

st.divider()

st.caption(
    "CS3081 Artificial Intelligence | Water Harvesting AI Project"
)
