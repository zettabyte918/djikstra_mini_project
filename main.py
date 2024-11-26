import folium
import heapq


def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

from math import radians, sin, cos, sqrt, atan2

def haversine(coord1, coord2):
    # Earth radius in kilometers
    R = 6371.0
    
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def build_graph(locations):
    graph = {}
    for loc1 in locations:
        graph[loc1] = {}
        for loc2 in locations:
            if loc1 != loc2:
                graph[loc1][loc2] = haversine(locations[loc1], locations[loc2])
    return graph


def main():
    locations = {
        'Tunis': (36.8065, 10.1815),
        'Sousse': (35.8256, 10.6084),
        'Gafsa': (33.8869, 9.5375)
    }
    
    graph = build_graph(locations)
    start = input("Enter the starting city: ").strip().capitalize()
    end = input("Enter the destination city: ").strip().capitalize()
    
    distances = dijkstra(graph, start)
    print(f"Shortest distance from {start} to {end}: {distances[end]:.2f} km")
    path = ['Tunis', 'Sousse', 'Gafsa']
    visualize_path(locations, path)



def visualize_path(locations, path):
    map = folium.Map(location=list(locations.values())[0], zoom_start=6)
    for city, coords in locations.items():
        folium.Marker(coords, tooltip=city).add_to(map)
    
    path_coords = [locations[city] for city in path]
    folium.PolyLine(path_coords, color="blue", weight=2.5, opacity=1).add_to(map)
    map.save("shortest_path.html")

main()