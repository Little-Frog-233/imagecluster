#coding:utf-8
import os
import pandas as pd
import numpy as np
from imagecluster import calc as ic
from imagecluster import common as co
from imagecluster import postproc as pp
from imagecluster.log import log

pj = os.path.join


ic_base_dir = 'imagecluster'



def main_hierarchy(imagedir, sim=0.5, layer='fc2', size=(224,224), links=True, vis=False,
         max_csize=None, pca=False, pca_params=dict(n_components=0.9)):
    """Example main app using this library.

    Upon first invocation, the image and fingerprint databases are built and
    written to disk. Each new invocation loads those and only repeats
        * clustering
        * creation of links to files in clusters
        * visualization (if `vis=True`)

    This is good for playing around with the `sim` parameter, for
    instance, which only influences clustering.

    Parameters
    ----------
    imagedir : str
        path to directory with images
    sim : float (0..1)
        similarity index (see :func:`calc.cluster`)
    layer : str
        which layer to use as feature vector (see
        :func:`calc.get_model`)
    size : tuple
        input image size (width, height), must match `model`, e.g. (224,224)
    links : bool
        create dirs with links
    vis : bool
        plot images in clusters
    max_csize : max number of images per cluster for visualization (see
        :mod:`~postproc`)
    pca : bool
        Perform PCA on fingerprints before clustering, using `pca_params`.
    pca_params : dict
        kwargs to sklearn's PCA

    Notes
    -----
    imagedir : To select only a subset of the images, create an `imagedir` and
        symlink your selected images there. In the future, we may add support
        for passing a list of files, should the need arise. But then again,
        this function is only an example front-end.
    """
    logger_hierarchy = log(logger_name='hierarchy').logger
    fps_fn = pj(imagedir, ic_base_dir, 'fingerprints.pk')
    ias_fn = pj(imagedir, ic_base_dir, 'images.pk')
    ias = None
    try:
        if not os.path.exists(fps_fn):
            print("no fingerprints database {} found".format(fps_fn))
            logger_hierarchy.info("no fingerprints database {} found".format(fps_fn))
            os.makedirs(os.path.dirname(fps_fn), exist_ok=True)
            try:
                model = ic.get_model(layer=layer)
            except Exception as e:
                logger_hierarchy.error(e)
            if not os.path.exists(ias_fn):
                print("create image array database {}".format(ias_fn))
                logger_hierarchy.info("create image array database {}".format(ias_fn))
                ias = ic.image_arrays(imagedir, size=size)
                co.write_pk(ias, ias_fn)
            else:
                ias = co.read_pk(ias_fn)
            print("running all images through NN model ...")
            fps = ic.fingerprints(ias, model)
            co.write_pk(fps, fps_fn)
        else:
            print("loading fingerprints database {} ...".format(fps_fn))
            fps = co.read_pk(fps_fn)
        if pca:
            fps = ic.pca(fps, **pca_params)
            print("pca dims:", list(fps.values())[0].shape[0])
        #将每张图片转换成向量
        #进行聚类
        print("clustering ...")
        clusters = ic.cluster(fps, sim)
        if links:
            pp.make_links(clusters, pj(imagedir, ic_base_dir, 'clusters'))
        if vis:
            if ias is None:
                ias = co.read_pk(ias_fn)
            pp.visualize(clusters, ias, max_csize=max_csize)
    except Exception as e:
        logger_hierarchy.error(e)

def main_kmeans(imagedir, n_clusters=5, layer='fc2', size=(224,224), links=True, pca=False, pca_params=dict(n_components=0.9)):
    """Example main app using this library.

    Upon first invocation, the image and fingerprint databases are built and
    written to disk. Each new invocation loads those and only repeats
        * clustering
        * creation of links to files in clusters
        * visualization (if `vis=True`)

    This is good for playing around with the `sim` parameter, for
    instance, which only influences clustering.

    Parameters
    ----------
    imagedir : str
        path to directory with images
    n_cluster : int (1...999)
        num of kmeans cluster (see :func:`calc.cluster_kmeans`)
    layer : str
        which layer to use as feature vector (see
        :func:`calc.get_model`)
    size : tuple
        input image size (width, height), must match `model`, e.g. (224,224)
    links : bool
        create dirs with links
    pca : bool
        Perform PCA on fingerprints before clustering, using `pca_params`.
    pca_params : dict
        kwargs to sklearn's PCA

    Notes
    -----
    imagedir : To select only a subset of the images, create an `imagedir` and
        symlink your selected images there. In the future, we may add support
        for passing a list of files, should the need arise. But then again,
        this function is only an example front-end.
    """
    fps_fn = pj(imagedir, ic_base_dir, 'fingerprints.pk')
    ias_fn = pj(imagedir, ic_base_dir, 'images.pk')
    ias = None
    logger_kmeans = log(logger_name='kmeans').logger
    try:
        if not os.path.exists(fps_fn):
            print("no fingerprints database {} found".format(fps_fn))
            logger_kmeans.info("no fingerprints database {} found".format(fps_fn))
            os.makedirs(os.path.dirname(fps_fn), exist_ok=True)
            try:
                model = ic.get_model(layer=layer)
            except Exception as e:
                logger_kmeans.error(e)
            if not os.path.exists(ias_fn):
                logger_kmeans.info("create image array database {}".format(ias_fn))
                print("create image array database {}".format(ias_fn))
                ias = ic.image_arrays(imagedir, size=size)
                co.write_pk(ias, ias_fn)
            else:
                ias = co.read_pk(ias_fn)
            print("running all images through NN model ...")
            fps = ic.fingerprints(ias, model)
            co.write_pk(fps, fps_fn)
        else:
            print("loading fingerprints database {} ...".format(fps_fn))
            fps = co.read_pk(fps_fn)
        if pca:
            fps = ic.pca(fps, **pca_params)
            print("pca dims:", list(fps.values())[0].shape[0])
            logger_kmeans.info("pca dims: " + str(list(fps.values())[0].shape[0]))
        #将每张图片转换成向量
        #进行聚类
        print("clustering ...")
        logger_kmeans.info("clustering ...")
        clusters = ic.cluster_kmeans(fps, n_clusters=n_clusters)
        if links:
            pp.make_links_v2(clusters, pj(imagedir, ic_base_dir, 'clusters'))
    except Exception as e:
        logger_kmeans.error(e)

