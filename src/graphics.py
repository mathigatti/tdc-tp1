import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

import sys

protocols_mapping = {'0x806': 'ARP (0x806)', '0x800': 'IPv4 (0x800)', '0x86dd': 'IPv6 (0x86dd)'}

def plot_broadcast_proportion(file_name):
	df = pd.read_csv(file_name, header=0)
	df.Symbol = df.Symbol.map(lambda s: re.search(u'(UNI|BROAD)CAST', s).group(0))
	df = df.groupby(['Symbol'])['Count'].sum()

	fig, ax = plt.subplots()
	ax.axis('equal')
	df.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)

	plt.savefig('broadcast_proportion_{}.png'.format(re.search(u'([^/]+/)*([^\.]+)', file_name).group(2)))

def plot_protocols_proportion(file_name):
	df = pd.read_csv(file_name, header=0)
	df.Symbol = df.Symbol.map(lambda s: re.search(u",\s*\'([^\']+)\'", s).group(1))
	print df.Symbol
	df.Symbol = df.Symbol.map(protocols_mapping)
	df = df.groupby(['Symbol'])['Count'].sum()

	fig, ax = plt.subplots()
	ax.axis('equal')
	df.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)

	plt.savefig('protocols_proportion_{}.png'.format(re.search(u'([^/]+/)*([^\.]+)', file_name).group(2)))

def plot_information(file_name):
	df = pd.read_csv(file_name, header=0)
	
	#Calculates the entropy and max_entropy
	entropy = 0
	for index, row in df.iterrows():
		entropy -= row['Probability'] * math.log(row['Probability'], 2)

	max_entropy = math.log(df.shape[0], 2)

	def formatter(y, pos):
	    if y == entropy:
	        return 'Entropia'
	    elif y == max_entropy:
	        return 'Entropia Maxima'
	    else:
	        return y

	print df

	series = pd.Series(data=df['Information'].values, index=df['Symbol'])
	series = series.sort_index()

	print series

	fig, ax = plt.subplots()
	ax.hlines(entropy, -0.5, 5.5, linestyle='--', linewidth=1, label=u'Entropia', color='red')
	ax.hlines(max_entropy, -0.5, 5.5, linestyle='--', linewidth=1, label=u'Maxima Entropia', color='green')
	ax.set_ylabel('Informacion (bits)')
	ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))
	ax.legend(title='Rotulos')
	series.plot.bar(ax=ax, rot=20, fontsize=8, sort_columns=True)

	plt.tight_layout()
	plt.savefig('information_{}.png'.format(re.search(u'([^/]+/)*([^\.]+)', file_name).group(2)))

if __name__ == "__main__":
    if sys.argv[1] == 'broadcast_proportion':
    	plot_broadcast_proportion(sys.argv[2])
    elif sys.argv[1] == 'protocols_proportion':
    	plot_protocols_proportion(sys.argv[2])
    elif sys.argv[1] == 'information':
    	plot_information(sys.argv[2])