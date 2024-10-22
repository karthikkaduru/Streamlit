import streamlit as st
import numpy as np
import pandas as pd
import json
from pyvis.network import Network
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
st.title("Node Visualization Flowchart")

# Sidebar for team selection
st.sidebar.header("Select a Team")
team_option = st.sidebar.selectbox("Team", ["Team A", "Team B"])

# Load the appropriate team JSON data based on selection
nodes_data = json.loads(team_a_json) if team_option == "Team A" else json.loads(team_b_json)

# Create the network graph
net = Network(height='600px', width='100%', notebook=True, bgcolor='#001f3f', font_color='white')

# Add nodes with detailed labels inside square shapes
for node in nodes_data:
    store_count = get_store_count(node['attributes']['sql_query'])
    incident_number = node['attributes']['incident_number']
    
    # Construct the label
    label_info = f"{node['node_name']}\nStores Count: {store_count}\nIncident Number: {incident_number}"

    # Add node as square shape with detailed label
    net.add_node(node['id'], label=label_info, shape='box', color='skyblue', size=20)

# Add edges based on the team
if team_option == "Team A":
    links = ["1", "2", "3"]
elif team_option == "Team B":
    links = ["4", "5", "6", "7"]

for i in range(len(links) - 1):
    net.add_edge(links[i], links[i + 1])

# Set options for the layout and physics with increased spacing
options = '''
{
  "edges": {
    "smooth": {
      "enabled": false
    }
  },
  "layout": {
    "hierarchical": {
      "enabled": true,
      "direction": "LR",
      "levelSeparation": 150,
      "nodeSpacing": 200,  // Increased spacing between nodes
      "treeSpacing": 300    // Increased spacing between tree branches
    }
  },
  "physics": {
    "enabled": false
  }
}
'''

# Set the options for the network
net.set_options(options)

# Generate the network graph
net.show("network.html")

# Display the network graph
HtmlFile = open("network.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
st.components.v1.html(source_code, height=600)

# Function to display node details
def display_node_details(node_id):
    node_data = next((node for node in nodes_data if node['id'] == node_id), None)
    if node_data:
        create_sales_plot(node_data['node_name'])  # Automatically generate the sales plot
        return node_data
    return None

# Select box to choose a node
selected_node_id = st.selectbox("Select a node to view details", [node['id'] for node in nodes_data])

if selected_node_id:
    details = display_node_details(selected_node_id)
    if details:
        st.write(f"### Details for {details['node_name']}")
        st.write(f"**Stores Count:** {get_store_count(details['attributes']['sql_query'])}")
        st.write(f"**Incident Number:** {details['attributes']['incident_number']}")
