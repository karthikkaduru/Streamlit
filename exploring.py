import streamlit as st
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

# Sample JSON data for nodes
nodes_json = '''
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

# Define links as a simple string
links_string = "1>>2>>3"

# Parse JSON data
nodes_data = json.loads(nodes_json)

# Sample data to simulate a database
data = {
    'location': ['Location-1', 'Location-1', 'Location-2', 'Location-3', 'Location-3', 'Location-3'],
    'store_name': ['Store A', 'Store B', 'Store C', 'Store D', 'Store E', 'Store F'],
    'sales': np.random.randint(100, 500, size=6)  # Random sales data
}
stores_df = pd.DataFrame(data)

# Function to get the count of stores based on the SQL query
def get_store_count(sql_query):
    location = sql_query.split("'")[1]  # Extract location from query
    return stores_df[stores_df['location'] == location].shape[0]

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
st.title("Node Visualization Flowchart")

# Create a container for node details
details_box = st.empty()  # Placeholder for details

# Create buttons for nodes
selected_node_id = None

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Location-1"):
        selected_node_id = "1"
with col2:
    if st.button("Location-2"):
        selected_node_id = "2"
with col3:
    if st.button("Location-3"):
        selected_node_id = "3"

# Show details for the selected node
if selected_node_id:
    node_data = next(node for node in nodes_data if node['id'] == selected_node_id)
    attributes = node_data['attributes']
    store_count = get_store_count(attributes['sql_query'])
    incident_number_link = f"[{attributes['incident_number']}](https://www.google.com)"

    # Display node details
    details_box.markdown("### Node Details")
    details_box.markdown(f"**Node Name:** {node_data['node_name']}")
    details_box.markdown(f"**Node ID:** {node_data['id']}")
    details_box.markdown(f"**Incident Number:** {incident_number_link}")
    details_box.markdown(f"**Stores Count:** {store_count}")

    # Display the sales plot for the clicked node
    create_sales_plot(node_data['node_name'])

# Draw connections between buttons using Markdown
st.markdown(
    """
    <style>
    .line {
        height: 2px;
        background-color: black;
        position: relative;
        top: -30px;
        z-index: -1;
        width: 70%; /* Adjust width as needed */
        margin: 0 auto;
    }
    </style>
    <div class="line"></div>
    """, unsafe_allow_html=True
)
