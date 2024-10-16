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

    'store_name': ['Store A', 'Store B', 'Store C', 'Store D', 'Store E', 'Store F']

}

stores_df = pd.DataFrame(data)
 
# Function to get the count of stores based on the SQL query

def get_store_count(sql_query):

    location = sql_query.split("'")[1]  # Extract location from query

    return stores_df[stores_df['location'] == location].shape[0]
 
# Function to create a random plot

def create_random_plot(node_name):

    x = np.linspace(0, 10, 100)

    y = np.random.rand(100) * 10  # Random data

    plt.figure()

    plt.plot(x, y, label=f"Random Data for {node_name}")

    plt.title(f"Random Plot for {node_name}")

    plt.xlabel("X-axis")

    plt.ylabel("Y-axis")

    plt.legend()

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
 
# Display nodes with details

for node in nodes_data:

    node_id = node['id']

    node_name = node['node_name']

    attributes = node['attributes']

    store_count = get_store_count(attributes['sql_query'])
 
    # Create a button for each node

    if st.button(node_name):

        st.write(f"**Node ID:** {node_id}")

        st.write(f"**Incident Number:** [{attributes['incident_number']}](https://www.example.com/{attributes['incident_number']})")

        st.write(f"**Number of Stores:** {store_count}")

        # Display the random plot

        create_random_plot(node_name)
 
# Draw the graph to show links

plt.figure(figsize=(10, 5))

pos = nx.spring_layout(G)  # positions for all nodes

nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)

plt.title("Flowchart of Nodes")

st.pyplot(plt)
 
