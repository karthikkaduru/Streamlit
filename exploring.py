import streamlit as st
import numpy as np
import pandas as pd
import json
from pyvis.network import Network
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
st.title("Node Visualization Flowchart")

# Create the network graph
net = Network(height='600px', width='100%', notebook=True)

# Add nodes
for node in nodes_data:
    net.add_node(node['id'], label=node['node_name'], title=f"Incident: {node['attributes']['incident_number']}", color='lightblue')

# Add edges based on the simple links string
links = links_string.split('>>')
for i in range(len(links) - 1):
    net.add_edge(links[i], links[i + 1])  # Create a directed edge from one node to the next

# Save and display the network graph
net.show("network.html")
HtmlFile = open("network.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
st.components.v1.html(source_code, height=600)

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

        # Incident number as a hyperlink
        incident_number_link = f"[{attributes['incident_number']}](https://www.google.com)"

        # Display each detail separately to ensure all are shown
        details_box.markdown("### Node Details")
        details_box_1.markdown(f"**Node Name:** {node_name}")
        details_box.markdown(f"**Node ID:** {node_id}")
        details_box_2.markdown(f"**Stores Count:** {store_count}")  # Should display the store count
        details_box.markdown(f"**Incident Number:** {incident_number_link}")  # Incident number as hyperlink

        # Display the sales plot for the clicked node
        create_sales_plot(node_name)
    else:
        details_box.markdown("Node not found.")

# **New Search Functionality**
search_query = st.text_input("Search for Node ID:", "")  # **Added this line**
filtered_node_ids = [node['id'] for node in nodes_data if search_query in node['id']]  # **Added this line**

# Select box to choose a node
if filtered_node_ids:
    selected_node_id = st.selectbox("Select a node to view details", filtered_node_ids)  # **Updated this line**
else:
    selected_node_id = st.selectbox("Select a node to view details", [node['id'] for node in nodes_data])  # **Updated this line**

if selected_node_id:
    display_node_details(selected_node_id)
