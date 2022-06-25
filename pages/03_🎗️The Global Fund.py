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
               "<a href='https://data-service.theglobalfund.org/api'>The Global Fund API </a></p>",
                unsafe_allow_html=True)

# ---- HEADER SECTION ----

st.title("Using API to explore International Health data: The Global Fund")

intro_container =  st.container()
with intro_container:

    api_container = st.container()
    with api_container:
        st.markdown("<p style='text-align: justify; font-size: 160%'>"
                    "<br>The Global Fund"
                    "</p>"
                    "<p style='text-align: justify;'>"
                    "<a href='https://www.theglobalfund.org/en/'>The Global Fund </a> is a partnership designed to accelerate the end of AIDS, tuberculosis and "
                            "malaria as epidemics. <br> It prioritizes: results-based work, accountability, preparing countries"
                            " for graduation from aid, investing in people as assets for development and inclusive governance."
                            " To do so, the Global Fund mobilizes and invests more than US$4 billion a year to support programs "
                            "run by local experts in more than 100 countries in partnership with governments, civil society, "
                            "technical agencies, the private sector and people affected by the diseases.</p>",
                    unsafe_allow_html=True)
        with st.expander("Read more about international health"):
            # The Global Fund details
            st.markdown("<p style='text-align: justify;color:#3d5c5c'>"
            "<em>International health is defined as the branch of public health focusing on developing nations and"
            " foreign aid efforts. <br> The predominant agency associated with global and international health is the"
            " World Health Organization (WHO). Other important agencies are also involved with different missions:"
            " funders, implementing partners etc.</em></p>",unsafe_allow_html=True)


    exploring_api_container =  st.container()
    with exploring_api_container:
        st.markdown("<p style='text-align: justify; font-size: 160%''>"
                    "Accessing API to load data"
                    "</p>", unsafe_allow_html=True)
        col1, colblank, col2 = st.columns([30, 1, 30])
        col1.markdown("<p style='text-align: justify;'>"
                    "The Global Fund API <a href='https://data-service.theglobalfund.org/api'> (link to documentation)</a>"
                      " is providing access to different data including: <br>Lookup Lists, Funding Allocations, Donors & Implementation Partners,"
                      " various Grants information, information on Resource Mobilization and several de-normalized views of all eligibility records."
                    "</p>", unsafe_allow_html=True)
        col2.markdown("<p style='text-align: justify;'>"
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

## List of GF Disbursements
GF_container = st.container()
with GF_container:
    st.markdown("<p style='text-align: justify; font-size: 160%'>"
                "Disbursements records <br>"
                "</p>",
                unsafe_allow_html=True)
    @st.cache
    def import_api_GF(url):
        service_url0 = url
        response0 = requests.get(service_url0)
        # make sure we got a valid response
        print(response0)
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
        df1['disbursementDate'] =  pd.to_datetime(df1.disbursementDate).dt.date

    st.markdown("<p style='text-align: justify;'>"
                "A disbursement corresponds to the transfer of a specific tranche of the Grant Funds for the implementation"
                " of Programs. You can go to <a href='https://www.theglobalfund.org/en/funding-model/'>this link</a> to know"
                " more about the organization Funding Model.<br>"
                "In order to explore the Global Fund Disbursement information we loaded the de-normalized view of all Grant Agreement "
                "Disbursements records. <br>"
                "</p>", unsafe_allow_html=True)

    col1, col2, col3= st.columns([15, 30, 30])
    col1.markdown("<p style='text-align: justify; font-size: 110%'>"
                "Records overview <br>"
                "</p>",
                unsafe_allow_html=True)
    col1.metric("Total disbursements", "${}B".format(round(df1.disbursementAmount.sum()/1000000000,2)))
    col1.metric("First record", "{}".format(min(df1.disbursementDate)))
    col1.metric("Last record", "{}".format(max(df1.disbursementDate)))

    #merge with country info
    df1.rename(columns={"geographicAreaCode_ISO3":"SpatialDim"}, inplace = True)
    df1 = pd.merge(df1,
                  country_list,
                  on='SpatialDim',
                  how='inner')


    #------------------------------------

    # Component overview
    component_container = st.container()
    with component_container:
        df_line = df1[["componentName", "disbursementAmount", "disbursementDate"]].sort_values(by="disbursementDate",
                                                                                               ascending=True)
        fig = px.line(df_line.join(df_line.groupby("componentName", as_index=False).cumsum(), rsuffix="_cumsum"),
                      y="disbursementAmount_cumsum", x="disbursementDate", color="componentName")
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
                'text': 'Cumulated disbursements',
                'x': 0.5,
                'xanchor': 'center'},
            paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)"
        )
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''
        col2.plotly_chart(fig, use_container_width=True)

        df_bar = df1.groupby(['componentName'], as_index=False)['disbursementAmount'].sum()
        y = ['Multicomponent', 'RSSH', 'TB/HIV', 'Tuberculosis', 'Malaria', 'HIV']
        fig = px.bar(df_bar, y='componentName', x='disbursementAmount', text_auto=True)
        fig.update_layout(barmode='stack', yaxis={'categoryorder': 'array', 'categoryarray': y},
                          paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)")
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''
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
                'text': 'Disbursements per component and region',
                'x': 0.5,
                'xanchor': 'center'}
        )
        col3.plotly_chart(fig, use_container_width=True)


    # Region overview
    st.markdown("<p style='text-align: justify; font-size: 120%'>"
                "Regional overview <br>"
                "</p>",
                unsafe_allow_html=True)
    region_container = st.container()
    with region_container:
        col1, col2 = st.columns(2)
        df_line = df1[["Region", "disbursementAmount", "disbursementDate"]].sort_values(by="disbursementDate",
                                                                                               ascending=True)
        fig = px.line(df_line.join(df_line.groupby("Region", as_index=False).cumsum(), rsuffix="_cumsum"),
                      y="disbursementAmount_cumsum", x="disbursementDate", color="Region")
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
                'text': 'Cumulated disbursements per region',
                'x': 0.5,
                'xanchor': 'center'},
            paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)"
        )
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''
        col1.plotly_chart(fig, use_container_width=True)

        df_bar2 = df1.groupby(['Country'], as_index=False)['disbursementAmount'].sum().sort_values(
            by='disbursementAmount', ascending=True).tail(10)
        fig = px.bar(df_bar2, y='Country', x='disbursementAmount', text_auto=True)
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''
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
                'text': 'Top 10 disbursement receivers',
                'x': 0.5,
                'xanchor': 'center'},
            paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)"
        )
        col2.plotly_chart(fig, use_container_width=True)


    df_geo = df1.groupby(['componentName','geographicAreaName','SpatialDim'], as_index=False)['disbursementAmount'].sum().sort_values(by="disbursementAmount")
    fig = px.choropleth(df_geo, locations="SpatialDim",
                        color="disbursementAmount",  # lifeExp is a column of gapminder
                        hover_name="geographicAreaName",  # column to add to hover information
                        color_continuous_scale="Blues",
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
        'xanchor': 'center'},
        geo=dict(
            visible=False,
            landcolor='gray',
            showland=True,
            showcountries=True,
            countrycolor='dark gray',
            countrywidth=0.5,
            projection=dict(
                type='natural earth'
                            )
                )
    )

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


## List of GF Disbursements
GF_container = st.container()
with GF_container:
    st.markdown("<p style='text-align: justify; font-size: 160%'>"
                "Grant Agreement Implementation Periods <br>"
                "</p>",
                unsafe_allow_html=True)
    @st.cache
    def import_api_GF(url):
        service_url0 = url
        response0 = requests.get(service_url0)
        # make sure we got a valid response
        print(response0)
        if (response0.ok):
            # get the full data from the response
            data0j = response0.json()
        else:
            st.caption("Global Fund API cannot be loaded")
        df1 = pd.DataFrame(data0j["value"])
        return df1

    with st.spinner('Loading all disbursements data from API (it will take a few seconds the first time)'):
        df1 = import_api_GF("https://data-service.theglobalfund.org/v3.3/odata/VGrantAgreementImplementationPeriods")
    st.caption("Data loaded! A total number of {} Grant Agreement Implementation Periods records have been loaded.".format(len(df1)))
    st.write("I am still working on it but you can have a peak at the imported dataframe we will be using below:")
    df1
