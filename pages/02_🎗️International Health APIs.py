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
    color:#527a7a;   
    }
.st-bd {border-style: none;}
</style>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
with st.sidebar:
    st.caption("<p style='text-align: justify;'>"
                "Disclaimer: <br /> The information presented in this page is solely made by me in my private capacity. "
                " <br /> All the data used and displayed is publicly available via the "
                "<a href='https://www.who.int/data/gho/info/gho-odata-api#exe3'>WHO API </a>" 
                "and <a href='https://data-service.theglobalfund.org/api'>The Global Fund API </a>  pages. </p>",
                unsafe_allow_html=True)

# ---- HEADER SECTION ----

st.title("Using API to explore International Health data")

intro_container =  st.container()
with intro_container:

    api_container = st.container()
    with api_container:
        st.markdown("<p style='text-align: justify; font-size: 160%'>"
                    "<br>What is international health?"
                    "</p>"
                    "<p style='text-align: justify;'>"
                    "International health is defined as the branch of public health focusing on developing nations and"
                    " foreign aid efforts. <br> The predominant agency associated with global and international health is the"
                    " World Health Organization (WHO). Other important agencies are also involved with different missions:"
                    " funders, implementing partners etc.</p>",
                    unsafe_allow_html=True)
        with st.expander("Read more"):
            # WHO details
            col1, col2 = st.columns([1, 1])
            col1.markdown( "**The World Health Organization**"
                "<p style='text-align: justify;color:#3d5c5c'>"
                "The WHO leads global efforts to expand universal health coverage by directing and"
                " coordinating the world’s response to health emergencies. <br> It promotes healthier lives – from pregnancy care"
                " through old age. Its Triple Billion targets outline an ambitious plan for the world to achieve good health"
                " for all using science-based policies and programmes.</p>",unsafe_allow_html=True)
            col1.write("[WHO website](https://www.who.int/)")
            # The Global Fund details
            col2.markdown("**The Global Fund**"
                          "<p style='text-align: justify;color:#3d5c5c'>"
                            "The Global Fund (TGF) is a partnership designed to accelerate the end of AIDS, tuberculosis and "
                            "malaria as epidemics. <br> It prioritizes: results-based work, accountability, preparing countries"
                            " for graduation from aid, investing in people as assets for development and inclusive governance."
                            " To do so, the Global Fund mobilizes and invests more than US$4 billion a year to support programs "
                            "run by local experts in more than 100 countries in partnership with governments, civil society, "
                            "technical agencies, the private sector and people affected by the diseases.</p>",unsafe_allow_html=True)
            col2.write("[TGF website](https://www.theglobalfund.org/en/)")

    exploring_api_container =  st.container()
    with exploring_api_container:
        st.markdown("<p style='text-align: justify; font-size: 160%''>"
                    "Accessing API to load data"
                    "</p>", unsafe_allow_html=True)
        col1, colblank, col2, colblank2, col3 = st.columns([30, 1, 30, 1, 30])
        col1.markdown("<p style='text-align: justify;'>"
                    "The WHO API <a href='https://www.who.int/data/gho/info/gho-odata-api#exe3'> (link to documentation)</a>"
                      " is providing access to 2,197 indicators at the time of writing.<br>"
                    "To simplify data exploration here we will only display indicators related to the three epidemics "
                      "targeted by the Global Fund (i.e. AIDS, tuberculosis and malaria)."
                    "</p>", unsafe_allow_html=True)
        col2.markdown("<p style='text-align: justify;'>"
                    "The Global Fund API <a href='https://data-service.theglobalfund.org/api'> (link to documentation)</a>"
                      " is providing access to different data including: <br>Lookup Lists, Funding Allocations, Donors & Implementation Partners,"
                      " various Grants information, information on Resource Mobilization and several de-normalized views of all eligibility records"
                    "</p>", unsafe_allow_html=True)
        col3.markdown("<p style='text-align: justify;'>"
                    "In order to offer more visualization filtering we also imported the "
                    "<a href='https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups'> World Bank regional groupings and Income group classifications </a>"
                    " from the World Bank API through the Python wbgapi library and merged it with the country list from the WHO and Global Fund datasets.</p>",
                    unsafe_allow_html=True)
        with st.expander("Wait, what's an API?"):
            st.markdown("<p style='text-align: justify;color:#3d5c5c'>"
                        "<em>The term API stands for Application Programming Interface. "
                        "API enable applications, here our web app, to communicate with an external data source using simple commands. "
                        "<a href='https://en.wikipedia.org/wiki/API'> Wikipedia</a> defines it as a connection "
                        "between computers or between computer programs offering a service to other pieces of software."
                        "<br>In the case of the WHO, The Global Fund and the World Bank, all 3 APIs have been created by these organizations"
                        " with the purpose of ensuring transparency and a better access to information generated, "
                        "for the benefit of the stakeholders in their activities."
                        "</em></p>", unsafe_allow_html=True)


st.write("---")

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
            fig.update_layout(paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)")
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
                fig.update_layout(plot_bgcolor="rgb(255,255,255)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                container = col1.container()
                selected_options = container.multiselect("Select one or more countries:", df.sort_values('Country').Country.unique())
                df_country = df[df["Country"].isin(selected_options)]
                fig = px.line(df_country.groupby(['Year','Country'], as_index=False).mean(), x="Year", y="Value",color ="Country", title = "{}".format(option_indicators_name))
                fig.update_layout(plot_bgcolor="rgb(255,255,255)")
                st.plotly_chart(fig, use_container_width=True)

st.write("---")

## List of GF Disbursements
GF_container = st.container()
with GF_container:
    st.subheader("The Global Fund Disbursements")
    @st.cache
    def import_api_GF(url):
        service_url0 = url
        response0 = requests.get(service_url0)
        # make sure we got a valid response
        if (response0.ok):
            # get the full data from the response
            data0j = response0.json()
        else:
            st.caption("Global Fund API cannot be loaded")
        df1 = pd.DataFrame(data0j["value"])
        return df1

    with st.spinner('Loading all disbursements data from API (it will take a few seconds the first time)'):
        df1 = import_api_GF("https://data-service.theglobalfund.org/v3.3/odata/VGrantAgreementDisbursements")
        df1 = df1[df1["geographicAreaLevelName"] == 'Country'][['geographicAreaCode_ISO3',
                                                                'geographicAreaName',
                                                                'componentName',
                                                                'grantAgreementStatusTypeName',
                                                                'principalRecipientSubClassificationName',
                                                                'disbursementDate',
                                                                'disbursementAmount']]
    st.caption("Data loaded! A total number of {} disbursements records have been loaded.".format(len(df1)))
    st.markdown("<p style='text-align: justify;'>"
                "A disbursement corresponds to the transfer of a specific tranche of the Grant Funds for the implementation"
                " of Programs. You can go to <a href='https://www.theglobalfund.org/en/funding-model/'>this link</a> to know"
                " more about the organization Funding Model.<br>"
                "In order to explore the Global Fund Disbursement information we loaded the de-normalized view of all Grant Agreement "
                "Disbursements records."
                "</p>", unsafe_allow_html=True)
    #merge with country info
    df1.rename(columns={"geographicAreaCode_ISO3":"SpatialDim"}, inplace = True)
    df1 = pd.merge(df1,
                  country_list,
                  on='SpatialDim',
                  how='inner')

    # Component and Disbursements

    st.markdown("<p style='text-align: justify; font-size: 160%'>"
                "<br>Disbursements overview <br>"
                "</p>",
                unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        df_bar = df1.groupby(['componentName','Region'], as_index=False)['disbursementAmount'].sum()
        y = ['Multicomponent','RSSH','TB/HIV','Tuberculosis','Malaria','HIV']
        fig = px.bar(df_bar, y='componentName', x= 'disbursementAmount', color = 'Region')
        fig.update_layout(barmode='stack', yaxis={'categoryorder': 'array', 'categoryarray': y})
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = 'Disbursement amount ($)'
        fig.update_layout(
            autosize=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=50,
                pad=4,
                autoexpand=True
            ),
            width=800,
            height=350,
            title={
            'text' : 'Disbursements per component and region',
            'x':0.5,
            'xanchor': 'center'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_bar2 = df1.groupby(['Country'], as_index=False)['disbursementAmount'].sum().sort_values(by='disbursementAmount',ascending=True).tail(20)
        fig = px.bar(df_bar2, y='Country', x='disbursementAmount')
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = 'Disbursement amount ($)'
        fig.update_layout(
            autosize=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=50,
                pad=4,
                autoexpand=True),
            width=800,
            height=350,
            title={
            'text' : 'Top 20 disbursement receivers',
            'x':0.5,
            'xanchor': 'center'}
        )
        st.plotly_chart(fig, use_container_width=True)

    df_geo = df1.groupby(['componentName','geographicAreaName','SpatialDim'], as_index=False)['disbursementAmount'].sum().sort_values(by="disbursementAmount")
    fig = px.choropleth(df_geo, locations="SpatialDim",
                        color="disbursementAmount",  # lifeExp is a column of gapminder
                        hover_name="geographicAreaName",  # column to add to hover information
                        color_continuous_scale="Viridis",
                        height=580,
                        labels={'disbursementAmount': 'Disbursement amount ($)'},
                        title='Map of total disbursements'
                        )
    fig.update_layout(
        autosize=False,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50,
            pad=4,
            autoexpand=True
                        ),
        width=800,
        title={
        'text' : 'Map of total disbursements',
        'x':0.5,
        'xanchor': 'center'})

    st.plotly_chart(fig, use_container_width=True)

    # Data preparation for Sankey diagrame

    df2 = df1.groupby(['componentName', 'Region'], as_index=False)['disbursementAmount'].sum()
    df3 = df1.groupby(['Region', 'geographicAreaName'], as_index=False)['disbursementAmount'].sum()

    df2.columns = ['a', 'b', 'Quantity']
    df3.columns = ['a', 'b', 'Quantity']

    df4 = df2.append(df3)

    df4["Total disbursement"] = df4['Quantity']

    def genSankey(df, cat_cols=[], value_cols='', title='Sankey Diagram'):
        # maximum of 6 value cols -> 6 colors
        colorPalette = ['#FFD43B', '#646464']
        labelList = []
        colorNumList = []
        for catCol in cat_cols:
            labelListTemp = list(set(df[catCol].values))
            colorNumList.append(len(labelListTemp))
            labelList = labelList + labelListTemp

        # remove duplicates from labelList
        labelList = list(dict.fromkeys(labelList))

        # define colors based on number of levels
        colorList = []
        for idx, colorNum in enumerate(colorNumList):
            colorList = colorList + [colorPalette[idx]] * colorNum

        # transform df into a source-target pair
        for i in range(len(cat_cols) - 1):
            if i == 0:
                sourceTargetDf = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
                sourceTargetDf.columns = ['source', 'target', 'count']
            else:
                tempDf = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
                tempDf.columns = ['source', 'target', 'count']
                sourceTargetDf = pd.concat([sourceTargetDf, tempDf])
            sourceTargetDf = sourceTargetDf.groupby(['source', 'target']).agg({'count': 'sum'}).reset_index()

        # add index for source-target pair
        sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
        sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))

        # creating the sankey diagram
        data = dict(
            type='sankey',
            node=dict(
                pad=15,
                thickness=20,
                line=dict(
                    color="black",
                    width=0.5
                ),
                label=labelList,
                color = colorList
            ),
            link=dict(
                source=sourceTargetDf['sourceID'],
                target=sourceTargetDf['targetID'],
                value=sourceTargetDf['count']
            ),
            textfont = dict(size=15)
        )
        layout = dict(
            title=title,
            font=dict(size=12),
            height=825

        )

        fig = dict(data=[data], layout=layout)
        return fig

    fig = genSankey(df4, cat_cols=['a', 'b'], value_cols='Total disbursement', title='Sankey Diagram of The Global Fund Disbursements till date (G values should be read as Billion)')

    st.plotly_chart(fig, use_container_width=True)
