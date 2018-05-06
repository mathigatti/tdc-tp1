import pandas as pd
import re
import matplotlib.pyplot as plt

import sys

protocols_mapping = {'0x806': 'ARP (0x806)', '0x800': 'IPv4 (0x800)', '0x86dd': 'IPv6 (0x86dd)'}

def plot_broadcast_proportion(file_name):
	df = pd.read_csv(file_name, header=0)
	df.Symbol = df.Symbol.map(lambda s: re.search(u'(UNI|BROAD)CAST', s).group(0))
	df = df.groupby(['Symbol'])['Count'].sum()

	fig, ax = plt.subplots()
	ax.axis('equal')
	df.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)

	plt.savefig('broadcast_proportion_{}.png'.format(re.search(u'([^/]+/)*([^_]+)', file_name).group(2)))

def plot_protocols_proportion(file_name):
	df = pd.read_csv(file_name, header=0)
	df.Symbol = df.Symbol.map(lambda s: re.search(u",\s*\'([^\']+)\'", s).group(1))
	print df.Symbol
	df.Symbol = df.Symbol.map(protocols_mapping)
	df = df.groupby(['Symbol'])['Count'].sum()

	fig, ax = plt.subplots()
	ax.axis('equal')
	df.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)

	plt.savefig('protocols_proportion_{}.png'.format(re.search(u'([^/]+/)*([^_]+)', file_name).group(2)))

if __name__ == "__main__":
    if sys.argv[1] == 'broadcast_proportion':
    	plot_broadcast_proportion(sys.argv[2])
    elif sys.argv[1] == 'protocols_proportion':
    	plot_protocols_proportion(sys.argv[2])
