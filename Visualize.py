import networkx as nx
import numpy as np
import string
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm
import matplotlib.colors
import matplotlib as mpl
from matplotlib import cm
from colorspacious import cspace_converter
#from colormaps import cmaps  # the colormaps, grouped by category

class Visualize:

    def distance_matrix_colormap(self,distance_matrix,is_grey=False):
        if is_grey:
            my_cmap='Greys'
        else:

            cdict = {'red': ((0., 0, 0),
                             (0.66, 1, 1),
                             (0.89, 1, 1),
                             (1, 1, 1)),
                     'green': ((0., 0, 0),
                               (0.375, 1, 1),
                               (0.64, 1, 1),
                               (0.91, 0, 0),
                               (1, 0, 0)),
                     'blue': ((0., 1, 1),
                              (0.05, 1, 1),
                              (0.11, 1, 1),
                              (0.34, 1, 1),
                              (0.65, 0, 0),
                              (1, 0, 0))}
            my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 256)
        plt.pcolor(distance_matrix, cmap=my_cmap)
        plt.colorbar()
        plt.show()

    def distance_matrix_network(self,distance_matrix):
        dm=np.mat(distance_matrix)

        G = nx.from_numpy_matrix(dm)
        G = nx.relabel_nodes(G, dict(zip(range(len(G.nodes())),string.ascii_uppercase)))

        G = nx.drawing.nx_agraph.to_agraph(G)

        G.node_attr.update(color="red", style="filled")
        G.edge_attr.update(color="blue", width="2.0")

        G.draw('/tmp/out.png', format='png', prog='neato')

    def cluster_result_linechart(self,eps,cluster_num,noise_num):
        x=eps
        y1=cluster_num
        y2=noise_num
        fig = plt.figure()

        ax1 = fig.add_subplot(111)
        line1=ax1.plot(x, y1)
        ax1.set_ylabel('Cluster Number')
        ax1.set_title("eps")
        ax1.legend(line1,('Cluster Number',))
        ax2 = ax1.twinx()  # this is the important function
        line2=ax2.plot(x, y2, 'r')
        ax2.set_ylabel('Noise Number')
        ax2.set_xlabel('eps')
        ax2.legend(line2, ('Noise Number',),bbox_to_anchor=(1,0.9))