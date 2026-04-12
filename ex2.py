import heapq
class Graph:
    def __init__(self):
        self.nodes = {}  # {node_name: heuristic}
        self.edges = {}  # {node_name: {neighbor: weight}}
    def add_node(self, name, heuristic):
        # Convert heuristic to int to remove .0
        self.nodes[name] = int(heuristic)
        if name not in self.edges:
            self.edges[name] = {}
    def add_edge(self, u, v, weight):
        if u in self.nodes and v in self.nodes:
            # Convert edge weight to int
            self.edges[u][v] = int(weight)
            return True
        return False
    def a_star_search(self, start, goal):
        if start not in self.nodes or goal not in self.nodes:
            return None, float('inf')
        # open_list stores: (f_score, g_score, current_node, path)
        open_list = [(self.nodes[start], 0, start, [start])]
        g_costs = {node: float('inf') for node in self.nodes}
        g_costs[start] = 0
        print(f"\n--- Starting A* Search: {start} to {goal} ---")
        step = 1
        while open_list:
            open_list.sort()
            f, g, current, path = heapq.heappop(open_list)
            print(f"\nStep {step}:")
            print(f"  Current Node: {current} (f={int(f)}, g={int(g)}, h={self.nodes[current]})")
            print(f"  Current Path: {' -> '.join(path)}")
            if current == goal:
                print(f"  Goal reached!")
                return path, int(g)
            for neighbor, weight in self.edges[current].items():
                tentative_g = g + weight

# Condition: Check if new path cost is lower than previous known cost
                if tentative_g < g_costs[neighbor]:
                    print(f"    - Found better path to {neighbor}: Cost {int(tentative_g)} (Prev: {g_costs[neighbor] if g_costs[neighbor] != float('inf') else 'inf'})")
                    g_costs[neighbor] = tentative_g
                    f_score = tentative_g + self.nodes[neighbor]
                    heapq.heappush(open_list, (f_score, tentative_g, neighbor, path + [neighbor]))
                else:
                    print(f"    - Path to {neighbor} via {current} is higher cost. Skipping.")
            step += 1
        return None, float('inf')
    def display_graph(self):
        print("\n--- Current Graph Structure ---")
        if not self.nodes:
            print("Graph is empty.")
            return
        for node, h in self.nodes.items():
            neighbors = ", ".join([f"{n}(w:{int(w)})" for n, w in self.edges[node].items()])
            print(f"Node {node} [h={int(h)}] -> Neighbors: [{neighbors}]")
   def menu():
    g = Graph()
    print("\n" + "="*30)
    print("      A* SEARCH SYSTEM      ")
    print("="*30)
    print("1. Add Multiple Nodes")
    print("2. Delete Node")
    print("3. Add Multiple Edges")
    print("4. Delete Edge")
    print("5. Run A* Search")
    print("6. Display Graph")
    print("7. Exit")
    while True:
        choice = input("\nSelect Option (1-7): ")
        if choice == '1':
            print("(Type 'done' to stop adding nodes)")
            while True:
                name = input("Node Name: ")
                if name.lower() == 'done': break
                try:
                    h = int(float(input(f"Heuristic for {name}: ")))
                    g.add_node(name, h)
                except ValueError: print("Invalid numeric value.")
        elif choice == '3':
            print("(Type 'done' to stop adding edges)")
            while True:
                u = input("Source Node: ")
                if u.lower() == 'done': break
                v = input("Target Node: ")
                try:
                    w = int(float(input("Edge Weight: ")))
                    if not g.add_edge(u, v, w): print("Error: Nodes do not exist.")
                except ValueError: print("Invalid numeric value.")
        elif choice == '5':
            start = input("Start Node: ")
            goal = input("Goal Node: ")
            path, cost = g.a_star_search(start, goal)
            if path:
                print(f"\nFINAL RESULT:")
                print(f"Lowest Path: {' -> '.join(path)}")
                print(f"Total Lowest Cost: {int(cost)}")
            else:
                print("\nNo path found.")
        elif choice == '6':
            g.display_graph()
        elif choice == '7':
            print("Exiting...")
            break
         # Other simple options (delete) can be added as per previous logic
        elif choice == '2':
            name = input("Node name to delete: ")
            if name in g.nodes:
                del g.nodes[name]
                if name in g.edges: del g.edges[name]
                print(f"Node {name} deleted.")
            else: print("Node not found.")
menu()
