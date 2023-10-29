import streamlit as st
from streamlit_lottie import st_lottie
import json
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
from kneed import KneeLocator

st.set_page_config(layout="centered", page_icon="🔠")
# Use local CSS for background waves
with open('./style/wave.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Set initial title
title = st.title("Clustering, what's that about?")

col1, col2 = st.columns([1, 3], gap='small')

# Web app path
path = "Images/Clustering.json"
# Local path
#path = r"C:\Users\adrie\Documents\GitHub\streamlit_app\Images\Clustering.json"
with open(path, "r") as file:
    url = json.load(file)
with col1:
    st_lottie(url,
              reverse=True,
              height=200,
              speed=0.4,
              loop=True,
              quality='high',
              key='Car'
              )

col2.markdown("<p style='text-align: justify; font-size: 18px;'>"
             "Clustering is an unsupervised machine learning algorithm that is used to group similar data points "
            "together based on their features or characteristics. <br>Unlike supervised learning algorithms, clustering "
            "does not rely on predefined labels or outcomes, making it useful in cases where the structure of the "
            "data is not well-defined or when we want to discover patterns in the data without any prior knowledge. "
            , unsafe_allow_html=True)
st.markdown("<p style='text-align: justify; font-size: 18px;'>"
            "Clustering is also relatively easy to implement and can be applied to a wide range of problems, "
            "from image segmentation to customer segmentation in marketing. <br><br>"
            "There are various types of clustering algorithms, such as k-means, hierarchical clustering, DBSCAN, "
            "and more. Each algorithm has its strengths and weaknesses, and is suitable for different types of data and "
          "applications.", unsafe_allow_html=True)

st.subheader(':blue[Starting with clustering: Data preprocessing]')
st.markdown("<p style='text-align: justify; font-size: 18px;'>"
             "Clustering is a powerful technique for finding patterns in data, but it can also be very sensitive to the"
            " way the data is prepared. Here are some important data preprocessing steps you should consider before "
            "applying clustering algorithms:", unsafe_allow_html=True)

st.subheader('1. :green[Encoding categorical data]')
st.markdown("<p style='text-align: justify; font-size: 18px;'>"
             "Many real-world datasets include categorical features, such as gender, location, or product type. "
            "However, most clustering algorithms are designed to work with numerical data, so we need to convert "
            "categorical data into numerical values.<br> One common technique for encoding categorical data is one-hot "
            "encoding, which creates a binary column for each category in the feature. For example, a 'gender' feature "
            "with categories 'male' and 'female' would be transformed into two binary columns, one for each category.",
                                               unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Create a sample dataframe
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob', 'Sarah'],
    'gender': ['male', 'female', 'male', 'female']})

# Encode the 'gender' column using LabelEncoder
encoder = LabelEncoder()
df['gender_encoded'] = encoder.fit_transform(df['gender'])

# Display the original and encoded dataframes in Streamlit
col1, col2 = st.columns([1, 1], gap='small')
col1.write('Original Dataframe')
col1.table(df[['name', 'gender']])
col2.write('Encoded Dataframe')
col2.table(df[['name', 'gender_encoded']])

with st.expander('Encoding data with Python'):
    st.code('''
    import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Create a sample dataframe
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob', 'Sarah'],
    'gender': ['male', 'female', 'male', 'female']})

# Encode the 'gender' column using LabelEncoder
encoder = LabelEncoder()
df['gender_encoded'] = encoder.fit_transform(df['gender'])

# Display the original and encoded dataframes in Streamlit
st.write('Original Dataframe', df[['name', 'gender']])
st.write('Encoded Dataframe', df[['name', 'gender_encoded']])
''')

st.subheader('2. :green[Scaling data]')
st.markdown("<p style='text-align: justify; font-size: 18px;'>"
             "Another important preprocessing step for clustering is scaling the data. Clustering algorithms are "
            "often sensitive to the scale of the features, so it's important to ensure that all features have the "
            "same scale. This can be done using techniques such as standardization or normalization. Standardization "
            "scales the data to have zero mean and unit variance, while normalization scales the data to a fixed range,"
            " typically [0, 1] or [-1, 1].", unsafe_allow_html=True)

from sklearn.preprocessing import MinMaxScaler

# Create a sample dataframe
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob', 'Sarah'],
    'age': [20, 30, 25, 40],
    'income': [50000, 80000, 60000, 100000]
})
# Display the original and encoded dataframes in Streamlit
col1, col2 = st.columns([1, 1], gap='small')

col1.write('Original Dataframe')
col1.table(df)

# Scale the 'age' and 'income' columns using MinMaxScaler
scaler = MinMaxScaler()
df[['age', 'income']] = scaler.fit_transform(df[['age', 'income']])

# Display the scaled dataframe in Streamlit
col2.write('Scaled Dataframe')
col2.table(df)

with st.expander('Scaling data with Python'):
    st.code('''
    import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Create a sample dataframe
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob', 'Sarah'],
    'age': [20, 30, 25, 40],
    'income': [50000, 80000, 60000, 100000]})

# Scale the 'age' and 'income' columns using MinMaxScaler
scaler = MinMaxScaler()
df[['age', 'income']] = scaler.fit_transform(df[['age', 'income']])

# Display the scaled dataframe in Streamlit
st.write('Scaled Dataframe')
st.table(df)
''')

st.subheader('3. :green[Applying dimensionality reduction]')
st.markdown("<p style='text-align: justify; font-size: 18px;'>"
             "Clustering can also be challenging when working with high-dimensional data, where the number of features "
            "is very large. In these cases, it may be helpful to perform dimensionality reduction to reduce the number "
            "of features while preserving the most important information. Principal Component Analysis (PCA) and "
            "t-Distributed Stochastic Neighbor Embedding (t-SNE) are common techniques for dimensionality "
            "reduction.", unsafe_allow_html=True)
st.caption('Example of Principal Component Analysis ')

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load sample customer data
data = pd.DataFrame({
    'age': [28, 35, 45, 22, 38],
    'income': [45000, 60000, 80000, 30000, 70000],
    'savings': [10000, 20000, 50000, 5000, 30000],
    'debt': [5000, 10000, 20000, 2000, 15000]})

# Scale the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Apply PCA to reduce the number of dimensions
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_scaled)

# Display the original and reduced-dimension data in Streamlit
col1, col2 = st.columns([1, 1], gap='small')
col1.write('Original Data ({} dimensions)'.format(len(data.columns)))
col1.dataframe(data)

col2.write('Reduced-dimension Data (2 PCs)')
data_pca_df = pd.DataFrame(data_pca, columns=['PC1', 'PC2'])
col2.dataframe(data_pca_df)

with st.expander('Applying Principal Component Analysis'):
    st.code('''
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load sample customer data
data = pd.DataFrame({
    'age': [28, 35, 45, 22, 38],
    'income': [45000, 60000, 80000, 30000, 70000],
    'savings': [10000, 20000, 50000, 5000, 30000],
    'debt': [5000, 10000, 20000, 2000, 15000]})

# Scale the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Apply PCA to reduce the number of dimensions
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_scaled)

# Display the original and reduced-dimension data in Streamlit
col1, col2 = st.columns([1, 1], gap='small')
col1.write('Original Data ({} dimensions)'.format(len(data.columns)))
col1.dataframe(data)

col2.write('Reduced-dimension Data (2 PCs)')
data_pca_df = pd.DataFrame(data_pca, columns=['PC1', 'PC2'])
col2.dataframe(data_pca_df)''')

st.subheader('3. :green[Choosing the right algorithm]')
st.markdown("<p style='text-align: justify; font-size: 18px;'>"
             "Finally, it's important to choose the right clustering algorithm for your specific problem and data."
            " There are many different clustering algorithms available, each with its own strengths and weaknesses. "
            "Some common clustering algorithms include k-means, DBSCAN and others.", unsafe_allow_html=True)

from sklearn.datasets import make_blobs
import plotly.express as px

# Generate sample dataset
X, y = make_blobs(n_samples=500, centers=4, n_features=4, random_state=42)


from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

col1, col2 = st.columns([1, 1], gap='small')

model = KMeans(n_clusters=4)
y_pred = model.fit_predict(X)
y_pred_str = [str(val) for val in y_pred.tolist()]
# Display the results in a scatter plot
fig = px.scatter(x=X[:, 0], y=X[:, 1], color=y_pred_str, opacity=0.8,color_continuous_scale=px.colors.diverging.BrBG,
                 labels={"color": "Clusters"},
                 title="K-means algorithm",
                 template="plotly_white")
fig.update_traces(marker=dict(size=15,line=dict(width=1, color='black')))

fig.update_layout(
    width=400,  # set the plot height to 500 pixels
    font=dict(size=15),
    title_font=dict(size=24),
    legend_font=dict(size=16),
    xaxis_title_font=dict(size=20),
    yaxis_title_font=dict(size=20),
    xaxis_tickfont=dict(size=16),
    yaxis_tickfont=dict(size=16))
col1.plotly_chart(fig, config={'displayModeBar': False})

model = DBSCAN(eps=1.5, min_samples=5)
y_pred = model.fit_predict(X)
y_pred_str = [str(val) for val in y_pred.tolist()]
fig = px.scatter(x=X[:, 0], y=X[:, 1], color=y_pred_str, opacity=0.8,color_continuous_scale=px.colors.diverging.BrBG,
                 labels={"color": "Clusters"},
                 title="DBSCAN algorithm",
                 template="plotly_white")
fig.update_traces(marker=dict(size=15,line=dict(width=1, color='black')))

fig.update_layout(
    width=400,  # set the plot height to 500 pixels
    font=dict(size=15),
    title_font=dict(size=24),
    legend_font=dict(size=16),
    xaxis_title_font=dict(size=20),
    yaxis_title_font=dict(size=20),
    xaxis_tickfont=dict(size=16),
    yaxis_tickfont=dict(size=16))
col2.plotly_chart(fig, config={'displayModeBar': False})

st.subheader(":blue[Try it yourself with the clustering tool:] ")

st.markdown(
    "<h6>Use a sample dataset or import your own <a href='https://adrien.streamlit.app/Clustering_tool' target='_blank' style='font-size: 20x;'>here</a></h6>",
    unsafe_allow_html=True
)



