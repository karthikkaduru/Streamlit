import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import json
import pandas as pd

# Sample JSON data for nodes and links
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

links_json = '''
[
    {"source": "1", "target": "2"},
    {"source": "2", "target": "3"},
    {"source": "3", "target": "1"}
]
'''

# Parse JSON data
nodes_data = json.loads(nodes_json)
links_data = json.loads(links_json)

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

# Create a network graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for node in nodes_data:
    node_id = node['id']
    G.add_node(node_id, name=node['node_name'], incident_number=node['attributes']['incident_number'])

for link in links_data:
    G.add_edge(link['source'], link['target'])

# Store plot visibility state
if 'plot_visibility' not in st.session_state:
    st.session_state.plot_visibility = {node['id']: False for node in nodes_data}

# Display nodes with details and toggle button for plots
cols = st.columns(len(nodes_data))  # Create columns based on number of nodes

for i, node in enumerate(nodes_data):
    node_id = node['id']
    node_name = node['node_name']
    attributes = node['attributes']
    store_count = get_store_count(attributes['sql_query'])

    with cols[i]:  # Place button in the respective column
        button_label = f"""
        {node_name}
        ---
        Node ID: {node_id}  
        Incident: [{attributes['incident_number']}] 
        Stores: {store_count}
        """
        
        if st.button(button_label, key=node_id):
            # Toggle visibility
            st.session_state.plot_visibility[node_id] = not st.session_state.plot_visibility[node_id]

        # Show plot if visibility is true
        if st.session_state.plot_visibility[node_id]:
            create_sales_plot(node_name)

# Button to display the network graph
if st.button("Show Network Graph"):
    plt.figure(figsize=(10, 5))
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
    plt.title("Flowchart of Nodes")
    st.pyplot(plt)

