import heapq
import folium
from geopy.distance import geodesic
import webbrowser
import os

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
    locations = {
        'Tunis': (36.8064, 10.1817),
        'Sidi Bouzid': (35.0381, 9.4858),
        'Sfax': (34.7400, 10.7600),
        'Sousse': (35.8333, 10.6333),
        'Kairouan': (35.6772, 10.1008),
        'Métouia': (33.9667, 10.0000),
        'Kebili': (33.7050, 8.9650),
        'Jendouba': (36.5072, 8.7757),
        'Sukrah': (36.8833, 10.2500),
        'Gabès': (33.8833, 10.1167),
        'Ariana': (36.8625, 10.1956),
        'Gafsa': (34.4225, 8.7842),
        'Msaken': (35.7333, 10.5833),
        'Medenine': (33.3547, 10.5053),
        'Béja': (36.7333, 9.1833),
        'Kasserine': (35.1667, 8.8333),
        'Radès': (36.7667, 10.2833),
        'Hammamet': (36.4000, 10.6167),
        'Tataouine': (32.9306, 10.4500),
        'Monastir': (35.7694, 10.8194),
        'La Marsa': (36.8764, 10.3253),
        'Ben Arous': (36.7472, 10.3333),
        'Sakiet ez Zit': (34.8000, 10.7700),
        'Zarzis': (33.5000, 11.1167),
        'Ben Gardane': (33.1389, 11.2167),
        'Mahdia': (35.5000, 11.0667),
        'Bizerte': (37.2768, 9.8642),
        'Houmt Souk': (33.8667, 10.8500),
        'Fouchana': (36.7000, 10.1667),
        'Le Kram': (36.8333, 10.3167),
        'El Kef': (36.1822, 8.7147),
        'El Hamma': (33.8864, 9.7951),
        'Nabeul': (36.4542, 10.7347),
        'Le Bardo': (36.8092, 10.1406),
        'Djemmal': (35.6400, 10.7600),
        'Korba': (36.5667, 10.8667),
        'Menzel Temime': (36.7833, 10.9833),
        'Mat': (36.7833, 10.9833),
        'Ghardimaou': (36.4500, 8.4333),
        'Midoun': (33.8000, 11.0000),
        'Menzel Bourguiba': (37.1500, 9.7833),
        'Manouba': (36.8078, 10.1011),
        'Matmata': (33.4552, 9.7679)
        
    }

    connections = {
        'Tunis': ['Ariana', 'Sukrah', 'Hammamet', 'Nabeul', 'Radès', 'La Marsa'],
        'Sidi Bouzid': ['Kasserine', 'Gafsa', 'Kairouan'],
        'Sfax': ['Mahdia', 'Gabès', 'Medenine'],
        'Sousse': ['Mahdia', 'Monastir', 'Msaken'],
        'Kairouan': ['Sidi Bouzid', 'Kasserine', 'Tunis'],
        'Métouia': ['Kebili', 'Gafsa', 'Medenine'],
        'Kebili': ['Métouia', 'Gafsa', 'Medenine', 'Gabès'],
        'Sukrah': ['Tunis', 'Ariana', 'Radès', 'La Marsa'],
        'Gabès': ['Sfax', 'Kebili', 'Medenine', 'Tataouine'],
        'Ariana': ['Tunis', 'Sukrah', 'La Marsa', 'Ben Arous'],
        'Gafsa': ['Sidi Bouzid', 'Kasserine', 'Métouia'],
        'Msaken': ['Sousse', 'Monastir', 'Mahdia', 'Djemmal'],
        'Medenine': ['Sfax', 'Kebili', 'Gabès', 'Tataouine'],
        'Béja': ['Jendouba', 'Bizerte', 'Tunis'],
        'Kasserine': ['Sidi Bouzid', 'Kairouan', 'Gafsa', 'Béja'],
        'Radès': ['Tunis', 'La Marsa', 'Ben Arous'],
        'Hammamet': ['Tunis', 'Sousse', 'Nabeul', 'Kairouan'],
        'Tataouine': ['Gabès', 'Medenine', 'Zarzis', 'Matmata'],
        'Monastir': ['Sousse', 'Mahdia', 'Msaken', 'Kairouan'],
        'La Marsa': ['Tunis', 'Ariana', 'Sukrah', 'Radès'],
        'Ben Arous': ['Tunis', 'Ariana', 'La Marsa', 'Radès'],
        'Sakiet ez Zit': ['Radès', 'Sousse', 'Hammamet', 'La Marsa'],
        'Zarzis': ['Gabès', 'Medenine', 'Tataouine', 'Midoun'],
        'Ben Gardane': ['Zarzis', 'Medenine', 'Tataouine', 'Matmata'],
        'Mahdia': ['Sousse', 'Monastir', 'Msaken', 'Sfax'],
        'Houmt Souk': ['Midoun', 'Zarzis', 'Medenine', 'Menzel Bourguiba'],
        'Fouchana': ['Tunis', 'Ben Arous', 'Radès', 'La Marsa'],
        'Le Kram': ['Tunis', 'La Marsa', 'Ariana', 'Radès'],
        'El Kef': ['Tunis', 'Kasserine', 'Gafsa', 'Béja'],
        'El Hamma': ['Gabès', 'Medenine', 'Zarzis', 'Tataouine'],
        'Nabeul': ['Hammamet', 'Tunis', 'Béja', 'Korba'],
        'Le Bardo': ['Tunis', 'La Marsa', 'Ariana', 'Sakiet ez Zit'],
        'Djemmal': ['Sousse', 'Monastir', 'Mahdia', 'Msaken'],
        'Korba': ['Nabeul', 'Menzel Temime', 'Hammamet', 'Zarzis'],
        'Menzel Temime': ['Nabeul', 'Korba', 'Monastir', 'Sousse'],
        'Ghardimaou': ['Jendouba', 'El Kef', 'Béja'],
        'Midoun': ['Houmt Souk', 'Zarzis', 'Medenine', 'Menzel Bourguiba'],
        'Menzel Bourguiba': ['Béja', 'Menzel Temime', 'Midoun', 'Ghardimaou'],
        'Manouba': ['Tunis', 'Ariana', 'Le Bardo', 'Kairouan']
    }



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
