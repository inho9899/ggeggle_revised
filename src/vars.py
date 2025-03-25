from collections import defaultdict

class Node:
    def __init__(self, word):
        self.word = word
        self.color = 'white'
    def __repr__(self):
        return self.word
    

word_list = []
word_graph = defaultdict(list)
priority_map = {}
user_custom_map = {}