import streamlit as st
import numpy as np
import plotly.graph_objects as go
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

# Streamlit App
st.title("Interactive Node Visualization Flowchart")

# Create a list to store node positions
node_positions = {
    "1": (0, 0),
    "2": (1, 1),
    "3": (1, -1)
}

# Create Plotly graph
edge_x = []
edge_y = []
for link in links_data:
    x0, y0 = node_positions[link['source']]
    x1, y1 = node_positions[link['target']]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)  # Break line
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)  # Break line

# Create edges
edges_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'
)

# Create nodes
node_x = []
node_y = []
node_text = []
for node in nodes_data:
    node_id = node['id']
    node_name = node['node_name']
    incident_number = node['attributes']['incident_number']
    store_count = get_store_count(node['attributes']['sql_query'])
    
    node_x.append(node_positions[node_id][0])
    node_y.append(node_positions[node_id][1])
    node_text.append(f"{node_name}<br>Incident: {incident_number}<br>Stores: {store_count}")

nodes_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=20,
        color=[],
        line_width=2
    ),
    text=node_text,
    textposition="top center",
    hoverinfo='text'
)

# Create the figure
fig = go.Figure(data=[edges_trace, nodes_trace],
                layout=go.Layout(
                    title='Interactive Flowchart of Nodes',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0,l=0,r=0,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

# Display the figure
st.plotly_chart(fig)
