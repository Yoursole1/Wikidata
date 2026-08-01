import networkx as nx
import re
import json

def average_shortest_path():

    with open("graph.txt") as txt:
        G = nx.Graph()
        i = 0
        for line in txt.readlines():
            i += 1
            if i % 10000 == 0:
                print(i)

            # I did this because some article titles have a colon in them
            # Cast to tuple for unpacking
            article, edges = tuple(re.split(r":(?=\[)", line, maxsplit=1))

            # turns string version of list to actual list, is more robust to edge cases than what I might come up with
            edges = edges.strip()
            edges = edges[1:-1]
            articles = edges.split(",")
            articles = [a.strip()[1:-1] for a in articles]

            for a in articles:
                G.add_edge(article, a)

        path = nx.shortest_path(G, source="Mathematics", target="Spanish language")
        print(path)










if __name__ == "__main__":
    average_shortest_path()