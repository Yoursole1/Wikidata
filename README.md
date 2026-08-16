Welcome to the Wikipedia analyzer!

Python libraries that you will need to install:
- networkx
- scipy
- numpy
- mwparserfromhell

System Requirements
- Minimum of 64gb of ram and 20gb of memory swap available
- Fairly good single thread performance if you want this to run within a week

File Explanations
- parse_xml.py: Takes wikidump xml files and converts to a graph.txt file that is an adjacency list for the network
- page_rank.py: Takes graph.txt and performs pagerank on the network
- clustering_coefficient.py: Takes graph.txt and finds the global clustering coefficient
- shortest_path.py: Takes graph.txt and finds the average shortest path between nodes in the network

Steps to Run
1. Download all files here (https://dumps.wikimedia.org/other/mediawiki_content_current/enwiki/2026-07-01/xml/bzip2/)
2. Run parse_xml.py on the folder where all these files live.  This will probably take a day or two.  When it finishes you should have a file called graph.txt
3. You can now run page_rank.py, shortest_path.py, and clustering_coefficient.py on graph.txt to get the data
   1. Note that for page_rank.py, you should watch your system memory usage while it starts.  I had to increase swap space to keep it from crashing