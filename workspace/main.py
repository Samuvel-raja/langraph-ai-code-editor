import sys
from langraph import Langraph

def main():
    graph = Langraph()
    graph.add_node('A')
    graph.add_node('B')
    graph.add_edge('A', 'B')
    print(graph)

if __name__ == '__main__':
    main()