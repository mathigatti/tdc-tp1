
import matplotlib.pyplot as plt
import networkx as nx

def grafo_dirigido(edges):
	G = nx.DiGraph()

	for a,b,w in edges:
		G.add_edge(a, b, weight=w)

	weight = list(map(lambda x: -x[-1], list(edges)))
	print weight
	edges_processed = [(u, v) for (u, v, d) in G.edges(data=True)]

	pos = nx.spring_layout(G, k=1000)  # positions for all nodes

	# nodes
	nx.draw_networkx_nodes(G, pos, alpha=1.0, node_color='#A0CBE2', node_size=100)
	# edges
	nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=30, edge_color=weight, edgelist=edges_processed,
	                       width=6, arrows=True, edge_cmap=plt.cm.Blues)
	
	# labels
	nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

	plt.axis('off')
	plt.show()
	plt.savefig('grafo.png')