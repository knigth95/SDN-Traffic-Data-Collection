import networkx as nx
import matplotlib.pyplot as plt
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import info
from mininet.node import RemoteController

class MyTopo(Topo):
    def build(self):
        # Create an empty network and add nodes to it.
        net = Mininet(controller=RemoteController)

        # Adding controller
        info('*** Adding controller\n')
        net.addController('c0')

        # Adding hosts
        info('*** Adding hosts\n')
        h1 = net.addHost('h1', ip='10.0.0.1')
        h2 = net.addHost('h2', ip='10.0.0.2')
        h3 = net.addHost('h3', ip='10.0.0.3')
        h4 = net.addHost('h4', ip='10.0.0.4')

        # Adding switches
        info('*** Adding switch\n')
        s1 = net.addSwitch('s1')
        s2 = net.addSwitch('s2')
        s3 = net.addSwitch('s3')
        s4 = net.addSwitch('s4')
        s5 = net.addSwitch('s5')
        s6 = net.addSwitch('s6')
        s7 = net.addSwitch('s7')
        s8 = net.addSwitch('s8')
        s9 = net.addSwitch('s9')
        s10 = net.addSwitch('s10')

        # Creating links
        info('*** Creating links\n')
        net.addLink(h1, s10)
        net.addLink(s3, s10)
        net.addLink(s4, s10)
        net.addLink(s1, s3)
        net.addLink(s1, s4)
        net.addLink(s1, s2)
        net.addLink(s1, s6)
        net.addLink(s6, s9)
        net.addLink(s2, s9)
        net.addLink(h2, s9)
        net.addLink(s5, s4)
        net.addLink(s4, s7)
        net.addLink(s5, s7)
        net.addLink(s5, s6)
        net.addLink(s5, s8)
        net.addLink(s6, s8)
        net.addLink(h3, s8)
        net.addLink(h4, s7)

        # Starting network
        info('*** Starting network\n')
        net.start()

        # Running CLI
        info('*** Running CLI\n')
        CLI(net)

        # Stopping network
        info('*** Stopping network\n')
        net.stop()

if __name__ == '__main__':
    topo = MyTopo()
    net = Mininet(topo)

    # Starting network
    net.start()

    # Creating a directed graph
    G = nx.DiGraph()

    while True:
        # Adding nodes
        for node in net.hosts + net.switches:
            G.add_node(node)

        # Adding edges
        for link in net.links:
            G.add_edge(link.intf1.node, link.intf2.node)

        # Clear previous plot
        plt.clf()

        # Draw the network
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, with_labels=True)

        # Show the plot
        plt.axis('off')
        plt.pause(1)
        plt.show(block=False)

        # Check whether to exit the loop
        if input("Press Enter to continue or q to quit: ") == 'q':
            break

    # Stop the network
    net.stop()
