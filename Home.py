import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json


st.set_page_config(page_title="Global Impact Portfolio", layout="wide")

# Custom function for printing text
def txt3(a, b):
  col1, col2 = st.columns([1,2])
  with col1:
    st.markdown(a)
  with col2:
    st.markdown(b)

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Use CSS for background
with open('./style/wave.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Adding a styled sidebar with hyperlinks (white text, no underline)
with st.sidebar:
    st.header("App Navigation")
    st.text('Business application')
    st.markdown("<a style='text-decoration: none; color: white;' href='https://process-analysis.streamlit.app/'>🔎 Process Analysis</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://adrien-clustering.streamlit.app/'>🔠 Clustering Overview</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://clustering-tool.streamlit.app/'>🧰 Clustering Tool</a>", unsafe_allow_html=True)
    st.text('API Explorer')
    st.markdown("<a style='text-decoration: none; color: white;' href='https://theglobalfund-api.streamlit.app'>🎗️ Global Fund Grants Implementations</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://theglobalfund-disbursements.streamlit.app'>🎗️ Global Fund Grants Disbursements</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://world-health-organization-api.streamlit.app/'>⚕️ WHO Indicators</a>", unsafe_allow_html=True)

    
# ---- HEADER SECTION ----
with st.container():
    st.title("Adrien Debruge")
    col1, col2, col3, col4  = st.columns((2,2,9,1))
    with col3:
        st.subheader("Global impact portfolio")
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
                    "I am enthusiastic about the intersections of Project Management, the Development sector and Analytics."
                    "<br>Constantly searching for new and innovative ways to present and display strategic insights,"
                    " this website contains my profile information and a collection of personal projects using Python for data visualization and machine learning."
                    '<br><br>If you have any inquiries or feedback, please reach out to me at <a href="mailto:adrien.debruge+StreamlitPortfolio@proton.me">adrien.debruge@proton.me</a>'
                    "<br>I hope you find my work engaging."
                    ,
                    unsafe_allow_html=True)
    with col1:
        # picture
        from PIL import Image
        img = Image.open("./Images/fixed.png")
        st.image(img,width = 275)


# ---- Portfolio ----
portfolio_container = st.container()
with portfolio_container:
    st.write("---")
    col1, col2 = st.columns([5, 8])
    col2.header('Portfolio')

    #Web app path
    path = "./Images/Dataviz.json"
    #Local path
    #path = r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Dataviz.json"
    with col1:
        num_empty_lines = 6
        for _ in range(num_empty_lines):
            st.text("")
        with open(path, "r") as file:
            url = json.load(file)
        st_lottie(url,
                  reverse=True,
                  height=400,
                  speed=0.6,
                  loop=True,
                  quality='high',
                  key='Car2')
        
    with col2:
        col2.subheader(':green[Business application]')
        with col2.expander("Process analysis"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "In this post we are looking at how to conduct process analysis and visualize business process outcome," 
            " compared to theoretical process. <br> The app allows you to generate dummy data for customizing "
            "process steps and provides an initial framework to approach process steps pre-processing and visualization."
            , unsafe_allow_html=True)
            st.markdown(
            "###### [💻 link](https://adrien.streamlit.app/Process_Analysis)"
            )
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Process_picture.png")
            #online
            img = "./Images/Process_picture.png"
            st.image(img, width=650)
            
        with col2.expander("Clustering, what's that about?"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "This article provides an overview of clustering analysis in Python, including key concepts such as encoding categorical data, "
            "scaling data, dimensionality reduction, and choosing the right algorithm. This post is designed to help you understand the basics"
            "of clustering analysis in Python and provide you with a solid foundation to build upon as you delve deeper into this topic."
            , unsafe_allow_html=True)
            st.markdown(
            "###### [💻 link](https://adrien.streamlit.app/~/+/Clustering)"
            )
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Clustering_picture.png")
            #online
            img = "./Images/Clustering.png"
            st.image(img, width=650)
            
            
        with col2.expander("Clustering tool"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "This clustering tool enables you to import a CSV file for K-means clustering on one or more columns."
            " It encodes categorical values, scales the dataset, and uses Principal Component Analysis (PCA) for multivariate clustering. "
            "A sample dataset is also available as an option."
            , unsafe_allow_html=True)
            st.markdown(
            "###### [💻 link](https://adrien.streamlit.app/~/+/Clustering_tool)"
            )
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Clustering_picture.png")
            #online
            img = "./Images/Clustering_picture.png"
            st.image(img, width=650)
         
       
        col2.subheader(':green[API explorer]')

        with col2.expander("The Global Fund: Grants/Implementation Periods, Disbursements"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "Powered by data from the Global Fund API, this app presents information for exploration and visualization."
            " Users can navigate between different dimensions of data, such as region, country, component "
            "(disease), or partner involved, and represent it visually with varying levels of granularity. "
            "The app also provides options for grouping the data by Region, Income level, or Country based"
            " on the user's selection, using the World Bank API.", unsafe_allow_html=True)
            st.markdown(
                "###### [💻 link](https://adrien.streamlit.app/The_Global_Fund_API)"
            )
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\GF_app.jpg")
            #online
            img = "./Images/GF_app.jpg"
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\GF_app.jpg")
            st.image(img, width=650)    
                
        with st.expander("World Health Organization: Indicators"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "Powered by data from the World Health Organization (WHO) API, users of the app can explore indicators or"
            " enter relevant keywords. Upon selecting a topic such as Tuberculosis, Malaria, or HIV, "
            "a list of related indicators is presented for visualization. "
            "<br> The app also provides the option to group the data by region, income level, or country "
            "based on user selection, using the World Bank API.", unsafe_allow_html=True)
            # picture
            st.markdown(
                "###### [💻 link](https://adrien.streamlit.app/~/+/World_Health_Organization_API)"
            )
            from PIL import Image
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\WHO_app.jpg")
            #online
            img = "./Images/WHO_app.jpg"
            st.image(img, width=650)

# ---- Work experience ----
work_container = st.container()
with work_container:
    st.write("---")
    col1, col2 = st.columns([5, 8])
    col2.header('Work Experience')

    #Web app path
    path = "Images/Home_work.json"
    #Local path
    #path = r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Home_work.json"
    with col1:
        num_empty_lines = 6
        for _ in range(num_empty_lines):
            st.text("")
        with open(path, "r") as file:
            url = json.load(file)
        st_lottie(url,
                  reverse=True,
                  height=300,
                  speed=0.75,
                  loop=True,
                  quality='high',
                  key='Car'
                  )


    st.markdown("""
    <style>
    .streamlit-expanderHeader {
        font-size: large;
    }
    </style>
    """, unsafe_allow_html=True)

    with col2.expander("2022 – Today | The Global Fund : Officer, Grant Management Division"):
        st.markdown(
            """
            <style>
                .larger-text {
                    font-size: 18px;
                }
            </style>
            
            <p class="larger-text" style='text-align: justify;'>
            <b>OPERATIONAL EFFICIENCY</b> <code>Grant Life Cycle Business Process</code>
            </p>
            
            <ul class="larger-text">
                <li>Business Process Monitoring & Analytics
                    <p>Develop and issuance of milestone-driven business process reporting and monitoring for distribution to and use by the Grant Management Division directorate</p>
                </li>
                <li>Business Process Management
                    <p>Ensure resolution of challenges escalated by Country Teams, provide analytical support to Grant Operations, Finance, and Risk departments</p>
                </li>
                <li>Business Process Enhancement
                    <p>Define enhancements and develop business requirements, review the translation into functional specifications, for the grant lifecycle processes, procedures, system solutions, data flows, quality & reporting</p>
                </li>
            </ul>
            """,
            unsafe_allow_html=True
        )


    with col2.expander("2020 – 2022 | Cepheid : Lead AccessCare Program Manager"):
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        '''
        <b>PROGRAM MANAGEMENT</b> <code>9 High-Burden Diseases Countries</code>
        \n- Managed AccessCare program including financial, schedules, R&O, contracts and maturity road map
        \n- Implemented program standardization & governance framework for cross-regional application (SOP, Toll-Gate, Country Reviews & Steering Committee)
        \n- Coordinated cross-functional teams in EMEA and APAC on program activities: 30+ stakeholders; 9 countries
        \n- Managed program: funnel, finance, schedules, risks & opportunities, contracts & maturity road map 
        \n**ANALYTICS: Reporting automation, dashboard development**
        \n- Developped automated reports & dashboards (PowerBI/SFDC/SAP BI) to monitor: program financials, project life cycle, gov. customer KPI, installed base & support status
        \n- Conducted Ad hoc analysis (Python) on instrument reliability in High Burden Developing Countries        
        ''', unsafe_allow_html=True)
    with col2.expander("2020 | United Nations : Information Management Specialist"):
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        '''
        <b>INFORMATION MANAGEMENT</b> <code>Morocco Common Country Analysis (CCA)</code>
        \nWith the Resident Coordinator Office (RCO):
        \n- Produced information and visualization products in support of resource mobilization for the UN agencies, program advocacy and strategic decision-making for the UN System.
        \nIn the frame of the Common Country Analysis:
            \n - Produced reports on Sustainable Development Goals of the 2030 Agenda and analysis on official development assistance
            \n - Coordinated and reported on internal focus groups of 21 agencies and 136 speakers
        ''', unsafe_allow_html=True)
    with col2.expander("2018 – 2020 | Thales India : In-Country Project Manager"):
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        '''
        <b>PROJECT MANAGEMENT</b> <code>Projects of €8M+</code>
        \n- Managed projects: finance, schedules, Risks & Opportunities, SoW and Technical Proposal
        \n- Managed customer relationship (Govt. and private)
        \n- Created project capability in the local team

        \n<b>BUSINESS INTELLIGENCE</b>
        \nTracked and mapped company footprint in India; carried out business simulations  \n

        \n<b>NGO VOLUNTEERING</b>
        \n- IT education with _Life Project 4 Youth_: classes on basics of data exploration and data visualization
        \n- ICT project with _Cameroon Association of Active Youth_: ICT for education
        ''', unsafe_allow_html=True)
    with col2.expander("2016 – 2017 | Thales AVS : Service Delivery Manager"):
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        '''
        <b>PROJECT MANAGEMENT</b> <code>Project of €3M</code>
        \nCoordinated several departments to oversee the implementation of a project in India:
        \n- Defined support scheme to respect the contractual system availability commitment
        \n- Developed a dedicated IS between France and New Delhi office (VBA) to monitor CRM, logistics, program financial outcome and to generate automated KPIs for Govt. customer
        ''', unsafe_allow_html=True)
    with col2.expander("2016 | Airbus : Analyst trainee"):
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        '''
        <b>*BUSINESS ANALYSIS</b> <code>Simulation and Predictive Analytics</code>
        \nCarried out a profitability analysis on the creation of a performance simulation department to anticipate the fleet support performance level and optimize logistics schemes (OPUS & SIMLOX)
        ''', unsafe_allow_html=True)



st.write('---')

# ---- IT Skills ----
# Custom function for printing text
def txt3(a, b):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(a)
    with col2:
        st.markdown(b)

skills_container = st.container()
with skills_container:
    col1, col2 = st.columns([5, 8])
    with col1:
        # Web app path
        path = "./Images/Computer.json"
        # Local path
        # By Downloading and importing path
        #path = r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Computer.json"
        with col1:
            with open(path, "r") as file:
                url = json.load(file)
            st_lottie(url,
                      reverse=True,
                      height=350,
                      speed=1,
                      loop=True,
                      quality='high',
                      key='Car3')
    def txt3(title, content):
      st.markdown(f"<p style='font-size: 18px;'>{title}: <code>{content}</code></p>", unsafe_allow_html=True)
    with col2:
        col2.header('IT Skills')
        txt3('Programming', 'Python, DAX, VBA')
        txt3('Data Processing', 'pandas, numpy, PowerQuery')
        txt3('Data Visualization', 'matplotlib, seaborn, plotly, PowerBI')
        txt3('Machine Learning', 'scikit-learn')
        txt3('Model Deployment', 'streamlit')

# ---- CONTACT FORM ----

# contact_form_container = st.container()
# with contact_form_container:
#     st.write("---")
#     st.header("Get in touch with me!")
#     st.write("##")
# 
#     # Documention: https://formsubmit.co/
#     contact_form = """
#         <form action="https://formsubmit.co/b5839c863db066636bf7d8e36d51e283" method="POST">
#             <input type="hidden" name="_captcha" value="false">
#             <input type="text" name="name" placeholder="Your name" required>
#             <input type="email" name="email" placeholder="Your email" required>
#             <textarea name="message" placeholder="Your message here" required></textarea>
#             <button type="submit">Send</button>
#         </form>
#         """
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.markdown(contact_form, unsafe_allow_html=True)
#     with right_column:
#         st.empty()
