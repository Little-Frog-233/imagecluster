#coding:utf-8
'''
使用层次聚类或者kmeans聚类
'''
from imagecluster import main


# main.main_hierarchy('/imagecluster/test/dog/', sim=0.65, max_csize=10, pca=True)

main.main_kmeans('imagecluster/test/dog/', n_clusters=3, pca=True)
