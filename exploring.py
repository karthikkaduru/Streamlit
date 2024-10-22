# Streamlit App
st.title("Node Visualization Flowchart")

# Sidebar for team selection
st.sidebar.header("Select a Team")
team_option = st.sidebar.selectbox("Team", ["Team A", "Team B"])

# Load the appropriate team JSON data based on selection
nodes_data = json.loads(team_a_json) if team_option == "Team A" else json.loads(team_b_json)

# Create the network graph
net = Network(height='600px', width='100%', notebook=True, bgcolor='#001f3f', font_color='white')

# Add nodes with detailed labels inside rectangular shapes
for node in nodes_data:
    store_count = get_store_count(node['attributes']['sql_query'])
    incident_number = node['attributes']['incident_number']
    
    # Construct the label with details
    label_info = (f"<strong>{node['node_name']}</strong><br>"
                  f"Stores Count: {store_count}<br>"
                  f"Incident Number: {incident_number}")

    # Add node as rectangular shape with detailed label
    net.add_node(node['id'], label=label_info, shape='box', color='skyblue', size=20)

# Add edges based on the team
links = "1>>2>>3" if team_option == "Team A" else "4>>5>>6>>7"
for i in range(len(links.split('>>')) - 1):
    net.add_edge(links[i], links[i + 1])

# Generate the network graph
net.force_atlas_2based()
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
        st.write(f"[Incident Number: {details['attributes']['incident_number']}](https://www.google.com/search?q={details['attributes']['incident_number']})")
