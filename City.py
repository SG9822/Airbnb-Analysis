import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine, text
from urllib.parse import quote
import folium
from streamlit_folium import st_folium


user = 'root'
password = quote('MySQL@123')
host = '127.0.0.1'
port = 3306
database = 'Airbnb'

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')
engine = engine.connect()


def map(data):
    mymap = folium.Map(location=[data[0][2], data[0][1]], zoom_start=9)
    fg = folium.FeatureGroup(name='Country')

    # Add markers for each location with pop-up text
    for location in data:
        popup_content = f"Property Count: {location[3]}| Average Price: {location[4]}| Averarge Rating: {location[5]}"
        pp = f"Property Name: {location[3]} | Property Type: {location[4]}"
        tooltip_content = f"{location[0]}<br>{popup_content}"
        fg.add_child(folium.Marker(
            location=[location[2], location[1]],
            popup=folium.Popup(f"{popup_content}\n{pp}", parse_html=True),
            tooltip=folium.Tooltip(tooltip_content, sticky=True),
            icon=folium.Icon(color='green', icon='home', prefix='fa')
        ))
    mymap.add_child(fg)
    return mymap


def city(select):
    q6 = pd.DataFrame(engine.execute(text(f"select distinct Market from airbnb_analysis where Country='{select}'")))
    l_city = list(q6['Market'])

    select_city = st.selectbox("Select city", l_city, index=None)
    if select_city:
        q = pd.DataFrame(engine.execute(text(
            f"select Market, floor(count(Market)) Count from airbnb_analysis where Market = '{select_city}' group by 1")))
        st.write(
            f"### Welcome to `{select_city}`, Select suitable & your Favourite one Over `{q['Count'][0]} Properties` in this beautiful city")
        sel = st.selectbox("Select anyone", ['Average Price', 'Average Rating', 'Property Count Near Neighbourhood'])

        if sel == 'Average Price':
            q7 = pd.DataFrame(engine.execute(text(
                f"select Suburban Neighbourhood, round(avg(price), 2) `Average Price` from airbnb_analysis where Market = '{select_city}' group by 1")))
            st.write(f"### Average Price ($) of the {select_city} Neighbourhood")
            fig1 = px.bar(q7, x='Neighbourhood', y='Average Price', color='Neighbourhood', text='Average Price',
                          height=600, width=1000, title=f'Average price of the Neighbourhoods in {select_city}')
            st.plotly_chart(fig1, use_container_width=True)
            st.divider()

        elif sel == 'Average Rating':
            q8 = pd.DataFrame(engine.execute(text(
                f"select distinct Suburban, round(avg(`Average Rating`), 2) `Average Rating` from airbnb_analysis where Market = '{select_city}' group by 1")))
            st.write(f"### Average rating of Properties in Neighbourhood of {select_city}")
            fig2 = px.scatter(q8, x='Suburban', y='Average Rating', color='Suburban', size='Average Rating',
                              title=f"Average Rating of Properties of Neighbourhood in {select_city}")
            st.plotly_chart(fig2, use_container_width=True)
            st.divider()

        elif sel == 'Property Count Near Neighbourhood':
            q9 = pd.DataFrame(engine.execute(text(
                f"select Suburban, Count(Suburban) Count from airbnb_analysis where Market = '{select_city}' group by 1")))
            st.write(f"### Number of Properties in Neighbourhood of {select_city}")
            fig3 = px.bar(q9, x='Suburban', y='Count', color='Suburban', title='Number of Properties in Neighbourhood')
            st.plotly_chart(fig3, use_container_width=True)
            st.divider()

        q10 = pd.DataFrame(engine.execute(
            text(
                f"select Suburban, Latitude,Longitude from airbnb_analysis where Market = '{select_city}'")))
        q10['Suburban'] = q10['Suburban'].apply(lambda x: x.title())
        q10 = q10.drop_duplicates('Suburban')

        q10i = pd.DataFrame(engine.execute(text(
            f"select Suburban, count(Market) Number, concat('$', round(avg(price), 2)) price, round(avg(`Average "
            f"Rating`), 1) Rating  from airbnb_analysis where Market = '{select_city}' group by Suburban")))
        q10i['Suburban'] = q10i['Suburban'].apply(lambda x: x.title())
        data = q10.merge(q10i, how='left', on='Suburban')
        data = data.values.tolist()

        st.write(f"### Map for Properties Available (Markets) in {select}, {select_city}")
        st_folium(
            map(data),
            key="old",
            height=500,
            width=1000,
            use_container_width=True
        )

        st.divider()

        st.markdown("### Select Neighbourhood and Some details for precisely Selecting your property")
        col1, col2, col3 = st.columns(3)
        with col1:
            q11 = pd.DataFrame(
                engine.execute(text(f"select distinct Suburban from airbnb_analysis where market = '{select_city}'")))
            l_q11 = list(q11['Suburban'])
            st.markdown("#### Select the Neighbourhood")
            s1 = st.selectbox("s1", l_q11, label_visibility='collapsed', index=None)
        with col2:
            if s1:
                q12 = pd.DataFrame(
                    engine.execute(text(f"select distinct property_type from airbnb_analysis where Suburban = '{s1}'")))
                l_q12 = list(q12['property_type'])
                st.markdown("#### Select Property Type")
                s2 = st.selectbox("s2", l_q12, label_visibility='collapsed', index=None)
        with col3:
            if s1 and s2:
                q13 = pd.DataFrame(engine.execute(text(
                    f"select distinct bedrooms from airbnb_analysis where Suburban = '{s1}' and property_type='{s2}'")))
                q13['bedrooms'] = q13['bedrooms'].astype('int')
                l_q13 = list(q13['bedrooms'])
                l_q13.sort()
                st.markdown("#### Select Bedroom(s) Available")
                s3 = st.selectbox("s3", l_q13, label_visibility='collapsed', index=None)

        if s1 and s2 and s3:
            q14 = pd.DataFrame(engine.execute(text(f"select round(avg(price), 2) `Average Price`, round(avg(`Average "
                                                   f"Rating`), 2) `Average Rating` from airbnb_analysis where "
                                                   f"Suburban = '{s1}' and property_type = '{s2}' and bedrooms = "
                                                   f"{s3}")))
            st.markdown(
                f"#### Average Price of the :blue[{s2}] for :blue[{int(s3)}] Bedroom(s) in :blue[{s1}] is :blue[${q14['Average Price'][0]}] & Average Rating is :blue[{q14['Average Rating'][0]}]")

            q15 = pd.DataFrame(engine.execute(text(
                f"select listing_url `ID/Booking Link`, name `Property Name`, `Image URL`, minimum_nights `Min Nights`, maximum_nights `Max "
                f"Nights`, Accommodates, Bathrooms, Price, host_id `Host Id`, host_name `Host Name`, "
                f"`Property Address`, `Average Rating`, number_of_reviews `No.of.Reviews` from airbnb_analysis where Suburban = '{s1}' and property_type = "
                f"'{s2}' and bedrooms = {int(s3)} order by number_of_reviews desc, `Average Rating` desc")))

            if len(q15['ID/Booking Link']) > 5:
                st.markdown("### Want to select Price Range?")

                col4, col5 = st.columns([1, 2])
                with col4:
                    radio = st.radio("r1", ["Yes", "No"], index=None, horizontal=True, label_visibility='collapsed')

                if radio == 'Yes':
                    col6, col7, col8 = st.columns([1, 2, 2])

                    with col6:
                        st.markdown(f"### Select Price Range")
                    with col7:
                        price_1 = st.number_input("p1", value=None, placeholder="Min Price",
                                                  label_visibility='collapsed')
                    with col8:
                        price_2 = st.number_input("p2", value=None, placeholder="Max Price",
                                                  label_visibility='collapsed')

                    st.write(f":blue[Note: Please select between {int(q15['Price'].min())} and {int(q15['Price'].max())}]")
                    b3 = st.button("Ok")

                    if b3:
                        q15_q = q15[(q15['Price'] >= price_1) & (q15['Price'] <= price_2)]
                        st.dataframe(q15_q, column_config={'ID/Booking Link': st.column_config.LinkColumn(
                            display_text="https://www.airbnb.com/rooms/(\d.*)"),
                            'Image URL': st.column_config.ImageColumn("Preview")},
                                     hide_index=True)
                elif radio == 'No':
                    st.dataframe(q15, column_config={
                        'ID/Booking Link': st.column_config.LinkColumn(
                            display_text="https://www.airbnb.com/rooms/(\d.*)"),
                        'Image URL': st.column_config.ImageColumn("Preview")}, hide_index=True)

            else:
                st.dataframe(q15, column_config={
                    'ID/Booking Link': st.column_config.LinkColumn(display_text="https://www.airbnb.com/rooms/(\d.*)"),
                    'Image URL': st.column_config.ImageColumn("Preview")}, hide_index=True)
