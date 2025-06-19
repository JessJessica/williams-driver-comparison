import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import fastf1


fastf1.Cache.enable_cache('cache')

races = [('Australia', 1), 
         ('China', 2), 
         ('Japan', 3), 
         ('Bahrain', 4),
         ('Saudi Arabia', 5),
         ('USA', 6), 
         ('Italy', 7), 
         ('Monaco', 8), 
         ('Spain', 9), 
         ('Canada', 10)]


@st.cache_data(show_spinner= True)
def load_results(year, race_number):
    try:
        race_session = fastf1.get_session(2025, race_number, 'R')
        race_session.load()
        race_results = race_session.results
    except:
        race_results = None

    try:
        quali_session = fastf1.get_session(2025, race_number, 'Q')
        quali_session.load()
        quali_results = quali_session.results
    except:
        quali_results = None

    return race_results, quali_results

def get_position(results, driver_initials):
    if results is None:
        return None
    position = results[results['Abbreviation'] == driver_initials]['Position']
    return int(position.values[0]) if not position.empty else None

    

        

alex_results = []
carlos_results = []
alex_qualifying = []
carlos_qualifying = []
race_names = []



for race_name, race_number in races:
    race_results, quali_results = load_results(2025, race_number)

    alex_results.append(get_position(race_results, 'ALB'))
    carlos_results.append(get_position(race_results, 'SAI'))

    alex_qualifying.append(get_position(quali_results, 'ALB'))
    carlos_qualifying.append(get_position(quali_results, 'SAI'))

    race_names.append(race_name)

# for race_name, round_number in races:
#     try:
#         race_session = fastf1.get_session(2025, round_number, 'R')
#         race_session.load()
#         race_results = race_session.results

#         alex_results.append(race_results[race_results['Abbreviation'] == 'ALB']['Position'].values[0])
#         carlos_results.append(race_results[race_results['Abbreviation'] == 'SAI']['Position'].values[0])

#     except:
#         alex_results.append(None)
#         carlos_results.append(None)

#     try:
#         quali_session = fastf1.get_session(2025, round_number, 'Q')
#         quali_session.load()
#         quali_results = quali_session.results

#         alex_qualifying.append(quali_results[quali_results['Abbreviation'] == 'ALB']['Position'].values[0])
#         carlos_qualifying.append(quali_results[quali_results['Abbreviation'] == 'SAI']['Position'].values[0])

#     except:
#         alex_qualifying.append(None)
#         carlos_qualifying.append(None)

#     race_names.append(race_name)

results_dataframe = pd.DataFrame({
    'Race': race_names,
    'Alex': alex_results,
    'Carlos': carlos_results
})

qualifying_dataframe = pd.DataFrame({
    'Race': race_names,
    'Alex': alex_qualifying,
    'Carlos': carlos_qualifying
})


st.set_page_config(page_title="Williams Driver Comparisons", layout="wide")
st.title("Williams Driver Comparisons")
# st.write("Compare: ")

page = st.radio("Select Comparisons: ", ["Race Results", "Qualifying Positions"])

show_Alex = st.checkbox("Alex")
show_Carlos = st.checkbox("Carlos")

if page == "Race Results":
    st.header("Race Results Comparisons")
    df = results_dataframe
    title = "Race Results"

else:
    st.header("Qualifying Positions Comparisons")
    df = qualifying_dataframe
    title = "Qualifying Position"

fig, ax = plt.subplots()

if not show_Alex and not show_Carlos:
    st.write("Please select a driver to view data")
else:
    x = range(len(races))

    if show_Alex:
        ax.plot(x, df['Alex'], marker = 'o', linestyle = '-', color = 'royalblue', label = 'ALB')
    if show_Carlos:
        ax.plot(x, df['Carlos'], marker = 's', linestyle = '--', color = 'red', label = 'SAI')

    ax.set_xticks(x)
    ax.set_xticklabels(df['Race'], rotation = 45)
    ax.invert_yaxis()
    ax.set_ylabel("Results")
    ax.set_title(title)
    ax.legend()
    st.pyplot(fig)

