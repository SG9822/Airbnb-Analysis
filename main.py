import folium
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine, text
from urllib.parse import quote
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from City import city
from About import about

st.set_page_config(layout="wide", page_title='Airbnb Analysis', page_icon="https://a0.muscache.com/airbnb/static/icons/apple-touch-icon-76x76-3b313d93b1b5823293524b9764352ac9.png")

user = 'root'
password = quote('MySQL@123')
host = '127.0.0.1'
port = 3306
database = 'Airbnb'

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')
engine = engine.connect()

tit1, tit2 = st.columns([1, 3])

with tit1:
    st.markdown("### [:red[Airbnb Analysis | Project]]() <style>a { text-decoration: none; }</style>", unsafe_allow_html=True)

with tit2:
    selected = option_menu(
        menu_title=None,
        options=["Home", 'About Project'],
        icons=["house", "info-square-fill"],
        menu_icon=None,
        default_index=0,
        orientation="horizontal", )


@st.cache_data
def map(data):
    mymap = folium.Map(location=[data[0][2], data[0][1]], zoom_start=3)
    fg = folium.FeatureGroup(name='Country')

    # Add markers for each location with pop-up text
    for location in data:
        popup_content = f"Property Count: {location[3]}| Average Price: {location[4]}| Averarge Rating: {location[5]}"
        tooltip_content = f"{location[0]}<br>{popup_content}"
        fg.add_child(folium.Marker(
            location=[location[2], location[1]],
            popup=folium.Popup(popup_content, parse_html=True),
            tooltip=folium.Tooltip(tooltip_content, sticky=True),
            icon=folium.Icon(color='green')
        ))
    mymap.add_child(fg)
    return mymap


def home():
    country = pd.DataFrame(engine.execute(text("select distinct country from airbnb_analysis")))

    l_c = list(country['country'])

    st.markdown('### Select a country you want to book a place')
    select = st.selectbox("Select the country", l_c, index=None, label_visibility='collapsed')
    try:
        if select:
            tab1, tab2 = st.tabs([f'{select} Properties Insights', 'City Wise Properties Insights'])
            with tab1:
                q1 = pd.DataFrame(engine.execute(text(
                    f"select Market, round(avg(price), 2) `Average Price` from airbnb_analysis where country = '{select}' group by market")))
                q1i = pd.DataFrame(engine.execute(text(
                    f"select property_type `Property Type`, round(avg(price), 2) `Average Price` from airbnb_analysis where country = '{select}' group by property_type")))
                st.markdown(f"### Average Price of Properties & Property Types in {select}")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(px.bar(q1, x='Market', y='Average Price', color='Market', text='Average Price',
                                    title=f"Average price ($) of Properties in {select}"))
                with col2:
                    st.write(
                        px.bar(q1i, x='Property Type', y='Average Price', color='Property Type', text='Average Price',
                               title=f"Average price ($) of Property Types in {select}"))
                st.divider()

                q4 = pd.DataFrame(engine.execute(text(
                    f"select Bedrooms, round(avg(price), 2) `Average Price`, max(price) `Max Price`, min(price) `Min Price`, round(avg(`Average Rating`), 1) Rating from airbnb_analysis where country = '{select}' group by Bedrooms order by Bedrooms")))
                st.write("### Bedroom wise Average Price, Max Price, Min Price & Average Rating")
                col5, col6 = st.columns(2)
                with col5:
                    st.plotly_chart(
                        px.line(q4, x='Bedrooms', y='Average Price', hover_data=['Max Price', 'Min Price'],
                                markers=True,
                                title=f'Prices Bedroom wise in {select} (Average Price, Max Price, Min Price)'))

                with col6:
                    fig = px.pie(q4, values='Rating', names='Bedrooms',
                                 title=f"Average Rating of Bedrooms wise on the Market in {select}",
                                 color_discrete_sequence=px.colors.diverging.RdYlGn
                                 )
                    fig.update_traces(
                        textinfo='value+label'

                    )
                    st.plotly_chart(fig)
                st.divider()

                st.write("### Number & Ratings of Properties and Property Types")
                col3, col4 = st.columns(2)
                with col3:
                    q2 = pd.DataFrame(engine.execute(text(
                        f"select Market, count(Market) Count from airbnb_analysis where Country = '{select}' group by Market")))
                    st.write(
                        px.bar(q2, x='Market', y='Count', color='Market', text='Count',
                               title=f'Number of Properties on the  Market in {select}'))
                    st.divider()
                    q3 = pd.DataFrame(engine.execute(text(
                        f"select property_type `Property Types`, count(Market) Count from airbnb_analysis where Country = '{select}' group by `property_type`")))
                    st.write(
                        px.bar(q3, x='Property Types', y='Count', color='Property Types', text='Count',
                               title=f'Number of Property Types on the  Market in {select}'))
                with col4:
                    q2i = pd.DataFrame(engine.execute(text(
                        f"select Market, round(avg(`Average Rating`), 1) `Average Rating` from airbnb_analysis where country = '{select}' group by Market")))
                    fig = px.pie(q2i, values='Average Rating', names='Market', hover_name='Market',
                                 title=f"Average Rating of Properties on the Market in {select}",
                                 color_discrete_sequence=px.colors.diverging.RdYlGn
                                 )
                    fig.update_traces(
                        textinfo='value+label'

                    )
                    st.plotly_chart(fig)
                    st.divider()

                    q3i = pd.DataFrame(engine.execute(text(
                        f"select property_type `Property Types`, round(avg(`Average Rating`), 1) `Average Rating` from airbnb_analysis where country = '{select}' group by `Property Types`")))
                    st.plotly_chart(
                        px.scatter(q3i, x='Property Types', y='Average Rating', color='Property Types',
                                   size='Average Rating',
                                   title=f'Average Rating of Property Types on the Market in {select}'))
                st.divider()

                st.subheader(f"Top Rating Properties in {select}")

                # col7, col8 = st.columns([0.1, 2.9])
                # with col8:
                q5 = pd.DataFrame(engine.execute(text(
                    f"select _id `Property ID `, name `Property Name`, listing_url `Listing URL`, host_id `Host ID`, host_name `Host Name`, property_type `Property Type`, price `Price`, `Average Rating` Rating, number_of_reviews `Review Counts` from airbnb_analysis where country='{select}' order by `Review Counts` desc, `Average Rating` desc limit 10")))
                st.dataframe(q5, column_config={'Listing URL': st.column_config.LinkColumn("Booking Link")},
                             hide_index=True,
                             use_container_width=True)
                st.divider()

                q6 = pd.DataFrame(engine.execute(
                    text(f"select Market, Latitude,Longitude from airbnb_analysis where country = '{select}'")))
                q6['Market'] = q6['Market'].apply(lambda x: x.title())
                q6 = q6.drop_duplicates('Market')

                q6i = pd.DataFrame(engine.execute(text(
                    f"select Market, count(Market) Number, concat('$', round(avg(price), 2)) price, round(avg(`Average Rating`), 1) Rating  from airbnb_analysis where country = '{select}' group by Market")))
                data = q6.merge(q6i, how='left', on='Market')
                data = data.values.tolist()

                st.write(f"### Map for Properties Available (Markets) in {select}")
                st_folium(
                    map(data),
                    key="old",
                    height=550,
                    width=1000,
                    use_container_width=True
                )

                st.divider()

                st.markdown(
                    "## Want to select the specific Property from the Specific City go to `City Wise Properties "
                    "Insights`")

            with tab2:
                st.write("## Welcome")
                st.warning("Some booking links may not work, because the data is taken from MongoDB Atlas sample "
                           "data, sorry for your inconvenience")
                st.write("### Select the City you want to book")
                city(select)

    except:
        st.warning("Please Select any Country")


if selected == 'Home':
    home()
elif selected == 'About Project':
    about()
