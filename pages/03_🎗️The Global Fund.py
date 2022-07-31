import streamlit as st
import requests
import pandas as pd
import wbgapi as wb
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie

# emojis list: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="GF API explorer", page_icon="🎗", layout="wide")

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

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

# ---- SIDEBAR ----
with st.sidebar:
    with st.expander("Read more about The Global Fund"):
        # The Global Fund details
        st.markdown("<p style='text-align: justify;'>"
                "<a href='https://www.theglobalfund.org/en/'>The Global Fund </a> is a partnership designed to accelerate the end of AIDS, tuberculosis and "
                "malaria as epidemics. <br> It prioritizes: results-based work, accountability, preparing countries"
                " for graduation from aid, investing in people as assets for development and inclusive governance."
                " To do so, the Global Fund mobilizes and invests more than US$4 billion a year to support programs "
                "run by local experts in more than 100 countries in partnership with governments, civil society, "
                "technical agencies, the private sector and people affected by the diseases. <br><br>"
                "The Global Fund API <a href='https://data-service.theglobalfund.org/api'> (link to documentation)</a>"
                      " is providing access to different data including: <br>Lookup Lists, Funding Allocations, Donors & Implementation Partners,"
                      " various Grants information, information on Resource Mobilization and several de-normalized views of all eligibility records.</p>",
                unsafe_allow_html=True)
    with st.expander("What's an API?"):
        st.markdown("<p style='text-align: justify;'>"
                    "The term API stands for Application Programming Interface. "
                    "API enable applications, here our web app, to communicate with an external data source using simple commands. "
                    "<a href='https://en.wikipedia.org/wiki/API'> Wikipedia</a> defines it as a connection "
                    "between computers or between computer programs offering a service to other pieces of software."
                    "<br>In the case of the WHO, The Global Fund and the World Bank, all 3 APIs have been created by these organizations"
                    " with the purpose of ensuring transparency and a better access to information generated, "
                    "for the benefit of the stakeholders in their activities.<br>"
                    "In order to offer more filter options in this app I also imported the "
                    "<a href='https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups'> World Bank regional groupings and Income group classifications </a>"
                    " from the World Bank API through the Python wbgapi library and merged it with the country list from the WHO and Global Fund datasets."
                    "</p>", unsafe_allow_html=True)
    st.caption("<p style='text-align: justify;'>"
                "Disclaimer: <br /> The information presented in this page is solely made by me in my private capacity. "
                " <br /> All the data used and displayed is publicly available via the "
               "<a href='https://data-service.theglobalfund.org/api'>The Global Fund API </a></p>",
                unsafe_allow_html=True)


st.title("Global Fund API explorer")
col1, col2 = st.columns([20,50],gap='medium')
dataset = col1.radio("",('Disbursement records', 'Grant Agreements', 'Implementation periods'))


if dataset == "Disbursement records":
    col2.markdown("<p style='text-align: justify; font-size: 160%'>"
            "Disbursements records"
            "</p>"
            "<p style='text-align: justify;font-size: 90%''>"
            "A disbursement corresponds to the transfer of a specific tranche of the grant funds for the implementation"
            " of Programs. You can visit <a href='https://www.theglobalfund.org/en/funding-model/'>this page</a> to know"
            " learn about the organization Funding Model."
            " In order to visualize disbursement information data we load and explore the API de-normalized view of all Grant Agreement "
            "Disbursements records. <br> "
            "<span style='color:grey'>Loading data takes a few seconds the first time</span> </p>", unsafe_allow_html=True)
    st.write("---")
    ## List of WHO countries
    @st.cache(show_spinner=False)
    def import_api_WHO_countries(url):
        service_url0 = url
        response0 = requests.get(service_url0)
        # make sure we got a valid response
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

    # Loading GF API
    count = 0
    gif_runner = st.empty()
    @st.cache(show_spinner=False,suppress_st_warning=True,allow_output_mutation=True)
    def Loading_API(url):
        # check if first load, if so it will take a few sec to load so we want to display a nice gif
        global count
        count += 1
        if count == 1:
            global gif_runner
            gif_runner = st.markdown("![Alt Text](https://media.giphy.com/media/l0MYvEEv2Zndet9hC/giphy.gif)", unsafe_allow_html=True)

        # reading api
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

    #-------- TEST Lottie

    with open(".Images/lottie_loading.json", "r") as f:
        data = json.load(f)
    st_lottie(data)

#--------

    df1 = Loading_API("https://data-service.theglobalfund.org/v3.3/odata/VGrantAgreementDisbursements")
    df1.principalRecipientSubClassificationName.fillna('Not indicated',inplace=True)

    gif_runner.empty()

    df1 = df1[df1["geographicAreaLevelName"] == 'Country'][['geographicAreaCode_ISO3',
                                                            'geographicAreaName',
                                                            'componentName',
                                                            'grantAgreementStatusTypeName',
                                                            'principalRecipientSubClassificationName',
                                                            'disbursementDate',
                                                            'disbursementAmount']]
    df1['disbursementDate'] =  df1['disbursementDate'].astype('datetime64[ns]')
    df1['disbursementDate'] = df1['disbursementDate'].dt.date

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

    color_discrete_map2={
                    "Sub-Saharan Africa": "#0081a7",
                    "East Asia and Pacific": "#b392ac",
                    "Europe and Central Asia": "#02c39a",
                    "Latin America & the Caribbean": "#fdfcdc",
                    "Middle East and North Africa": "#736ced",
                    "South Asia": "#f07167"}

     #------------------------------------


    #clear filters button
    def clear_multi():
        for key in st.session_state.keys():
            st.session_state[key] = []

    col1, col2, col3, col4 = st.columns([10,10,10,2],gap='medium')

    # Component filter
    option_map1 = col2.multiselect(
        'Filter component(s)',
        options=list(df1.componentName.sort_values(ascending=True).unique()),
        key= "component_multiselect")
    if len(option_map1) == 0:
        df_group_compo = df1
    else:
        df_group_compo = df1[df1["componentName"].isin(option_map1)]

    # Principal recipient filter
    option_map2 = col3.multiselect(
        'Filter Principal Recipient type',
        options=list(df_group_compo.principalRecipientSubClassificationName.sort_values(ascending=True).unique()),
        key= "pr_multiselect")
    if len(option_map2) == 0:
        df1_filtered = df_group_compo
    else:
        df1_filtered = df_group_compo[df_group_compo["principalRecipientSubClassificationName"].isin(option_map2)]

    # Timeline filter
    start_year, end_year = col1.select_slider(
        'Disbursement year range',
        options=list(df1.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).unique()),
        value=(df1.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).min(),
               df1.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).max()))

    # Filtered dataset:
    df1_filtered_dates = df1_filtered[(df1_filtered.disbursementDate.astype('datetime64[ns]').dt.year >= start_year) & (
            df1_filtered.disbursementDate.astype('datetime64[ns]').dt.year <= end_year)]

    col1, col2, col3= st.columns([30, 30, 30])
    col1.metric("Disbursements ($)", "{:,}".format(round(df1_filtered_dates.disbursementAmount.sum())))
    col2.metric("First record", "{}".format(min(df1_filtered_dates.disbursementDate)))
    col3.metric("Last record", "{}".format(max(df1_filtered_dates.disbursementDate)))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Components overview 📈", "Regional overview 📈️", "Disbursements map 🗺️","Components - Region - Country (Sankey Diagram) 📍", "Download Data 🔢"])

    df1_filtered_dates["Year"] = df1_filtered_dates.disbursementDate.astype('datetime64[ns]').dt.year
    df1_filtered_dates["Year"] = df1_filtered_dates["Year"].astype(int)

    # Reset filters button
    col4.write("")
    col4.write("")
    col4.button("Clear filters", on_click= clear_multi)

    with tab1:
        col1, col2, col3 = st.columns([15, 15, 15])
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
            #width=800,
            height=600,
            title={
                'text': 'Yearly disbursements ($)',
                'x': 0.5,
                'xanchor': 'center'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                yanchor="top",
                orientation="h",
                title="Component")
        )
        fig.update_xaxes(showgrid=False, zeroline=True)
        fig.update_yaxes(showgrid=True, zeroline=True)
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''
        col1.plotly_chart(fig, use_container_width=True)

        fig = px.area(df_line,
                      y = "disbursementAmount",
                      x = "Year",
                      color = "componentName",
                      color_discrete_map=color_discrete_map,
                      groupnorm='percent')
        fig.update_layout(
            autosize=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=50,
                pad=4,
                autoexpand=True),
            #width=800,
            height=600,
            title={
                'text': 'Yearly disbursements normalized (%)',
                'x': 0.5,
                'xanchor': 'center'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        fig.update_xaxes(showgrid=False, zeroline=True)
        fig.update_yaxes(showgrid=False, zeroline=True)
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''
        col2.plotly_chart(fig, use_container_width=True)


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
            #width=800,
            height=600,
            title={
                'text': 'Total per component ($)',
                'x': 0.5,
                'xanchor': 'center'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        fig.update_xaxes(showgrid=False, zeroline=True)
        fig.update_yaxes(showgrid=False, zeroline=False)
        col3.plotly_chart(fig, use_container_width=True)

    # Regional overview
    with tab2:
        col1, col2, col3 = st.columns([15, 15, 15],gap='medium')
        df_line = df1_filtered_dates[["Region", "disbursementAmount", "Year"]].groupby(["Year","Region"]).sum().reset_index()
        fig = px.bar(df_line, x="Year", y="disbursementAmount", color="Region", color_discrete_map=color_discrete_map2)
        fig.update_layout(
            autosize=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=50,
                pad=4,
                autoexpand=True),
            #width=800,
            height=600,
            title={
                'text': 'Yearly disbursements ($)',
                'x': 0.5,
                'xanchor': 'center'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                yanchor="top",
                orientation="h")
        )
        fig.update_xaxes(showgrid=False, zeroline=True)
        fig.update_yaxes(showgrid=True, zeroline=True)
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''
        col1.plotly_chart(fig, use_container_width=True)

        fig = px.area(df_line,
                      y = "disbursementAmount",
                      x = "Year",
                      color = "Region",
                      color_discrete_map=color_discrete_map2,
                      groupnorm='percent')
        fig.update_layout(
            autosize=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=50,
                pad=4,
                autoexpand=True),
            #width=800,
            height=600,
            title={
                'text': 'Yearly disbursements normalized (%)',
                'x': 0.5,
                'xanchor': 'center'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        fig.update_xaxes(showgrid=False, zeroline=True)
        fig.update_yaxes(showgrid=False, zeroline=True)
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.YAxis:
                fig.layout[axis].title.text = ''
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''
        col2.plotly_chart(fig, use_container_width=True)


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
            height=600,
            title={
                'text': 'Top 10 disbursement receivers',
                'x': 0.5,
                'xanchor': 'center'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_xaxes(showgrid=False, zeroline=True)
        fig.update_yaxes(showgrid=False, zeroline=False)
        fig.update_traces(marker_color='#003566',opacity=1)
        col3.plotly_chart(fig, use_container_width=True)

        #Disbursement map
        with tab3:

            df_geo = df1_filtered_dates.groupby(['geographicAreaName', 'SpatialDim'], as_index=False)[
                'disbursementAmount'].sum().sort_values(by="disbursementAmount")

            fig = go.Figure(
                data=go.Choropleth(
                    locations=df_geo["SpatialDim"],
                    z = df_geo['disbursementAmount'],
                    colorscale  = "Blues",
                    showscale=True
                ),
                layout = go.Layout(height=500,
                                   margin=dict(
                                       l=0,
                                       r=10,
                                       b=0,
                                       t=0,
                                       pad=4,
                                       autoexpand=True
                                   ),
                                   geo=dict(bgcolor='rgba(0,0,0,0)',
                                            lakecolor='#4E5D6C',
                                            visible=False,
                                            landcolor='#3d3d3d',
                                            showland=True,
                                            showcountries=True,
                                            countrycolor='#5c5c5c',
                                            countrywidth=0.5,
                                            projection=dict(
                                                type='natural earth'
                                            )
                                            ))
            )


            st.plotly_chart(fig, use_container_width=True)

    # Sankey diagriam
        with tab4:
            # Data preparation for Sankey diagrame

            df1_sankey = df1_filtered_dates
            df1_sankey["GF"] = "Global Fund"
            df1_sankey = df1_sankey.groupby(['GF', 'componentName'], as_index=False)['disbursementAmount'].sum()
            df2 = df1_filtered_dates.groupby(['componentName', 'Region'], as_index=False)['disbursementAmount'].sum()
            df3 = df1_filtered_dates.groupby(['Region', 'geographicAreaName'], as_index=False)['disbursementAmount'].sum()

            df1_sankey.columns = ['a', 'b', 'Quantity']
            df2.columns = ['a', 'b', 'Quantity']
            df3.columns = ['a', 'b', 'Quantity']

            df4 = df1_sankey.append(df2)
            df5 = df4.append(df3)

            df5["Total disbursement"] = df5['Quantity']


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
                        color=colorList
                    ),
                    link=dict(
                        source=sourceTargetDf['sourceID'],
                        target=sourceTargetDf['targetID'],
                        value=sourceTargetDf['count']
                    ),
                    textfont=dict(size=15)
                )
                layout = dict(
                    title=title,
                    font=dict(size=12),
                    height=825

                )

                fig = dict(data=[data], layout=layout)
                return fig


            fig = genSankey(df5, cat_cols=['a', 'b'], value_cols='Total disbursement',
                            title='Sankey Diagram of The Global Fund Disbursements till date')

            st.plotly_chart(fig, use_container_width=True)

        with tab5:

            col1, col2 = st.columns([8, 20])

            #Dataframe wrangler
            groupby = col1.radio(
                "Which dataset do you want?",
                ('Keep the same filters','Focus on a specific country','All disbursements records'))

            if groupby == 'All disbursements records':
                dl_file = df1[["Country", "componentName", "principalRecipientSubClassificationName", "disbursementDate", "disbursementAmount"]].sort_values(by="disbursementDate",ascending = True)
                dl_file.columns = ["Country", "Component", "Principal Recipient", "Disbursement date", "Disbursement amount ($)"]

            if groupby == 'Keep the same filters':
                dl_file = df1_filtered_dates[["Country", "componentName", "principalRecipientSubClassificationName", "disbursementDate", "disbursementAmount"]].sort_values(by="disbursementDate",ascending = True)
                dl_file.columns = ["Country", "Component", "Principal Recipient", "Disbursement date", "Disbursement amount ($)"]

            if groupby == 'Focus on a specific country':
                option = col1.selectbox(
                    'Select country',
                    (list(df1_filtered_dates.Country.sort_values(ascending=True).unique())))
                df_group = df1_filtered_dates[df1_filtered_dates["Country"]==option]
                df_group.sort_values(by="disbursementDate",ascending = True, inplace = True)
                dl_file = df_group[["Country", "componentName", "principalRecipientSubClassificationName", "disbursementDate",
                             "disbursementAmount"]]
                dl_file.columns = ["Country", "Component", "Principal Recipient", "Disbursement date", "Disbursement amount"]
            col2.dataframe(dl_file.reset_index(drop=True))

            @st.cache
            def convert_df(dl_file):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return dl_file.to_csv().encode('utf-8')
            csv = convert_df(dl_file)
            col1.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='GF_Disbursements_API.csv'
            )





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



if dataset == "Grant Agreements":
    col2.markdown("<br>![Alt Text](https://media.giphy.com/media/shNla43zRRWazpOS2X/giphy.gif)", unsafe_allow_html=True)     

    # Loading GF API
    count = 0
    gif_runner = st.empty()
    @st.cache(show_spinner=False,suppress_st_warning=True,allow_output_mutation=True)
    def Loading_API(url):
        # check if first load, if so it will take a few sec to load so we want to display a nice gif
        global count
        count += 1
        if count == 1:
            global gif_runner
            gif_runner = st.markdown("![Alt Text](https://media.giphy.com/media/l0MYvEEv2Zndet9hC/giphy.gif)", unsafe_allow_html=True)

        # reading api
        service_url0 = url
        response0 = requests.get(service_url0)
        # make sure we got a valid response
        if (response0.ok):
            # get the full data from the response
            data0j = response0.json()
        else:
            st.caption("Global Fund API cannot be loaded")
        df2 = pd.DataFrame(data0j["value"])
        return df2

    df2 = Loading_API("https://data-service.theglobalfund.org/v3.3/odata/VGrantAgreements")
    df2.principalRecipientSubClassificationName.fillna('Not indicated',inplace=True)

    gif_runner.empty()

    df2 = df2[df2["geographicAreaLevelName"] == 'Country']

    df2['programStartDate'] = df2['programStartDate'].astype('datetime64[ns]')
    df2['programStartDate'] = df2['programStartDate'].dt.date
    df2['programEndDate'] = df2['programEndDate'].astype('datetime64[ns]')
    df2['programEndDate'] = df2['programEndDate'].dt.date

    df2["grantAgreementStatusTypeName"] = pd.Categorical(df2["grantAgreementStatusTypeName"],
                                                         categories=["Terminated", "Administratively Closed", "In Closure", "Active"],
                                                         ordered=True)
    df2.sort_values('grantAgreementStatusTypeName', inplace=True)

    color_discrete_map = {
        "HIV": "#fe9000",
        "Malaria": "#5b8e7d",
        "Tuberculosis": "#5adbff",
        "TB/HIV": "#3c6997",
        "RSSH": "#094074",
        "Multicomponent": "#ffdd4a"}

    color_discrete_map2 = {
        "Sub-Saharan Africa": "#0081a7",
        "East Asia and Pacific": "#b392ac",
        "Europe and Central Asia": "#02c39a",
        "Latin America & the Caribbean": "#fdfcdc",
        "Middle East and North Africa": "#736ced",
        "South Asia": "#f07167"}

    color_discrete_map3 = {
        "Administratively Closed": "#fcd5ce",
        "Terminated": "#ffffff",
        "In Closure": "#e63946",
        "Active": "#48cae4"}

    # ------------------------------------


    fig = px.scatter(df2, x="programStartDate", y="totalDisbursedAmount", color="grantAgreementStatusTypeName",
                     log_y=True, hover_data=['totalSignedAmount'],color_discrete_map = color_discrete_map3,
                     marginal_y="box")
    fig.update_layout(
        autosize=False,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50,
            pad=4,
            autoexpand=True),
        height=800,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01),
        legend_title = 'Grant Agreement Status' )
    fig.update_traces(opacity=1,marker=dict(line=dict(width=0)))
    fig.update_xaxes(showgrid=False, zeroline=True)
    fig.update_yaxes(showgrid=False, zeroline=True)
    st.plotly_chart(fig, use_container_width=True)




if dataset == "Implementation periods":
    col2.markdown("<br>![Alt Text](https://media.giphy.com/media/shNla43zRRWazpOS2X/giphy.gif)", unsafe_allow_html=True)   
