import streamlit as st
import requests
import pandas as pd
import wbgapi as wb
import plotly.express as px
import plotly.graph_objects as go

# emojis list: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="International Health", page_icon="🎗", layout="wide")

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")

# resize expanders
st.markdown("""
<style>
.streamlit-expanderHeader {
    font-size: medium;
    color:#ad8585;   
    }
.st-bd {border-style: none;}
</style>
""", unsafe_allow_html=True)


st.title("WHO indicators API explorer")

# ---- SIDEBAR ----
with st.sidebar:
    with st.expander("Read more about the World Health Organization (WHO)"):
        # WHO details
        st.markdown("<p style='text-align: justify'>"
        "The <a href='https://www.who.int/'>World Health Organization (WHO) </a> leads global efforts to expand universal health coverage by directing and"
            " coordinating the world’s response to health emergencies. It promotes healthier lives – from pregnancy care"
            " through old age. Its Triple Billion targets outline an ambitious plan for the world to achieve good health"
            " for all using science-based policies and programmes.<br><br>International health is defined as the branch of public health focusing on developing nations and"
        " foreign aid efforts. <br> The predominant agency associated with global and international health is the"
        " World Health Organization (WHO). Other important agencies are also involved with different missions:"
        " funders, implementing partners etc.</p>",unsafe_allow_html=True)
    with st.expander("Accessing WHO API to load data"):
        # WHO details
        st.markdown("<p style='text-align: justify>"
            "The WHO API <a href='https://www.who.int/data/gho/info/gho-odata-api#exe3'> (see documentation) </a> is providing access to 2,197"
                "  indicators at the time of writing.<br>"
                "To simplify data exploration here we will only display indicators related to the three epidemics "
                "targeted by the Global Fund (i.e. AIDS, tuberculosis and malaria).<br>"
                "In order to offer more visualization filtering we also imported the "
                "<a href='https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups'> World Bank regional groupings and Income group classifications </a>"
                " from the World Bank API through the Python wbgapi library and merged it with the country list from the WHO</p>",unsafe_allow_html=True)
    with st.expander("What's an API?"):
        st.markdown("<p style='text-align: justify;'>"
                    "The term API stands for Application Programming Interface. "
                    "API enable applications, here our web app, to communicate with an external data source using simple commands. "
                    "<a href='https://en.wikipedia.org/wiki/API'> Wikipedia</a> defines it as a connection "
                    "between computers or between computer programs offering a service to other pieces of software."
                    "<br>In the case of the WHO, The Global Fund and the World Bank, all 3 APIs have been created by these organizations"
                    " with the purpose of ensuring transparency and a better access to information generated, "
                    "for the benefit of the stakeholders in their activities.</p>", unsafe_allow_html=True)

    st.caption("<p style='text-align: justify;'>"
               "Disclaimer: <br /> The information presented in this page is solely made by me in my private capacity. "
               " <br /> All the data used and displayed is publicly available via the "
               "<a href='https://www.who.int/data/gho/info/gho-odata-api#exe3'>WHO API </a></p>",
               unsafe_allow_html=True)

## List of WHO countries
@st.cache
def import_api_WHO_countries(url):
    service_url0 = url
    response0 = requests.get(service_url0)
    # make sure we got a valid response
    print(response0)
    if (response0.ok):
        # get the full data from the response
        data0j = response0.json()
    else:
        st.caption("API data cannot be loaded")
    country_list = pd.DataFrame(data0j["value"])
    return country_list
with st.spinner('Loading country data from WHO API (it will take a few seconds the first time)'):
    country_list = import_api_WHO_countries("https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues")
    country_list.rename(columns={"Code": "SpatialDim", "Title": "Country"}, inplace=True)

## List of World Bank country with Region and Income Level

WorldBank_countries = wb.economy.DataFrame().reset_index()[['id','name','aggregate','region','incomeLevel']]
WorldBank_countries =  WorldBank_countries[WorldBank_countries['aggregate']==False].drop('aggregate', axis=1)
WorldBank_countries['incomeLevel'] = WorldBank_countries['incomeLevel'].map({
                            'LIC':'Low income country',
                            'HIC':'High income country',
                            'LMC':'Lower middle income country',
                            'INX': 'Upper middle income country',
                            'UMC':'Upper middle income country'})
WorldBank_countries['region'] = WorldBank_countries['region'].map({
                            'LCN':'Latin America & the Caribbean',
                            'SAS':'South Asia',
                            'SSF':'Sub-Saharan Africa',
                            'ECS':'Europe and Central Asia',
                            'MEA':'Middle East and North Africa',
                            'EAS':'East Asia and Pacific',
                            'NAC':'North America'})
WorldBank_countries.rename(columns={"id":"SpatialDim","incomeLevel":"Income level","region":"Region"}, inplace = True)
country_list = country_list.merge(WorldBank_countries, how='inner', on='SpatialDim')

## List of WHO indicators
who_indic_container = st.container()
with who_indic_container:
    st.subheader("WHO indicators")
    col1, col2 = st.columns([1, 2])
    with col1:
        disease = st.selectbox(
            'Display the list of indicators for: ',
            options=['Tuberculosis', 'Malaria', 'HIV'])
        # Import API data
        @st.cache
        def import_api_WHO_indicators(url):
            service_url0 = url
            response0 = requests.get(service_url0)
            # make sure we got a valid response
            print(response0)
            if (response0.ok):
                # get the full data from the response
                data0j = response0.json()
            else:
                st.caption("API data cannot be loaded")
            data0a = pd.DataFrame(data0j["value"])
            return data0a
        with st.spinner('Loading indicators data from WHO API (it will take a few seconds the first time)'):
            data0a = import_api_WHO_indicators("https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,'{}')".format(disease))

        option_indicators_name = st.selectbox('Display records for: ',data0a.IndicatorName.unique())
        selection_indicator_code = data0a[data0a['IndicatorName']==option_indicators_name][['IndicatorCode']].iloc[0][0]

        @st.cache
        def import_api_WHO_indicator_name(url):
            service_url0 = url
            response0 = requests.get(service_url0)
            # make sure we got a valid response
            if (response0.ok):
                # get the full data from the response
                data0j = response0.json()
            else:
                st.caption("API data cannot be loaded")

            return data0j

        with st.spinner('Loading country data from WHO API (it will take a few seconds the first time)'):
            data0j = import_api_WHO_indicator_name("https://ghoapi.azureedge.net/api/{}".format(selection_indicator_code))
            data0a[data0a['IndicatorName'] == selection_indicator_code]['IndicatorCode'].reset_index(drop=True)
            data0a = pd.DataFrame(data0j["value"])
        #merge with country info
        df = pd.merge(data0a,
                      country_list,
                      on='SpatialDim',
                      how='inner')
        df.rename(columns={"TimeDim":"Year","NumericValue":"Value"}, inplace = True)
        df = df[(df['SpatialDimType'] == 'COUNTRY') | (df['SpatialDimType'] == 'COUNTRY')][['Country','SpatialDim', 'Year', 'Value','ParentTitle','Region','Income level']]
        hue = st.radio("Display data per:", ('Region', 'Income level', 'Country'), horizontal=True)

    with col2:
        if hue == 'Income level':
            fig = px.line(df.groupby(['Year','Income level'], as_index=False).sum(), x="Year", y="Value", color="Income level", title = "{}".format(option_indicators_name))
            st.plotly_chart(fig, use_container_width=True)
        elif hue == 'Region':
            fig = px.line(df.groupby(['Year','Region'], as_index=False).sum(), x="Year", y="Value", color="Region", title = "{}".format(option_indicators_name))
            st.plotly_chart(fig, use_container_width=True)
        elif hue == 'Country':
            # checkbox all countries
            all = col1.checkbox("All countries", value=True)
            if all:
                selected_options = df.Country.unique()
                fig = px.line(df.groupby(['Year','Country'], as_index=False).mean(), x="Year", y="Value", color ="Country", title = "{}".format(option_indicators_name))
                st.plotly_chart(fig, use_container_width=True)
            else:
                container = col1.container()
                selected_options = container.multiselect("Select one or more countries:", df.sort_values('Country').Country.unique())
                df_country = df[df["Country"].isin(selected_options)]
                fig = px.line(df_country.groupby(['Year','Country'], as_index=False).mean(), x="Year", y="Value",color ="Country", title = "{}".format(option_indicators_name))
                st.plotly_chart(fig, use_container_width=True)


with st.expander("See code for importing the list of countries and information from the WHO & World Bank APIs "):
            st.code('''
# Download the list of WHO countries:

def import_api_WHO_countries(url):
    service_url0 = url
    response0 = requests.get(service_url0)
    # make sure we got a valid response
    print(response0)
    if (response0.ok):
        # get the full data from the response
        data0j = response0.json()
    else:
        st.caption("API data cannot be loaded")
    country_list = pd.DataFrame(data0j["value"])
    return country_list
with st.spinner('Loading country data from WHO API (it will take a few seconds the first time)'):
    country_list = import_api_WHO_countries("https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues")
    country_list.rename(columns={"Code": "SpatialDim", "Title": "Country"}, inplace=True)

# Download the list of World Bank country with Region and Income Level information:

WorldBank_countries = wb.economy.DataFrame().reset_index()[['id','name','aggregate','region','incomeLevel']]
WorldBank_countries =  WorldBank_countries[WorldBank_countries['aggregate']==False].drop('aggregate', axis=1)
WorldBank_countries['incomeLevel'] = WorldBank_countries['incomeLevel'].map({
                            'LIC':'Low income country',
                            'HIC':'High income country',
                            'LMC':'Lower middle income country',
                            'INX': 'Upper middle income country',
                            'UMC':'Upper middle income country'})
WorldBank_countries['region'] = WorldBank_countries['region'].map({
                            'LCN':'Latin America & the Caribbean',
                            'SAS':'South Asia',
                            'SSF':'Sub-Saharan Africa',
                            'ECS':'Europe and Central Asia',
                            'MEA':'Middle East and North Africa',
                            'EAS':'East Asia and Pacific',
                            'NAC':'North America'})
WorldBank_countries.rename(columns={"id":"SpatialDim","incomeLevel":"Income level","region":"Region"}, inplace = True)
country_list = country_list.merge(WorldBank_countries, how='inner', on='SpatialDim')                      
            ''', language='python')

with st.expander("See code for the Streamlit App"):
    st.code('''
    # Downloading the list of WHO indicators based on selected input: 
who_indic_container = st.container()
with who_indic_container:
    st.subheader("WHO indicators")
    col1, col2 = st.columns([1, 2])
    with col1:
        disease = st.selectbox(
            'Display the list of indicators for: ',
            options=['Tuberculosis', 'Malaria', 'HIV'])
        # Import API data
        @st.cache
        def import_api_WHO_indicators(url):
            service_url0 = url
            response0 = requests.get(service_url0)
            # make sure we got a valid response
            print(response0)
            if (response0.ok):
                # get the full data from the response
                data0j = response0.json()
            else:
                st.caption("API data cannot be loaded")
            data0a = pd.DataFrame(data0j["value"])
            return data0a
        with st.spinner('Loading indicators data from WHO API (it will take a few seconds the first time)'):
            data0a = import_api_WHO_indicators("https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,'{}')".format(disease))

        option_indicators_name = st.selectbox('Display records for: ',data0a.IndicatorName.unique())
        selection_indicator_code = data0a[data0a['IndicatorName']==option_indicators_name][['IndicatorCode']].iloc[0][0]

        @st.cache
        def import_api_WHO_indicator_name(url):
            service_url0 = url
            response0 = requests.get(service_url0)
            # make sure we got a valid response
            if (response0.ok):
                # get the full data from the response
                data0j = response0.json()
            else:
                st.caption("API data cannot be loaded")
            return data0j

        with st.spinner('Loading country data from WHO API (it will take a few seconds the first time)'):
            data0j = import_api_WHO_indicator_name("https://ghoapi.azureedge.net/api/{}".format(selection_indicator_code))
            data0a[data0a['IndicatorName'] == selection_indicator_code]['IndicatorCode'].reset_index(drop=True)
            data0a = pd.DataFrame(data0j["value"])
        #merge with country info
        df = pd.merge(data0a,
                      country_list,
                      on='SpatialDim',
                      how='inner')
        df.rename(columns={"TimeDim":"Year","NumericValue":"Value"}, inplace = True)
        df = df[(df['SpatialDimType'] == 'COUNTRY') | (df['SpatialDimType'] == 'COUNTRY')][['Country','SpatialDim', 'Year', 'Value','ParentTitle','Region','Income level']]
        hue = st.radio("Display data per:", ('Region', 'Income level', 'Country'), horizontal=True)

    with col2:
        if hue == 'Income level':
            fig = px.line(df.groupby(['Year','Income level'], as_index=False).sum(), x="Year", y="Value", color="Income level", title = "{}".format(option_indicators_name))
            fig.update_layout(paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)")
            st.plotly_chart(fig, use_container_width=True)
        elif hue == 'Region':
            fig = px.line(df.groupby(['Year','Region'], as_index=False).sum(), x="Year", y="Value", color="Region", title = "{}".format(option_indicators_name))
            fig.update_layout(paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)")
            st.plotly_chart(fig, use_container_width=True)
        elif hue == 'Country':
            # checkbox all countries
            all = col1.checkbox("All countries", value=True)
            if all:
                selected_options = df.Country.unique()
                fig = px.line(df.groupby(['Year','Country'], as_index=False).mean(), x="Year", y="Value", color ="Country", title = "{}".format(option_indicators_name))
                fig.update_layout(plot_bgcolor="rgb(255,255,255)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                container = col1.container()
                selected_options = container.multiselect("Select one or more countries:", df.sort_values('Country').Country.unique())
                df_country = df[df["Country"].isin(selected_options)]
                fig = px.line(df_country.groupby(['Year','Country'], as_index=False).mean(), x="Year", y="Value",color ="Country", title = "{}".format(option_indicators_name))
                fig.update_layout(plot_bgcolor="rgb(255,255,255)")
                st.plotly_chart(fig, use_container_width=True)
    ''')
