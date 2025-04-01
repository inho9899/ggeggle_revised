# textinput.py
from src.vars import word_list, word_graph, Node
from collections import defaultdict


def read_input_data(uploaded_file):
    global word_list, word_graph
    word_list.clear()
    word_graph.clear()

    try :
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
    
    except Exception as e:
        return ""