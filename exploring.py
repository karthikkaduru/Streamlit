import streamlit as st
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import networkx as nx

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

# Create a directed graph using NetworkX
G = nx.DiGraph()

# Add nodes and edges to the graph
edges = [("1", "2"), ("2", "3"), ("3", "1")]  # Define connections between nodes
for node in nodes_data:
    G.add_node(node['id'], name=node['node_name'], incident_number=node['attributes']['incident_number'])

for edge in edges:
    G.add_edge(*edge)

# Store node details in session state
if "node_details" not in st.session_state:
    st.session_state.node_details = None

# Display buttons for each node
for node in nodes_data:
    node_id = node['id']
    node_name = node['node_name']
    
    if st.button(node_name):
        # Update node details in session state
        attributes = node['attributes']
        store_count = get_store_count(attributes['sql_query'])
        incident_number_link = f"[{attributes['incident_number']}](https://www.google.com)"

        # Store details in session state
        st.session_state.node_details = {
            "name": node_name,
            "id": node_id,
            "incident_number": incident_number_link,
            "stores_count": store_count
        }

# Show node details if any node has been clicked
if st.session_state.node_details:
    details = st.session_state.node_details
    st.markdown(f"### Node Details")
    st.markdown(f"**Node Name:** {details['name']}")
    st.markdown(f"**Node ID:** {details['id']}")
    st.markdown(f"**Incident Number:** {details['incident_number']}")
    st.markdown(f"**Stores Count:** {details['stores_count']}")

    # Display the sales plot for the clicked node
    create_sales_plot(details['name'])

# Draw the network graph
plt.figure(figsize=(8, 5))
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
plt.title("Flowchart of Nodes")
st.pyplot(plt)
