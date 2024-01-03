# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt

def draw_topology(topo_edges):
    # 创建一个有向图
    G = nx.DiGraph()

    # 根据边缘添加节点和边缘
    for edge in topo_edges:
        src, dest = edge
        G.add_node(src)
        G.add_node(dest)
        G.add_edge(src, dest)

    # 绘制拓扑图
    pos = nx.spring_layout(G)  # 为图形定位节点
    nx.draw_networkx(G, pos, with_labels=True)

    # 展示拓扑图
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    topo_edges = [('h1', 's1'), ('h2', 's1')]  # 定义边缘
    draw_topology(topo_edges)
