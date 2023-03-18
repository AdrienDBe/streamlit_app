
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import missingno as msno
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
import json
import requests

st.set_page_config(page_title="Process analysis", page_icon="🔎", layout="centered")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title('Process analysis')
st.write('Python can be used to conduct process analysis and visualize business process outcome in comparison to theoretical process.'
         ' In this page we are going to go through a few steps required to perform such analysis. The main objective being to '
         'generate high-level insights on process performance and identify categories impacting our process.')

# Web app path
path = "./Images/Process_header.json"
# Local path
#path = r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Process_header.json"
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

st.subheader('Getting data')
st.markdown("<p style='text-align: justify'>"
            'First, we need a dataframe containing a list of run or completion timestamps for each step of our process.'
            ' Depending on the type of data we are working with, we might need to extract this data from different sources.'
            "<br><br>  For example, if we are working with customer relationship management (CRM) data, we might need to extract the data from a system like Salesforce. "
            "In this case, we could use the Salesforce API to access the necessary data and retrieve it as a dataframe. This would allow us to easily manipulate and analyze the data using Python."
            " Similarly, if we are working with data from an enterprise resource planning (ERP) system, we might need to extract the data using an extraction, transformation, and loading (ETL) process. "
            "This would involve extracting the necessary data from the ERP system, transforming it into a format suitable for analysis, "
            "and then loading it into a database or other storage system. <br> <br> Once the data is in a suitable format, we could then retrieve it as a dataframe using Python and use it for our analysis."
            " Overall, the specific method for getting data will depend on the type of data we are working with and the systems used to store and manage that data.", unsafe_allow_html=True)
with st.expander('Generating dummy data'):
    st.write('In this example we will be generating dummy data, when using real life data it can be useful to standardize your process'
         ' data by calculating the distance to the theoretical due date of each step, this way you can take into account any intended exceptions or '
         'delays.')
    st.info('''
    You can modify the dummy data parameters below or keep it as is (our dataframe will be called "df")
    ''')

    # Set the number of rows and columns
    num_rows = 500
    num_cols = 5

    col1, col2 = st.columns([1,1], gap='small')
    # Add a Streamlit slider for num_rows and num_cols
    new_num_cols = col1.slider('Number of steps in our process', min_value=1, max_value=20, value=num_cols)
    new_num_rows = col1.slider('Number of completion', min_value=1, max_value=1000, value=num_rows)

    # Update num_rows and num_cols if they have been changed
    if new_num_rows != num_rows:
        num_rows = new_num_rows
    if new_num_cols != num_cols:
        num_cols = new_num_cols

    np.random.seed(12345)
         
    # Create a dictionary of columns with random data
    #data = {f"Step {i}": np.random.randint(-50, 51, num_rows) for i in range(1, num_cols + 1)}
    data = {f"Step {i}": np.random.normal(loc=2.5, scale=1.1, size=num_rows) for i in range(1, num_cols + 1)}


    # Add some outliers randomly generated
    for i in range(50):
        col_name = f"Step {np.random.randint(2, num_cols + 1)}"
        data[col_name][np.random.randint(0, num_rows)] = np.random.randint(0, 50)

    # Add extra random numbers between -100 to +200
    for i in range(num_cols+1, num_cols):
        data[f"Step {num_cols+1}"] = np.random.randint(-100, 201, num_rows)

    # Create the DataFrame
    df = pd.DataFrame(data)

    # Add random NaN values in the last column in the last 1500 rows only
    df.iloc[-40:, -1] = np.nan

    # Display the DataFrame
    col2.dataframe(df)

st.subheader('Dealing with missing values')

st.markdown("<p style='text-align: justify'>"
         'We gathered our data, now we need to make a few verifications before diving into it. <br> '
         'First we want to check if our process data is complete, when analyzing real life data it is very much likely that '
         'not all steps of your process have been completed and we end up with a dataset including missing values.<br> '
         "For this purpose, we can use the 'missingno' library which provides an intuitive way to visualize missing values in our data.", unsafe_allow_html=True)
st.code('''
import missingno as msno
msno.matrix(df)
st.pyplot()
        ''')

def missingno(df):
    fig = msno.matrix(df, labels=True)
    plt.setp(fig.get_yticklabels(), color='white')
    plt.setp(fig.get_xticklabels(), color='white')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    return st.pyplot(fig.figure)
missingno(df)

st.markdown("<p style='text-align: justify'>"
        "Depending of the data and distribution you can either discard the rows with empty value or implement a strategy to replace them by a proxy (step median or average)."
        "<br> In this scenario we are simply going to remove them and consider completed process runs.", unsafe_allow_html=True)
df.dropna(inplace=True)
st.code('df.dropna(inplace=True)')

st.subheader('Dealing with outliers')

st.markdown("<p style='text-align: justify'>"
        "Real life data is full of surprise, and outliers. It is usually recommended to retain them in your dataset. "
        "Similarly to dealing with missing values, you can implement a strategy to replace them if necessary."
        "<br><br> in this example we are going to target the values which are falling outstide of the standard deviation for each step, "
        "meaning values which are either below 87% or above 87% of all values for each specific step.", unsafe_allow_html=True)
st.info('You can visualize the values falling within our outlier category with red dots below')

col1, col2 = st.columns([4, 1], gap='small')
# set the default value to the last column of the dataframe
default_value = df.columns[-1]
# create the selectbox with the default value
option = col2.selectbox('Visualize outliers on', df.columns, index=df.columns.get_loc(default_value))

col1, col2 = st.columns([4, 1], gap='small')

def violin_plots(df):
    # Create a figure with two subplots for each step
    fig = make_subplots(rows=1, cols=len(df.columns), shared_yaxes=True, horizontal_spacing=0.05)
    # Iterate over each step and add the violin and scatter plots to the corresponding subplots
    for i, col in enumerate(df.columns):
        # Add the violin plot to the subplot
        fig.add_trace(go.Violin(y=df[col], name=col, box_visible=True, fillcolor='black', opacity=1, line_color='white',
                                line_width=1,
                                points="all", jitter=0.2, side="negative"), row=1, col=i + 1)
        fig.update_layout(showlegend=False)
    # Set the top margin to 0
    fig.update_layout(showlegend=False, margin=dict(t=0))
    # Show the plot
    return st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
with col1:
    violin_plots(df)

#Visualize Outliers

# Create a figure with two subplots for each step
df_outliers = df.copy()
# Create a new column to identify outliers
df_outliers = df[[option]].copy()

for col in df_outliers.columns:
    mean = df_outliers[col].mean()
    std = df_outliers[col].std()
    N = 1
    upper = mean + N * std
    lower = mean - N * std
    median = df_outliers[col].median()
    outlier = []
    for val in df_outliers[col]:
        if val < lower or val > upper:
            outlier.append(True)
        else:
            outlier.append(False)
    df_outliers['Outlier'] = outlier


# Create figure and axis objects
sns.set(rc={'axes.facecolor':'#0E1117', 'figure.facecolor':(0,0,0,0)})
fig, ax1 = plt.subplots(figsize=(6,20))

for n, i in enumerate(df_outliers.columns[:-1], 1):
    serie = df_outliers[i][df_outliers["Outlier"]==False]
    stripplot_kwargs = dict( native_scale=False, color='white', edgecolor='black', s=17, linewidth=1,
                            alpha=0.7, zorder=1)
    sns.stripplot(y=serie, x=n, **stripplot_kwargs)
    serie = df_outliers[i][df_outliers["Outlier"]==True]
    stripplot_kwargs = dict( native_scale=False, color='red', edgecolor='black', s=20, linewidth=1,
                            alpha=1, zorder=1,jitter=0)
    sns.stripplot(y=serie, x=n, **stripplot_kwargs)
    plt.ylim(bottom=-7, top=53)

sns.despine(top=True, right=True, left=True, bottom=True)
col2.pyplot(fig)

st.write('Our goal here being to generate high-level insight on the overall trend of our processes completion, we are going to deal with these outliers'
         'by replacing them with their step median value.')

#Replacing outliers (~87% above or below column mean) with median value
df_clean = df
for col in df_clean.columns:
    mean = df_clean[col].mean()
    std = df_clean[col].std()

    N = 1
    upper = mean + N * std
    lower = mean - N * std
    median = df_clean[col].median()
    newcol = []
    for val in df_clean[col]:
        if val < lower or val > upper:
            newcol.append(median)
        else:
            newcol.append(val)
    df_clean[col] = newcol
with st.expander('See code sample to detect outliers'):
    code = '''
    df_clean = df.copy()
    for col in df_clean.columns:
        mean = df_clean[col].mean()
        std = df_clean[col].std()
        N = 1
        upper = mean + N * std
        lower = mean - N * std
        median = df_clean[col].median()
        newcol = []
        for val in df_clean[col]:
            if val < lower or val > upper:
                newcol.append(median)
            else:
                newcol.append(val)
        df_clean[col] = newcol'''
    st.code(code, language='python')

st.markdown("<p style='text-align: justify'>"
        "We now have a cleaned, normally distributed, dataset without extreme values that may skew the results:", unsafe_allow_html=True)
violin_plots(df_clean)

import plotly.graph_objects as go
df_outliers_all = df.copy()

# Create a new column to identify outliers for each column in df_outliers
for col in df_outliers_all.columns:
    mean = df_outliers_all[col].mean()
    std = df_outliers_all[col].std()
    N = 1
    upper = mean + N * std
    lower = mean - N * std
    median = df_outliers_all[col].median()
    outlier = []
    for val in df_outliers_all[col]:
        if val < lower or val > upper:
            outlier.append(True)
        else:
            outlier.append(False)
    df_outliers_all[f'{col}_Outlier'] = outlier


###########################################################

np.random.seed(12345)
num_steps = num_cols

# Create the DataFrame
df_gantt = pd.DataFrame(columns=['Step', 'Start', 'End', 'Duration'])

for i in range(1, num_steps + 1):
    start = 0 if i == 1 else df_gantt.loc[i - 2, 'End']
    duration = np.random.randint(low=5, high=21)
    end = start + duration
    df_gantt = df_gantt.append({'Step': i, 'Start': start, 'End': end, 'Duration': duration}, ignore_index=True)


df_gantt.columns = ['Milestone','start_num','end_num','days_start_to_end']
df_gantt.reset_index(inplace=True,drop=True)

#random_gap= 2
#df_gantt['days_start_to_end_cum'] = df_gantt['days_start_to_end']
#df_gantt['days_start_to_end_cum'] = df_gantt['days_start_to_end_cum'].cumsum()-random_gap

# create a random array of numbers between 0 and 5 with the same length as the DataFrame
rand_arr = np.random.randint(0, 5, size=len(df_gantt))
# subtract the random array from the 'days_start_to_end_cum' column
df_gantt['days_start_to_end_cum'] = df_gantt['days_start_to_end'].cumsum() - rand_arr

df2 = df_clean.copy()

for col_idx, col in enumerate(df2.columns):
    # get the corresponding row from df_gantt
    row = df_gantt.iloc[col_idx]

    # add the value of days_start_to_end to the column
    df2[col] += row['days_start_to_end_cum']


st.subheader('Visualizing steps completion')

with st.expander("Gantt representation"):

    # Create figure and axis objects
    sns.set(rc={'axes.facecolor':'#0000FF', 'figure.facecolor':(0,0,0,0)})
    fig, ax1 = plt.subplots(figsize=(16,8))

    # Plot the first graph on the first axis
    ax1.barh(df_gantt.Milestone, df_gantt.days_start_to_end, left=df_gantt.start_num, color= "#04AA6D", edgecolor = "Black",zorder=0)
    for i in df_gantt.end_num.unique():
        ax1.axvline(x=i,color='grey', ls=':', lw=1.5,zorder=1)
    ax1.invert_yaxis()
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax1.axvline(x=0,color='white', ls=':', lw=1)

    stripplot_kwargs = dict(orient="h", native_scale=True, color='white', edgecolor='black', s=10, linewidth=1, alpha=0.7, zorder=1)

    for n, colname in enumerate(df2.columns, 1):
        serie = df2[colname]
        sns.stripplot(x=serie, y=n, **stripplot_kwargs)
        ax1.scatter(x=serie.mean(), y=n, zorder=2, marker="^", s=500, color="white", edgecolor='black', linewidth=2.5,alpha=1)

    ax1.axis("off")
    st.pyplot(fig)

    # generate a list of random category values
    cat_vals = ["Category " + str(np.random.randint(1, 4)) for _ in range(len(df2))]
    # add the categories to the DataFrame
    df2['Category'] = pd.Series(cat_vals)
    df2




st.markdown("<span style='text-align: justify; font-size: 150%; color:#04AA6D'> Section in development </span> </p>",
                unsafe_allow_html=True)
lottie_url = "https://assets5.lottiefiles.com/packages/lf20_s8nnfakd.json"
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json, height=500, key="loading_gif2")
