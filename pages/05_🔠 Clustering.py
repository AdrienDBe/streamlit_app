import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
from kneed import KneeLocator




st.set_page_config(layout="centered", page_icon="🔠")

# create a Streamlit app
st.title("Clustering tool")

# Define function to load data
def load_data(file):
    data = pd.read_csv(file)
    # Create a boolean mask that is True for rows with at least one NaN value
    has_empty_mask = data.isna().any(axis=1)
    # Select only the rows that have at least one NaN value
    data_HasEmpty = data[has_empty_mask]
    lenght_data_HasEmpty = len(data_HasEmpty)
    data.dropna(inplace=True)
    data.reset_index(drop=True,inplace=True)
    categorical_cols = list(data.select_dtypes(include=['object','category']))
    return data, categorical_cols, data_HasEmpty,lenght_data_HasEmpty

def has_categorical_data(data):
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    return len(categorical_cols) > 0

def has_morethan1_categorical_data(data):
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    return len(categorical_cols) > 1

# Define function to run clustering algorithm
def run_clustering(data, num_clusters):
    # Scale the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    # Run clustering algorithm
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(scaled_data)
    clusters = kmeans.predict(scaled_data)
    return clusters

# Load data
col1, col2 = st.columns([2, 1], gap='small')
data_file = col1.file_uploader('Upload your dataset', type=['csv', 'xlsx'],label_visibility="collapsed")
if data_file is None:
    info = col2.info('Upload your data to start clustering')
if data_file is not None:
    data, categorical_cols, data_HasEmpty,lenght_data_HasEmpty = load_data(data_file)
    # Show data summary
    if len(data_HasEmpty) >0:
        col2.warning('{} missing values have been removed from your dataset, {} remaining rows'.format(len(data_HasEmpty),len(data)))

    tab1, tab2 = st.tabs(["Cleaned dataset", "Data type summary"])
    with tab1:
        st.dataframe(data,height= 300)
    with tab2:
        # Show column names and types
        st.dataframe(data.dtypes)

    col1, col2 = st.columns([1, 1], gap='small')
    # Allow user to choose which columns to include in clustering analysis
    col1.caption("Select columns for clustering analysis")
    all_columns = list(data.columns)
    selected_columns = col1.multiselect('', options=all_columns,label_visibility="collapsed")

    # Create second dataset with selected columns only
    selected_data = data[selected_columns]

    # Check if any categorical columns are in selected_columns
    categorical_cols_selected = [col for col in categorical_cols if col in selected_columns]

    # If there are any categorical columns in selected_columns, Use OneHotEncoder to one-hot encode them
    if len(categorical_cols_selected) > 0:
        ohe = OneHotEncoder(categories=[data[col].unique() for col in categorical_cols_selected], sparse=False)
        encoded_cols = ohe.fit_transform(data[categorical_cols_selected])
        encoded_df = pd.DataFrame(encoded_cols, columns=ohe.get_feature_names(categorical_cols_selected))
        data_clean = pd.concat([data[selected_columns], encoded_df], axis=1)
        # Remove the original encoded categorical columns from data_clean
        for col in categorical_cols_selected:
            data_clean.drop(col, axis=1, inplace=True)

    else:
        # If there are no categorical columns in selected_columns, just use the selected columns
        data_clean = data[selected_columns].copy()

    if len(selected_columns) == 0:
        col2.info('Select at least one column for clustering analysis.')
    if len(selected_columns) != 0 and len(categorical_cols_selected) == selected_data.shape[1]:
        col2.info('Select at least one numerical value')

    col2.caption("Optimal cluster number: Elbow Method")

    tab1, tab2 = st.tabs(["Visualize clusters", "Display dataframe / download results"])

    if len(selected_columns) != 0 and len(categorical_cols_selected) != selected_data.shape[1]:

        # Run clustering algorithm
        num_clusters = col1.slider('Number of clusters', value = 3, min_value=2, max_value=10)
        clusters = run_clustering(data_clean, num_clusters)
        # Add an elbow plot
        sse = []
        for k in range(1, 11):
            kmeans_elbow = KMeans(n_clusters=k)
            kmeans_elbow.fit(data_clean)
            sse.append(kmeans_elbow.inertia_)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(1, 11)), y=sse, mode='lines'))
        fig.update_layout(
            title=None,
            margin=dict(t=0),
            xaxis_title="Number of Clusters",
            yaxis_title="Sum of Squared Distances",
            height=300,
            showlegend=False
        )

        # Find the optimal number of clusters
        kl = KneeLocator(list(range(1, 11)), sse, curve="convex", direction="decreasing")
        optimal_k = kl.elbow

        # Add a circle around the optimal number of clusters
        fig.add_trace(go.Scatter(x=[optimal_k], y=[sse[optimal_k - 1]],
                                 mode="markers", marker=dict(color="#04AA6D", symbol="circle", size=15),
                                 showlegend=False))

        with col2.container():
            st.plotly_chart(fig, use_container_width=True,config = {'staticPlot': True})

        with tab1:
            # Add cluster column to data
            selected_data['Cluster'] = clusters
            # Add a name and convert Cluster column to string type
            selected_data['Cluster'] = selected_data['Cluster'].apply(lambda x: 'Cluster ' + str(x))

            # Check number of columns in data_clean
            num_cols = len(data_clean.columns)
            # Check if there is categorical values
            has_categorical = has_categorical_data(selected_data.iloc[:, :-1])
            has_morethan1_categorical = has_morethan1_categorical_data(selected_data.iloc[:, :-1])

            # If only 1 column, use strip plot with hue as clusters
            if num_cols == 1 and len(categorical_cols_selected) ==0 :
                fig = px.strip(selected_data, x=selected_data.columns[0], color=selected_data.columns[1], stripmode = "overlay")
                st.plotly_chart(fig)

            # If 2 columns without categorical values, use scatter plot with color as clusters
            elif num_cols == 2 and len(categorical_cols_selected) ==0 :
                fig = px.scatter(data_clean, x=selected_data.columns[0], y=selected_data.columns[1], color=selected_data["Cluster"])
                st.plotly_chart(fig)

            # If 3 columns without categorical values, use 3D scatter plot with color as clusters
            elif num_cols == 3 and len(categorical_cols_selected) ==0 :
                fig = px.scatter_3d(data_clean, x=selected_data.columns[0], y=selected_data.columns[1], z=selected_data.columns[2],
                                    color=selected_data["Cluster"])

                camera = dict(
                    eye=dict(x=1.5, y=1.7, z=0.8),
                    center=dict(x=0, y=0, z=-0.3)
                )

                fig.update_layout(
                    title=None,
                    margin=dict(t=0, b=10), # set the bottom margin to 100
                    height=600,  # set the plot height to 500 pixels
                    scene_camera = camera
                )

                st.plotly_chart(fig)

            # If 1 columns including boolean categorical variable
            elif selected_data.shape[1] == 1 and len(categorical_cols_selected) == 1 :
                st.error('Select at least one numerical value')

            # If 1 columns including boolean categorical variable
            elif num_cols == 1 and len(categorical_cols_selected) == 1 :
                fig = px.scatter(selected_data, x=selected_data.columns[0], y=selected_data.columns[1],
                                    color=selected_data["Cluster"])
                st.plotly_chart(fig)

            # If more than 3 columns, use PCA to reduce dimensions to 2 and plot scatter plot with color as clusters
            else:
                # Fit PCA model to data_clean
                pca = PCA(n_components=2)
                data_pca = pca.fit_transform(data_clean)

                # Create dataframe with PCA results
                pca_df = pd.DataFrame(data_pca, columns=['PC1', 'PC2'])

                # Run clustering algorithm
                if len(selected_columns) > 0:
                    clusters = run_clustering(data_pca, num_clusters)

                    # Add cluster column to pca_df
                    pca_df['Cluster'] = clusters
                    pca_df['Cluster'] = pca_df['Cluster'].apply(lambda x: 'Cluster ' + str(x))

                    # Plot scatter plot with color as clusters
                    fig = px.scatter(pca_df, x='PC1', y='PC2', color='Cluster')
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
                    st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Show clustering results
        st.write('Clustering results:')
        st.dataframe(selected_data)

        # Allow user to download clustering results
        #st.download_button('Download clustering results', data=pd.DataFrame({'Cluster': selected_data}).to_csv(index=False), file_name='clustering_results.csv')

else:
    st.write('Please upload a CSV or Excel file.')



