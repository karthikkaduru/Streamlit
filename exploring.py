import io
import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from datetime import datetime
import networkx as nx

# Sample JSON data with incident hyperlinks
json_data = '''
{
    "nodes": [
        {
            "id": "1",
            "node_name": "Location-1",
            "attributes": {
                "sql_query": "SELECT DISTINCT Location_no FROM dbdatascience.sf_fact_daily_combined_actual_sales_plan",
                "days": 7,
                "incident_number": "INC1234"
            },
            "linked_nodes": ["2"]
        },
        {
            "id": "2",
            "node_name": "Location-2",
            "attributes": {
                "sql_query": "SELECT DISTINCT Location_no FROM dbdatascience.sf_fact_daily_combined_actual_sales_plan",
                "days": 10,
                "incident_number": "INC5678"
            },
            "linked_nodes": ["1", "3"]
        },
        {
            "id": "3",
            "node_name": "Location-3",
            "attributes": {
                "sql_query": "SELECT DISTINCT Location_no FROM dbdatascience.sf_fact_daily_combined_actual_sales_plan",
                "days": 15,
                "incident_number": "INC9101"
            },
            "linked_nodes": ["1","2"]
        }
    ],
    "links": [
        {"source": "1", "target": "2"},
        {"source": "2", "target": "3"}
    ]
}
'''

# Parse the JSON data
data = json.loads(json_data)

# Mock function to simulate data fetching based on SQL query
def fetch_data(sql_query):
    return pd.DataFrame({
        'Location_no': np.random.randint(1000, 2000, size=10)  # Random location numbers
    })

# Function to calculate total stores from SQL query
def calculate_total_stores(sql_query):
    df = fetch_data(sql_query)
    return df['Location_no'].nunique()  # Count distinct Location_no

# Create a NetworkX graph
def create_network_graph(data):
    G = nx.DiGraph()  # Use DiGraph for directed graph
    
    for node in data["nodes"]:
        node_id = node["id"]
        node_name = node["node_name"]
        sql_query = node["attributes"]["sql_query"]
        days = node["attributes"]["days"]
        incident_number = node["attributes"]["incident_number"]
        total_stores = calculate_total_stores(sql_query)
        
        # Adding node with attributes
        G.add_node(node_id, name=node_name, total_stores=total_stores, days=days, 
                   date=datetime.now().strftime("%Y-%m-%d"), incident_number=incident_number)
        
        # Adding links
        for linked_node in node["linked_nodes"]:
            G.add_edge(node_id, linked_node)

    return G

# Function to draw the graph
def draw_graph(G):
    pos = nx.spring_layout(G)  # positions for all nodes
    node_labels = {
        node: f"{G.nodes[node]['name']}<br>Stores: {G.nodes[node]['total_stores']}<br>Date: {G.nodes[node]['date']}<br>Incident: <a href='https://www.example.com/{G.nodes[node]['incident_number']}'>{G.nodes[node]['incident_number']}</a>"
        for node in G.nodes()
    }

    plt.figure(figsize=(12, 8))
    
    # Increase node size
    node_sizes = [10000] * len(G.nodes())  # Set all nodes to a larger size
    nx.draw(G, pos, with_labels=False, node_size=node_sizes, node_color='lightblue', arrows=True)

    # Draw labels inside the nodes
    for node in G.nodes():
        x, y = pos[node]
        plt.text(x, y, node_labels[node], fontsize=10, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    plt.title('Network Graph of Nodes')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

# Create the network graph
G = create_network_graph(data)

# Generate the plot
base64_image = draw_graph(G)

# HTML to display the graph
html_content = f"""
<div style="text-align: center;">
    <h2>Network Graph of Nodes</h2>
    <img src="data:image/png;base64,{base64_image}" style="width: 80%; max-width: 600px;">
</div>
"""

# Display the HTML content
# Note: Replace the following with your preferred method of rendering HTML.
# In Jupyter Notebook, you might use display(HTML(html_content)), for example.
# displayHTML(html_content)
print(html_content)  # Change this line as needed in your environment
