"""
Joshua Beard
CSE 163 AA
Shortest path test to verify data
"""
import random

import networkx as nx
import re


def average_shortest_path():
    '''
    Will find the average shortest
    path between nodes in the graph
    specified in graph.txt.  As is,
    it finds the shortest path between
    two specific nodes, but this is
    only being used for testing.
    '''
    with open("graph.txt") as txt:
        G = nx.DiGraph()

        i = 0
        for line in txt.readlines():
            i += 1
            if i % 10000 == 0:
                print(i)

            # I did this because some article titles have a colon in them
            # Cast to tuple for unpacking
            article, edges = tuple(re.split(r":(?=\[)", line, maxsplit=1))
            article = article.lower()

            edges = edges.strip()
            edges = edges[1:-1]
            articles = edges.split(",")
            articles = [a.strip()[1:-1] for a in articles]

            for a in articles:
                G.add_edge(article, a.lower())

        total_distance = 0
        num_valid_paths = 0

        while True:
            node1, node2 = random.sample(list(G.nodes), 2)

            try:
                distance = nx.shortest_path_length(G, node1, node2)

                total_distance += distance
                num_valid_paths += 1

                average_distance = total_distance / num_valid_paths

                print(f"Average shortest path: {average_distance:.4f}")

            except nx.NetworkXNoPath:
                continue


if __name__ == "__main__":
    average_shortest_path()
