import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json

st.set_page_config(page_title="Adrien Debruge portfolio – From data to action", layout="wide")

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
# Add custom CSS for styling
st.markdown(
    """
    <style>
    /* Sidebar font styling */
    [data-testid="stSidebar"] .st-markdown-container {
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        line-height: 1.5;
    }
    [data-testid="stSidebar"] a {
        text-decoration: none;
        color: white;
    }
    [data-testid="stSidebar"] a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Projects")
    st.markdown("<p style='text-align: left; font-size: 18px;'><u>Business application:</u></p>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://evm-support.streamlit.app/'>🎯 Earned Value Management</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://process-analysis.streamlit.app/'>🔎 Process Analysis</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://adrien-clustering.streamlit.app/'>🔠 Clustering Overview</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://clustering-tool.streamlit.app/'>🧰 Clustering Tool</a>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; font-size: 18px;'><u>API Explorers:</u></p>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://theglobalfund-api.streamlit.app'>🌐 Global Fund Grants Implementations</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://theglobalfund-disbursements.streamlit.app'>🌐 Global Fund Grants Disbursements</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://theglobalfundallocations.streamlit.app/'>🌐 Grants Allocations</a>", unsafe_allow_html=True)
    st.markdown("<a style='text-decoration: none; color: white;' href='https://world-health-organization-api.streamlit.app/'>⚕️ WHO Indicators</a>", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Hide the link button in the main area only */
    .main .stApp a:first-child {
        display: none;
    }
    
    .main .css-15zrgzn {display: none}
    .main .css-eczf16 {display: none}
    .main .css-jn99sy {display: none}
    </style>
    """, unsafe_allow_html=True)


# ---- HEADER SECTION ----
with st.container():
    resume_url = "https://github.com/AdrienDBe/streamlit_app/raw/main/Images/2025%2006%20-%20Resume%20Adrien%20Debruge.pdf"
    response = requests.get(resume_url)
    col1, col2  = st.columns((4,7))
    with col1:
        st.title("Adrien Debruge")
        st.subheader("From data to action")
        st.markdown(
            "<p style='text-align: justify; font-size: 18px;'>"
            "We're living in a world overflowing with data, and making sense of it all is key to making smart decisions and running things smoothly. "
            "My portfolio is all about showing how data can be transformed into practical insights and actions through the right tools and techniques. "
            "<br><br>"
            "With a focus on Python, I've put together some interactive projects and visualizations that demonstrate how complex data can be simplified and turned into useful information. "
            "But this isn't just for the tech-savvy; it's for anyone in any field. Being able to understand, manipulate, and apply data, even using advanced methods like machine learning and AI, can really make a difference in how we work and the decisions we make. "
            "<br><br>"
            "This collection is here to show how important data skills are for everyone. Whether you're presenting to your team or making big decisions, having a handle on data can help you make your point clearly and confidently. "
            "<br><br>"
            'For inquiries or feedback, feel free to reach out at <a href="mailto:adrien.debruge+StreamlitPortfolio@proton.me">adrien.debruge@proton.me</a>'
            "</p>",
            unsafe_allow_html=True
        )

        st.download_button(
        label="📄 Download my resume (PDF)",
        data=response.content,
        file_name="Adrien_Debruge_CV.pdf",
        mime="application/pdf")
          
    with col2:
        # picture
        st.markdown(
           "<br><br><br><br><br><br>",
            unsafe_allow_html=True)
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
        num_empty_lines = 9
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
        with col2.expander("Monitoring project performance with Earned Value Management (EVM)"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
                "This post introduces Earned Value Management (EVM) principles to track and forecast project progress and financial outcomes. "
                "The dashboard enables users to simulate data, evaluate key indicators like CPI, SPI, CV, and EAC, "
                "and visualize how project performance evolves under different scenarios (positive, neutral, negative).<br> "
                "It also provides a few insights on how to deploy EVM concepts within an organization for real-time decision-making."
                , unsafe_allow_html=True)
            st.markdown(
                "###### [📊 link](https://evm-support.streamlit.app/)"
            )
            # Image preview
            img = "./Images/EVM_simulation.png"
            st.image(img, width=400)

        with col2.expander("Conducting process analysis and visualizing business outcomes "):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "In this post we are looking at how to conduct process analysis and visualize business process outcome," 
            " compared to theoretical process. <br> The app allows you to generate dummy data for customizing "
            "process steps and provides an initial framework to approach process steps pre-processing and visualization."
            , unsafe_allow_html=True)
            st.markdown(
            "###### [💻 link](https://process-analysis.streamlit.app)"
            )
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Process_picture.png")
            #online
            img = "./Images/Process_picture.png"
            st.image(img, width=650)
            
        with col2.expander("Introduction to clustering analysis in python"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "This article provides an overview of clustering analysis in Python, including key concepts such as encoding categorical data, "
            "scaling data, dimensionality reduction, and choosing the right algorithm. This post is designed to help you understand the basics"
            "of clustering analysis in Python and provide you with a solid foundation to build upon as you delve deeper into this topic."
            , unsafe_allow_html=True)
            st.markdown(
            "###### [💻 link](https://adrien-clustering.streamlit.app)"
            )
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Clustering_picture.png")
            #online
            img = "./Images/Clustering.png"
            st.image(img, width=650)
            
            
        with col2.expander("K-means clustering tool with encoding, scaling, and PCA"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "This clustering tool enables you to import a CSV file for K-means clustering on one or more columns."
            " It encodes categorical values, scales the dataset, and uses Principal Component Analysis (PCA) for multivariate clustering. "
            "A sample dataset is also available as an option."
            , unsafe_allow_html=True)
            st.markdown(
            "###### [💻 link](https://clustering-tool.streamlit.app)"
            )
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Clustering_picture.png")
            #online
            img = "./Images/Clustering_picture.png"
            st.image(img, width=650)
         
       
        col2.subheader(':green[API explorer]')

        with col2.expander("Global Fund Grants life cycle overview"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "Powered by data from the Global Fund API, this app presents information for exploration and visualization."
            " Users can navigate between different dimensions of data, such as region, country, component "
            "(disease), or partner involved, and represent it visually with varying levels of granularity. "
            "The app also provides options for grouping the data by Region, Income level, or Country based"
            " on the user's selection, using the World Bank API.", unsafe_allow_html=True)
            st.markdown(
                "###### [💻 link](https://theglobalfund-api.streamlit.app)"
            )
            #local
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\GF_app.jpg")
            #online
            img = "./Images/GF_app.jpg"
            #img = Image.open(r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\GF_app.jpg")
            st.image(img, width=650)    

        with col2.expander("Global Fund disbursement analysis tool"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "This app leverages data from the Global Fund API to visualize and explore disbursement records."
            " Users can filter and analyze the data based on various dimensions such as grant component, PR type,"
            " region, and portfolio. The visualization options include scatter plots and box plots, providing a"
            " comprehensive view of the disbursements over time and across different categories."
            " Interactive filters allow for tailored data insights and improved understanding of fund allocation."
            "</p>", unsafe_allow_html=True)
            st.markdown(
                "###### [💻 link](https://theglobalfund-disbursements.streamlit.app)"
            )
            img = "./Images/Disbursements.png"
            st.image(img, width=650)

        with col2.expander("Global Fund allocations and clustering analysis "):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
                        "This app leverages data from the Global Fund API to visualize and explore allocation records."
                        " Users can also create clusters of countries using Scikit-learn, enhancing the analysis of fund"
                        " allocation patterns. Additionally, there is an option to download the cluster dataset for further"
                        " analysis."
                        "</p>", unsafe_allow_html=True)
            st.markdown(
                "###### [💻 link](https://theglobalfundallocations.streamlit.app)"
            )
            img = "./Images/Allocations.png"
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
                "###### [💻 link](https://world-health-organization-api.streamlit.app)"
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

    with col2.expander("2024 – Today | The Global Fund: Program Officer, High Impact Africa 1"):
      st.markdown(
          """
          <style>
              .larger-text {
                  font-size: 18px;
              }
          </style>
          
          <p class="larger-text" style='text-align: justify;'>
          <b>PROGRAM MANAGEMENT & STRATEGY</b> <code>Grant Management Division</code>
          </p>
          
          <ul class="larger-text">
            <li>Business Intelligence
                <p>Develop and deliver insight reports to senior leadership to enable proactive monitoring of grants, trend analysis and process improvements and prioritization across portfolios ($2.9 billion allocation).</p>
            </li>
            <li>Program Management
                <p>Coordinate grant lifecycle processes, including budget reviews, disbursement requests, and work plans, ensuring compliance with organizational objectives</p>
            </li>
            <li>Risk Management
                <p>Identify and mitigate grant management risks, ensuring data integrity and adherence to policies in all processes</p>
            </li>
          </ul>
          """,
          unsafe_allow_html=True
      )


  
    with col2.expander("2022 – 2024 | The Global Fund : Business Process Reporting Officer"):
        st.markdown(
            """
            <style>
                .larger-text {
                    font-size: 18px;
                }
            </style>
            
            <p class="larger-text" style='text-align: justify;'>
            <b>OPERATIONAL EFFICIENCY</b> <code>Grant Management Division</code>
            </p>
            
            <ul class="larger-text">
              <li>Process Optimization and Strategic Enhancements
                  <p>Led the optimization of grant lifecycle processes by capturing business requirements and translating into functional specifications.</p>
              </li>
              <li>Business Process Analytics
                  <p>Developped BI frameworks using Python and Salesforce Analytics, enhancing strategic reporting and decision-making processes for senior management and policy hubs </p>
              </li>
            </ul>
            """,
            unsafe_allow_html=True
        )


    with col2.expander("2020 – 2022 | Cepheid (Danaher Group): Lead Program Manager"):
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        '''
        <b>FINANCIAL OVERSIGHT & GOVERNANCE EXCELLENCE</b> <code>Govt. projects in EMEA and APAC</code>
        \n- Management of AccessCare program ($8 million): financial, schedules, risks, contracts and maturity road map
        \n- Developed reports and dashboards (Python, PowerBI DAX) to monitor program financials, including Earned Value Management (EVM) for cost performance and project progress, baseline budgets and cost-to-completion projections to ensure accurate Actual vs. Budget reporting and provide variance analysis to senior leadership
        \n- Implemented a program standardization and governance framework, incorporating DBS Toll-Gate reviews for project lifecycle management with Phase Gate methodology, and structured Country Reviews & Steering Committee sessions to ensure consistent project oversight, risk management, and alignment.        
        ''', unsafe_allow_html=True)
    with col2.expander("2020 | United Nations : Information Management Specialist"):
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        '''
        <b>INFORMATION MANAGEMENT</b> <code>Analytics for the Resident Coordinator Office</code>
        \nWith the Resident Coordinator Office (RCO) of the UN in Morocco:
        \n- Produced information and visualization products in support of resource mobilization for the UN agencies, program advocacy and strategic decision-making for the UN System.
        \nIn the frame of the Common Country Analysis:
            \n - Produced reports on Sustainable Development Goals of the 2030 Agenda and analysis on official development assistance
            \n - Coordinated and reported on internal focus groups of 21 agencies and 136 speakers
        ''', unsafe_allow_html=True)
      
    with col2.expander("2018 – 2020 | Thales India: In-Country Project Manager"):
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        '''
        <b>PROJECTS IMPLEMENTATION & ANALYTICS</b> <code>Operations & business analyses across India</code>
        \n- Led India support programs in coordination with France PMO
        \n- Oversaw financial planning, budgeting, forecasting, risk/opportunity assessment, and customer engagement (Govt. & private)
        \n- Conducted business analyses (Python) to assess organizational structure and regional operations, identifying optimization opportunities
        ''', unsafe_allow_html=True)
    
    with col2.expander("2016 – 2017 | Thales AVS: Service Delivery Manager"):
        st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        '''
        <b>SYSTEM DESIGN FOR SERVICE AVAILABILITY</b> <code>Logistics, KPI automation, and IT solutions</code>
        \n- Managed rollout of a testing bench for fighter jets autopilot systems in India
        \n- Designed a supply chain model aligned with system availability contract requirements
        \n- Developed an IT solution (VBA) to streamline logistics, monitor financials, and automate KPI generation between France and New Delhi teams
        ''', unsafe_allow_html=True)
    
    
        with col2.expander("2016 | Airbus : Analyst trainee"):
            st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            '''
            <b>*BUSINESS ANALYSIS</b> <code>Simulation and predictive analytics investment case</code>
            \nDeveloped an investment case for establishing a performance simulation department to project support performance and optimize logistics schemes (SIMLOX, OPUS)
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
        txt3('Programming', 'Python, SQL, VBA')
        txt3('Data Processing', 'pandas, numpy, PowerQuery, Salesforce recipies')
        txt3('Data Visualization', 'matplotlib, seaborn, plotly, PowerBI (DAX), Salesforce Analytics')
        txt3('Machine Learning', 'scikit-learn')
        txt3('Model Deployment', 'Streamlit, Azure')

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
