#Python project making comparisons of Williams F1 drivers in the 2025 season
#Started 19/06/2025
#Author: Jessica Parkes



import streamlit as st #importing needed libraries
import pandas as pd
import matplotlib.pyplot as plt
import fastf1


fastf1.Cache.enable_cache('cache') #sets API data to be stored in 'cache'

races = [('Australia', 1), 
         ('China', 2), 
         ('Japan', 3), 
         ('Bahrain', 4),
         ('Saudi Arabia', 5),
         ('USA', 6), 
         ('Italy', 7), #races array with locations and race numbers
         ('Monaco', 8), 
         ('Spain', 9), 
         ('Canada', 10),
         ('Austria', 11),
         ('United Kingdom', 12),
         ('Belgium', 13),
         ('Hungary', 14),
         ('Netherlands', 15),
         ('Italy', 16),
         ('Azerbaijan', 17),
         ('Singapore', 18),
         ('USA', 19),
         ('Mexico', 20),
         ('Brazil', 21),
         ('USA', 22),
         ('Qatar', 23),
         ('Abu Dhabi', 24)
         ]


@st.cache_data(show_spinner= True) #tells streamlit to cache the output of the function and shows spinenr the first time it loads
def load_results(year, race_number): #function to load results from fastf1 and save in needed variables
    try:
        race_session = fastf1.get_session(2025, race_number, 'R')
        race_session.load(laps=True)
        race_results = race_session.results#gets results
        laps = race_session.laps
    except:
        race_results = None #sets results to none if race hasnt happened yet to avoid errors
        laps = None

    try:
        quali_session = fastf1.get_session(2025, race_number, 'Q')
        quali_session.load()
        quali_results = quali_session.results
    except:
        quali_results = None

    return race_results, quali_results, laps #returns results to be plotted

def get_position(results, driver_initials):
    if results is None:
        return None
    position = results[results['Abbreviation'] == driver_initials]['Position'] #filters results to get position of driver with correct initials
    return int(position.values[0]) if not position.empty else None #returns position as an integer

    

        

alex_results = []
carlos_results = []
alex_qualifying = [] #intiialises results arrays
carlos_qualifying = []
race_names = []
laps_list = []



for race_name, race_number in races:
    race_results, quali_results, laps = load_results(2025, race_number)

    alex_results.append(get_position(race_results, 'ALB'))#adds the correct data to corrects arrays
    carlos_results.append(get_position(race_results, 'SAI'))

    alex_qualifying.append(get_position(quali_results, 'ALB'))
    carlos_qualifying.append(get_position(quali_results, 'SAI'))

    laps_list.append(laps)
    race_names.append(race_name) #gets the race name to plot


results_dataframe = pd.DataFrame({#sets the data for if results is selected
    'Race': race_names,
    'Alex': alex_results,
    'Carlos': carlos_results
})

qualifying_dataframe = pd.DataFrame({#sets the data for if qualifying is selected
    'Race': race_names,
    'Alex': alex_qualifying,
    'Carlos': carlos_qualifying
})


st.set_page_config(page_title="Williams Driver Comparisons", layout="wide")
st.title("Williams Driver Comparisons") #setting up UI


page = st.radio("Select Comparisons: ", ["Race Results", "Qualifying Positions"])#radio button to choose filter

show_Alex = st.checkbox("Alex")
show_Carlos = st.checkbox("Carlos")

if page == "Race Results":#chooses the correct dataframes based on driver chosen
    st.header("Race Results Comparisons")
    df = results_dataframe
    title = "Race Results"

else:
    st.header("Qualifying Positions Comparisons")
    df = qualifying_dataframe
    title = "Qualifying Position"

fig, ax = plt.subplots()

if not show_Alex and not show_Carlos:#makes sure at least one driver is chosen
    st.write("Please select a driver to view data")
else:
    x = range(len(races))

    if show_Alex:#plots results
        ax.plot(x, df['Alex'], marker = 'o', linestyle = '-', color = 'royalblue', label = 'ALB')
    if show_Carlos:
        ax.plot(x, df['Carlos'], marker = 's', linestyle = '--', color = 'red', label = 'SAI')

    ax.set_xticks(x)#sets axis
    ax.set_xticklabels(df['Race'], rotation = 90)
    ax.invert_yaxis()
    ax.set_ylabel("Results")
    ax.set_title(title)
    ax.legend() #shows a key to link drivers and lines
    st.pyplot(fig) #displays graph

    # def plot_tyre_pie(laps, Driver_initials):
    #     driver_laps = laps.pick_driver(Driver_initials)
    #     compound_counts = driver_laps['Compound'].value_counts()
        
    #     plt.figure(figsize=(6,6))
    #     plt.pie(compound_counts, labels=compound_counts.index, autopct='%1.1f%%', startangle=140)
    #     plt.title(f'Tyre Usage for {Driver_initials}')
    #     plt.show()

st.header("Tyre Usage Pie Chart")

selected_race = st.selectbox("Select Race", race_names)#gets race and driver to make pie chart
selected_driver = st.radio("Select Driver", ['Alex (ALB)', 'Carlos (SAI)'])

race_index = race_names.index(selected_race)
laps_for_race = laps_list[race_index]

if laps_for_race is not None:
    driver_initials = 'ALB' if selected_driver.startswith('Alex') else 'SAI'
    driver_laps = laps_for_race.pick_driver(driver_initials)
    compound_counts = driver_laps['Compound'].value_counts()
    
    fig2, ax2 = plt.subplots(figsize=(5,5)) #draws pie chart
    ax2.pie(compound_counts, labels=compound_counts.index, autopct='%1.1f%%', startangle=140)
    ax2.set_title(f'Tyre Usage for {driver_initials} at {selected_race}')
    st.pyplot(fig2)
else:
    st.write(f"No lap data available for {selected_race}") #shows message for if there was no results
