import streamlit as st
import numpy as np
import pandas as pd
import json
from pyvis.network import Network

# Sample JSON data for nodes (same as before)
nodes_json = '''
[
    {"id": "1", "node_name": "Location-1", "attributes": {"sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-1'", "incident_number": "INC1234"}},
    {"id": "2", "node_name": "Location-2", "attributes": {"sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-2'", "incident_number": "INC5678"}},
    {"id": "3", "node_name": "Location-3", "attributes": {"sql_query": "SELECT COUNT(*) FROM stores WHERE location = 'Location-3'", "incident_number": "INC9101"}}
]
'''

# Define links as a simple text string
links_string = "1 >> 2 >> 3"

# Parse nodes data
nodes_data = json.loads(nodes_json)

# Parse links from the string
links_data = []
nodes = links_string.split(" >> ")
for i in range(len(nodes) - 1):
    links_data.append({"source": nodes[i], "target": nodes[i + 1]})

# Sample data to simulate a database
data = {
    'location': ['Location-1', 'Location-1', 'Location-2', 'Location-3', 'Location-3', 'Location-3'],
    'store_name': ['Store A', 'Store B', 'Store C', 'Store D', 'Store E', 'Store F'],
    'sales': np.random.randint(100, 500, size=6)
}
stores_df = pd.DataFrame(data)

def get_store_count(sql_query):
    location = sql_query.split("'")[1]
    return stores_df[stores_df['location'] == location].shape[0]

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

# Store plot visibility state
if 'plot_visibility' not in st.session_state:
    st.session_state.plot_visibility = {node['id']: False for node in nodes_data}

# Display nodes with details and toggle button for plots
cols = st.columns(len(nodes_data))

for i, node in enumerate(nodes_data):
    node_id = node['id']
    node_name = node['node_name']
    attributes = node['attributes']
    store_count = get_store_count(attributes['sql_query'])

    with cols[i]:
        button_label = f"""
        {node_name}
        ---
        Node ID: {node_id}  
        Incident: [{attributes['incident_number']}] 
        Stores: {store_count}
        """
        
        if st.button(button_label, key=node_id):
            st.session_state.plot_visibility[node_id] = not st.session_state.plot_visibility[node_id]

        if st.session_state.plot_visibility[node_id]:
            create_sales_plot(node_name)

# Interactive Network Graph using Pyvis
if st.button("Show Interactive Network Graph"):
    net = Network(height='600px', width='100%', notebook=True)

    # Add nodes
    for node in nodes_data:
        net.add_node(node['id'], label=node['node_name'], title=f"Incident: {node['attributes']['incident_number']}")
    
    # Add edges from the parsed links
    for link in links_data:
        net.add_edge(link['source'], link['target'], label=f"{link['source']} >> {link['target']}", title=f"From {link['source']} to {link['target']}")
    
    # Show the network graph
    net.show("network.html")
    HtmlFile = open("network.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    st.components.v1.html(source_code, height=600)
