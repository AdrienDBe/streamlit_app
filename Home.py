import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json


st.set_page_config(page_title="Home", page_icon="🏚️", layout="wide")

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
    
# ---- HEADER SECTION ----
with st.container():
    st.title("Adrien Debruge")
    col1, col2 = st.columns((2,1))
    with col1:
        st.subheader("Welcome:wave:")
        st.markdown("<p style='text-align: justify;'>"
                    "I am enthusiastic about the intersection of Development and Analytics,"
                    " and constantly searching for new and innovative ways to present and display strategic insights."
                    "<br><br>This website contains my profile information and a collection of personal projects using Python for data visualization and machine learning."
                    "<br><br>If you have any inquiries or feedback, please reach out to me through the form on this page. <br>I hope you find my work engaging."
                    ,
                    unsafe_allow_html=True)
    with col2:
        # picture
        from PIL import Image
        img = Image.open("./Images/Image1_black.png")
        st.image(img,width = 300)

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
        st.write("")
        st.write("")
        st.write("")
        st.write("")
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
        st.markdown('''
        **OPERATIONAL EFFICIENCY** `280+ Grants`
        \n- Business Process Monitoring & Analytics
        \nDevelop and issuance of milestone-driven business process reporting and monitoring for distribution to and use by the Grant Management Division directorate
        \n- Business Process Management
        \nEnsure resolution of challenges escalated by Country Teams, provide analytical support to Grant Operations, Finance and Risk departments
        \n- Business Process Enhancement
        \nDefine enhancements and develop business requirements, review the translation into functional specifications, for the grant lifecycle processes, procedures, system solutions, data flows, quality & reporting
        ''')
    with col2.expander("2020 – 2022 | Cepheid : Lead AccessCare Program Manager"):
        st.markdown('''
        **PROGRAM MANAGEMENT** `9 High-Burden Diseases Countries`
        \n- Created program control and reports to MoHs & global funders
        \n- Coordinated cross-functional teams in EMEA and APAC on program activities
        \n- Managed program: funnel, finance, schedules, risks & opportunities, contracts & maturity road map 
        \n**ANALYTICS: Reporting automation, dashboard development**
        \n- Developped automated reports & dashboards (PowerBI/SFDC/SAP BI) to monitor: program financials, project life cycle, gov. customer KPI, installed base & support status
        \n- Conducted Ad hoc analysis (Python) on instrument reliability in High Burden Developing Countries
        ''')
    with col2.expander("2020 | United Nations : Information Management Specialist"):
        st.markdown('''
        **INFORMATION MANAGEMENT** `Morocco Common Country Analysis (CCA)`
        \nWith the Resident Coordinator Office (RCO):
        \n- Produced information and visualization products in support of resource mobilization for the UN agencies, program advocacy and strategic decision-making for the UN System.
        \nIn the frame of the Common Country Analysis:
            \n - Produced reports on Sustainable Development Goals of the 2030 Agenda and analysis on official development assistance
            \n - Coordinated and reported on internal focus groups of 21 agencies and 136 speakers
        ''')
    with col2.expander("2018 – 2020 | Thales India : In-Country Project Manager"):
        st.markdown('''
        **PROJECT MANAGEMENT**  `Projects of €8M+`
        \n- Managed projects: finance, schedules, Risks & Opportunities, SoW and Technical Proposal
        \n- Managed customer relationship (Govt. and private)
        \n- Created project capability in the local team

        \n**BUSINESS INTELLIGENCE**
        \nTracked and mapped company footprint in India; carried out business simulations  \n

        \n**NGO VOLUNTEERING**
        \n- IT education with _Life Project 4 Youth_: classes on basics of data exploration and data visualization
        \n- ICT project with _Cameroon Association of Active Youth_: ICT for education
        ''')
    with col2.expander("2016 – 2017 | Thales AVS : Service Delivery Manager"):
        st.markdown('''
        **PROJECT MANAGEMENT** `Project of €3M`
        \nCoordinated several departments to oversee the implementation of a project in India:
        \n- Defined support scheme to respect the contractual system availability commitment
        \n- Developed a dedicated IS between France and New Delhi office (VBA) to monitor CRM, logistics, program financial outcome and to generate automated KPIs for Govt. customer
        ''')
    with col2.expander("2016 | Airbus : Analyst trainee"):
        st.markdown('''
        **BUSINESS ANALYSIS** `Simulation and Predictive Analytics`
        \nCarried out a profitability analysis on the creation of a performance simulation department to anticipate the fleet support performance level and optimize logistics schemes (OPUS & SIMLOX)
        ''')


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
            st.markdown("<p style='text-align: justify'>"
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
            st.markdown("<p style='text-align: justify'>"
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
            st.markdown("<p style='text-align: justify'>"
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
                
        with st.expander("World Health Organization: Indicators"):
            st.markdown("<p style='text-align: justify'>"
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
        
        with col2.expander("The Global Fund: Implementation periods, Grants, Disbursements"):
            st.markdown("<p style='text-align: justify'>"
            "Powered by data from the Global Fund API, this app presents information for exploration and visualization."
            " Users can navigate between different dimensions of data, such as region, country, component "
            "(disease), or partner involved, and represent it visually with varying levels of granularity. "
            "The app also provides options for grouping the data by Region, Income level, or Country based"
            " on the user's selection, using the World Bank API.", unsafe_allow_html=True)
            st.markdown(
                "###### [💻 link](https://adrien.streamlit.app/The_Global_Fund)"
            )
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\GF_app.jpg")
            #online
            img = "./Images/GF_app.jpg"
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\GF_app.jpg")
            st.image(img, width=650)     
           

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
    with col2:
        col2.header('IT Skills')
        txt3('Programming', '`Python`, `DAX`, `VBA`')
        txt3('Data processing/wrangling', '`pandas`, `numpy`, `PowerQuery`')
        txt3('Data visualization', '`matplotlib`, `seaborn`, `plotly`, `PowerBI`')
        txt3('Machine Learning', '`scikit-learn`')
        txt3('Model deployment', '`streamlit`')

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
