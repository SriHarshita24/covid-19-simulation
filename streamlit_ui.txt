import pandas as pd
import streamlit as st
from pathlib import Path
import assignment2

A2_CSV = "a2-countries.csv"
PLOT_IMG = "a2-covid-simulation.png"

st.set_page_config(page_title="COVID-19 CTMC Simulation", layout="wide")
st.title("COVID-19 Simulation")

col1, col2, col3 = st.columns(3)
SAMPLE_RATIO = col1.number_input("Sample Ratio", 1.0, value=1_000_000.0, step=1000.0, format="%.0f")
START_DATE = col2.date_input("Start Date", pd.to_datetime("2021-04-01")).strftime("%Y-%m-%d")
END_DATE = col3.date_input("End Date", pd.to_datetime("2022-04-30")).strftime("%Y-%m-%d")

try:
    countries = pd.read_csv(Path(__file__).parent / A2_CSV)["country"].dropna().astype(str).tolist()
except Exception as e:
    st.error(f"Could not read {A2_CSV}: {e}")
    countries = []

selected = st.multiselect("Choose Countries", countries, default=[])

if st.button("Run Simulation"):
    if not selected:
        st.warning("Please select at least one country.")
    else:
        with st.spinner("Running simulation..."):
            result = assignment2.run(
                countries_csv_name=A2_CSV,
                countries=selected,
                sample_ratio=SAMPLE_RATIO,
                start_date=START_DATE,
                end_date=END_DATE
            )
        st.success("Simulation complete!")
        st.write(f"Results saved at: {result['summary_csv']}")

plot_file = Path(__file__).parent / PLOT_IMG
if plot_file.exists():
    st.image(str(plot_file), caption="COVID-19 Simulation Results", use_container_width=True)
else:
    st.info("Run a simulation to see the chart here.")
