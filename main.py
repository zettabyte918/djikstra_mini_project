import heapq
import folium
from geopy.distance import geodesic
import webbrowser
import os

from locations import locations
from connections import connections

def build_graph(locations, connections):
    """Build a graph using only defined connections."""
    graph = {city: {} for city in locations}
    for city1, neighbors in connections.items():
        for city2 in neighbors:
            distance = geodesic(locations[city1], locations[city2]).kilometers
            graph[city1][city2] = distance
    return graph


def dijkstra(graph, start):
    """Dijkstra's algorithm to find shortest paths."""
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}  # To reconstruct the path
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, predecessors


def reconstruct_path(predecessors, start, end):
    """Reconstruct the shortest path from start to end using the predecessors."""
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]
    if path[0] != start:  # No path exists
        return None
    return path


def visualize_path(locations, path):
    """Visualize the path on a map using folium."""
    if not path:
        print("No path to visualize.")
        return

    # Start with a map centered around the first location in the path
    start_coords = locations[path[0]]
    map = folium.Map(location=start_coords, zoom_start=7)

    # Add markers for each city
    for city, coords in locations.items():
        folium.Marker(coords, tooltip=city).add_to(map)

    # Add the path as a polyline
    path_coords = [locations[city] for city in path]
    folium.PolyLine(path_coords, color="blue", weight=2.5, opacity=1).add_to(map)

    # Save the map as an HTML file
    map.save("shortest_path.html")
    print("Map saved as 'shortest_path.html'. Open it in your browser to view the path.")
    file_path = 'shortest_path.html'
    file_path = os.path.abspath(file_path)
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Change this to the correct path
    webbrowser.get(chrome_path).open(f'file://{file_path}')



def main():
    """Main function to execute the shortest path program."""

     # Build the graph based on connections
    graph = build_graph(locations, connections)

    # User input
    start = input("Enter the starting city: ").strip().capitalize()
    end = input("Enter the destination city: ").strip().capitalize()

    if start not in locations or end not in locations:
        print("Invalid city. Please enter valid city names.")
        return

    # Find shortest path
    distances, predecessors = dijkstra(graph, start)
    path = reconstruct_path(predecessors, start, end)

    # Display results
    if path:
        print(f"Shortest distance from {start} to {end}: {distances[end]:.2f} km")
        print(f"Path: {' -> '.join(path)}")
        visualize_path(locations, path)
    else:
        print(f"No path found from {start} to {end}.")



if __name__ == "__main__":
    main()
