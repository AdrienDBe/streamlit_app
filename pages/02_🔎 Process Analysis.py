
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
             #MainMenu {visibility: visible;}
             footer {visibility: visible;}
             header {visibility: visible;}
             </style>
             """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Use local CSS for background waves
with open('./style/wave.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


st.title('Process analysis')
st.markdown("<p style='text-align: justify; font-size: 18px;'>"'Python can be used to conduct process analysis and visualize business process outcome in comparison to the theoretical process duration.'
         '<br>In this page we are going to go through a few steps required to perform such analysis. The main objective being to '
         'generate high-level insights on process performance and identify categories impacting our process.', unsafe_allow_html=True)

# Web app path
path = "Images/Process_header.json"
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
st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            'The dataframe we will be working with has to contain a list of run, or completion timestamps, for each step of our process.'
            '<br><br> Depending on the type of data we are working with, we might need to extract this data from different sources.'
            " For instance, if we are dealing with CRM data, we will access data from a system like Salesforce using "
            "the Salesforce API. Similarly, if we are working with ERP data, we might need to use an ETL process to extract, "
            "transform and load the data into a suitable format for analysis. Once the data is in the required format, we can "
            "easily manipulate and analyze it using Python."
            "<br><br> Once you retrieve your process data it can be useful to standardize it by calculating the distance to the theoretical "
            "due date for each step, this way you can go beyond any intended exceptions or delays which might skew your analysis.", unsafe_allow_html=True)
with st.expander('Generating dummy data'):
    st.info('''
    Modify the dummy data parameters below (or keep it as is)
    ''')

    # Set the number of rows and columns
    num_rows = 500
    num_cols = 5

    col1, col2 = st.columns([1,1], gap='small')
    # Add a Streamlit slider for num_rows and num_cols
    new_num_cols = col1.slider('Number of steps in our process', min_value=1, max_value=7, value=num_cols)
    new_num_rows = col1.slider('Number of completion', min_value=1, max_value=1000, value=num_rows)

    # Update num_rows and num_cols if they have been changed
    if new_num_rows != num_rows:
        num_rows = new_num_rows
    if new_num_cols != num_cols:
        num_cols = new_num_cols

    np.random.seed(12345)
    # Create a dictionary of columns with random data
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
    # calculate the number of columns to select
    x = int(3 / 4 * len(df.columns))
    # select the last x columns and replace random values with NaN
    df.iloc[:, -x:] = df.iloc[:, -x:].where(np.random.rand(*df.iloc[:, -x:].shape) > 0.1, np.nan)
    # Add random NaN values in the last column
    df.iloc[-40:, -1] = np.nan
    # Display the DataFrame
    col2.dataframe(df)

with st.expander('See sample code to generate dummy data'):
    code = '''
# Define the size of the dataframe
rows  = 50
cols = 5
# Create a dictionary of columns with random data
data = {f"Step {i}": np.random.normal(loc=2.5, scale=1.1, size=rows ) for i in range(1, cols + 1)}
# Add some outliers randomly generated
for i in range(50):
    col_name = f"Step {np.random.randint(2, cols + 1)}"
    data[col_name][np.random.randint(0, rows )] = np.random.randint(0, 50)
# Create the DataFrame
df = pd.DataFrame(data)
# Select the last x columns and replace random values with NaN
# calculate the number of columns to select
x = int(3 / 4 * len(df.columns))
# Add Nan values
df.iloc[:, -x:] = df.iloc[:, -x:].where(np.random.rand(*df.iloc[:, -x:].shape) > 0.1, np.nan)'''
    st.code(code, language='python')

st.subheader('Dealing with missing values')

st.markdown("<p style='text-align: justify; font-size: 18px;'>"
         'We gathered our data, now we need to make a few verifications before diving into it. <br><br> '
         'First we want to check if our process data is complete, when analyzing real life data it is very much likely that '
         'not all steps of your process have been completed and this will result in dealing with a dataset including missing values.<br> '
         "For this purpose, we can use the 'missingno' library which provides an intuitive way to visualize it:", unsafe_allow_html=True)

def missingno(df):
    fig = msno.matrix(df, labels=True)
    plt.setp(fig.get_yticklabels(), color='white')
    plt.setp(fig.get_xticklabels(), color='white')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    return st.pyplot(fig.figure)
missingno(df)

with st.expander('See code to visualize missing data with the missingno library'):
    code = '''
# Import the missingno package
import missingno as msno
# Visualize the missing data using missingno
msno.matrix(df)'''
    st.code(code, language='python')

st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        "Depending of the data, you can either discard the rows with empty value or implement a strategy to replace them by a proxy (step median or average)."
        " In this scenario we are simply going to remove them and consider completed process runs only.", unsafe_allow_html=True)
df.dropna(inplace=True)
df.reset_index(drop=True,inplace=True)

with st.expander('See sample code to remove missing values'):
    st.code(
'''df.dropna(inplace=True)
df.reset_index(drop=True,inplace=True)''')

st.subheader('Dealing with outliers')

st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        "Real life data is full of surprise, and outliers. It is usually recommended to retain them in your dataset. "
        "Similarly to dealing with missing values, you can implement a strategy to replace them too."
        "<br><br> In this example we are going to target the values which are falling outstide of the standard deviation for each step, "
        "meaning the values either 87% below or above the mean.", unsafe_allow_html=True)

with st.expander('See sample code to detect outliers'):
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

st.info('You can visualize the values identified as outliers with red dots below')
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

st.write('Our goal here being to generate high-level insight on the overall trend of our processes completion, we dealt with these outliers'
         ' by replacing them with their step median value.')

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


st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        "We now have a cleaned, normally distributed, dataset without extreme values that may skew our process analysis:", unsafe_allow_html=True)
violin_plots(df_clean)

with st.expander('See sample code to create a violin and scatter plots visual using the plotly library'):
    code = '''
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Create a dummy dataframe with random numerical values
df = pd.DataFrame(np.random.randn(100, 5), columns=["A", "B", "C", "D", "E"])

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
fig.show()
'''
    st.code(code, language='python')

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
    new_row = {'Step': i, 'Start': start, 'End': end, 'Duration': duration}
    df_gantt = pd.concat([df_gantt, pd.DataFrame([new_row])], ignore_index=True)

df_gantt.columns = ['Milestone','start_num','end_num','days_start_to_end']
df_gantt.reset_index(inplace=True,drop=True)

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
import streamlit as st

st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        "One way of have a visual representation of our process timeliness is to lay our data over a gantt chart. "
        "<br> A gant chart is a type of bar chart that illustrates a project schedule. "
            "In a Gantt chart, each bar represents a task or activity, and the length of the bar represents"
            " the duration of the task."
            , unsafe_allow_html=True)

sns.set(rc={'axes.facecolor': '#0000FF', 'figure.facecolor': (0, 0, 0, 0)})
fig, ax1 = plt.subplots(figsize=(16, 8))
# Plot the first graph on the first axis
ax1.barh(df_gantt.Milestone, df_gantt.days_start_to_end, left=df_gantt.start_num, color="#04AA6D", edgecolor="Black",
         zorder=0)
for i in df_gantt.end_num.unique():
    ax1.axvline(x=i, color='grey', ls=':', lw=1.5, zorder=1)

# Add the name of the column on each bar
for i, (milestone, start, end) in enumerate(zip(df_gantt.Milestone, df_gantt.start_num, df_gantt.end_num)):
    ax1.text((start + end) / 2, i+0.4, "Step {}: {} days".format(milestone,end-start), ha='center', va='center', fontsize=17, color='white', fontweight='bold')

ax1.invert_yaxis()
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax1.axvline(x=0, color='white', ls=':', lw=1)
ax1.axis("off")
st.pyplot(fig)

st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        "Now that we have a clean dataset we can start visualizing our process data "
        "by overlaying our process timeliness data onto a Gantt chart. "
            "The idea being to easily also identify any bottlenecks or delays in the process and optimize our workflow accordingly."
        "<br>In the graph below, each dot represents a step completion timeliness. "
            "The big triangle represents the average timeliness for each step.", unsafe_allow_html=True)

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

stripplot_kwargs = dict(orient="h", jitter=0.25, native_scale=True, color='white', edgecolor='black', s=10, linewidth=1, alpha=0.5, zorder=1)

for n, colname in enumerate(df2.columns, 1):
    serie = df2[colname]
    sns.stripplot(x=serie, y=n, **stripplot_kwargs)
    ax1.scatter(x=serie.mean(), y=n, zorder=2, marker="^", s=500, color="white", edgecolor='black', linewidth=2.5,alpha=1)

ax1.axis("off")
st.pyplot(fig)

with st.expander('See sample code to reproduce this visual'):
    code = '''
import seaborn as sns
import matplotlib.pyplot as plt

# Define the DataFrame
df = pd.DataFrame({
    "Milestone": ["Milestone A", "Milestone B", "Milestone C", "Milestone D", "Milestone E"],
    "days_start_to_end": [10, 15, 12, 8, 20],
    "start_num": [0, 10, 25, 37, 45],
    "end_num": [10, 25, 37, 45, 65],
    "col1": [5, 10, 12, 8, 15],
    "col2": [15, 7, 9, 11, 20],
    "col3": [8, 14, 10, 6, 13]
})

# Create figure and axis objects
fig, ax1 = plt.subplots(figsize=(16,8))

# Plot the first graph on the first axis
ax1.barh(df["Milestone"], df["days_start_to_end"], left=df["start_num"], color="#04AA6D", edgecolor="Black", zorder=0)
ax1.invert_yaxis()

for n, colname in enumerate(df.columns[5:], 1):
    serie = df[colname]
    sns.stripplot(x=serie, y=n, orient="h", jitter=0.25, native_scale=True, color='white', edgecolor='black', s=10, linewidth=1, alpha=0.5, zorder=1)
    ax1.scatter(x=serie.mean(), y=n, zorder=2, marker="^", s=500, color="white", edgecolor='black', linewidth=2.5,alpha=1)

ax1.axis("off")
plt.show()
'''
    st.code(code, language='python')

col1, col2 = st.columns([1, 1], gap='small')

col1.markdown("<p style='text-align: justify; font-size: 18px;'>"
        "The visualization is helpful to get an overall idea of how our process unfolded in real life, "
        "but it is also good to have high-level average values to share:", unsafe_allow_html=True)
df2_duration = df2.copy()
# create a new dataframe to display the results
results = pd.DataFrame(columns=['Step', 'Theoretical duration'])
df2_duration.reset_index(drop=True,inplace=True)
df_gantt.reset_index(drop=True,inplace=True)

for col_idx, col in enumerate(df2_duration.iloc[:,:].columns):
    # get the corresponding row from df_gantt
    row = df_gantt.iloc[col_idx]
    # remove the value of start_num to the column
    actual_duration = round(df2_duration[col].mean(), 1)
    theoretical_duration = row['end_num']
    # add the result to the new dataframe
    new_row = {'Step': col, 'Theoretical duration': theoretical_duration, 'Actual average duration': actual_duration}
    results = pd.concat([results, pd.DataFrame([new_row])], ignore_index=True)

results.set_index(results.columns[0], inplace=True)
results['Actual average duration'] = results['Actual average duration']
# display the results in a table
col2.dataframe(results)


st.subheader('Analyzing categories')

st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        "We now have a good understanding of the timeliness of our steps, but to further enhance our analysis"
        " it can be interesting to look at the timeliness of categorical variables available (e.g. teams, products)."
        "<br> In this scenario, utilizing boxplots enables us to effectively compare and visualize each category."
            , unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap='small')

col1.info("Generate a number of categorical values to analyze:")
# Add a Streamlit slider for number of categorical values
num_cat = 3
categorical_num = col2.slider('', min_value=1, max_value=5, value=num_cat, label_visibility="collapsed")

# generate a list of random category values with length equal to dataframe
cat_vals = ["Category " + str(np.random.randint(0, categorical_num)+1) for _ in range(len(df2_duration))]

# create a new Series for the categories
cat_series = pd.Series(cat_vals, name='Category')

# concatenate the categories Series with the original DataFrame
df2_duration = pd.concat([df2_duration, cat_series], axis=1)
df2 = pd.concat([df2, cat_series], axis=1)

# Create figure and axis objects
sns.set(rc={'axes.facecolor': '#0000FF', 'figure.facecolor': (0, 0, 0, 0)})
fig, ax1 = plt.subplots(figsize=(16, 8))

# Plot the first graph on the first axis
ax1.barh(df_gantt.Milestone, df_gantt.days_start_to_end, left=df_gantt.start_num, color="#04AA6D", edgecolor="Black",
         zorder=0)
for i in df_gantt.end_num.unique():
    ax1.axvline(x=i, color='grey', ls=':', lw=1.5, zorder=1)
ax1.invert_yaxis()
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax1.axvline(x=0, color='white', ls=':', lw=1)

colors = plt.cm.tab10(np.linspace(0, 1, len(df2['Category'].unique())))
boxplot_kwargs = dict(vert=False, notch=False, sym="o", widths=0.2, patch_artist=True,
                      boxprops=dict(facecolor='white', edgecolor='white', linewidth=1.5),
                      whiskerprops=dict(color='white', linewidth=1.5), medianprops=dict(color='white', linewidth=1.5),
                      capprops=dict(color='white', linewidth=1.5))

for n, colname in enumerate(df2.iloc[:, :-1].columns, 1):
    pos = n-(df2['Category'].nunique()/10-1/10)
    for i, category in enumerate(df2["Category"].unique()):
        # Get the data for the current category and column
        serie = df2[df2["Category"] == category][colname]
        # Add the boxplot at the current position
        bp = ax1.boxplot(x=[serie], positions=[pos],
                         flierprops=dict(marker='o', markersize=5, markerfacecolor=colors[i], markeredgecolor='white',linewidth=0.2),
                         **boxplot_kwargs)
        for patch in bp['boxes']:
            patch.set_facecolor(colors[i])

        # Increment the position for the next boxplot
        pos += 0.2

ax1.axis("off")
st.pyplot(fig)

st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        "We can now get the average timeliness for each category on each step and compare our values:", unsafe_allow_html=True)

df2_duration = df2.copy()
results = pd.DataFrame(columns=['Step', 'Category', 'Theoretical duration'])

for i in df2_duration.iloc[:, -1].unique():
    df2_duration_cate = df2_duration[df2_duration["Category"]==i]
    for col_idx, col in enumerate(df2_duration_cate.iloc[:, :-1].columns):
        # get the corresponding row from df_gantt
        row = df_gantt.iloc[col_idx]
        # remove the value of start_num to the column
        actual_duration = round(df2_duration_cate[col].mean(), 1)
        # add the result to the new dataframe
        new_row = {'Step': col, 'Category': i, 'Actual duration': actual_duration}
        results = pd.concat([results, pd.DataFrame([new_row])], ignore_index=True)

df_gantt = df_gantt.rename(columns={'Milestone': 'Step'})
df_gantt['Step'] = df_gantt['Step'].apply(lambda x: 'Step ' + str(x))
pivot_table = results.pivot_table(index='Step', columns='Category', values='Actual duration').reset_index()
# merge with the 'days_start_to_end' column
pivot_table = pivot_table.merge(df_gantt[['Step', 'end_num']], on='Step')
# rename the 'days_start_to_end' column to 'Theoretical duration'
pivot_table = pivot_table.rename(columns={'end_num': 'Theoretical duration'})
# move the 'Theoretical duration' column to the first position
theo_dur = pivot_table.pop('Theoretical duration')
pivot_table.insert(1, 'Theoretical duration', theo_dur)

# display the results in a table
st.dataframe(pivot_table)

st.subheader('To go further...')

st.markdown("<p style='text-align: justify; font-size: 18px;'>"
        "To summarize, we have worked with a dataset that contains process timeliness, cleaned it, "
            "and created visualizations to compare actual duration with theoretical target duration. "
            "We also examined results by categorical values. "
            "<br><br> <b><i> What next?</b></i> Moving forward, we could explore sub-category"
            " results or use machine learning clustering algorithms such as K-Means or DBSCAN to identify best or worst performers. "
            "This could provide insights into why certain groups are consistently late or performing better "
            "in our process, and allow us to implement best practices to improve the overall timeliness."
            , unsafe_allow_html=True)
