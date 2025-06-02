import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

# Title and Header
st.title("Worldwide Analysis of Quality of Life and Economic Factors")
st.header("Worldwide Analysis of Quality of Life and Economic Factors")
st.subheader("This app enables you to explore the relationships between poverty, life expectancy, and GDP across various countries and years. Use the panels to select options and interact with the data.")

## Add Three tabs
tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])
with tab1:
    st.subheader("Global Overview")
    st.write("This section provides a global overview of the relationships between poverty, life expectancy, and GDP.")
    
    data_tab1 = pd.read_csv("https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv")

    year = st.slider("Select a year",
                   min_value=int(data_tab1['year'].min()),
                   max_value=int(data_tab1['year'].max()),
                   value=(int(data_tab1['year'].min()), int(data_tab1['year'].max())),
                   step=1,
                   key="year_tab1")
    # filter the dataframe based on the selected year
    data_tab1 = data_tab1[(data_tab1['year'] >= year[0]) & (data_tab1['year'] <= year[1])]

    # Display only 4 main metrics:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Global Average Life Expectancy", f"{np.mean(data_tab1["Life Expectancy (IHME)"]):.1f} years")
    with col2:
        st.metric("Global Median GDP per Capita",
                  f"${np.median(data_tab1["GDP per capita"]):.0f}")
    with col3:
        st.metric("Global Poverty Average",
                  f"{np.mean(data_tab1["headcount_ratio_upper_mid_income_povline"]):.1f}%")
    with col4:
        st.metric("Number of Countries",
                  f"{data_tab1["country"].nunique()}")




with tab2:
    st.subheader("Country Deep Dive")
    st.write("This section allows you to select a specific country and explore its data in detail.")

with tab3:
    st.subheader("Data Explorer")
    st.write("This section allows you to explore the data in more detail, including filtering and visualizing the data.")
    
    # Displays the Dataframe
    data_tab3 = pd.read_csv("https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv").sort_values('year', ascending=True)

    # create a selection filter based on coutnry
    country = st.multiselect("Select a country",
                           data_tab3['country'].unique())
    # filter the dataframe based on the selected country
    if country:
        data_tab3 = data_tab3[data_tab3['country'].isin(country)]

    year = st.slider("Select a year",
                   min_value=int(data_tab3['year'].min()),
                   max_value=int(data_tab3['year'].max()),
                   value=(int(data_tab3['year'].min()), int(data_tab3['year'].max())),
                   step=1,
                   key="year_tab_3")
    # filter the dataframe based on the selected year
    data_tab3 = data_tab3[(data_tab3['year'] >= year[0]) & (data_tab3['year'] <= year[1])]
    # create a selection filter based on year
    st.dataframe(data_tab3)

    st.write(data_tab3.columns)

    # Create Dwonload button
    st.download_button(label = "Download Filtered Data",
                       data = data_tab3.to_csv().encode("utf-8"),
                       file_name="filtered_data.csv",
                       mime="text/csv",
                       )