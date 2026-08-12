import numpy as np
import scipy.sparse as sps
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

        A = nx.to_scipy_sparse_array(G, format="csr", dtype=float)
        del G

        row_sums = np.asarray(A.sum(axis=1)).ravel()
        no_outgoing = (row_sums == 0)
        row_sums[row_sums == 0] = 1


        A = sps.diags(1 / row_sums) @ A
        r = np.asarray([1 / G.number_of_nodes()] * G.number_of_nodes())
        r_0 = np.asarray([1 / G.number_of_nodes()] * G.number_of_nodes()) # same thing

        alpha = 0.85

        i = 0
        while True:
            total_no_outgoing = r[no_outgoing].sum()

            r = alpha * (A.T @ r) + (alpha * (total_no_outgoing / G.number_of_nodes())) + (1 - alpha) * r_0

            top_10 = sorted(range(len(r)), key=lambda i: r[i], reverse=True)[:10]

            print("Iteration: " + str(i))
            nodes = list(G.nodes())
            for top in top_10:
                print(nodes[top])

            print("Sum r: " + str(sum(r)))

            i += 1

if __name__ == "__main__":
    average_shortest_path()