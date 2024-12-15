from flask import Flask, request, jsonify
from flask_cors import CORS
import osmnx as ox
import networkx as nx

app = Flask(__name__)
CORS(app)

# Load the graph for Bengaluru
G = ox.graph_from_place("Bengaluru, India", network_type="drive")

@app.route("/shortest_path", methods=["POST"])
def shortest_path():
    data = request.json
    origin = data["origin"]
    destination = data["destination"]
    
    # Convert lat-lng to nearest graph nodes
    origin_node = ox.distance.nearest_nodes(G, origin["lng"], origin["lat"])
    destination_node = ox.distance.nearest_nodes(G, destination["lng"], destination["lat"])

    # Calculate the shortest path
    shortest_path = nx.shortest_path(G, origin_node, destination_node, weight="length")
    coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]
    
    return jsonify({"path": coordinates})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
