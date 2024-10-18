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

# Function to create a sales plot
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

# Load nodes from JSON
nodes_data = json.loads(nodes_json)

# Add nodes to the graph
for node in nodes_data:
    net.add_node(node['id'], label=node['node_name'], title=f"Incident: {node['attributes']['incident_number']}", color='lightblue')

# Define links between nodes
links = "1>>2>>3"  # You can modify this to represent your connections
for link in links.split(">>"):
    net.add_edge(link, str(int(link) % 3 + 1))  # Simple link logic to form a cycle

# Save and display the network graph
net.show("network.html")
HtmlFile = open("network.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
st.components.v1.html(source_code, height=600)

# Create a container for node details
details_box = st.empty()

# JavaScript to handle node clicks
st.markdown("""
<script>
    const network = document.getElementById("mynetwork");
    network.on("click", function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            window.parent.postMessage({node_id: nodeId}, '*');
        }
    });
</script>
""", unsafe_allow_html=True)

# Handling node click updates
if "node_id" not in st.session_state:
    st.session_state.node_id = None

def update_node_details():
    if st.session_state.node_id:
        node_data = next((node for node in nodes_data if node['id'] == st.session_state.node_id), None)
        if node_data:
            node_name = node_data['node_name']
            attributes = node_data['attributes']
            store_count = get_store_count(attributes['sql_query'])
            incident_number_link = f"[{attributes['incident_number']}](https://www.google.com)"

            # Display node details
            details_box.markdown(f"### Node Details")
            details_box.markdown(f"**Node Name:** {node_name}")
            details_box.markdown(f"**Node ID:** {st.session_state.node_id}")
            details_box.markdown(f"**Incident Number:** {incident_number_link}")
            details_box.markdown(f"**Stores Count:** {store_count}")

            # Display the sales plot for the clicked node
            create_sales_plot(node_name)

# Check if a node has been clicked
def handle_node_click():
    if st.session_state.node_id is not None:
        update_node_details()
        
# Call to handle clicks
handle_node_click()
