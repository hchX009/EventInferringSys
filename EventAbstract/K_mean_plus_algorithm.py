# /usr/bin/env python3
# coding: utf-8
# File: K_mean_plus_algorithm.py
# Author: hchX009
# python 3.5

import numpy
import math
import random


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
        self.points = dict()

    def add_point(self, p):
        self.points[p] = 1

    def remove_point(self, p):
        if self.points[p]:
            del self.points[p]

    # 更新类中心
    def update_center(self):
        if len(self.points) == 0:
            return
        sum_vect = [0] * len(self.center)
        for p in self.points.keys():
            sum_vect = numpy.add(sum_vect, p.data)
        self.center = numpy.divide(sum_vect, len(self.points))


# K-mean++算法实现
class Kmeanplusplus():
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

    # 初始化中心点
    def init_centers(self):
        # 随机初始化中心
        new_cluster_index = int(random.random() * self.num_point)
        token = [1] * self.num_point
        dist_squ_sum = 0.0
        token[new_cluster_index] = 0

        seed_cluster = Cluster(self.dataset[new_cluster_index])
        self.clusters.append(seed_cluster)
        new_cluster = seed_cluster

        for i in range(self.num_point):
            point = self.points[i]
            dist = point.compute_euclidean_distance(new_cluster.center)
            point.set_cluster(new_cluster, dist)
            if token[i]:
                dist_squ_sum += math.pow(dist, 2)
        k = 1
        while k < self.num_cluster:
            # 随机选择一个点作为新的中心
            rdist = random.random() * (dist_squ_sum / self.num_point)
            new_cluster_index = -1
            tmp = 0
            for i in range(self.num_point):
                tmp += self.points[i].get_dist()
                if tmp >= rdist:
                    new_cluster_index = i
                    break
            new_cluster = Cluster(self.dataset[new_cluster_index])
            self.clusters.append(new_cluster)
            k += 1
            dist_squ_sum = 0.0

            # 更新点与类中心的欧式距离
            for i in range(self.num_point):
                point = self.points[i]
                if token[i]:
                    dist = point.compute_euclidean_distance(new_cluster.center)
                    if dist < point.get_dist():
                        point.set_cluster(new_cluster, dist)
                    dist_squ_sum += math.pow(point.get_dist(), 2)
            token[new_cluster_index] = 0

    # 分配点到不同的类
    def assign_point_cluster(self, point):
        min_dist = point.get_dist()
        p_cluster = point.cluster
        flag = 0
        for cluster in self.clusters:
            dist = point.compute_euclidean_distance(cluster.center)
            if dist < min_dist:
                p_cluster = cluster
                min_dist = dist
                flag = 1
        if flag:
            point.set_cluster(p_cluster, min_dist)
        return flag

    def do_cluster(self, numiter):
        # 随机生成类中心
        self.init_centers()

        for i in range(numiter):
            flag = 0
            # E step % update the center for each cluster
            for cluster in self.clusters:
                cluster.update_center()

            # M step % assign the point to the newest cluster
            for point in self.points:
                flag += self.assign_point_cluster(point)

            if (flag == 0):
                break


if __name__ == "__main__":
    dataset = [[1, 1], [2, 3], [-1, 4], [5, 2], [-3, -7], [4, -2], [4, 2], [3, 3], [-2, 3], [-5, -3], [2, 5], [1, -2], [3, 0], [0, 0], [1, 6], [1, 7]]
    kmean = Kmeanplusplus(dataset, 6)
    kmean.do_cluster(1000)
    for cluster in kmean.clusters:
        print("============")
        print("cluster:")
        print(cluster.center)
        for point in cluster.points:
            print(point.data)
