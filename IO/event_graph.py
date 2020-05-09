# /usr/bin/env python3
# coding: utf-8
# File: event_graph.py
# Author: hchX009
# python 3.5


# 构造显示图谱页面
import os


class CreatePage:
    Event_Graph_HTML_FILE = os.path.join(
        os.path.abspath(os.path.dirname(os.getcwd())), "Data/event_graph.html")

    def __init__(self):
        self.base = '''
        <html>
        <head>
            <script type="text/javascript" src="VIS/dist/vis.js"></script>
            <link href="VIS/dist/vis.css" rel="stylesheet" type="text/css">
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        </head>
        <body>
            <div id="VIS_draw"></div>
            <script type="text/javascript">
                var nodes = data_nodes;
                var edges = data_edges;
                var container = document.getElementById("VIS_draw");
                var data = {
                    nodes: nodes,
                    edges: edges
                };
                var options = {
                    /*
                    configure:{
                        enabled: true,
                        filter: 'nodes,edges',
                        container: undefined,
                        showButton: true
                    },
                    */
                    nodes: {
                        shape: 'dot',
                        size: 10,
                        font: {
                            size: 5, //字体大小
                        }
                    },
                    edges: {
                        font: {
                            size: 6, //字体大小
                            align: 'middle' //文字位置
                        },
                        color: 'grey',
                        arrows: {
                            to: {enabled: true, scaleFactor: 1}
                        },
                        smooth: {
                            enabled: true,  //是否使用曲线
                            type: 'dynamic'
                        }
                    },
                    physics: {
                        enabled: true
                    }
                };
                var network = new vis.Network(container, data, options);
            </script>
        </body>
    </html>
    '''

    # 生成图数据
    def get_graph_data(self, nodes, edges):
        node_dict = {node: index for index, node in enumerate(nodes)}
        data_nodes = list()
        data_edges = list()
        for node, index in node_dict.items():
            data = dict()
            data["id"] = index
            data["label"] = node
            data_nodes.append(data)
        for edge in edges:
            data = dict()
            data['from'] = node_dict.get(edge[0])
            data['label'] = edge[1]
            data['to'] = node_dict.get(edge[2])
            data_edges.append(data)
        return data_nodes, data_edges

    # 利用图数据生成html文件
    def create_html(self, data_nodes, data_edges):
        fd = open(self.Event_Graph_HTML_FILE, 'w+')
        html = self.base.replace('data_nodes', str(data_nodes)).replace('data_edges', str(data_edges))
        fd.write(html)
        fd.close()


class EventGraph:
    EVENT_RELATIONS_LIST_FILE_NAME = os.path.join(
        os.path.abspath(os.path.dirname(os.getcwd())), "Data/event_relations_list.csv")

    def __init__(self):
        fd = open(self.EVENT_RELATIONS_LIST_FILE_NAME, 'r')
        self.event_triple_sets = fd.readlines()

    # 统计事件频次
    def collect_events_frequence(self):
        relation_dict = dict()
        node_dict = dict()
        for event_triple_set in self.event_triple_sets:
            event_triple = event_triple_set.strip()
            if not event_triple:
                continue
            nodes = event_triple.split(',')
            relation = nodes.pop(1)
            for node in nodes:
                if node not in node_dict:
                    node_dict[node] = 1
                else:
                    node_dict[node] += 1
            if relation not in relation_dict:
                relation_dict[relation] = 1
            else:
                relation_dict[relation] += 1
        return node_dict, relation_dict #relation换成事件

    # 构建事理图谱的节点和边
    def get_graph_nodes_and_edges(self):
        edges = list()
        nodes = list()
        #for event in sorted(event_dict.items(), key=lambda asd: asd[1], reverse=True)[:500]:
        for event_triple_set in self.event_triple_sets:
            event_triple = event_triple_set.strip()
            e1 = event_triple.split(',')[0]
            r = event_triple.split(',')[1]
            e2 = event_triple.split(',')[2]
            #if e1 in node_dict and e2 in node_dict:
            nodes.append(e1)
            nodes.append(e2)
            edges.append([e1, r, e2])
            #else:
            #    continue
        return nodes, edges

    '''调用VIS插件,进行事件图谱展示'''
    def show_graph(self, edges, nodes):
        handler = CreatePage()
        #data_nodes, data_edges = handler.collect_data(nodes, edges)
        #handler.create_html(data_nodes, data_edges)


if __name__ == "__main__":
    t = EventGraph()
    a, b = t.get_graph_nodes_and_edges()
    c, d = t.collect_events_frequence()
    print(c)
    print(d)
    q = CreatePage()
    e, f = q.get_graph_data(a, b)
    print(e)
    print(f)
    q.create_html(e, f)