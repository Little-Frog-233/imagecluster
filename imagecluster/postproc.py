import os
import shutil
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

from . import calc as ic

pj = os.path.join


def plot_clusters(clusters, ias, max_csize=None, mem_limit=1024**3):
    """Plot `clusters` of images in `ias`.

    For interactive work, use :func:`visualize` instead.

    Parameters
    ----------
    clusters : see :func:`calc.cluster`
    ias : see :func:`calc.image_arrays`
    max_csize : int
        plot clusters with at most this many images
    mem_limit : float or int, bytes
        hard memory limit for the plot array (default: 1 GiB), increase if you
        have (i) enough memory, (ii) many clusters and/or (iii) large
        max(csize) and (iv) max_csize is large or None
    """
    stats = ic.cluster_stats(clusters)
    if max_csize is not None:
        stats = stats[stats[:,0] <= max_csize, :]
    # number of clusters
    ncols = stats[:,1].sum()
    # csize (number of images per cluster)
    nrows = stats[:,0].max()
    shape = ias[list(ias.keys())[0]].shape[:2]
    mem = nrows * shape[0] * ncols * shape[1] * 3
    if mem > mem_limit:
        raise Exception("size of plot array ({} MiB) > mem_limit({} MiB)".format(mem/1024**2, mem_limit/1024**2))
    # uint8 has range 0..255, perfect for images represented as integers, makes
    # rather big arrays possible
    arr = np.ones((nrows*shape[0], ncols*shape[1], 3), dtype=np.uint8) * 255
    icol = -1
    for csize in stats[:,0]:
        for cluster in clusters[csize]:
            icol += 1
            for irow, filename in enumerate(cluster):
                img_arr = ias[filename]
                arr[irow*shape[0]:(irow+1)*shape[0],
                    icol*shape[1]:(icol+1)*shape[1], :] = img_arr
    print("plot array ({}) size: {} MiB".format(arr.dtype, arr.nbytes/1024**2))
    fig,ax = plt.subplots()
    ax.imshow(arr)
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig,ax


def visualize(*args, **kwds):
    plot_clusters(*args, **kwds)
    plt.show()


def make_links(clusters, cluster_dr):
    print("cluster dir: {}".format(cluster_dr))
    if os.path.exists(cluster_dr):
        shutil.rmtree(cluster_dr)
    for csize, group in clusters.items():
        for iclus, cluster in enumerate(group):
            dr = pj(cluster_dr,
                    'cluster_with_{}'.format(csize),
                    'cluster_{}'.format(iclus))
            for fn in cluster:
                link = pj(dr, os.path.basename(fn))
                os.makedirs(os.path.dirname(link), exist_ok=True)
                os.symlink(os.path.abspath(fn), link)

def make_links_v2(cluster, cluster_dr):
    '''

    :param cluster: pandas.DataFrame['file_path', 'file_label']
    :param cluster_dr:
    :return:
    '''
    print(cluster.head())
    print("cluster dir: {}".format(cluster_dr))
    if os.path.exists(cluster_dr):
        shutil.rmtree(cluster_dr)
    labels = cluster['label'].to_list()
    file_path = cluster['file_path'].to_list()
    clusters = {}
    for i in range(len(labels)):
        if labels[i] in clusters.keys():
            clusters[labels[i]].append(file_path[i])
        else:
            clusters[labels[i]] = [file_path[i]]
    for i in clusters.keys():
        dr = pj(cluster_dr, 'cluster_{}'.format(i))
        for path in clusters[i]:
            link = pj(dr, os.path.basename(path))
            os.makedirs(os.path.dirname(link), exist_ok=True)
            os.symlink(os.path.abspath(path), link)
