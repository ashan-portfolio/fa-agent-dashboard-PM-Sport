import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="FA Agent Global Map", layout="wide")

# Load data with caching to improve performance
@st.cache_data
def load_data():
    df = pd.read_csv('FA REGISTERED FOOTBALL AGENTS - No-independent.csv')
    
    name_fixes = {
        'UK': 'United Kingdom',
        'England': 'United Kingdom',
        'UK (Scotland)': 'United Kingdom',
        'Scotland': 'United Kingdom',
        'USA': 'United States of America',
        'UAE': 'United Arab Emirates'
    }
    
    df['Country'] = df['Country'].replace(name_fixes)
    
    # Remove rows that aren't countries
    df = df[df['Country'] != 'Specialist Boutique']
    return df

df = load_data()

st.markdown("""
    <style>
    img {
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
    }
    .centered-text {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

head_left, head_mid, head_right = st.columns([1, 4, 0.5])

with head_left:
    st.write("")

with head_mid:
    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("<h1 style='text-align: center; color: black;'>FA Licensed Agents Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")


with head_right:
    st.image('The_team.png', use_container_width=True)

# Prepare common data for visualizations
map_data = df['Country'].value_counts().reset_index()
map_data.columns = ['Country', 'Agent Count']


top_col1, top_col2 = st.columns(2)

with top_col1:
    st.markdown("<h3 style='text-align: center; color: black;'>Global Distribution</h3>", unsafe_allow_html=True)
    
    fig_map = px.choropleth(
        map_data,
        locations="Country",
        locationmode="country names",
        color="Agent Count",
        hover_name="Country",
        projection="orthographic",
        color_continuous_scale=["#C8DEC8", "#2E7040"],
    )
    # Adding globe-specific styling (ocean color and rotations)
    fig_map.update_geos(
        showocean=True, oceancolor="#f0f2f6",
        showcountries=True,
        showcoastlines=True, 
        coastlinecolor="black",
        framecolor="black",       
        coastlinewidth=1,          
        countrywidth=1,
        countrycolor="black"
    )
    fig_map.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with top_col2:
    st.markdown("<h3 style='text-align: center; color: black;'>Agent Count by Country</h3>", unsafe_allow_html=True)
    # Displaying the list of countries and counts
    st.dataframe(map_data, hide_index=True, use_container_width=True, height=500)

st.markdown("---") # Visual separator

# --- BOTTOM ROW: Agent Categories and Minor Authorization ---
bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    st.markdown("<h3 style='text-align: center; color: black;'>Agent Categories</h3>", unsafe_allow_html=True)
    type_counts = df['Agent Type'].value_counts().reset_index()
    type_counts.columns = ['Agent Type', 'Count']

    fig_bar = px.bar(
        type_counts,
        x='Agent Type', 
        y='Count',      
        orientation='v',
        color_discrete_sequence=["#2E7040"]
    )
    fig_bar.update_layout(
        yaxis={'categoryorder':'total ascending'}, 
        height=400,
        margin={"t":20, "b":20}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with bottom_col2:
    st.markdown("<h3 style='text-align: center; color: black;'>Minor Authorization</h3>", unsafe_allow_html=True)
    minor_counts = df['Authorised to Represent Minors'].value_counts().reset_index()
    minor_counts.columns = ['Status', 'Count']
    
    fig_pie = px.pie(
        minor_counts,
        names='Status',
        values='Count',
        color_discrete_sequence=["#2E7040", "#A9CBA3"] 
    )
    fig_pie.update_layout(height=400, margin={"t":20, "b":20})
    st.plotly_chart(fig_pie, use_container_width=True)