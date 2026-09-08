import random
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass
from helper import create_plot, get_filepath
from sim_parameters import TRANSITION_PROBS, HOLDING_TIMES
SIM_TIMESERIES_CSV = 'a2-covid-simulated-timeseries.csv'
SUMMARY_TIMESERIES_CSV = 'a2-covid-summary-timeseries.csv'
AGE_GROUPS = ['less_5','5_to_14','15_to_24','25_to_64','over_65']
@dataclass
class Person:
    person_id: int
    country: str
    age_group: str
    state: str = 'H'
    staying_days: int = 0
def daterange(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d").date()
    end_date = datetime.strptime(end, "%Y-%m-%d").date()
    return [(start_date + timedelta(days=i)).isoformat() for i in range((end_date - start_date).days + 1)]
def next_state(age_group, current_state):
    probabilities = TRANSITION_PROBS[age_group][current_state]
    random_val, cumulative = random.random(), 0
    for state, prob in probabilities.items():
        cumulative += prob
        if random_val <= cumulative:
            return state
    return state
def allocate_samples(row, ratio):
    total_samples = int(row['population'] // ratio)
    if total_samples <= 0:
        return {group: 0 for group in AGE_GROUPS}
    allocation = {group: round(total_samples * float(row[group]) / 100) for group in AGE_GROUPS}
    difference = total_samples - sum(allocation.values())
    if difference:
        for group in sorted(AGE_GROUPS, key=lambda k: row[k] % 1, reverse=difference > 0):
            if not difference: break
            allocation[group] += 1 if difference > 0 else -1
            difference += -1 if difference > 0 else 1
    return allocation
def create_population(df, selected_countries, ratio):
    people, pid = [], 0
    for _, row in df[df['country'].isin(selected_countries)].iterrows():
        for group, count in allocate_samples(row, ratio).items():
            for _ in range(count):
                people.append(Person(pid, row['country'], group))
                pid += 1
    return people
def simulate(people, dates):
    records = []
    for person in people:
        state, days = 'H', 0
        for date in dates:
            records.append((person.person_id, person.age_group, person.country, date, state, days, state))
            days += 1
            if days >= max(1, HOLDING_TIMES[person.age_group][state]):
                state, days = next_state(person.age_group, state), 0
    return pd.DataFrame(records, columns=['person_id','age_group_name','country','date','state','staying_days','prev_state'])
def summarize(df):
    grouped = df.groupby(['date','country','state']).size().unstack(fill_value=0)
    for col in ['D','H','I','M','S']:
        if col not in grouped.columns:
            grouped[col] = 0
    return grouped.reset_index()[['date','country','D','H','I','M','S']]
def run(countries_csv_name, countries, sample_ratio, start_date, end_date):
    data = pd.read_csv(get_filepath(countries_csv_name))
    data['country'] = data['country'].astype(str)
    if not countries:
        countries = data.nlargest(3, 'population')['country'].tolist()
    people = create_population(data, countries, sample_ratio)
    dates = daterange(start_date, end_date)
    sim_df = simulate(people, dates) if people else pd.DataFrame(columns=['person_id','age_group_name','country','date','state','staying_days','prev_state'])
    sim_df.to_csv(get_filepath(SIM_TIMESERIES_CSV), index=False)
    summary = summarize(sim_df) if not sim_df.empty else pd.DataFrame(columns=['date','country','D','H','I','M','S'])
    all_pairs = pd.MultiIndex.from_product([dates, countries], names=['date','country']).to_frame(index=False)
    summary = all_pairs.merge(summary, on=['date','country'], how='left').fillna(0)
    summary[['D','H','I','M','S']] = summary[['D','H','I','M','S']].astype(int)
    summary.to_csv(get_filepath(SUMMARY_TIMESERIES_CSV), index=False)
    create_plot(summary_csv=SUMMARY_TIMESERIES_CSV, countries=countries)
    return {'sim_csv': get_filepath(SIM_TIMESERIES_CSV), 'summary_csv': get_filepath(SUMMARY_TIMESERIES_CSV), 'plot_png': get_filepath('a2-covid-simulation.png')}
if __name__ == "__main__":
    print("Run this module via Streamlit app or test.py")
