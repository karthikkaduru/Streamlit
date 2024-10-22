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
