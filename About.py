import streamlit as st


import streamlit as st

def about():
    st.title("About Airbnb Analysis Project")

    st.markdown(
        """
        Welcome to the Airbnb Analysis Project! This project is designed to provide insightful analysis and visualizations of Airbnb data, focusing on the Travel Industry, Property Management, and Tourism domains.

        ## Project Overview
        The Airbnb Analysis Project leverages Python scripting, Data Preprocessing, Visualization, Exploratory Data Analysis (EDA), Streamlit, MongoDB, and PowerBI to offer comprehensive insights into Airbnb listings across various countries and cities.

        ## Technology Stack
        - **Python Scripting:** Used for data manipulation, analysis, and visualization.
        - **Data Preprocessing:** Ensures data quality and prepares it for analysis.
        - **Visualization:** Utilizes charts, graphs, and maps for effective data representation.
        - **EDA:** Exploratory Data Analysis techniques for extracting meaningful patterns.
        - **Streamlit:** Empowers interactive and user-friendly web applications.
        - **MongoDB:** A NoSQL database for efficient data storage and retrieval.
        - **PowerBI:** Enables additional visualization and reporting capabilities.

        ## Domain Focus
        The project revolves around the Travel Industry, Property Management, and Tourism domains, providing valuable insights into Airbnb listings and trends.

        ## Home Page
        ### Basic Country Insights
        - Select a country to view insights such as average price, property types, bedroom sizes, and average ratings.
        - Interactive Folium map showcasing key property-related data.

        ### City-wise Insights
        - Explore specific cities within the selected country.
        - View city-level details like average rating, price, and property count.
        - Filter by neighborhood, property type, bedroom size, and optional price range.
        - Detailed data frame for in-depth analysis.

        ## About Page
        The project is a collaborative effort, utilizing a technology stack tailored for efficient data analysis and user interaction. It is designed to cater to users interested in understanding Airbnb trends across countries and cities.
        """
    )


