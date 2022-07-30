import streamlit as st

# emojis list: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title="Adrien Debruge", page_icon=":computer:", layout="wide")

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
        st.header("Welcome:wave:")
        st.markdown("<p style='text-align: justify;'>I am passionate about International Development, "
                    "Technology and looking for ways to frame and visualize strategic insights.<br>"
                    "<br> This web app is built on Streamlit and here you will find information on my profile along"
                    " with a portfolio of projects. Please note that I am no expert, just a casual coder and analytics"
                    " practitioner so any feedback is welcome!<br>"
                    "<br>Feel free to reach out via the form at the bottom of this page and I hope you enjoy my work.",
                    unsafe_allow_html=True)
    with col2:
        # picture
        from PIL import Image
        img = Image.open("./Images/Image1.png")
        st.image(img,width = 250)

    # ---- Work experience & IT skills ----

    st.markdown("""
    <style>
    .streamlit-expanderHeader {
        font-size: x-large;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.expander("Work Experience"):
        st.markdown(
        "<span style='color:green'>2020 – 2022 | Cepheid : Lead AccessCare Program Manager</span>   <br>"
        "<u>PROGRAM MANAGEMENT</u> `10 High-Burden Diseases Countries` <br>"
         "▹ Created program control and reports to MoHs & global funders <br>"
         "▹ Coordinate cross-functional teams in EMEA and APAC on program activities <br>"
         "▹ Manage program: funnel, finance, schedules, risks & opportunities, contracts & maturity road map <br>"

        "<u>ANALYTICS</u><br>"
         "▹ Developped automated reports & dashboards (PowerBI/SFDC/SAP BI) to monitor: program financials, project life cycle, gov. customer KPI, installed base & support status<br>"
         "▹ Conducted Ad hoc analysis (Python) on instrument reliability in High Burden Developing Countries<br>"
        
        "<br><span style='color:green'>2020 | United Nations : Information Management Specialist</span>   <br>"      
        "<u>INFORMATION MANAGEMENT</u> `Morocco Common Country Analysis (CCA)`<br>"
         "With the Resident Coordinator Office (RCO): <br>"
         "▹ Produced information and visualization products in support of resource mobilization for the UN agencies, program advocacy and strategic decision-making for the UN System. <br>"
         "▹ In the frame of the Common Country Analysis: <br>"
         "     - Produced reports on Sustainable Development Goals of the 2030 Agenda and analysis on official development assistance<br>"
         "     - Coordinated and reported on internal focus groups of 21 agencies and 136 speakers<br>"

        "<br><span style='color:green'>2018 – 2020 | Thales India : In-Country Project Manager</span>"
        "<br><u>PROJECT MANAGEMENT</u> `Projects of €8M+`<br>"
        "With the Resident Coordinator Office (RCO): <br>"
        "Managed projects: finance, schedules, Risks & Opportunities, SoW and Technical Proposal<br>"
        "Managed customer relationship (Govt. and private)<br>"
        "Created project capability in the local team<br>"

        "<u>BUSINESS INTELLIGENCE</u> <br>"
        "Tracked and mapped company footprint in India; carried out business simulations<br>"

        "<br><span style='color:green'>2016 – 2017 | Thales AVS : Service Delivery Manager</span>"
        "<br><u>PROJECT MANAGEMENT</u> `Projects of €3M`<br>"
        "Coordinated several departments to oversee the implementation of a project in India: <br>"
        "▹ Defined support scheme to respect the contractual system availability commitment<br>"
        "▹ Developed a dedicated IS between France and New Delhi office (VBA) to monitor CRM, logistics, program financial outcome and to generate automated KPIs for Govt. customer<br>"

        "<br><span style='color:green'>2016 | Airbus : Analyst trainee</span>"
        "<br><u>BUSINESS ANALYSIS</u> `Simulation and Predictive Analytics`<br>"
        "Carried out a profitability analysis on the creation of a performance simulation department to anticipate the fleet support performance level and optimize logistics schemes (OPUS & SIMLOX)<br>"
        ,unsafe_allow_html = True)

    with st.expander("IT Skills"):
        txt3('Programming', '`Python`, `DAX`, `VBA`')
        txt3('Data processing/wrangling', '`pandas`, `numpy`, `PowerQuery`')
        txt3('Data visualization', '`matplotlib`, `seaborn`, `plotly`, `PowerBI`')
        txt3('Machine Learning', '`scikit-learn`')
        txt3('Model deployment', '`streamlit`')


    # ---- CONTACT FORM ----
    # Use local CSS
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style/style.css")

    contact_form_container = st.container()
    with contact_form_container:
        st.write("---")
        st.header("Get in touch with me!")
        st.write("##")

        # Documention: https://formsubmit.co/
        contact_form = """
            <form action="https://formsubmit.co/b5839c863db066636bf7d8e36d51e283" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here" required></textarea>
                <button type="submit">Send</button>
            </form>
            """
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown(contact_form, unsafe_allow_html=True)
        with right_column:
            st.empty()

