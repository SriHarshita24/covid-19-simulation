
# COVID-19 Simulation

A Python-based COVID-19 simulation project that models changes in population health states over time across selected countries and visualizes the resulting time-series data.

The project combines probabilistic state transitions, age-group-based parameters, population sampling, data processing, and visualization through a Streamlit interface.

## Overview

This project simulates the progression of population health states over a selected date range. Users can choose countries, configure the population sample ratio, select start and end dates, and run a simulation to generate CSV outputs and a visualization.

The simulation uses country-level population and age-group data along with transition probabilities and state holding-time parameters.

## Features

- Select countries for simulation
- Configure the population sample ratio
- Choose a simulation date range
- Model health-state transitions using probabilistic parameters
- Account for different age groups
- Generate detailed and summarized CSV time-series outputs
- Visualize simulation results using Matplotlib
- Interact with the simulation through a Streamlit interface

## Tech Stack

- **Python** — simulation logic and application code
- **Pandas** — population data processing and time-series aggregation
- **Matplotlib** — results visualization
- **Streamlit** — interactive user interface
- **CSV** — input data and generated simulation results

## How It Works

1. Load country-level population and age-group data.
2. Select the countries and simulation parameters.
3. Create a sampled population using the configured sample ratio.
4. Simulate health-state transitions over the selected dates using the configured probabilities and holding times.
5. Aggregate results by country, date, and state.
6. Export detailed and summarized CSV files.
7. Generate a chart showing the simulated results.

## Project Structure

```text
covid-19-simulation/
├── a2-countries.csv
├── assignment2.py
├── helper.py
├── sim_parameters.py
├── streamlit_ui.py
├── test.py
├── a2-covid-simulated-timeseries.csv
├── a2-covid-summary-timeseries.csv
├── a2-covid-simulation.png
└── README.md
```

The CSV output files and plot may be regenerated when the simulation runs.

## Getting Started

### Prerequisites

- Python 3
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/SriHarshita24/covid-19-simulation.git
cd covid-19-simulation
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install pandas matplotlib streamlit
```

### Run the Application

Start the Streamlit interface:

```bash
streamlit run streamlit_ui.py
```

Open the local URL displayed in your terminal.

### Run a Simulation

1. Choose one or more countries.
2. Set the sample ratio.
3. Select the start and end dates.
4. Click **Run Simulation**.
5. Review the generated chart and summarized CSV output.

## Outputs

The simulation generates:

- `a2-covid-simulated-timeseries.csv` — detailed records for simulated individuals over time
- `a2-covid-summary-timeseries.csv` — aggregated state counts by date and country
- `a2-covid-simulation.png` — visualization of the simulation results

## Configuration

Transition probabilities and holding-time parameters are defined in `sim_parameters.py`.

The simulation's results depend on the selected countries, population sample ratio, date range, and configured parameters.

## Limitations

- Results depend on the assumptions and parameters defined in the simulation.
- Probabilistic transitions can produce different outcomes across runs.
- A simulated population is not the same as a complete real-world population.
- The results should not be interpreted as validated epidemiological forecasts or medical advice.

## Future Improvements

- Add automated tests for simulation logic and parameter validation.
- Improve the visualization with clearer labels and a legend for each health state.
- Add reproducible runs using configurable random seeds.
- Improve input validation and error handling.
- Document the transition model and the sources of its parameters.

## Disclaimer

This is an educational simulation project. Its outputs are illustrative and should not be used to make public-health or medical decisions.
