"""
Joshua Beard
CSE 163 AA
Shortest path test to verify data
"""
import networkx as nx
import re
import matplotlib.pyplot as plt


# Change this to the node/article you want to visualize.
TARGET_NODE = "Joshua Beard"


def build_graph():
    """Build and return the directed graph from graph.txt."""
    G = nx.DiGraph()

    with open("graph.txt") as txt:
        i = 0

        for line in txt.readlines():
            i += 1
            if i % 10000 == 0:
                print(i)

            # Some article titles have a colon in them.
            article, edges = tuple(
                re.split(r":(?=\[)", line, maxsplit=1)
            )

            article = article.lower()

            edges = edges.strip()
            edges = edges[1:-1]

            # Handle articles with no outgoing connections.
            if not edges:
                continue

            articles = edges.split(",")
            articles = [a.strip()[1:-1] for a in articles]

            for a in articles:
                G.add_edge(article, a.lower())

    return G


def draw_node_connections(G, node_name):
    """
    Draw a node and all of its incoming and outgoing connections.

    Incoming connections are displayed on the left.
    Outgoing connections are displayed on the right.
    The resulting image is saved as a PNG.
    """
    node_name = node_name.lower()

    if node_name not in G:
        print(f"Node '{node_name}' was not found in the graph.")
        return

    incoming = list(G.predecessors(node_name))
    outgoing = list(G.successors(node_name))

    print(f"Node: {node_name}")
    print(f"Incoming connections: {len(incoming)}")
    print(f"Outgoing connections: {len(outgoing)}")

    # Create a graph containing only the target and its neighbors.
    H = nx.DiGraph()
    H.add_node(node_name)

    for source in incoming:
        H.add_edge(source, node_name)

    for target in outgoing:
        H.add_edge(node_name, target)

    # Position nodes manually.
    pos = {
        node_name: (0, 0)
    }

    # Put incoming nodes on the left.
    if incoming:
        incoming_spacing = max(1.0, 5.0 / len(incoming))

        start_y = (len(incoming) - 1) * incoming_spacing / 2

        for i, node in enumerate(incoming):
            y = start_y - i * incoming_spacing
            pos[node] = (-1, y)

    # Put outgoing nodes on the right.
    if outgoing:
        outgoing_spacing = max(1.0, 5.0 / len(outgoing))

        start_y = (len(outgoing) - 1) * outgoing_spacing / 2

        for i, node in enumerate(outgoing):
            y = start_y - i * outgoing_spacing
            pos[node] = (1, y)

    # Make the figure larger when there are many connections.
    number_of_neighbors = len(incoming) + len(outgoing)
    height = max(6, number_of_neighbors * 0.35)

    plt.figure(figsize=(14, height))

    # Draw incoming nodes.
    nx.draw_networkx_nodes(
        H,
        pos,
        nodelist=incoming,
        node_color="lightblue",
        node_size=2500,
        edgecolors="black"
    )

    # Draw outgoing nodes.
    nx.draw_networkx_nodes(
        H,
        pos,
        nodelist=outgoing,
        node_color="lightgreen",
        node_size=2500,
        edgecolors="black"
    )

    # Draw the target node differently.
    nx.draw_networkx_nodes(
        H,
        pos,
        nodelist=[node_name],
        node_color="gold",
        node_size=3500,
        edgecolors="black",
        linewidths=2
    )

    # Draw arrows.
    nx.draw_networkx_edges(
        H,
        pos,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=20,
        edge_color="gray",
        width=1.5,
        connectionstyle="arc3,rad=0.05"
    )

    # Draw labels.
    nx.draw_networkx_labels(
        H,
        pos,
        font_size=8,
        font_weight="bold"
    )

    # Add labels identifying each side.
    plt.text(
        -1,
        max(3, len(incoming) * 0.2),
        "Incoming",
        horizontalalignment="center",
        fontsize=14,
        fontweight="bold",
        color="blue"
    )

    plt.text(
        1,
        max(3, len(outgoing) * 0.2),
        "Outgoing",
        horizontalalignment="center",
        fontsize=14,
        fontweight="bold",
        color="green"
    )

    plt.title(
        f"Connections for: {node_name}",
        fontsize=16,
        fontweight="bold"
    )

    plt.axis("off")
    plt.tight_layout()

    # Make a safe filename.
    filename = re.sub(r"[^a-zA-Z0-9_-]", "_", node_name)
    filename = f"{filename}_connections.png"

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved image to: {filename}")


def average_shortest_path():
    """
    Build the graph and create a visualization of TARGET_NODE.
    """
    G = build_graph()
    draw_node_connections(G, TARGET_NODE)


if __name__ == "__main__":
    average_shortest_path()