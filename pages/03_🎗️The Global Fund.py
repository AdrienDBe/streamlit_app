import streamlit as st
import requests
import pandas as pd
import numpy as np
import wbgapi as wb
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
from datetime import date



# emojis list: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="GF API explorer", page_icon="🎗", layout="wide")

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
        col1, col2 = st.columns([15, 35], gap='small')
        col2.markdown(
            "<br><br>"
            "<span style='text-align: justify; font-size: 280%; font-family: Arial ; color:#ffffff'> **Disclaimer** </span> </p>",
            unsafe_allow_html=True)
        col2.write("<p style='text-align: justify;'>"
                   "The information presented in this page is solely made by me in my private capacity. "
                   "<br/> This app is using a subset (2018 onwards) of data publicly available from the "
                   "<a href='https://data-service.theglobalfund.org/api'>The Global Fund API </a>."
                   "<br/><br/> I made this app to demonstrate streamlit library capacity for data exploration and visualization, please do not consider it as a "
                   "source of information related to the Global Fund."
                   "<br/> Always refer to the Global Fund official <a href='https://data.theglobalfund.org/'> data explorer </a> for more information.</p>",
                   unsafe_allow_html=True)
        disclaimer_confirmation = col2.button('I understand')
        if disclaimer_confirmation:
            st.session_state.count = 1
            st.experimental_rerun()
        lottie_url = "https://lottie.host/285a7a0c-1d81-4a8f-9df5-c5bebaae5663/UDqNAwwYUo.json"
        lottie_json = load_lottieurl(lottie_url)
        with col1:
            st.markdown("<br>",unsafe_allow_html=True)
            st_lottie(lottie_json, height=350, key="loading_gif2")


@st.cache(show_spinner=False,suppress_st_warning=True,allow_output_mutation=True)
def Loading_country_list():

    service_url0 = "https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues"
    response0 = requests.get(service_url0)
    # make sure we got a valid response
    if (response0.ok):
        # get the full data from the response
        data0j = response0.json()
    else:
        st.caption("API data cannot be loaded")
    country_list = pd.DataFrame(data0j["value"])
    country_list.rename(columns={"Code": "SpatialDim", "Title": "Country"}, inplace=True)

    ## List of World Bank country with Region and Income Level
    WorldBank_countries = wb.economy.DataFrame().reset_index()[
        ['id', 'name', 'aggregate', 'region', 'incomeLevel']]
    WorldBank_countries = WorldBank_countries[WorldBank_countries['aggregate'] == False].drop('aggregate',
                                                                                              axis=1)
    WorldBank_countries['incomeLevel'] = WorldBank_countries['incomeLevel'].map({
        'LIC': 'Low income country',
        'HIC': 'High income country',
        'LMC': 'Lower middle income country',
        'INX': 'Upper middle income country',
        'UMC': 'Upper middle income country'})
    WorldBank_countries['region'] = WorldBank_countries['region'].map({
        'LCN': 'Latin America & the Caribbean',
        'SAS': 'South Asia',
        'SSF': 'Sub-Saharan Africa',
        'ECS': 'Europe and Central Asia',
        'MEA': 'Middle East and North Africa',
        'EAS': 'East Asia and Pacific',
        'NAC': 'North America'})
    WorldBank_countries.rename(columns={"id": "SpatialDim", "incomeLevel": "Income level", "region": "Region"},
                               inplace=True)
    country_list = country_list.merge(WorldBank_countries, how='left', on='SpatialDim')
    return country_list

country_list = Loading_country_list()

if st.session_state.count >= 1:
    # Enabling Plotly Scroll Zoom
    config = dict({'scrollZoom': True, 'displaylogo': False})

    color_discrete_map_ip_status = {
        "Financially Closed": "grey",
        "Financial Closure": "#e63946",
        "Active": "#48cae4"}

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

    color_discrete_map3={
                    "Ministry of Health": "#e6194B",
                    "Ministry of Finance": "#3cb44b",
                    "UN Agency": "#4363d8",
                    "International NGO": "#ffe119",
                    "Other Governmental": "#42d4f4",
                    "International Faith Based Organization": "#f032e6",
                    "Not indicated": "#ffffff",
                    "Local Faith Based Organization": "#fabed4",
                    "Private Sector Entity": "#a9a9a9",
                    "Other Multilateral Organization": "#094074",
                    "Other Community Sector Entity": "#3c6997",
                    "Community Based Organization": "#5b8e7d"}

    color_discrete_map4 = {
        "Administratively Closed": "grey",
        "Terminated": "#fcd5ce",
        "In Closure": "#e63946",
        "Active": "#48cae4"}

    header_space = st.container()

    with header_space:
        col1, col2 = st.columns([15, 35], gap='small')
        col1.write("")
        #col1.title("Global Fund API explorer")
        col1.markdown("<span style='text-align: justify; font-size: 280%; font-family: Arial ; color:#ffffff'> **Global Fund API explorer** </span> </p>", unsafe_allow_html=True)
        dataset = st.radio("Select Dataset", ('Implementation periods', 'Disbursements', 'Reporting results' ), horizontal=True)

    if dataset == "Reporting results":
        col2.markdown("<span style='text-align: justify; font-size: 280%;font-family: Arial; color:#04AA6D'> **Reporting results <br >Section in development** </span> </p>", unsafe_allow_html=True)
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_s8nnfakd.json"
        lottie_json = load_lottieurl(lottie_url)
        st_lottie(lottie_json, height=500, key="loading_gif2")

    if dataset == "Implementation periods":

        # Loading API from WHO WB and GF ---------------------------------------------------

        count = 0
        gif_runner = st.empty()

        @st.cache(show_spinner=False,suppress_st_warning=True,allow_output_mutation=True)
        def Loading_API():
            # check if first load, if so it will take a few sec to load so we want to display a nice svg
            global count
            count += 1
            if count == 1:
                lottie_url = "https://assets1.lottiefiles.com/packages/lf20_18ple6ro.json"
                lottie_json = load_lottieurl(lottie_url)
                lottie_container = st.empty()
                with lottie_container:
                    st_lottie(lottie_json, height=350, key="loading_gif")

            service_url0 = "https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues"
            response0 = requests.get(service_url0)
            # make sure we got a valid response
            if (response0.ok):
                # get the full data from the response
                data0j = response0.json()
            else:
                st.caption("API data cannot be loaded")
            country_list = pd.DataFrame(data0j["value"])
            country_list.rename(columns={"Code": "SpatialDim", "Title": "Country"}, inplace=True)

            ## List of World Bank country with Region and Income Level
            WorldBank_countries = wb.economy.DataFrame().reset_index()[
                ['id', 'name', 'aggregate', 'region', 'incomeLevel']]
            WorldBank_countries = WorldBank_countries[WorldBank_countries['aggregate'] == False].drop('aggregate',
                                                                                                      axis=1)
            WorldBank_countries['incomeLevel'] = WorldBank_countries['incomeLevel'].map({
                'LIC': 'Low income country',
                'HIC': 'High income country',
                'LMC': 'Lower middle income country',
                'INX': 'Upper middle income country',
                'UMC': 'Upper middle income country'})
            WorldBank_countries['region'] = WorldBank_countries['region'].map({
                'LCN': 'Latin America & the Caribbean',
                'SAS': 'South Asia',
                'SSF': 'Sub-Saharan Africa',
                'ECS': 'Europe and Central Asia',
                'MEA': 'Middle East and North Africa',
                'EAS': 'East Asia and Pacific',
                'NAC': 'North America'})
            WorldBank_countries.rename(columns={"id": "SpatialDim", "incomeLevel": "Income level", "region": "Region"},
                                       inplace=True)
            country_list = country_list.merge(WorldBank_countries, how='left', on='SpatialDim')

            # reading api
            service_url0 = 'https://data-service.theglobalfund.org/v3.3/odata/VGrantAgreementImplementationPeriods'
            response0 = requests.get(service_url0)
            # make sure we got a valid response
            if (response0.ok):
                # get the full data from the response
                data0j = response0.json()
            else:
                st.caption("Global Fund API cannot be loaded")
            df2 = pd.DataFrame(data0j["value"])
            if count == 1:
                lottie_container.empty()

            df2.principalRecipientSubClassificationName.fillna('Not indicated', inplace=True)

            # merge with country info
            df2.rename(columns={"geographicAreaCode_ISO3": "SpatialDim"}, inplace=True)
            df2 = pd.merge(df2,
                           country_list,
                           on='SpatialDim',
                           how='left')
            df2.Region.fillna('Non-regional IP', inplace=True)
            df2.principalRecipientName.fillna('Not indicated', inplace=True)
            df2.grantAgreementTitle.fillna('Not indicated', inplace=True)

            df2['implementationPeriodStartDate'] = df2['implementationPeriodStartDate'].astype('datetime64[ns]')
            df2['implementationPeriodStartDate'] = df2['implementationPeriodStartDate'].dt.date
            df2['implementationPeriodEndDate'] = df2['implementationPeriodEndDate'].astype('datetime64[ns]')
            df2['implementationPeriodEndDate'] = df2['implementationPeriodEndDate'].dt.date
            df2['programStartDate'] = df2['programStartDate'].astype('datetime64[ns]')
            df2['programStartDate'] = pd.to_datetime(df2['programStartDate']).dt.date
            df2['programStartDate'] = df2['programStartDate'].astype('datetime64[ns]')
            df2['programEndDate'] = pd.to_datetime(df2['programEndDate']).dt.date

            df2["implementationPeriodStatusTypeName"] = pd.Categorical(df2["implementationPeriodStatusTypeName"],
                                                                       categories=["Active", "Financial Closure",
                                                                                   "Financially Closed"],
                                                                       ordered=True)
            df2.sort_values('implementationPeriodStatusTypeName', inplace=True)
            df2 = df2[df2['programStartDate'].dt.year >= 2018]
            return country_list, df2

        country_list, df2 = Loading_API()
        gif_runner.empty()

        col2.markdown("<span style='text-align: justify; font-size: 280%;font-family: Arial; color:#04AA6D'> **Implementation Periods** </span> "
                    "<p style='text-align: justify'> A country’s funding request to the Global Fund is turned into one or more grants through a process called grant-making.  "
                    "The Country Coordinating Mechanism and the Global Fund work with the partner implementing a grant, the Principal Recipient, to prepare the grant. </span> "
                    "<span style='color:grey'>Loading takes a few seconds the first time.</span> </p>", unsafe_allow_html=True)

        # FILTERS ------------------------------------

        #clear filters button
        def clear_multi():
            for key in st.session_state.keys():
                st.session_state[key] = []

        with st.sidebar:

            # Active Grant filter
            isActive = st.radio("Filter", ('All IPs', 'Active IPs', 'Financially closed IPs'),horizontal=True)
            if isActive == "All IPs":
                df2_group = df2
            if isActive == "Active IPs":
                df2_group = df2[df2["isActive"]==True]
            elif isActive == "Financially closed IPs":
                df2_group = df2[df2["implementationPeriodStatusTypeName"]=='Financially Closed']

            # Component filter
            option_Component = st.multiselect(
                'Filter component(s)',
                options=list(df2_group.componentName.sort_values(ascending=True).unique()),
                key= "component_multiselect")
            if len(option_Component) == 0:
                df_group_compo = df2_group
            else:
                df_group_compo = df2_group[df2_group["componentName"].isin(option_Component)]

            # Principal recipient filter
            option_map_pr = st.multiselect(
                'Filter PR type',
                options=list(
                    df_group_compo.principalRecipientSubClassificationName.sort_values(ascending=True).unique()),
                key="pr_multiselect")
            if len(option_map_pr) == 0:
                df_group_pr = df_group_compo
            else:
                df_group_pr = df_group_compo[
                    df_group_compo["principalRecipientSubClassificationName"].isin(option_map_pr)]

            # Region filter
            region_filter = st.multiselect(
                'Select region',
                options=list(df_group_pr.Region.sort_values(ascending=True).unique()),
                key= "pr_multiselect")
            if len(region_filter) == 0:
                df2_group_region = df_group_pr
            else:
                df2_group_region = df_group_pr[df_group_pr["Region"].isin(region_filter)]

            # Country filter
            country_filter = st.multiselect(
                'Select country',
                options=list(df2_group_region.geographicAreaName.sort_values(ascending=True).unique()),
                key= "pr_multiselect")
            if len(country_filter) == 0:
                df2_group_country = df2_group_region
            else:
                df2_group_country = df2_group_region[df2_group_region["geographicAreaName"].isin(country_filter)]

            # Timeline filter
            if len(df2_group_country.groupby(['grantAgreementNumber'])) != 1 :
                start_year, end_year = st.select_slider(
                    'Program starting date',
                    options=list(df2_group_country.programStartDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).unique()),
                    value=(df2_group_country.programStartDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).min(),
                           df2_group_country.programStartDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).max()))
                # Filtered dataset:
                df1_filtered_dates = df2_group_country[(df2_group_country.programStartDate.astype('datetime64[ns]').dt.year >= start_year) & (
                        df2_group_country.programStartDate.astype('datetime64[ns]').dt.year <= end_year)]
            else :
                df1_filtered_dates = df2_group_country

            # Reset filters button
            st.button("Clear filters", on_click=clear_multi)


        # TABS ------------------------------------
        tab1, tab2 = st.tabs(["View per category", "All"])

        with tab1:
            view = st.radio(
                "Select category",
                ('Component', 'Principal Recipient', 'Region'),
                horizontal = True, key = "scatter_view")

            if view == 'Component':

                for i in df1_filtered_dates.componentName.unique():
                    df_temp = df1_filtered_dates[df1_filtered_dates['componentName']==i]
                    with st.container():

                        st.markdown(
                            "<span style='text-align: justify; font-size: 120%;font-family: Arial; color:#04AA6D'> **{}** </span></p>".format(i),
                            unsafe_allow_html=True)

                        col1, col2, col3, col4 = st.columns([30, 30, 30, 30])
                        if isActive == "Active IPs":
                            col1.metric("Number of active IPs",
                                        "{:,}".format(len(df_temp.groupby(['grantAgreementNumber']))))
                            col2.metric("Number of active Grants", "{:,}".format(
                                len(df_temp['grantAgreementImplementationPeriodId'].unique())))
                        else:
                            col1.metric("Number of IPs",
                                        "{:,}".format(len(df_temp.groupby(['grantAgreementNumber']))))
                            col2.metric("Number of Grants", "{:,}".format(
                                len(df_temp['grantAgreementImplementationPeriodId'].unique())))
                        Number_renewed = df_temp.grantAgreementId.value_counts()
                        Number_renewed = Number_renewed[Number_renewed > 1].count()
                        col3.metric("Grants renewed once or more", "{} %".format(
                            round(Number_renewed / len(df_temp.grantAgreementId.unique()) * 100)))
                        min = df_temp.groupby('grantAgreementId')['implementationPeriodStartDate'].agg(['min'])
                        max = df_temp.groupby('grantAgreementId')['implementationPeriodEndDate'].agg(['max'])
                        df_temp_min_max = pd.merge(min,
                                              max,
                                              on='grantAgreementId',
                                              how='left').reset_index()
                        df_temp_min_max['min'] = df_temp_min_max['min'].apply(pd.Timestamp)
                        df_temp_min_max['max'] = df_temp_min_max['max'].apply(pd.Timestamp)
                        col4.metric("Average IP overall duration", "{:,} year(s)".format(
                            round(((df_temp_min_max['max'] - df_temp_min_max['min']) / np.timedelta64(1, 'Y')).mean(), 1)))

                        col1, col2= st.columns([15,15],gap ='large')

                        if len(df_temp.principalRecipientName.unique()) == 1:
                            col1.write(df_temp.principalRecipientName.unique()[0])
                        else:
                            PR = col1.multiselect(
                                "{} Principal Recipient(s)".format(len(df_temp.principalRecipientName.unique())),
                                (list(df_temp.principalRecipientName.unique())))
                            if len(PR) != 0:
                                df_temp = df_temp[df_temp['principalRecipientName'].isin(PR)]

                        if len(df_temp.grantAgreementNumber.unique()) == 1:
                            col2.write(df_temp.grantAgreementNumber.unique()[0])
                        else:
                            GN = col2.multiselect(
                                "{} IP(s)".format(len(df_temp.grantAgreementNumber.unique())),
                                (list(df_temp.grantAgreementNumber.unique())))
                            if len(GN) != 0:
                                df_temp = df_temp[df_temp['grantAgreementNumber'].isin(GN)]

                        fig = px.timeline(df_temp.sort_values('programStartDate'),
                                          x_start="implementationPeriodStartDate",
                                          x_end="implementationPeriodEndDate",
                                          y="grantAgreementNumber",
                                          color = "implementationPeriodStatusTypeName",
                                          color_discrete_map=color_discrete_map_ip_status,
                                          hover_data={"grantAgreementStatusTypeName": False,
                                                      "geographicAreaName": True,
                                                      "principalRecipientName": True,
                                                      "programStartDate": True,
                                                      "programEndDate": True,
                                                      "grantAgreementTitle": True},
                                          labels={'geographicAreaName': 'Country',
                                                  'implementationPeriodStartDate': 'Program start date',
                                                  'principalRecipientName': 'Principal Recipient',
                                                  'implementationPeriodEndDate': 'Program end date',
                                                  'grantAgreementNumber': 'Grant agreement number',
                                                  'grantAgreementTitle': 'Grant agreement title'})

                        fig.add_vline(x=date.today(), line_width=2, line_color="white", line_dash="dot")
                        fig.add_annotation(x=date.today(), y=1, showarrow=False, text="{}".format(date.today()), xshift=50)
                        fig.update_annotations(font_color="white", font_size=15)
                        fig.add_vrect(x0="2020-01-01", x1="2022-12-24",
                                      fillcolor="green",
                                      opacity=0.25,
                                      line_width=0)

                        fig.update_yaxes(showgrid=False, zeroline=True, title_text="", visible=False)
                        fig.update_layout(autosize=False,
                                    margin=dict(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=50,
                                        pad=4,
                                        autoexpand=True),
                                    height=300,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    legend_title = '',
                                    font=dict(
                                        family="Arial",
                                        size=15))
                        col1.plotly_chart(fig, use_container_width=True, config=config)

                        df_temp2 = df_temp.sort_values('programStartDate')
                        df_temp2['disbursedtocommited'] = df_temp2['totalDisbursedAmount'] * 100 / df_temp2['totalCommittedAmount']
                        df_temp2['disbursedtocommited'].fillna(0, inplace=True)
                        df_temp2['disbursedtocommited'] = round(df_temp2['disbursedtocommited']).astype(int)
                        df_temp2['disbursedtocommited'] = df_temp2['disbursedtocommited'].astype(str) + '%'

                        fig = {
                            'data': [go.Bar(x=df_temp2["totalSignedAmount"],
                                            y=df_temp2['grantAgreementNumber'],
                                            width=0.7,
                                            orientation='h',
                                            marker=dict(color="#023824"),
                                            name= "Signed amount"
                                            ),
                                     go.Bar(x=df_temp2["totalCommittedAmount"],
                                            y=df_temp2['grantAgreementNumber'],
                                            width=0.7,
                                            orientation='h',
                                            marker=dict(color="#046944"),
                                            name= "Committed amount"
                                            ),
                                     go.Bar(x=df_temp2["totalDisbursedAmount"],
                                            y=df_temp2['grantAgreementNumber'],
                                            width=0.4,
                                            orientation='h',
                                            marker=dict(color="#C1EADB"),
                                            name= "Disbursed amount",
                                            text=df_temp2['disbursedtocommited']
                                            )
                                     ],
                            'layout': go.Layout(barmode='overlay',autosize=False,
                                    margin=dict(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=50,
                                        pad=4,
                                        autoexpand=True),
                                    height=300,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    legend_title = '',
                                    font=dict(
                                        family="Arial",
                                        size=15))
                            }

                        col2.plotly_chart(fig, use_container_width=True, config=config)

                        with st.expander("See grant(s) detail"):
                            col1, col2 = st.columns([90, 10])
                            df_temp1 = df_temp[['geographicAreaName',
                                                   'componentName',
                                                   'grantAgreementNumber',
                                                   'isActive',
                                                   'grantAgreementStatusTypeName',
                                                   'grantAgreementTitle',
                                                   'programStartDate',
                                                   'programEndDate',
                                                   'portfolioManager',
                                                   'portfolioManagerEmailAddress',
                                                   'applicantName',
                                                   'principalRecipientName',
                                                   'principalRecipientSubClassificationName',
                                                   'currency',
                                                   'totalSignedAmount',
                                                   'totalCommittedAmount',
                                                   'totalDisbursedAmount']]
                            df_temp2 = df_temp1.reset_index(drop=True)
                            df_temp2.columns = ['Country',
                                                   'Component',
                                                   'Grant agreement number',
                                                   'Is the Grant Active',
                                                   'Grant agreement status type',
                                                   'Grant agreement title',
                                                   'Program start date',
                                                   'Program end date',
                                                   'Portfolio manager',
                                                   'Portfolio manager email address',
                                                   'Applicant name',
                                                   'Principal recipient name',
                                                   'Principal recipient sub-classification',
                                                   'Currency',
                                                   'Signed amount',
                                                   'Committed amount',
                                                   'Disbursed amount']
                            col1.dataframe(df_temp2)
                            @st.cache
                            def convert_df(df1_filtered_dates2):
                                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                                return df_temp.to_csv().encode('utf-8')
                            csv = convert_df(df_temp2)
                            col2.download_button(
                                label="Download data as CSV",
                                data=csv,
                                file_name='GF_Grants_API.csv'
                            )
                        st.write('---')

            if view == 'Principal Recipient':

                for i in df1_filtered_dates.principalRecipientSubClassificationName.unique():
                    df_temp = df1_filtered_dates[df1_filtered_dates['principalRecipientSubClassificationName']==i]
                    with st.container():

                        st.markdown(
                            "<span style='text-align: justify; font-size: 120%;font-family: Arial; color:#04AA6D'> **{}** </span></p>".format(i),
                            unsafe_allow_html=True)

                        col1, col2, col3, col4 = st.columns([30, 30, 30, 30])
                        if isActive == "Active IPs":
                            col1.metric("Number of active IPs",
                                        "{:,}".format(len(df_temp.groupby(['grantAgreementNumber']))))
                            col2.metric("Number of active Grants", "{:,}".format(
                                len(df_temp['grantAgreementImplementationPeriodId'].unique())))
                        else:
                            col1.metric("Number of IPs",
                                        "{:,}".format(len(df_temp.groupby(['grantAgreementNumber']))))
                            col2.metric("Number of Grants", "{:,}".format(
                                len(df_temp['grantAgreementImplementationPeriodId'].unique())))
                        Number_renewed = df_temp.grantAgreementId.value_counts()
                        Number_renewed = Number_renewed[Number_renewed > 1].count()
                        col3.metric("Grants renewed once or more", "{} %".format(
                            round(Number_renewed / len(df_temp.grantAgreementId.unique()) * 100)))
                        min = df_temp.groupby('grantAgreementId')['implementationPeriodStartDate'].agg(['min'])
                        max = df_temp.groupby('grantAgreementId')['implementationPeriodEndDate'].agg(['max'])
                        df_temp_min_max = pd.merge(min,
                                              max,
                                              on='grantAgreementId',
                                              how='left').reset_index()
                        df_temp_min_max['min'] = df_temp_min_max['min'].apply(pd.Timestamp)
                        df_temp_min_max['max'] = df_temp_min_max['max'].apply(pd.Timestamp)
                        col4.metric("Average IP overall duration", "{:,} year(s)".format(
                            round(((df_temp_min_max['max'] - df_temp_min_max['min']) / np.timedelta64(1, 'Y')).mean(), 1)))

                        col1, col2= st.columns([15,15],gap ='large')

                        if len(df_temp.principalRecipientName.unique()) == 1:
                            col1.write(df_temp.principalRecipientName.unique()[0])
                        else:
                            PR = col1.multiselect(
                                "{} Principal Recipient(s)".format(len(df_temp.principalRecipientName.unique())),
                                (list(df_temp.principalRecipientName.unique())))
                            if len(PR) != 0:
                                df_temp = df_temp[df_temp['principalRecipientName'].isin(PR)]

                        if len(df_temp.grantAgreementNumber.unique()) == 1:
                            col2.write(df_temp.grantAgreementNumber.unique()[0])
                        else:
                            GN = col2.multiselect(
                                "{} IP(s)".format(len(df_temp.grantAgreementNumber.unique())),
                                (list(df_temp.grantAgreementNumber.unique())))
                            if len(GN) != 0:
                                df_temp = df_temp[df_temp['grantAgreementNumber'].isin(GN)]

                        fig = px.timeline(df_temp.sort_values('programStartDate'),
                                          x_start="implementationPeriodStartDate",
                                          x_end="implementationPeriodEndDate",
                                          y="grantAgreementNumber",
                                          color = "implementationPeriodStatusTypeName",
                                          color_discrete_map=color_discrete_map_ip_status,
                                          hover_data={"grantAgreementStatusTypeName": False,
                                                      "geographicAreaName": True,
                                                      "principalRecipientName": True,
                                                      "programStartDate": True,
                                                      "programEndDate": True,
                                                      "grantAgreementTitle": True},
                                          labels={'geographicAreaName': 'Country',
                                                  'implementationPeriodStartDate': 'Program start date',
                                                  'principalRecipientName': 'Principal Recipient',
                                                  'implementationPeriodEndDate': 'Program end date',
                                                  'grantAgreementNumber': 'Grant agreement number',
                                                  'grantAgreementTitle': 'Grant agreement title'})

                        fig.add_vline(x=date.today(), line_width=2, line_color="white", line_dash="dot")
                        fig.add_annotation(x=date.today(), y=1, showarrow=False, text="{}".format(date.today()), xshift=50)
                        fig.update_annotations(font_color="white", font_size=15)
                        fig.add_vrect(x0="2020-01-01", x1="2022-12-24",
                                      fillcolor="green",
                                      opacity=0.25,
                                      line_width=0)
                        fig.update_layout(autosize=False,
                                    margin=dict(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=50,
                                        pad=4,
                                        autoexpand=True),
                                    height=300,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    legend_title = '',
                                    font=dict(
                                        family="Arial",
                                        size=15))
                        fig.update_yaxes(showgrid=False, zeroline=True, title_text="", visible=False)
                        col1.plotly_chart(fig, use_container_width=True, config=config)

                        df_temp2 = df_temp.sort_values('programStartDate')
                        df_temp2['disbursedtocommited'] = df_temp2['totalDisbursedAmount'] * 100 / df_temp2['totalCommittedAmount']
                        df_temp2['disbursedtocommited'].fillna(0, inplace=True)
                        df_temp2['disbursedtocommited'] = round(df_temp2['disbursedtocommited']).astype(int)
                        df_temp2['disbursedtocommited'] = df_temp2['disbursedtocommited'].astype(str) + '%'
                        fig = {
                            'data': [go.Bar(x=df_temp2["totalSignedAmount"],
                                            y=df_temp2['grantAgreementNumber'],
                                            width=0.7,
                                            orientation='h',
                                            marker=dict(color="#023824"),
                                            name= "Signed amount"
                                            ),
                                     go.Bar(x=df_temp2["totalCommittedAmount"],
                                            y=df_temp2['grantAgreementNumber'],
                                            width=0.7,
                                            orientation='h',
                                            marker=dict(color="#046944"),
                                            name= "Committed amount"
                                            ),
                                     go.Bar(x=df_temp2["totalDisbursedAmount"],
                                            y=df_temp2['grantAgreementNumber'],
                                            width=0.4,
                                            orientation='h',
                                            marker=dict(color="#C1EADB"),
                                            name= "Disbursed amount",
                                            text=df_temp2['disbursedtocommited']
                                            )
                                     ],
                            'layout': go.Layout(barmode='overlay',autosize=False,
                                    margin=dict(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=50,
                                        pad=4,
                                        autoexpand=True),
                                    height=300,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    legend_title = '',
                                    font=dict(
                                        family="Arial",
                                        size=15))
                            }

                        col2.plotly_chart(fig, use_container_width=True, config=config)

                        with st.expander("See grant(s) detail"):
                            col1, col2 = st.columns([90, 10])
                            df_temp1 = df_temp[['geographicAreaName',
                                                   'componentName',
                                                   'grantAgreementNumber',
                                                   'isActive',
                                                   'grantAgreementStatusTypeName',
                                                   'grantAgreementTitle',
                                                   'programStartDate',
                                                   'programEndDate',
                                                   'portfolioManager',
                                                   'portfolioManagerEmailAddress',
                                                   'applicantName',
                                                   'principalRecipientName',
                                                   'principalRecipientSubClassificationName',
                                                   'currency',
                                                   'totalSignedAmount',
                                                   'totalCommittedAmount',
                                                   'totalDisbursedAmount']]
                            df_temp2 = df_temp1.reset_index(drop=True)
                            df_temp2.columns = ['Country',
                                                   'Component',
                                                   'Grant agreement number',
                                                   'Is the Grant Active',
                                                   'Grant agreement status type',
                                                   'Grant agreement title',
                                                   'Program start date',
                                                   'Program end date',
                                                   'Portfolio manager',
                                                   'Portfolio manager email address',
                                                   'Applicant name',
                                                   'Principal recipient name',
                                                   'Principal recipient sub-classification',
                                                   'Currency',
                                                   'Signed amount',
                                                   'Committed amount',
                                                   'Disbursed amount']
                            col1.dataframe(df_temp2)
                            @st.cache
                            def convert_df(df1_filtered_dates2):
                                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                                return df_temp.to_csv().encode('utf-8')
                            csv = convert_df(df_temp2)
                            col2.download_button(
                                label="Download data as CSV",
                                data=csv,
                                file_name='GF_Grants_API.csv'
                            )
                        st.write('---')

            if view == 'Region':
                for i in df1_filtered_dates.Region.unique():
                    df_temp = df1_filtered_dates[df1_filtered_dates['Region']==i]

                    with st.container():
                        st.markdown(
                            "<span style='text-align: justify; font-size: 120%;font-family: Arial; color:#04AA6D'> **{}** </span></p>".format(i),
                            unsafe_allow_html=True)

                        col1, col2, col3, col4 = st.columns([30, 30, 30, 30])
                        if isActive == "Active IPs":
                            col1.metric("Number of active IPs",
                                        "{:,}".format(len(df_temp.groupby(['grantAgreementNumber']))))
                            col2.metric("Number of active Grants", "{:,}".format(
                                len(df_temp['grantAgreementImplementationPeriodId'].unique())))
                        else:
                            col1.metric("Number of IPs",
                                        "{:,}".format(len(df_temp.groupby(['grantAgreementNumber']))))
                            col2.metric("Number of Grants", "{:,}".format(
                                len(df_temp['grantAgreementImplementationPeriodId'].unique())))
                        Number_renewed = df_temp.grantAgreementId.value_counts()
                        Number_renewed = Number_renewed[Number_renewed > 1].count()
                        col3.metric("Grants renewed once or more", "{} %".format(
                            round(Number_renewed / len(df_temp.grantAgreementId.unique()) * 100)))
                        min = df_temp.groupby('grantAgreementId')['implementationPeriodStartDate'].agg(['min'])
                        max = df_temp.groupby('grantAgreementId')['implementationPeriodEndDate'].agg(['max'])
                        df_temp_min_max = pd.merge(min,
                                              max,
                                              on='grantAgreementId',
                                              how='left').reset_index()
                        df_temp_min_max['min'] = df_temp_min_max['min'].apply(pd.Timestamp)
                        df_temp_min_max['max'] = df_temp_min_max['max'].apply(pd.Timestamp)
                        col4.metric("Average IP overall duration", "{:,} year(s)".format(
                            round(((df_temp_min_max['max'] - df_temp_min_max['min']) / np.timedelta64(1, 'Y')).mean(), 1)))

                        col1, col2= st.columns([15,15],gap ='large')
                        if len(df_temp.geographicAreaLevelName.unique()) == 1:
                            geoAreaLevelName_option = col1.multiselect(
                                'Select country',
                                (list(df_temp.geographicAreaName.unique())))
                            if len(geoAreaLevelName_option) != 0:
                                df_temp = df_temp[df_temp['geographicAreaName'].isin(geoAreaLevelName_option)]
                        elif len(df_temp.geographicAreaLevelName.unique()) != 1:
                            geoAreaLevelName_option = col1.multiselect(
                                'Select scope',
                                (list(df_temp.geographicAreaLevelName.unique())))
                            if len(geoAreaLevelName_option) != 0:
                                df_temp = df_temp[df_temp['geographicAreaLevelName'].isin(geoAreaLevelName_option)]

                        if len(df_temp.grantAgreementNumber.unique()) == 1:
                            col2.write(df_temp.grantAgreementNumber.unique()[0])
                        else:
                            GN = col2.multiselect(
                                "{} IP(s)".format(len(df_temp.grantAgreementNumber.unique())),
                                (list(df_temp.grantAgreementNumber.unique())))
                            if len(GN) != 0:
                                df_temp = df_temp[df_temp['grantAgreementNumber'].isin(GN)]

                        fig = px.timeline(df_temp.sort_values('programStartDate'),
                                          x_start="implementationPeriodStartDate",
                                          x_end="implementationPeriodEndDate",
                                          y="grantAgreementNumber",
                                          color = "implementationPeriodStatusTypeName",
                                          color_discrete_map=color_discrete_map_ip_status,
                                          hover_data={"grantAgreementStatusTypeName": False,
                                                      "geographicAreaName": True,
                                                      "principalRecipientName": True,
                                                      "programStartDate": True,
                                                      "programEndDate": True,
                                                      "grantAgreementTitle": True},
                                          labels={'geographicAreaName': 'Country',
                                                  'implementationPeriodStartDate': 'Program start date',
                                                  'principalRecipientName': 'Principal Recipient',
                                                  'implementationPeriodEndDate': 'Program end date',
                                                  'grantAgreementNumber': 'Grant agreement number',
                                                  'grantAgreementTitle': 'Grant agreement title'})
                        fig.update_traces( marker_line_color='white',line_width=10, opacity=1,selector=dict(fill='toself'))
                        fig.add_vline(x=date.today(), line_width=2, line_color="white", line_dash="dot")
                        fig.add_annotation(x=date.today(), y=1, showarrow=False, text="{}".format(date.today()), xshift=50)
                        fig.update_annotations(font_color="white", font_size=15)
                        fig.add_vrect(x0="2020-01-01", x1="2022-12-24",
                                      fillcolor="green",
                                      opacity=0.25,
                                      line_width=0)
                        fig.update_layout(
                            autosize=False,
                            margin=dict(
                                l=0,
                                r=0,
                                b=0,
                                t=50,
                                pad=4,
                                autoexpand=True),
                            height=300,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            legend_title='',
                            font=dict(
                                family="Arial",
                                size=15)
                            )
                        fig.update_yaxes(showgrid=False, zeroline=True, title_text="", visible=False)
                        col1.plotly_chart(fig, use_container_width=True, config=config)

                        df_temp2 = df_temp.sort_values('programStartDate')
                        df_temp2['disbursedtocommited'] = df_temp2['totalDisbursedAmount'] * 100 / df_temp2[
                            'totalCommittedAmount']
                        df_temp2['disbursedtocommited'].fillna(0, inplace=True)
                        df_temp2['disbursedtocommited'] = round(df_temp2['disbursedtocommited']).astype(int)
                        df_temp2['disbursedtocommited'] = df_temp2['disbursedtocommited'].astype(str) + '%'

                        fig = {
                            'data': [go.Bar(x=df_temp2["totalSignedAmount"],
                                            y=df_temp2['grantAgreementNumber'],
                                            width=0.7,
                                            orientation='h',
                                            marker=dict(color="#023824"),
                                            name="Signed amount"
                                            ),
                                     go.Bar(x=df_temp2["totalCommittedAmount"],
                                            y=df_temp2['grantAgreementNumber'],
                                            width=0.7,
                                            orientation='h',
                                            marker=dict(color="#046944"),
                                            name="Committed amount"
                                            ),
                                     go.Bar(x=df_temp2["totalDisbursedAmount"],
                                            y=df_temp2['grantAgreementNumber'],
                                            width=0.4,
                                            orientation='h',
                                            marker=dict(color="#C1EADB"),
                                            name="Disbursed amount",
                                            text=df_temp2['disbursedtocommited']
                                            )
                                     ],
                            'layout': go.Layout(barmode='overlay', autosize=False,
                                                margin=dict(
                                                    l=0,
                                                    r=0,
                                                    b=0,
                                                    t=50,
                                                    pad=4,
                                                    autoexpand=True),
                                                height=300,
                                                paper_bgcolor='rgba(0,0,0,0)',
                                                plot_bgcolor='rgba(0,0,0,0)',
                                                font=dict(
                                                    family="Arial",
                                                    size=15))
                        }

                        col2.plotly_chart(fig, use_container_width=True, config=config)
                        with st.expander("See grant(s) detail"):
                            col1, col2 = st.columns([90, 10])
                            df_temp1 = df_temp[['geographicAreaName',
                                                   'componentName',
                                                   'grantAgreementNumber',
                                                   'isActive',
                                                   'grantAgreementStatusTypeName',
                                                   'grantAgreementTitle',
                                                   'programStartDate',
                                                   'programEndDate',
                                                   'portfolioManager',
                                                   'portfolioManagerEmailAddress',
                                                   'applicantName',
                                                   'principalRecipientName',
                                                   'principalRecipientSubClassificationName',
                                                   'currency',
                                                   'totalSignedAmount',
                                                   'totalCommittedAmount',
                                                   'totalDisbursedAmount']]
                            df_temp2 = df_temp1.reset_index(drop=True)
                            df_temp2.columns = ['Country',
                                                   'Component',
                                                   'Grant agreement number',
                                                   'Is the Grant Active',
                                                   'Grant agreement status type',
                                                   'Grant agreement title',
                                                   'Program start date',
                                                   'Program end date',
                                                   'Portfolio manager',
                                                   'Portfolio manager email address',
                                                   'Applicant name',
                                                   'Principal recipient name',
                                                   'Principal recipient sub-classification',
                                                   'Currency',
                                                   'Signed amount',
                                                   'Committed amount',
                                                   'Disbursed amount']
                            col1.dataframe(df_temp2)
                            @st.cache
                            def convert_df(df1_filtered_dates2):
                                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                                return df_temp.to_csv().encode('utf-8')
                            csv = convert_df(df_temp2)
                            col1.download_button(
                                label="Download data as CSV",
                                data=csv,
                                file_name='GF_Grants_API.csv'
                            )
                        st.write('---')

        with tab2:
            # METRICS ------------------------------------
            col1, col2, col3, col4 = st.columns([30, 30, 30, 30])
            if isActive == "Active IPs":
                col1.metric("Number of active IPs",
                            "{:,}".format(len(df1_filtered_dates.groupby(['grantAgreementNumber']))))
                col2.metric("Number of active Grants",
                            "{:,}".format(len(df1_filtered_dates['grantAgreementImplementationPeriodId'].unique())))
            else:
                col1.metric("Number of IPs", "{:,}".format(len(df1_filtered_dates.groupby(['grantAgreementNumber']))))
                col2.metric("Number of Grants",
                            "{:,}".format(len(df1_filtered_dates['grantAgreementImplementationPeriodId'].unique())))
            Number_renewed = df1_filtered_dates.grantAgreementId.value_counts()
            Number_renewed = Number_renewed[Number_renewed > 1].count()
            col3.metric("Grants renewed once or more",
                        "{} %".format(round(Number_renewed / len(df1_filtered_dates.grantAgreementId.unique()) * 100)))
            min = df1_filtered_dates.groupby('grantAgreementId')['implementationPeriodStartDate'].agg(['min'])
            max = df1_filtered_dates.groupby('grantAgreementId')['implementationPeriodEndDate'].agg(['max'])
            df_min_max = pd.merge(min,
                                  max,
                                  on='grantAgreementId',
                                  how='left').reset_index()
            df_min_max['min'] = df_min_max['min'].apply(pd.Timestamp)
            df_min_max['max'] = df_min_max['max'].apply(pd.Timestamp)
            col4.metric("Average IP overall duration", "{:,} year(s)".format(
                round(((df_min_max['max'] - df_min_max['min']) / np.timedelta64(1, 'Y')).mean(), 1)))

            df_temp2 = df1_filtered_dates
            df_temp2['disbursedtocommited'] = df_temp2['totalDisbursedAmount'] * 100 / df_temp2['totalCommittedAmount']
            df_temp2['disbursedtocommited'].fillna(0, inplace=True)
            df_temp2['disbursedtocommited'] = round(df_temp2['disbursedtocommited']).astype(int)
            df_temp2['disbursedtocommited'] = df_temp2['disbursedtocommited'].astype(str) + '%'

            col1, col2 = st.columns([15, 15], gap='large')

            fig = px.timeline(df1_filtered_dates.sort_values(by='implementationPeriodStartDate', ascending=True),
                              x_start="implementationPeriodStartDate",
                              x_end="implementationPeriodEndDate",
                              y="grantAgreementNumber",
                              color="implementationPeriodStatusTypeName",
                              color_discrete_map=color_discrete_map_ip_status,
                              hover_data={"implementationPeriodStatusTypeName": True,
                                          "geographicAreaName": True,
                                          "principalRecipientName": True,
                                          "implementationPeriodStartDate": True,
                                          "implementationPeriodEndDate": True,
                                          "componentName": True},
                              labels={'geographicAreaName': 'Country',
                                      'principalRecipientName': 'Principal Recipient',
                                      'implementationPeriodStartDate': 'IP start date',
                                      'implementationPeriodEndDate': 'IP end date',
                                      'grantAgreementNumber': 'Grant agreement number',
                                      'grantAgreementTitle': 'Grant agreement title'})

            fig.add_vline(x=date.today(), line_width=2, line_color="white", line_dash="dot")
            fig.add_annotation(x=date.today(), y=1, showarrow=False, text="{}".format(date.today()), xshift=50)
            fig.update_annotations(font_color="white", font_size=20)
            fig.add_vrect(x0="2020-01-01", x1="2022-12-24",
                          fillcolor="green",
                          opacity=0.25,
                          line_width=0)
            fig.update_layout(
                autosize=False,
                margin=dict(
                    l=0,
                    r=0,
                    b=0,
                    t=50,
                    pad=4,
                    autoexpand=True),
                height=600,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend_title='Implementation Period Status')
            fig.update_yaxes(showgrid=False, zeroline=True, title_text="", visible=False)
            col1.plotly_chart(fig, use_container_width=True, config=config)

            fig = {
                'data': [go.Bar(x=df_temp2["totalSignedAmount"],
                                y=df_temp2['grantAgreementNumber'],
                                width=0.7,
                                orientation='h',
                                marker=dict(color="#023824"),
                                name="Signed amount"
                                ),
                         go.Bar(x=df_temp2["totalCommittedAmount"],
                                y=df_temp2['grantAgreementNumber'],
                                width=0.7,
                                orientation='h',
                                marker=dict(color="#046944"),
                                name="Committed amount"
                                ),
                         go.Bar(x=df_temp2["totalDisbursedAmount"],
                                y=df_temp2['grantAgreementNumber'],
                                width=0.4,
                                orientation='h',
                                marker=dict(color="#C1EADB"),
                                name="Disbursed amount",
                                text=df_temp2['disbursedtocommited']
                                )
                         ],
                'layout': go.Layout(barmode='overlay', autosize=False,
                                    margin=dict(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=50,
                                        pad=4,
                                        autoexpand=True),
                                    height=600,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font=dict(
                                        family="Arial",
                                        size=15))
                }
            col2.plotly_chart(fig, use_container_width=True, config=config)

    if dataset == "Disbursements":
        col2.markdown("<span style='text-align: justify; font-size: 280%;font-family: Arial; color:#04AA6D'> **Disbursements records** </span> "
                    "<p style='text-align: justify'> A disbursement corresponds to a tranche transfer of the grant funds for the implementation"
                    " of Programs.<br>"
                    " In order to visualize disbursement information data we load and explore the API de-normalized view of all Grant Agreement "
                    "Disbursements records. </span> "
                    "<span style='color:grey'>Loading takes a few seconds the first time.</span> </p>", unsafe_allow_html=True)

        # Loading GF API
        count = 0
        @st.cache(show_spinner=False,suppress_st_warning=True,allow_output_mutation=True)
        def Loading_API_disbursements():
            # check if first load, if so it will take a few sec to load so we want to display a nice svg
            global count
            count += 1
            if count == 1:
                    lottie_url = "https://assets1.lottiefiles.com/packages/lf20_18ple6ro.json"
                    lottie_json = load_lottieurl(lottie_url)
                    lottie_container = st.empty()
                    with lottie_container:
                        st_lottie(lottie_json, height=350, key="loading_gif")
            # reading api
            service_url0 = "https://data-service.theglobalfund.org/v3.3/odata/VGrantAgreementDisbursements"
            response0 = requests.get(service_url0)
            # make sure we got a valid response
            if (response0.ok):
                # get the full data from the response
                data0j = response0.json()
            else:
                st.caption("Global Fund API cannot be loaded")
            df1 = pd.DataFrame(data0j["value"])

            if count == 1:
                lottie_container.empty()

            df1.principalRecipientSubClassificationName.fillna('Not indicated', inplace=True)
            df1['disbursementDate'] = df1['disbursementDate'].astype('datetime64[ns]')
            df1['disbursementDate'] = pd.to_datetime(df1['disbursementDate'], errors='coerce')
            df1 = df1[df1['disbursementDate'].dt.year >= 2018]
            # merge with country info
            df1.rename(columns={"geographicAreaCode_ISO3": "SpatialDim"}, inplace=True)
            return df1

        df1 = Loading_API_disbursements()
        df1 = pd.merge(df1,
                       country_list,
                       on='SpatialDim',
                       how='left')


        # FILTERS ------------------------------------

        #clear filters button
        def clear_multi():
            for key in st.session_state.keys():
                st.session_state[key] = []

        with st.sidebar:

            # Component filter
            option_Component = st.multiselect(
                'Filter component(s)',
                options=list(df1.componentName.sort_values(ascending=True).unique()),
                key="component_multiselect")
            if len(option_Component) == 0:
                df1_df_group_compo = df1
            else:
                df1_df_group_compo = df1[df1["componentName"].isin(option_Component)]

            # Principal recipient filter
            option_map_pr = st.multiselect(
                'Filter PR type',
                options=list(
                    df1_df_group_compo.principalRecipientSubClassificationName.sort_values(ascending=True).unique()),
                key="pr_multiselect")
            if len(option_map_pr) == 0:
                df_group_pr = df1_df_group_compo
            else:
                df_group_pr = df1_df_group_compo[
                    df1_df_group_compo["principalRecipientSubClassificationName"].isin(option_map_pr)]

            # Region filter
            region_filter = st.multiselect(
                'Select region',
                options=list(df_group_pr.Region.sort_values(ascending=True).unique()),
                key="pr_multiselect")
            if len(region_filter) == 0:
                df1_group_region = df_group_pr
            else:
                df1_group_region = df_group_pr[df_group_pr["Region"].isin(region_filter)]

            # Country filter
            country_filter = st.multiselect(
                'Select country',
                options=list(df1_group_region.geographicAreaName.sort_values(ascending=True).unique()),
                key="pr_multiselect")
            if len(country_filter) == 0:
                df1_group_country = df1_group_region
            else:
                df1_group_country = df1_group_region[df1_group_region["geographicAreaName"].isin(country_filter)]

            # Timeline filter
            if len(df1_group_country) != 0 :
                start_year, end_year = st.select_slider(
                    'Disbursement year range',
                    options=list(
                        df1_group_country.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).unique()),
                    value=(df1_group_country.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).min(),
                           df1_group_country.disbursementDate.astype('datetime64[ns]').dt.year.sort_values(ascending=True).max()))
                # Filtered dataset:
                df1_filtered_dates = df1_group_country[
                    (df1_group_country.disbursementDate.astype('datetime64[ns]').dt.year >= start_year) & (
                            df1_group_country.disbursementDate.astype('datetime64[ns]').dt.year <= end_year)]
            else:
                df1_filtered_dates == df1_group_country

            # Reset filters button
            st.button("Clear filters", on_click=clear_multi)

        # METRICS ------------------------------------
        col1, col2, col3, col4= st.columns([30, 30, 30, 30])
        col1.metric("Number of disbursements","{:,}".format(len(df1_filtered_dates.disbursementAmount)))
        col2.metric("Total amount ($)", "{:,}".format(round(df1_filtered_dates.disbursementAmount.sum())))
        col3.metric("First record", "{}".format(min(df1_filtered_dates.disbursementDate)))
        col4.metric("Last record", "{}".format(max(df1_filtered_dates.disbursementDate)))

        # TABS ------------------------------------
        tab1, tab2, tab3, tab4 = st.tabs(["Disbursements overview 📈", "Disbursements map 🗺️","Components - Region - Country (Sankey Diagram) 📍", "Download Data 🔢"])

        df1_filtered_dates["Year"] = df1_filtered_dates.disbursementDate.astype('datetime64[ns]').dt.year
        df1_filtered_dates["Year"] = df1_filtered_dates["Year"].astype(int)

        with tab1:
            view = st.radio(
                "Select view",
                ('All disbursements','Component', 'Region', 'Principal Recipient'),
                horizontal = True)
            if view == 'All disbursements':
                fig = px.scatter(df1_filtered_dates, x="disbursementDate", y="disbursementAmount",
                                 color="componentName",
                                 log_y=True, hover_data=['disbursementAmount'], color_discrete_map=color_discrete_map,
                                 marginal_y="box", opacity=0.45)
                fig.update_layout(
                    autosize=False,
                    margin=dict(
                        l=0,
                        r=0,
                        b=0,
                        t=50,
                        pad=4,
                        autoexpand=True),
                    height=600,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    legend_title='Component')
                fig.update_traces(opacity=1, marker=dict(line=dict(width=0)))
                fig.update_xaxes(showgrid=False, zeroline=True, title_text="")
                fig.update_yaxes(showgrid=False, zeroline=True, title_text="Total disbursed amount ($)")
                st.plotly_chart(fig, use_container_width=True, config=config)
            if view == 'Component':
                col1, col2, col3 = st.columns([15, 15, 15])
                df_line = df1_filtered_dates[["componentName", "disbursementAmount", "Year"]].groupby(["Year","componentName"]).sum().reset_index()
                fig = px.bar(df_line, x="Year", y="disbursementAmount", color="componentName",color_discrete_map=color_discrete_map)
                fig.update_traces(hovertemplate='%{x} <br> %{y}')
                fig.update_layout(
                    modebar_remove = ['zoom'],
                    autosize=True,
                    margin=dict(
                        l=0,
                        r=0,
                        b=0,
                        t=50,
                        pad=4,
                        autoexpand=True),
                    #width=800,
                    height=380,
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
                col1.plotly_chart(fig, use_container_width=True,config=config)

                fig = px.area(df_line,
                              y = "disbursementAmount",
                              x = "Year",
                              color = "componentName",
                              color_discrete_map=color_discrete_map,
                              groupnorm='percent')
                fig.update_traces(mode="lines",
                                  hovertemplate='%{x} <br> %{y:.2f}%')
                fig.update_layout(
                    autosize=True,
                    margin=dict(
                        l=0,
                        r=0,
                        b=0,
                        t=50,
                        pad=4,
                        autoexpand=True),
                    #width=800,
                    height=400,
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
                col2.plotly_chart(fig, use_container_width=True,config=config)


                df_bar = df1_filtered_dates.groupby(['componentName'], as_index=False)['disbursementAmount'].sum().sort_values('disbursementAmount')
                list_comp = list(df_bar.componentName.unique())
                fig = px.bar(df_bar, y='componentName', x='disbursementAmount',color = 'componentName',
                             text_auto=True, color_discrete_map=color_discrete_map)
                y = list_comp
                fig.update_layout(barmode='stack', yaxis={'categoryorder': 'array', 'categoryarray': y})
                fig.update_traces(hovertemplate=None, hoverinfo='skip')
                                  #paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)")
                for axis in fig.layout:
                    if type(fig.layout[axis]) == go.layout.YAxis:
                        fig.layout[axis].title.text = ''
                    if type(fig.layout[axis]) == go.layout.XAxis:
                        fig.layout[axis].title.text = ''
                fig.update_layout(
                    autosize=True,
                    margin=dict(
                        l=0,
                        r=0,
                        b=0,
                        t=50,
                        pad=4,
                        autoexpand=True
                    ),
                    #width=800,
                    height=400,
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
                col3.plotly_chart(fig, use_container_width=True,config=config)

            if view == 'Region':
                col1, col2, col3 = st.columns([15, 15, 15],gap='medium')
                df_line = df1_filtered_dates[["Region", "disbursementAmount", "Year"]].groupby(["Year","Region"]).sum().reset_index()
                fig = px.bar(df_line, x="Year", y="disbursementAmount", color="Region", color_discrete_map=color_discrete_map2)
                fig.update_traces(hovertemplate='%{x} <br> %{y}')
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
                    height=380,
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
                col1.plotly_chart(fig, use_container_width=True,config=config)

                fig = px.area(df_line,
                              y = "disbursementAmount",
                              x = "Year",
                              color = "Region",
                              color_discrete_map=color_discrete_map2,
                              groupnorm='percent')
                fig.update_traces(mode="lines",
                                  hovertemplate='%{x} <br> %{y:.2f}%')
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
                    height=400,
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
                col2.plotly_chart(fig, use_container_width=True,config=config)


                df_bar2 = df1_filtered_dates.groupby(['Country'], as_index=False)['disbursementAmount'].sum().sort_values(
                    by='disbursementAmount', ascending=True).tail(10)
                fig = px.bar(df_bar2, y='Country', x='disbursementAmount', text_auto=True)
                fig.update_traces(hovertemplate=None, hoverinfo='skip')
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
                    height=400,
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
                col3.plotly_chart(fig, use_container_width=True,config=config)

            if view =="Principal Recipient":
                col1, col2, col3 = st.columns([15, 15, 15],gap='medium')
                df_line = df1_filtered_dates[["principalRecipientSubClassificationName", "disbursementAmount", "Year"]].groupby(["Year","principalRecipientSubClassificationName"]).sum().reset_index()
                fig = px.bar(df_line, x="Year", y="disbursementAmount", color="principalRecipientSubClassificationName", color_discrete_map=color_discrete_map3)
                fig.update_traces(hovertemplate='%{x} <br> %{y}')
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
                    height=400,
                    title={
                        'text': 'Yearly disbursements ($)',
                        'x': 0.5,
                        'xanchor': 'center'},
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                fig.update_xaxes(showgrid=False, zeroline=True)
                fig.update_yaxes(showgrid=True, zeroline=True)
                for axis in fig.layout:
                    if type(fig.layout[axis]) == go.layout.YAxis:
                        fig.layout[axis].title.text = ''
                    if type(fig.layout[axis]) == go.layout.XAxis:
                        fig.layout[axis].title.text = ''
                col1.plotly_chart(fig, use_container_width=True,config=config)

                fig = px.area(df_line,
                              y = "disbursementAmount",
                              x = "Year",
                              color = "principalRecipientSubClassificationName",
                              color_discrete_map=color_discrete_map3,
                              groupnorm='percent')
                fig.update_traces(mode="lines",
                                  hovertemplate='%{x} <br> %{y:.2f}%')
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
                    height=400,
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
                col2.plotly_chart(fig, use_container_width=True,config=config)

                # Top disbursement receivers
                df_pr = df1_filtered_dates.groupby(['principalRecipientSubClassificationName'], as_index=False)['disbursementAmount'].sum().sort_values('disbursementAmount')
                list_pr = list(df_pr.principalRecipientSubClassificationName.unique())
                fig = px.bar(df_pr, y='principalRecipientSubClassificationName', x='disbursementAmount',color = 'principalRecipientSubClassificationName',
                             text_auto=True, color_discrete_map=color_discrete_map3)
                y = list_pr
                fig.update_layout(barmode='stack', yaxis={'categoryorder': 'array', 'categoryarray': y})
                fig.update_traces(hovertemplate=None, hoverinfo='skip')
                                  #paper_bgcolor="rgb(255,255,255)", plot_bgcolor="rgb(255,255,255)")
                for axis in fig.layout:
                    if type(fig.layout[axis]) == go.layout.YAxis:
                        fig.layout[axis].title.text = ''
                    if type(fig.layout[axis]) == go.layout.XAxis:
                        fig.layout[axis].title.text = ''
                fig.update_layout(
                    autosize=True,
                    margin=dict(
                        l=0,
                        r=0,
                        b=0,
                        t=50,
                        pad=4,
                        autoexpand=True
                    ),
                    #width=800,
                    height=400,
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
                col3.plotly_chart(fig, use_container_width=True,config=config)



            #Disbursement map
            with tab2:
                view = st.radio(
                    "Select view",
                    ('All disbursements', 'Per components'),
                    horizontal=True)

                df_geo = df1_filtered_dates.groupby(['componentName', 'geographicAreaName', 'SpatialDim'], as_index=False)[
                    'disbursementAmount'].sum().sort_values(by="disbursementAmount")

                if view == 'All disbursements':
                    fig = go.Figure(
                            data=go.Choropleth(
                                locations=df_geo["SpatialDim"],
                                z = df_geo['disbursementAmount'],
                                colorscale  = "Blues",
                                showscale=True),
                            layout = go.Layout(height=500,
                                               margin=dict(
                                                   l=0,
                                                   r=10,
                                                   b=0,
                                                   t=0,
                                                   pad=4,
                                                   autoexpand=True),
                                               geo=dict(bgcolor='rgba(0,0,0,0)',
                                                        lakecolor='#4E5D6C',
                                                        visible=False,
                                                        landcolor='#3d3d3d',
                                                        showland=True,
                                                        showcountries=True,
                                                        countrycolor='#5c5c5c',
                                                        countrywidth=0.5,
                                                        projection=dict(type='natural earth'))))
                    st.plotly_chart(fig, use_container_width=True,config=config)

                if view == 'Per components':
                    for i in df_geo["componentName"].unique():
                        df_geo2 = df_geo[df_geo["componentName"] ==i]
                        fig = go.Figure(
                            data=go.Choropleth(
                                locations=df_geo2["SpatialDim"],
                                z=df_geo2['disbursementAmount'],
                                colorscale="Blues",
                                showscale=True),
                            layout=go.Layout(height=500,
                                             margin=dict(
                                                 l=0,
                                                 r=10,
                                                 b=0,
                                                 t=10,
                                                 pad=4,
                                                 autoexpand=True),
                                             geo=dict(bgcolor='rgba(0,0,0,0)',
                                                      lakecolor='#4E5D6C',
                                                      visible=False,
                                                      landcolor='#3d3d3d',
                                                      showland=True,
                                                      showcountries=True,
                                                      countrycolor='#5c5c5c',
                                                      countrywidth=0.5,
                                                      projection=dict(type='natural earth'))))
                        fig.update_layout(
                            title={
                                'text': i,
                                'xanchor': 'center',
                                'yanchor': 'top',
                                'x': 0.5
                                },
                            title_font_color = "white")
                        st.plotly_chart(fig, use_container_width=True, config=config)

        # Sankey diagriam
            with tab3:
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
                    colorPalette = ['#04AA6D', '#646464']
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

                st.plotly_chart(fig, use_container_width=True,config=config)

            with tab4:

                col1, col2 = st.columns([8, 20])

                #Dataframe wrangler
                groupby = col1.radio(
                    "Which dataset do you want?",
                    ('Keep the same filters','All disbursements records'))

                if groupby == 'All disbursements records':
                    dl_file = df1[["Country", "componentName", "principalRecipientSubClassificationName", "disbursementDate", "disbursementAmount"]].sort_values(by="disbursementDate",ascending = True)
                if groupby == 'Keep the same filters':
                    dl_file = df1_filtered_dates[["Country", "componentName", "principalRecipientSubClassificationName", "disbursementDate", "disbursementAmount"]].sort_values(by="disbursementDate",ascending = True)

                dl_file.columns = ["Country", "Component", "Principal Recipient", "Disbursement date",
                                   "Disbursement amount ($)"]
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


    # ---- SIDEBAR ----
    with st.sidebar:
        with st.expander("Read more about The Global Fund"):
            # Information on dataset chosen
            info_para = st.empty
            # The Global Fund details
            st.markdown("<p style='text-align: justify;'>"
                    "<a href='https://www.theglobalfund.org/en/'>The Global Fund </a> is a partnership designed to accelerate the end of AIDS, tuberculosis and "
                    "malaria as epidemics. <br> It prioritizes: results-based work, accountability, preparing countries"
                    " for graduation from aid, investing in people as assets for development and inclusive governance."
                    " To do so, the Global Fund mobilizes and invests more than US$4 billion a year to support programs "
                    "run by local experts in more than 100 countries in partnership with governments, civil society, "
                    "technical agencies, the private sector and people affected by the diseases. <br> You can visit <a href='https://www.theglobalfund.org/en/funding-model/'>this page</a> to"
                    " learn more about the organization Funding Model.<br><br>"
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
