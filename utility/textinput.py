from src.vars import Node, word_list, word_graph
from collections import defaultdict


def read_input_data(uploaded_file):
    with open(uploaded_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            node = Node(line.strip())
            word_list.append(node)

    tmp = defaultdict(list)
    for word in word_list:
        tmp[word.name[0]].append(word)

    for word in word_list:
        word_graph[word] = tmp[word.name[-1]]

    return len(lines)
