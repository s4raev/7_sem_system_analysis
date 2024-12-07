import csv
from io import StringIO
from collections import defaultdict

csv_data = """1,2
1,3
3,4
3,5""" 


def parse_csv_to_graph(var: str):
    graph = defaultdict(list)
    reader = csv.reader(var.splitlines())
    for row in reader:
        if len(row) == 2:
            parent, child = int(row[0]), int(row[1])
            graph[parent].append(child)
    return graph

def count_all_descendants(graph, node):
    count = 0
    for child in graph[node]:
        count += 1
        count += count_all_descendants(graph, child)
    return count

def count_all_ancestors(graph, node):
    count = 0
    for parent in graph:
        if node in graph[parent]:
            count += 1
            count += count_all_ancestors(graph, parent)  
    return count

def main(var: str) -> str:
    graph = parse_csv_to_graph(var)
    print(graph)

    result = []
    nodes = set(graph.keys()).union(*graph.values())
    for node in nodes:
        r1 = len(graph[node])
        r2 = len([parent for parent in graph if node in graph[parent]])
        r3 = count_all_descendants(graph, node) - r1
        r4 = count_all_ancestors(graph, node) -  r2
        r5 = sum(len(graph[parent]) - 1 for parent, children in graph.items() if node in children)

        result.append([node, r1, r2, r3, r4, r5])

    csv_string = StringIO()
    csv.writer(csv_string).writerows(result)
    return csv_string.getvalue().strip()

if __name__ == "__main__":
    res = main(csv_data)
    print(res)