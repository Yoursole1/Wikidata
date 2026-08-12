import numpy as np
import scipy.sparse as sps
import re


def parse_line(line):
    # Split only at the colon before the edge list.
    article, edges = re.split(r":(?=\[)", line, maxsplit=1)

    article = article.lower()

    edges = edges.strip()[1:-1]  # remove [ and ]

    if not edges:
        return article, []

    articles = edges.split(",")
    articles = [a.strip()[1:-1].lower() for a in articles]

    return article, articles


def page_rank():
    # ------------------------------------------------------------
    # Pass 1:
    # Build the article -> integer ID mapping.
    #
    # We do this without storing the graph itself.
    # ------------------------------------------------------------

    node_to_id = {}
    id_to_node = []

    with open("graph.txt") as txt:
        for i, line in enumerate(txt, 1):
            if i % 10000 == 0:
                print("Reading:", i)

            article, articles = parse_line(line)

            if article not in node_to_id:
                node_to_id[article] = len(id_to_node)
                id_to_node.append(article)

            for target in articles:
                if target not in node_to_id:
                    node_to_id[target] = len(id_to_node)
                    id_to_node.append(target)

    n = len(id_to_node)

    print("Number of nodes:", n)

    # ------------------------------------------------------------
    # Pass 2:
    # Build the edge arrays.
    #
    # We read the file again because this avoids keeping the
    # entire graph in memory.
    # ------------------------------------------------------------

    rows = []
    cols = []

    with open("graph.txt") as txt:
        for i, line in enumerate(txt, 1):
            if i % 10000 == 0:
                print("Building edges:", i)

            article, articles = parse_line(line)

            source = node_to_id[article]

            for target in articles:
                rows.append(source)
                cols.append(node_to_id[target])

    print("Number of edges:", len(rows))

    # ------------------------------------------------------------
    # Create sparse adjacency matrix.
    # ------------------------------------------------------------

    rows = np.asarray(rows, dtype=np.int32)
    cols = np.asarray(cols, dtype=np.int32)

    A = sps.csr_matrix(
        (
            np.ones(len(rows), dtype=np.float64),
            (rows, cols)
        ),
        shape=(n, n)
    )

    # NetworkX DiGraph does not allow duplicate edges.
    # If graph.txt contains duplicate edges, CSR construction
    # sums them. Convert all nonzero values back to 1.
    A.sum_duplicates()
    A.data[:] = 1.0

    # rows/cols are no longer needed.
    del rows
    del cols

    # ------------------------------------------------------------
    # Normalize each row.
    # ------------------------------------------------------------

    row_sums = np.asarray(A.sum(axis=1)).ravel()

    no_outgoing = (row_sums == 0)

    # Avoid division by zero.
    row_sums[no_outgoing] = 1

    # Divide each stored value by its row's sum.
    A.data *= np.repeat(
        1.0 / row_sums,
        np.diff(A.indptr)
    )

    del row_sums

    # ------------------------------------------------------------
    # PageRank
    # ------------------------------------------------------------

    r = np.full(n, 1.0 / n)
    r_0 = r.copy()

    alpha = 0.85

    iteration = 0

    while True:

        total_no_outgoing = r[no_outgoing].sum()

        r = (
            alpha * (A.T @ r)
            + alpha * (total_no_outgoing / n)
            + (1 - alpha) * r_0
        )

        # Get top 10 without sorting the entire array.
        top_10 = np.argpartition(r, -10)[-10:]
        top_10 = top_10[np.argsort(r[top_10])[::-1]]

        print("Iteration:", iteration)

        for top in top_10:
            print(id_to_node[top], r[top])

        print("Sum r:", r.sum())

        iteration += 1


if __name__ == "__main__":
    page_rank()