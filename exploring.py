import streamlit as st
import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Sample JSON data for Team A
team_a_json = '''
[
    {
        "id": "1",
        "node_name": "Location-1",
        "attributes": {
            "sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-1'",
            "incident_number": "INC1234"
        }
    },
    {
        "id": "2",
        "node_name": "Location-2",
        "attributes": {
            "sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-2'",
            "incident_number": "INC5678"
        }
    },
    {
        "id": "3",
        "node_name": "Location-3",
        "attributes": {
            "sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-3'",
            "incident_number": "INC9101"
        }
    }
]
'''

# Sample JSON data for Team B
team_b_json = '''
[
    {
        "id": "4",
        "node_name": "Location-4",
        "attributes": {
            "sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-4'",
            "incident_number": "INC1122"
        }
    },
    {
        "id": "5",
        "node_name": "Location-5",
        "attributes": {
            "sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-5'",
            "incident_number": "INC3344"
        }
    },
    {
        "id": "6",
        "node_name": "Location-6",
        "attributes": {
            "sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-6'",
            "incident_number": "INC5566"
        }
    },
    {
        "id": "7",
        "node_name": "Location-7",
        "attributes": {
            "sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-7'",
            "incident_number": "INC7788"
        }
    }
]
'''

# Sample data to simulate a database
data = {
    'location': ['Location-1', 'Location-1', 'Location-2', 'Location-3', 'Location-3', 'Location-3', 
                 'Location-4', 'Location-5', 'Location-6', 'Location-7'],
    'store_name': ['Store A', 'Store B', 'Store C', 'Store D', 'Store E', 'Store F', 
                   'Store G', 'Store H', 'Store I', 'Store J'],
    'sales': np.random.randint(100, 500, size=10)  # Random sales data
}
stores_df = pd.DataFrame(data)

# Function to get the count of stores based on the SQL query
def get_store_count(sql_query):
    try:
        location = sql_query.split("'")[1]  # Extract location from query
        return stores_df[stores_df['location'] == location].shape[0]
    except IndexError:
        return 0  # Return 0 if query is malformed or location not found

# Function to create a fixed plot for sales
def create_sales_plot(node_name):
    location_sales = stores_df[stores_df['location'] == node_name]
    plt.figure()
    plt.bar(location_sales['store_name'], location_sales['sales'], color='skyblue')
    plt.title(f"Sales Data for {node_name}")
    plt.xlabel("Store Name")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Streamlit App
st.title("3D Node Visualization Flowchart")

# Team selection
team_option = st.selectbox("Select a Team", ["Team A", "Team B"])

# Load the appropriate team JSON data based on selection
if team_option == "Team A":
    nodes_data = json.loads(team_a_json)
elif team_option == "Team B":
    nodes_data = json.loads(team_b_json)

# Create 3D scatter plot
fig = go.Figure()

# Add nodes to the scatter plot
for node in nodes_data:
    store_count = get_store_count(node['attributes']['sql_query'])
    fig.add_trace(go.Scatter3d(
        x=[np.random.uniform(-10, 10)],  # Random x-coordinates
        y=[np.random.uniform(-10, 10)],  # Random y-coordinates
        z=[np.random.uniform(-10, 10)],  # Random z-coordinates
        mode='markers+text',
        marker=dict(size=10, color='skyblue'),
        text=['DQ'],
        textposition="top center",
        hoverinfo='text',
        name=f"Node: {node['node_name']}, Count: {store_count}, Incident: {node['attributes']['incident_number']}"
    ))

# Set the layout
fig.update_layout(
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis',
        bgcolor='#001f3f'  # Dark sky background
    ),
    title="3D DQ Visualization",
    margin=dict(l=0, r=0, b=0, t=40)
)

# Display the plot
st.plotly_chart(fig)

# Create containers for node details
details_box = st.empty()
details_box_1 = st.empty()
details_box_2 = st.empty()  # Placeholder for details

# Function to display node details
def display_node_details(node_id):
    node_data = next((node for node in nodes_data if node['id'] == node_id), None)

    if node_data:
        node_name = node_data['node_name']
        attributes = node_data['attributes']
        store_count = get_store_count(attributes['sql_query'])

        # Create the hyperlink for the incident number
        incident_number_link = f"[{attributes['incident_number']}](https://www.google.com)"

        # Display each detail separately to ensure all are shown
        details_box.markdown("### Node Details")
        details_box_1.markdown(f"**Node Name:** {node_name}")
        details_box.markdown(f"**Node ID:** {node_id}")
        details_box.markdown(f"**Stores Count:** {store_count}")  # Should display the store count
        details_box.markdown(f"**Incident Number:** {incident_number_link}")  # Incident number as hyperlink

        # Display the sales plot for the clicked node
        create_sales_plot(node_name)
    else:
        details_box.markdown("Node not found.")

# Select box to choose a node
node_ids = [node['id'] for node in nodes_data]
selected_node_id = st.selectbox("Select a node to view details", node_ids)

if selected_node_id:
    display_node_details(selected_node_id)
