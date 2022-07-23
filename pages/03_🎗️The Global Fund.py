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
            "International health is defined as the branch of public health focusing on developing nations and"
            " foreign aid efforts. <br> The predominant agency associated with global and international health is the"
            " World Health Organization (WHO). Other important agencies are also involved with different missions such as:"
            " funders or implementing partners.</p>",unsafe_allow_html=True)


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

    #merge with country info
    df1.rename(columns={"geographicAreaCode_ISO3":"SpatialDim"}, inplace = True)
    df1 = pd.merge(df1,
                  country_list,
                  on='SpatialDim',
                  how='inner')


color_discrete_map={
                "HIV": "#fe9000",
                "Malaria": "#5b8e7d",
                "Tuberculosis": "#5adbff",
                "TB/HIV": "#3c6997",
                "RSSH": "#094074",
                "Multicomponent": "#ffdd4a"}

 #------------------------------------

col1, col01, col2, col02, col3 = st.columns([10,1,10,1,10])

# Filter component
option_map1 = col2.multiselect(
    'Filter component(s)',
    options=list(df1.componentName.sort_values(ascending=True).unique()),
    default=[])
if len(option_map1) == 0:
    df_group_compo = df1
else:
    df_group_compo = df1[df1["componentName"].isin(option_map1)]

# Fitler recipient
option_map2 = col3.multiselect(
    'Filter Principal Recipient type',
    options=list(df_group_compo.principalRecipientSubClassificationName.sort_values(ascending=True).unique()),
    default=[])
if len(option_map2) == 0:
    df1_filtered = df_group_compo
else:
    df1_filtered = df_group_compo[df_group_compo["principalRecipientSubClassificationName"].isin(option_map2)]

# Filter years
start_year, end_year = col1.select_slider(
    'Filter years',
    options=list(df1.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).unique()),
    value=(df1.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).min(),
           df1.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).max()))

# Filtered dataset:
df1_filtered_dates = df1_filtered[(df1_filtered.disbursementDate.astype('datetime64[ns]').dt.year >= start_year) & (
        df1_filtered.disbursementDate.astype('datetime64[ns]').dt.year <= end_year)]

col1, col2, col3= st.columns([30, 30, 30])
col1.metric("Disbursements ($)", "{:,}".format(round(df1_filtered_dates.disbursementAmount.sum())))
col2.metric("First disbursements", "{}".format(min(df1_filtered_dates.disbursementDate)))
col3.metric("Last disbursements", "{}".format(max(df1_filtered_dates.disbursementDate)))

tab1, tab2, tab3, tab4 = st.tabs(["Components overview 📈", "Regional overview 📈️", "Disbursements map 🗺️", "Download Data 🔢"])

df1_filtered_dates["Year"] = df1_filtered_dates.disbursementDate.astype('datetime64[ns]').dt.year
df1_filtered_dates["Year"] = df1_filtered_dates["Year"].astype(int)

with tab1:
    col1, col2 = st.columns([15, 15])
    df_line = df1_filtered_dates[["componentName", "disbursementAmount", "Year"]].groupby(["Year","componentName"]).sum().reset_index()
    fig = px.bar(df_line, x="Year", y="disbursementAmount", color="componentName",color_discrete_map=color_discrete_map)
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
        height=250,
        title={
            'text': 'Yearly disbursements',
            'x': 0.5,
            'xanchor': 'center'},
        # paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)"
    )
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ''
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''
    col1.plotly_chart(fig, use_container_width=True)

    df_line = df1_filtered_dates[["componentName", "disbursementAmount", "disbursementDate"]].sort_values(by="disbursementDate",
                                                                                           ascending=True)
    fig = px.line(df_line.join(df_line.groupby("componentName", as_index=False).cumsum(), rsuffix="_cumsum"),
                  y="disbursementAmount_cumsum", x="disbursementDate", color="componentName",color_discrete_map=color_discrete_map)
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
        height=250,
        title={
            'text': 'Cumulated disbursements',
            'x': 0.5,
            'xanchor': 'center'},
        #paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)"
    )
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ''
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''
    col1.plotly_chart(fig, use_container_width=True)

    df_bar = df1_filtered_dates.groupby(['componentName'], as_index=False)['disbursementAmount'].sum()
    y = ['Multicomponent', 'RSSH', 'TB/HIV', 'Tuberculosis', 'Malaria', 'HIV']
    fig = px.bar(df_bar, y='componentName', x='disbursementAmount',color = 'componentName',
                 text_auto=True, color_discrete_map=color_discrete_map)
    fig.update_layout(barmode='stack', yaxis={'categoryorder': 'array', 'categoryarray': y})
                      #paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)")
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
        height=500,
        title={
            'text': 'Disbursements per component',
            'x': 0.5,
            'xanchor': 'center'}
    )
    col2.plotly_chart(fig, use_container_width=True)


# Regional overview
with tab2:
    col1, col2 = st.columns([15, 15])
    df_line = df1_filtered_dates[["Region", "disbursementAmount", "Year"]].groupby(["Year","Region"]).sum().reset_index()
    fig = px.bar(df_line, x="Year", y="disbursementAmount", color="Region", color_discrete_map=color_discrete_map)
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
        height=250,
        title={
            'text': 'Yearly disbursements',
            'x': 0.5,
            'xanchor': 'center'},
        # paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)"
    )
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ''
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''
    col1.plotly_chart(fig, use_container_width=True)


    df_line = df1_filtered_dates[["Region", "disbursementAmount", "disbursementDate"]].sort_values(by="disbursementDate",
                                                                                           ascending=True)
    fig = px.line(df_line.join(df_line.groupby("Region", as_index=False).cumsum(), rsuffix="_cumsum"),
                  y="disbursementAmount_cumsum", x="disbursementDate", color="Region", color_discrete_map=color_discrete_map)
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
        height=250,
        title={
            'text': 'Cumulated regional disbursements',
            'x': 0.5,
            'xanchor': 'center'}
    )
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ''
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''
    col1.plotly_chart(fig, use_container_width=True)


    df_bar2 = df1_filtered_dates.groupby(['Country'], as_index=False)['disbursementAmount'].sum().sort_values(
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
        height=500,
        title={
            'text': 'Top 10 disbursement receivers',
            'x': 0.5,
            'xanchor': 'center'}
        #paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)"
    )
    col2.plotly_chart(fig, use_container_width=True)

    #Disbursement map
    with tab3:

        df_geo = df1_filtered_dates.groupby(['geographicAreaName', 'SpatialDim'], as_index=False)[
            'disbursementAmount'].sum().sort_values(by="disbursementAmount")
        fig = px.choropleth(df_geo, locations="SpatialDim",
                            color="disbursementAmount",  # lifeExp is a column of gapminder
                            hover_name="geographicAreaName",  # column to add to hover information
                            color_continuous_scale="Blues",
                            height=600,
                            labels={'disbursementAmount': 'Disbursement amount ($)'},
                            title='Map of total disbursements'
                            )
        fig.update_layout(
            autosize=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=4,
                autoexpand=True
            ),
            title={
                'text': 'Map of total disbursements',
                'x': 0.5,
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


    with tab4:

        col1, col2 = st.columns([5, 20])

        #Dataframe wrangler
        groupby = col1.radio(
            "Which dataset do you want?",
            ('Keep the same filters','All disbursements records', 'Filtered by country', 'Filtered by component', 'Filtered by year'))

        if groupby == 'Keep the same filters':
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(
                    ["Country", "Component", "Principal Recipient", "Disbursement date", "Disbursement amount"]),
                            fill_color='Grey',
                            align='left'),
                cells=dict(values=[df1_filtered_dates.Country, df1_filtered_dates.componentName, df1_filtered_dates.principalRecipientSubClassificationName,
                                   df1_filtered_dates.disbursementDate, df1_filtered_dates.disbursementAmount],
                           # fill_color='lavender',
                           font=dict(color='black', family="arial"),
                           align='left'))
            ])
            fig.update_layout(height=500, margin=dict(r=5, l=5, t=5, b=5))
            col2.plotly_chart(fig, use_container_width=False)

        if groupby == 'All disbursements records':
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(
                    ["Country", "Component", "Principal Recipient", "Disbursement date", "Disbursement amount"]),
                            fill_color='Grey',
                            align='left'),
                cells=dict(values=[df1_filtered_dates.Country, df1.componentName, df1.principalRecipientSubClassificationName,
                                   df1.disbursementDate, df1.disbursementAmount],
                           # fill_color='lavender',
                           font=dict(color='black', family="arial"),
                           align='left'))
            ])
            fig.update_layout(height=500, margin=dict(r=5, l=5, t=5, b=5))
            col2.plotly_chart(fig, use_container_width=False)

        if groupby == 'Filtered by country':
            option = col1.selectbox(
                'Select country',
                (list(df1.Country.sort_values(ascending=True).unique()))
            )
            df_group = df1[df1["Country"]==option]
            df_group.sort_values(by="disbursementDate",ascending = True, inplace = True)
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(
                    ["Country", "Component", "Principal Recipient", "Disbursement date", "Disbursement amount"]),
                    fill_color='Grey',
                    align='left',
                    font=dict(color='white',size = 14, family="arial")),
                cells=dict(values=[df_group.Country,
                                   df_group.componentName,
                                   df_group.principalRecipientSubClassificationName,
                                   df_group.disbursementDate,
                                   df_group.disbursementAmount],
                           # fill_color='lavender',
                           font=dict(color='black', family="arial"),
                           align='left'))
            ])
            fig.update_layout(height=500, margin=dict(r=5, l=5, t=5, b=5))
            col2.plotly_chart(fig, use_container_width=False)

        if groupby == 'Filtered by component':
            option = col1.selectbox(
                'Select component',
                (list(df1.componentName.sort_values(ascending=True).unique()))
            )
            df_group = df1[df1["componentName"]==option]
            df_group.sort_values(by="disbursementDate",ascending = True, inplace = True)
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(
                    ["Country", "Component", "Principal Recipient", "Disbursement date", "Disbursement amount"]),
                    fill_color='Grey',
                    align='left',
                    font=dict(color='white',size = 14, family="arial")),
                cells=dict(values=[df_group.Country,
                                   df_group.componentName,
                                   df_group.principalRecipientSubClassificationName,
                                   df_group.disbursementDate,
                                   df_group.disbursementAmount],
                           # fill_color='lavender',
                           font=dict(color='black', family="arial"),
                           align='left'))
            ])
            fig.update_layout(height=500, margin=dict(r=5, l=5, t=5, b=5))
            col2.plotly_chart(fig, use_container_width=False)

        if groupby == 'Filtered by year':
            option = col1.selectbox(
                'Select country',
                (list(df1.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).unique()))
            )
            df_group = df1[df1["disbursementDate"].astype('datetime64[ns]').dt.year == option]
            df_group.sort_values(by="disbursementDate",ascending = True, inplace = True)
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(
                    ["Country", "Component", "Principal Recipient", "Disbursement date", "Disbursement amount"]),
                    fill_color='Grey',
                    align='left',
                    font=dict(color='white',size = 14, family="arial")),
                cells=dict(values=[df_group.Country,
                                   df_group.componentName,
                                   df_group.principalRecipientSubClassificationName,
                                   df_group.disbursementDate,
                                   df_group.disbursementAmount],
                           # fill_color='lavender',
                           font=dict(color='black', family="arial"),
                           align='left'))
            ])
            fig.update_layout(height=500, margin=dict(r=5, l=5, t=5, b=5))
            col2.plotly_chart(fig, use_container_width=False)

        if groupby == 'Keep the same filters':
            dl_file = df1_filtered_dates
        else:
            if groupby == 'All disbursements records' :
                dl_file = df1[["Country", "componentName", "principalRecipientSubClassificationName", "disbursementDate",
                               "disbursementAmount"]]
                dl_file.columns = ["Country", "Component", "Principal Recipient", "Disbursement date",
                                   "Disbursement amount"]
            else:
                dl_file = df_group

        @st.cache
        def convert_df(dl_file):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return dl_file.to_csv().encode('utf-8')
        csv = convert_df(dl_file)
        col1.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='GF_Disbursements_API.csv',
            key='download-csv',
        )



    st.markdown("<p style='text-align: justify; font-size: 110%'>"
                "Recipients overview <br>"
                "</p>",
                unsafe_allow_html=True)


    col1, col2, col3= st.columns([30, 30, 30])
    col1.metric("Total countries", "${}B".format(round(df1.disbursementAmount.sum()/1000000000,2)))
    col1.metric("Total Principal Recipients:", "{}".format(min(df1.disbursementDate)))
    col1.metric("Recipients this year", "{}".format(max(df1.disbursementDate)))




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
# GF_container = st.container()
# with GF_container:
#     st.markdown("<p style='text-align: justify; font-size: 160%'>"
#                 "Grant Agreement Implementation Periods <br>"
#                 "</p>",
#                 unsafe_allow_html=True)
#     @st.cache
#     def import_api_GF(url):
#         service_url0 = url
#         response0 = requests.get(service_url0)
#         # make sure we got a valid response
#         print(response0)
#         if (response0.ok):
#             # get the full data from the response
#             data0j = response0.json()
#         else:
#             st.caption("Global Fund API cannot be loaded")
#         df1 = pd.DataFrame(data0j["value"])
#         return df1
#
#     with st.spinner('Loading data from API (it will take a few seconds the first time)'):
#         df1 = import_api_GF("https://data-service.theglobalfund.org/v3.3/odata/VGrantAgreementImplementationPeriods")
#     st.caption("Data loaded! A total number of {} Grant Agreement Implementation Periods records have been loaded.".format(len(df1)))
#     st.write("I am still working on it but you can have a peak at the imported dataframe we will be using below:")
#     df1
