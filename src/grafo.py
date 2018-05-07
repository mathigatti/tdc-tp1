
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
def grafo_dirigido(edges):
	G = nx.DiGraph()

	for a,b,w in edges:
		G.add_edge(a, b, weight=w)

	weight = list(map(lambda x: -x[-1], list(edges)))

	edges_processed = [(u, v) for (u, v, d) in G.edges(data=True)]

	pos = nx.circular_layout(G)  # positions for all nodes

	# nodes
	nx.draw_networkx_nodes(G, pos, alpha=0.0, node_color='#A0CBE2', node_size=100000)
	# edges
	nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=30, edge_color='#A0CBE2', edgelist=edges_processed,
	                       width=2, arrows=True)
	
	# labels
	nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
	plt.title('Starbucks')
	plt.axis('off')
	plt.savefig('grafo.png')