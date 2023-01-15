import streamlit as st
import requests
import pandas as pd
import wbgapi as wb
import plotly.express as px
from streamlit_lottie import st_lottie
import plotly.graph_objects as go

st.set_page_config(page_title="International Health", page_icon="🎗", layout="wide")

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 3rem;
                    padding-right: 3rem}
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem}
               .streamlit-expanderHeader {
                    font-size: medium;
                    color:#05c37d}
                .st-bd {border-style: none;}
        </style>
        """, unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: #12151D;
   border: 1px solid #283648 ;
   border-radius: 5px;
   padding: 1% 1% 1% 5%;
   color: #04AA6D;
   overflow-wrap: break-word;
}
/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: white;
}
</style>
""", unsafe_allow_html=True)

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


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

if 'count' not in st.session_state:
	st.session_state.count = 0

if st.session_state.count == 0:
    arrival_message = st.empty()
    with arrival_message.container():

        st.title("WHO API explorer")
        st.subheader("Indicators exploration tool")
        st.write("<p style='text-align: justify;'>"
                   "This app imports data from the World Health Organization (WHO) API and displays it in a Streamlit web app."
                   "<br/>It allows the user to select a disease (Tuberculosis, Malaria, or HIV) and then displays a list of indicators"
                   " related to the chosen disease. The user can then select a specific indicator and view data for that indicator."
                   " The data is also grouped by Region, Income level, or Country (using the World Bank API) depending on the user's selection. ",
                   unsafe_allow_html=True)

        st.subheader("API status")
        url = "https://ghoapi.azureedge.net/api/Indicator"
        response = requests.get(url)
        if response.status_code != 200:
            st.warning(
                "There seems to be an error with the WHO API (status code: {})".format(response.status_code))
        else:
            st.success("Connection to the WHO API established successfully")
        if response.status_code != 200 or response2.status_code != 200:
            st.info("This app will be accessible once the connection is back")


        with st.expander("Read more about the World Health Organization, what is an API and how to access WHO API"):

            col1, col2, col3 = st.columns([1, 1, 1], gap='small')
            with col1:
                # WHO details
                st.subheader("WHO")
                st.markdown("<p style='text-align: justify'>"
                            "The <a href='https://www.who.int/'>World Health Organization (WHO) </a> plays a crucial role in the global health sector by leading efforts "
                            "to expand universal health coverage and coordinating the world's response to health emergencies. Its focus is on promoting healthier lives, "
                            "from pregnancy care through old age. WHO has set ambitious targets known as the Triple Billion, which aim to achieve good health for all through science-based policies and programs."
                            " International health, which focuses on developing nations and foreign aid efforts, is one branch of public health in which WHO plays a leading role. "
                            "While other important agencies also play a role in global health, WHO is considered the predominant agency associated with international health, and works "
                            "alongside various partners to achieve its mission.</p>", unsafe_allow_html=True)
            with col2:
                st.subheader("API")
                st.markdown("<p style='text-align: justify;'>"
                            "An API, or Application Programming Interface, allows different applications to communicate and exchange data with one another. "
                            "In the case of the World Health Organization (WHO), The Global Fund, and the World Bank, these organizations have created APIs "
                            "to increase transparency and provide better access to information for stakeholders in their activities."
                            "<a href='https://en.wikipedia.org/wiki/API'> <br>Read more on Wikipedia</a></p>",
                            unsafe_allow_html=True)
            with col3:
                st.subheader("WHO API")
                # WHO details
                st.markdown("<p style='text-align: justify;'>"
                            "The WHO API <a href='https://www.who.int/data/gho/info/gho-odata-api#exe3'> (see documentation) </a> is providing access to 2,197 indicators at the time of writing"
                            ", but for simplicity we will only be displaying indicators related to the three epidemics targeted by the Global Fund (i.e. AIDS, tuberculosis and malaria)."
                            "<br>To offer more visualization options, we also imported the <a href='https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups'> World Bank regional groupings and Income group classifications </a> from the World Bank API and merged them with the country list from the WHO.",
                            unsafe_allow_html=True)


        col1, col2 = st.columns([10, 35], gap='small')
        with col2:
            st.markdown("<br><br>",
                        unsafe_allow_html=True)
            st.subheader("Disclaimer")
            st.write("<p style='text-align: justify;'>"
                "Please note that the information provided in this page is created and shared by me as an individual and "
                "should not be taken as an official representation of the World Health Organization (WHO). "
                "For accurate and up-to-date information, please consult the WHO's official website.",
                unsafe_allow_html=True)
            if response.status_code == 200:
                disclaimer_confirmation = col2.button('I understand')
                if disclaimer_confirmation:
                    st.session_state.count = 1
                    st.experimental_rerun()

        lottie_url = "https://lottie.host/285a7a0c-1d81-4a8f-9df5-c5bebaae5663/UDqNAwwYUo.json"
        lottie_json = load_lottieurl(lottie_url)
        with col1:
            st_lottie(lottie_json, height=250, key="loading_gif2")

if st.session_state.count >= 1:

    st.title("WHO indicators")

    ## List of WHO countries
    # Define a function to import the data from the WHO API
    @st.cache(allow_output_mutation=True)
    def import_api_WHO_countries(url):
        # Make a request to the API
        service_url0 = url
        response0 = requests.get(service_url0)
        # Check if the response was successful
        print(response0)
        if (response0.ok):
            # Get the data from the response
            data0j = response0.json()
        else:
            st.caption("API data cannot be loaded")
        # Create a dataframe from the data
        country_list = pd.DataFrame(data0j["value"])
        # Rename columns
        country_list.rename(columns={"Code": "SpatialDim", "Title": "Country"}, inplace=True)
        # Return the dataframe
        return country_list

    # Use a spinner to show that the data is loading
    with st.spinner('Loading country data from WHO API (it will take a few seconds the first time)'):
        country_list = import_api_WHO_countries("https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues")

    ## List of World Bank country with Region and Income Level

    # Import data from the World Bank API
    WorldBank_countries = wb.economy.DataFrame().reset_index()[['id','name','aggregate','region','incomeLevel']]
    # Filter out aggregate data
    WorldBank_countries =  WorldBank_countries[WorldBank_countries['aggregate']==False].drop('aggregate', axis=1)
    # Map income level and region codes to their full names
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
    # Rename columns
    WorldBank_countries.rename(columns={"id":"SpatialDim","incomeLevel":"Income level","region":"Region"}, inplace = True)
    # Merge the data with the WHO country list
    country_list = country_list.merge(WorldBank_countries, how='inner', on='SpatialDim')

    # TABS ------------------------------------
    tab1, tab2 = st.tabs(["Single indicator", "Multidimensional indicators"])

    # ---- SIDEBAR ----

    with st.sidebar:

        url = "https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,'Turberculosis')"
        response = requests.get(url)
        if response.status_code == 200:
            st.caption("Connection to WHO API established successfully!")
        else:
            st.write("Error connecting to API. Status code:", response.status_code)

        ## List of WHO indicators
        who_indic_container = st.container()
        with who_indic_container:
            st.subheader("API explorer")
            disease = st.selectbox(
                'Display the list of indicators for: ',
                options=['Tuberculosis', 'Malaria', 'HIV'])

            # Import API data
            @st.cache(suppress_st_warning=True)
            def import_api_WHO_indicators(url):
                service_url0 = url
                response0 = requests.get(service_url0)
                if (response0.ok):
                    # get the full data from the response
                    data0j = response0.json()
                data0a = pd.DataFrame(data0j["value"])
                return data0a

            data0a = import_api_WHO_indicators("https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,'{}')".format(disease))
            option_indicators_name = st.selectbox('Display records for: ',data0a.IndicatorName.unique())
            selection_indicator_code = data0a[data0a['IndicatorName']==option_indicators_name][['IndicatorCode']].iloc[0][0]

            @st.cache(suppress_st_warning=True)
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


    with tab1:
        ## List of WHO indicators
        graphs = st.container()
        with graphs:

            # map hue category to a color
            c = dict(zip(df[hue].unique(), px.colors.qualitative.Plotly))

            col1, col2 = st.columns([3, 1])
            with col1:
                def generate_plot(hue):
                    fig = px.line(df.groupby(['Year', hue], as_index=False).mean(), x="Year", y="Value", color=hue,
                                  color_discrete_map=c,
                                  title="{}".format(option_indicators_name))
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        title=go.layout.Title(
                            text=fig.layout.title.text,
                            xref='paper',
                            x=0.5,
                            font=dict(size=20, color='white')
                        ),
                        legend=dict(
                            font=dict(size=15, color='white')
                        ),
                        xaxis=go.layout.XAxis(
                            tickfont=dict(size=15),
                            titlefont=dict(size=15),
                            showgrid=True,
                            gridcolor='#252323',
                            gridwidth=1
                        ),
                        yaxis=go.layout.YAxis(
                            tickfont=dict(size=15),
                            titlefont=dict(size=15),
                            showgrid=True,
                            gridcolor='#252323',
                            gridwidth=1
                        ),
                        height=600, margin={"r": 0, "t": 50, "l": 0, "b": 0}
                    )
                    for trace in fig.data:
                        trace.line.width = 2
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                if hue == 'Income level':
                    generate_plot('Income level')
                elif hue == 'Region':
                    generate_plot('Region')
                elif hue == 'Country':
                    # checkbox all countries
                    all = col1.checkbox("All countries", value=True)
                    if all:
                        selected_options = df.Country.unique()
                        generate_plot('Country')
                    else:
                        container = col1.container()
                        selected_options = container.multiselect("Select one or more countries:", df.sort_values('Country').Country.unique())
                        df_country = df[df["Country"].isin(selected_options)]
                        if len(selected_options) > 0:
                            fig = px.line(df_country.groupby(['Year','Country'], as_index=False).mean(), x="Year", y="Value",color ="Country",color_discrete_map=c, title = "{}".format(option_indicators_name))
                            fig.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                title=go.layout.Title(
                                    text=fig.layout.title.text,
                                    xref='paper',
                                    x=0.5,
                                    font=dict(size=20, color='white')
                                ),
                                legend=dict(
                                    font=dict(size=15, color='white')
                                ),
                                xaxis=go.layout.XAxis(
                                    tickfont=dict(size=15),
                                    titlefont=dict(size=15),
                                    showgrid=True,
                                    gridcolor='#252323',
                                    gridwidth=1
                                ),
                                yaxis=go.layout.YAxis(
                                    tickfont=dict(size=15),
                                    titlefont=dict(size=15),
                                    showgrid=True,
                                    gridcolor='#252323',
                                    gridwidth=1
                                ),
                                height=600, margin={"r": 0, "t": 50, "l": 0, "b": 0}
                            )
                            for trace in fig.data:
                                trace.line.width = 2
                            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            with col2:

                grouped_df = df.groupby([hue, 'Year']).mean().reset_index()
                year_max = grouped_df['Year'].max()
                year_max_min_val = round(grouped_df[grouped_df['Year'] == year_max]['Value'].min())
                year_max_max_val = round(grouped_df[grouped_df['Year'] == year_max]['Value'].max())
                year_min = grouped_df['Year'].min()
                year_min_min_val = round(grouped_df[grouped_df['Year'] == year_min]['Value'].min())
                year_min_max_val = round(grouped_df[grouped_df['Year'] == year_min]['Value'].max())


                # Get the last year from the "Year" column
                last_year = df['Year'].max()
                # Create a new DataFrame with only the rows from the last year
                df_last_year = df[df['Year'] == last_year]

                if (hue == "Country"):
                    if(len(selected_options) < len(df_last_year['Country'])):
                        df_last_year = df_last_year[df_last_year["Country"].isin(selected_options)]
                if (hue != "Country") or ((hue == "Country") and len(selected_options) > 0):
                    st.write("<p style='text-align: right;'>"
                             "{}: <br> ".format(year_min),
                             "Min value {}<br>".format(year_min_min_val),
                             "Max value {}<br><br>".format(year_min_max_val),
                             "{}: <br> ".format(year_max),
                             "Min value {}<br>".format(year_max_min_val),
                             "Max value {}".format(year_max_max_val),
                             unsafe_allow_html=True)


                    fig = px.choropleth(df_last_year, locations='Country', color=hue,color_discrete_map=c, locationmode='country names')
                    # Remove the background color
                    fig.update_layout(geo=dict(visible=False,bgcolor='rgba(0,0,0,0)',lakecolor='rgba(0,0,0,0)',landcolor='white',
                                                  subunitcolor='rgba(0,0,0,0)',showcountries=True,projection_type='natural earth',fitbounds="locations"))
                    fig.update_traces(marker_line_width=1)
                    #fig.update_geos()
                    # Remove the legend & Set the plot size
                    fig.update_layout(showlegend=False, width= 100, height=250, margin={"r":0,"t":0,"l":0,"b":0})
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


    # ---- SIDEBAR ----
    def sidebar():
        with st.sidebar:
            with st.expander("Read more about the World Health Organization (WHO)"):
                # WHO details
                st.markdown("<p style='text-align: justify'>"
                            "The <a href='https://www.who.int/'>World Health Organization (WHO) </a> plays a crucial role in the global health sector by leading efforts "
                            "to expand universal health coverage and coordinating the world's response to health emergencies. Its focus is on promoting healthier lives, "
                            "from pregnancy care through old age. <br> WHO has set ambitious targets known as the Triple Billion, which aim to achieve good health for all through science-based policies and programs.<br>"
                            " International health, which focuses on developing nations and foreign aid efforts, is one branch of public health in which WHO plays a leading role. "
                            "<br> While other important agencies also play a role in global health, WHO is considered the predominant agency associated with international health, and works "
                            "alongside various partners to achieve its mission.</p>", unsafe_allow_html=True)
            with st.expander("Accessing WHO API to load data"):
                # WHO details
                st.markdown("<p style='text-align: justify;'>"
                            "The WHO API <a href='https://www.who.int/data/gho/info/gho-odata-api#exe3'> (see documentation) </a> is providing access to 2,197 indicators at the time of writing"
                            ", but for simplicity we will only be displaying indicators related to the three epidemics targeted by the Global Fund (i.e. AIDS, tuberculosis and malaria)."
                            "<br>To offer more visualization options, we also imported the <a href='https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups'> World Bank regional groupings and Income group classifications </a> from the World Bank API and merged them with the country list from the WHO.",
                            unsafe_allow_html=True)
            with st.expander("What's an API?"):
                st.markdown("<p style='text-align: justify;'>"
                            "An API, or Application Programming Interface, allows different applications to communicate and exchange data with one another. "
                            "In the case of the World Health Organization (WHO), The Global Fund, and the World Bank, these organizations have created APIs "
                            "to increase transparency and provide better access to information for stakeholders in their activities."
                            "<a href='https://en.wikipedia.org/wiki/API'> <br>Read more on Wikipedia</a></p>",
                            unsafe_allow_html=True)

            st.caption("<p style='text-align: justify;'>"
                       "Disclaimer: <br /> All the data used and displayed is publicly available via the "
                       "<a href='https://www.who.int/data/gho/info/gho-odata-api#exe3'>WHO API </a></p>",
                       unsafe_allow_html=True)
    sidebar()



    # with st.expander("See code for importing the list of countries and information from the WHO & World Bank APIs "):
    #     st.code('''
    #     # Download the list of WHO countries:
    #
    #     def import_api_WHO_countries(url):
    #         service_url0 = url
    #         response0 = requests.get(service_url0)
    #         # make sure we got a valid response
    #         print(response0)
    #         if (response0.ok):
    #             # get the full data from the response
    #             data0j = response0.json()
    #         else:
    #             st.caption("API data cannot be loaded")
    #         country_list = pd.DataFrame(data0j["value"])
    #         return country_list
    #     with st.spinner('Loading country data from WHO API (it will take a few seconds the first time)'):
    #         country_list = import_api_WHO_countries("https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues")
    #         country_list.rename(columns={"Code": "SpatialDim", "Title": "Country"}, inplace=True)
    #
    #     # Download the list of World Bank country with Region and Income Level information:
    #
    #     WorldBank_countries = wb.economy.DataFrame().reset_index()[['id','name','aggregate','region','incomeLevel']]
    #     WorldBank_countries =  WorldBank_countries[WorldBank_countries['aggregate']==False].drop('aggregate', axis=1)
    #     WorldBank_countries['incomeLevel'] = WorldBank_countries['incomeLevel'].map({
    #                                 'LIC':'Low income country',
    #                                 'HIC':'High income country',
    #                                 'LMC':'Lower middle income country',
    #                                 'INX': 'Upper middle income country',
    #                                 'UMC':'Upper middle income country'})
    #     WorldBank_countries['region'] = WorldBank_countries['region'].map({
    #                                 'LCN':'Latin America & the Caribbean',
    #                                 'SAS':'South Asia',
    #                                 'SSF':'Sub-Saharan Africa',
    #                                 'ECS':'Europe and Central Asia',
    #                                 'MEA':'Middle East and North Africa',
    #                                 'EAS':'East Asia and Pacific',
    #                                 'NAC':'North America'})
    #     WorldBank_countries.rename(columns={"id":"SpatialDim","incomeLevel":"Income level","region":"Region"}, inplace = True)
    #     country_list = country_list.merge(WorldBank_countries, how='inner', on='SpatialDim')
    #                 ''', language='python')
    #
    # with st.expander("See code for the Streamlit App"):
    #     st.code('''
    #         # Downloading the list of WHO indicators based on selected input:
    #     who_indic_container = st.container()
    #     with who_indic_container:
    #         st.subheader("WHO indicators")
    #         col1, col2 = st.columns([1, 2])
    #         with col1:
    #             disease = st.selectbox(
    #                 'Display the list of indicators for: ',
    #                 options=['Tuberculosis', 'Malaria', 'HIV'])
    #             # Import API data
    #             @st.cache
    #             def import_api_WHO_indicators(url):
    #                 service_url0 = url
    #                 response0 = requests.get(service_url0)
    #                 # make sure we got a valid response
    #                 print(response0)
    #                 if (response0.ok):
    #                     # get the full data from the response
    #                     data0j = response0.json()
    #                 else:
    #                     st.caption("API data cannot be loaded")
    #                 data0a = pd.DataFrame(data0j["value"])
    #                 return data0a
    #             with st.spinner('Loading indicators data from WHO API (it will take a few seconds the first time)'):
    #                 data0a = import_api_WHO_indicators("https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,'{}')".format(disease))
    #
    #             option_indicators_name = st.selectbox('Display records for: ',data0a.IndicatorName.unique())
    #             selection_indicator_code = data0a[data0a['IndicatorName']==option_indicators_name][['IndicatorCode']].iloc[0][0]
    #
    #             @st.cache
    #             def import_api_WHO_indicator_name(url):
    #                 service_url0 = url
    #                 response0 = requests.get(service_url0)
    #                 # make sure we got a valid response
    #                 if (response0.ok):
    #                     # get the full data from the response
    #                     data0j = response0.json()
    #                 else:
    #                     st.caption("API data cannot be loaded")
    #                 return data0j
    #
    #             with st.spinner('Loading country data from WHO API (it will take a few seconds the first time)'):
    #                 data0j = import_api_WHO_indicator_name("https://ghoapi.azureedge.net/api/{}".format(selection_indicator_code))
    #                 data0a[data0a['IndicatorName'] == selection_indicator_code]['IndicatorCode'].reset_index(drop=True)
    #                 data0a = pd.DataFrame(data0j["value"])
    #             #merge with country info
    #             df = pd.merge(data0a,
    #                           country_list,
    #                           on='SpatialDim',
    #                           how='inner')
    #             df.rename(columns={"TimeDim":"Year","NumericValue":"Value"}, inplace = True)
    #             df = df[(df['SpatialDimType'] == 'COUNTRY') | (df['SpatialDimType'] == 'COUNTRY')][['Country','SpatialDim', 'Year', 'Value','ParentTitle','Region','Income level']]
    #             hue = st.radio("Display data per:", ('Region', 'Income level', 'Country'), horizontal=True)
    #
    #         with col2:
    #             if hue == 'Income level':
    #                 fig = px.line(df.groupby(['Year','Income level'], as_index=False).sum(), x="Year", y="Value", color="Income level", title = "{}".format(option_indicators_name))
    #                 fig.update_layout(paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)")
    #                 st.plotly_chart(fig, use_container_width=True)
    #             elif hue == 'Region':
    #                 fig = px.line(df.groupby(['Year','Region'], as_index=False).sum(), x="Year", y="Value", color="Region", title = "{}".format(option_indicators_name))
    #                 fig.update_layout(paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)")
    #                 st.plotly_chart(fig, use_container_width=True)
    #             elif hue == 'Country':
    #                 # checkbox all countries
    #                 all = col1.checkbox("All countries", value=True)
    #                 if all:
    #                     selected_options = df.Country.unique()
    #                     fig = px.line(df.groupby(['Year','Country'], as_index=False).mean(), x="Year", y="Value", color ="Country", title = "{}".format(option_indicators_name))
    #                     fig.update_layout(plot_bgcolor="rgb(255,255,255)")
    #                     st.plotly_chart(fig, use_container_width=True)
    #                 else:
    #                     container = col1.container()
    #                     selected_options = container.multiselect("Select one or more countries:", df.sort_values('Country').Country.unique())
    #                     df_country = df[df["Country"].isin(selected_options)]
    #                     fig = px.line(df_country.groupby(['Year','Country'], as_index=False).mean(), x="Year", y="Value",color ="Country", title = "{}".format(option_indicators_name))
    #                     fig.update_layout(plot_bgcolor="rgb(255,255,255)")
    #                     st.plotly_chart(fig, use_container_width=True)
    #         ''')
