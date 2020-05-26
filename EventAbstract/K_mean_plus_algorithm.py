# /usr/bin/env python3
# coding: utf-8
# File: K_mean_plus_algorithm.py
# Author: hchX009
# python 3.5

import numpy
import math
import random
import collections


class Kmean:
    def __init__(self):
        pass

    def do_cluster(self, mintoler, numiter):
        pass

# 多维向量点类
class Point:
    def __init__(self, data):
        self.data = data
        self.cluster = None
        self.center_dist = 1e5

    # 计算与中心的欧式距离
    def compute_euclidean_distance(self, center):
        if len(self.data) != len(center):
            return
        return math.sqrt(sum(numpy.power((numpy.subtract(self.data, center)), 2)))

    # 设置点所在的类
    def set_cluster(self, new_cluster, new_center_dist):
        # 如果该点已经被分配，则在那个类中去除该点
        if self.cluster:
            self.cluster.remove_point(self)
        # 得到新的类
        self.cluster = new_cluster
        # 在新类中添加该点
        self.cluster.add_point(self)
        # 更新与中心距离
        self.center_dist = new_center_dist

    def get_dist(self):
        return self.center_dist

    def set_dist(self, new_center_dist):
        self.center_dist = new_center_dist


# 分类操作的类
class Cluster:
    def __init__(self, center):
        self.center = center

        self.points = collections.defaultdict(lambda: 0)

    def add_point(self, p):
        self.points[p] = 1

    def remove_point(self, p):
        if self.points[p]:
            del self.points[p]

    # 更新类中心
    def update_center(self):
        if (len(self.points) == 0):
            return
        sum_vect = [0] * len(self.center)
        for p in self.points.keys():
            sum_vect = numpy.add(sum_vect, p.data)
        self.center = numpy.divide(sum_vect, len(self.points))


class Kmeanplusplus(Kmean):
    def __init__(self, dataset, num_cluster):
        self.dataset = dataset
        self.num_point = len(dataset)
        self.num_cluster = num_cluster
        self.points = list()
        self.clusters = list()
        # 将数据构成点集装入points中
        for i in range(self.num_point):
            point = Point(dataset[i])
            self.points.append(point)
# ===
    def init_centers(self):
        # 随机初始化中心
        new_cluster_index = int(random.random() * self.num_point)
        token = [1] * self.num_point
        dist_squ_sum = 0.0
        token[new_cluster_index] = 0

        # ===
        seed_cluster = Cluster(self.dataset[new_cluster_index])
        self.clusters.append(seed_cluster)
        new_cluster = seed_cluster
        for i in range(self.numPoint):
            point = self.points[i]
            dist = point.compute_euclidean_distance(new_cluster.center)
            point.set_cluster(new_cluster, dist)
            if (token[i]):
                dist_squ_sum += math.pow(dist, 2)
        k = 1
        while (k < self.numCluster):
            # random to select a point as the center of a new cluster
            rdist = random.random() * dist_squ_sum
            new_cluster_index = -1
            tmp = 0
            for i in range(self.numPoint):
                tmp += self.points[i].get_dist()
                if (tmp >= rdist):
                    new_cluster_index = i

            new_cluster = Cluster(self.dataset[new_cluster_index])
            self.clusters.append(new_cluster);
            k += 1
            dist_squ_sum = 0.0
            # update the euclidean distance between the point and its newest center
            for i in range(self.numPoint):
                point = self.points[i]
                if (token[i]):
                    dist = point.compute_euclidean_distance(new_cluster.center)
                    if (dist < point.get_dist()):
                        point.set_cluster(new_cluster, dist)
                    dist_squ_sum += math.pow(point.get_dist(), 2)

            token[new_cluster_index] = 0

    def assign_point_cluster(self, point):
        mindist = point.get_dist()
        cluster = point.cluster
        change = 0
        for c in self.clusters:
            dist = point.compute_euclidean_distance(c.center)
            if (dist < mindist):
                cluster = c
                mindist = dist
                change = 1
        if change:
            point.set_cluster(cluster, mindist)
        return change

    def do_cluster(self, numiter):
        # Select the initial cluster center randomly
        self.init_centers();

        for i in range(numiter):
            change = 0
            # E step % update the center for each cluster
            for cluster in self.clusters:
                cluster.update_center()

            # M step % assign the point to the newest cluster
            for point in self.points:
                change += self.assign_point_cluster(point)

            if (change == 0):
                break


if __name__ == "__main__":
    pass
