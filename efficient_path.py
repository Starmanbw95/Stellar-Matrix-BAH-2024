import math

class Graph:

    def __init__(self, nodes: list):
        self.nodes = nodes
        self.edges = []
        self.radius = 1737.1  # Radius of the moon in kilometers

    def add_edge(self, edge):
        # Edge is a tuple of (start_node, end_node, weight)
        self.edges.append(edge)

    def create_edge(self, start_node, end_node, start_coordinate: tuple, end_coordinate: tuple, extra):
        weight = extra
        lat1, lon1 = start_coordinate
        lat2, lon2 = end_coordinate

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = self.radius * c

        weight += distance
        edge = (start_node, end_node, weight)
        self.add_edge(edge)

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge[0] == node:
                neighbors.append(edge[1])
        return neighbors

    def shortest_path(self, src):
        dist = {node: float("Inf") for node in self.nodes}
        dist[src] = 0
        prev = {node: None for node in self.nodes}  # Keeps track of previous node in shortest path.
        unvisited = set(self.nodes)

        while unvisited:
            min_node = None
            for node in unvisited:
                if min_node is None:
                    min_node = node
                elif dist[node] < dist[min_node]:
                    min_node = node

            if dist[min_node] == float("Inf"):
                break

            unvisited.remove(min_node)
            current_weight = dist[min_node]

            for edge in self.edges:
                if edge[0] == min_node and edge[1] in unvisited:
                    weight = current_weight + edge[2]
                    if weight < dist[edge[1]]:
                        dist[edge[1]] = weight
                        prev[edge[1]] = min_node

        return dist, prev

    def print_distances(self, dist):
        for node in dist:
            print(f"Node {node} is at a distance of {dist[node]}")

    def print_paths(self, prev, src):
        for node in self.nodes:
            if prev[node] is None and node != src:
                print(f"No path to node {node}")
                continue

            path = []
            current = node
            while current is not None:
                path.append(current)
                current = prev[current]
            path = path[::-1]

            if path[0] == src:
                print(f"Shortest path to node {node}: {' - '.join(path)}")
            else:
                print(f"No path to node {node}")


def main():
    nodes = ["Landing Site", "A", "B", "C", "D"]  # Add all the nodes here in the form of strings (Use whatever format is comfortable). Eg. ["A", "B", "C"]
    graph = Graph(nodes)

    # Create and add edges here:
    # graph.create_edge(start_node, end_node, start_coordinate, end_coordinate, extra)
    # Extra - Any extra blockage or distance that needs to be added due to an inclination / boulder / etc. (Optional) Add 0 if not required.
    # Since most distances are in the order of 10s of metres, the extra blockage should be in the same order of magnitude (around 5-10m)
    # Coordinates are in the form of (latitude, longitude) in degrees.
    # Eg. graph.create_edge("A", "B", (10, 21), (11, 5), 2) 
    # Add all the edges (intermediate also) in the same way. (Keep adding graph.create_edge statements)

    # Example edges
    graph.create_edge("Landing Site", "A", (0, 0), (0, 1), 2)
    graph.create_edge("Landing Site", "B", (0, 0), (1, 1), 3)
    graph.create_edge("A", "C", (0, 1), (1, 2), 2)
    graph.create_edge("B", "C", (1, 1), (1, 2), 1)
    graph.create_edge("C", "D", (1, 2), (2, 2), 4)

    distances, predecessors = graph.shortest_path("Landing Site")
    graph.print_distances(distances)
    graph.print_paths(predecessors, "Landing Site")

    # Choose the node with the shortest path which is at least 100m from source.

if __name__ == "__main__":
    main()
