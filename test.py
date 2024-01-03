import networkx as nx
import matplotlib.pyplot as plt
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

class MyTopo(Topo):
    def build(self):
        # 添加主机和交换机
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')

        # 添加链接
        self.addLink(h1, s1)
        self.addLink(h2, s1)

if __name__ == '__main__':
    topo = MyTopo()
    net = Mininet(topo)

    # 启动网络
    net.start()

    # 实时获取拓扑图信息
    while True:
        # 创建一个有向图
        G = nx.DiGraph()

        # 添加节点
        for node in net.topo.get_nodes():
            G.add_node(node)

        # 添加边缘
        for link in net.topo.get_links():
            G.add_edge(link[0], link[1])

        # 清空之前的绘图
        plt.clf()

        # 绘制拓扑图
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, with_labels=True)

        # 展示拓扑图
        plt.axis('off')
        plt.pause(1)  # 暂停1秒钟
        plt.show(block=False)

        # 检查是否要退出循环
        if input("按Enter键继续，输入q退出：") == 'q':
            break

    # 停止网络
    net.stop()
