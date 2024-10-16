pip install matplotlib
import streamlit as st

import numpy as np

import matplotlib.pyplot as plt

import json
 
# Sample JSON data

json_data = '''

{

    "nodes": [

        {

            "id": "1",

            "node_name": "Location-1",

            "attributes": {"sql_query": "SELECT * FROM table1", "days": 7}

        },

        {

            "id": "2",

            "node_name": "Location-2",

            "attributes": {"sql_query": "SELECT * FROM table2", "days": 10}

        },

        {

            "id": "3",

            "node_name": "Location-3",

            "attributes": {"sql_query": "SELECT * FROM table3", "days": 15}

        }

    ]

}

'''
 
# Parse the JSON data

data = json.loads(json_data)
 
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

st.title("Node Visualization App")
 
# Display nodes with hover information

for node in data['nodes']:

    node_id = node['id']

    node_name = node['node_name']

    attributes = node['attributes']

    days = attributes['days']

    # Create a button for each node

    if st.button(node_name):

        st.write(f"**Node ID:** {node_id}")

        st.write(f"**SQL Query:** {attributes['sql_query']}")

        st.write(f"**Days:** {days}")

        create_random_plot(node_name)

 


