from collections import defaultdict
from src.vars import *
from utility.usercustom import UserCustom

# 결과 경로들을 저장할 전역 리스트
result_paths = []

def dfs_setup():
    global word_list, word_graph, priority_map, user_custom_map
    # priority_map을 기반으로 user_custom_map 초기화
    for key, value in priority_map.items():
        user_custom_map.append(UserCustom(None, None, key[0], key[1], value))

def apply_user_custom_rules(node, visited, graph):
    def sort_candidates(candidates):
        prioritized = []
        non_prioritized = []
        for candidate in candidates:
            key = (candidate.name[0], candidate.name[-1])
            if key in priority_map:
                prioritized.append((priority_map[key], candidate))
            else:
                non_prioritized.append(candidate)
        # 우선순위가 지정된 후보는 우선순위 값과 알파벳 순으로 정렬
        prioritized.sort(key=lambda x: (x[0], x[1].name))
        return [candidate for _, candidate in prioritized] + non_prioritized

    for rule in user_custom_map:
        if (rule.A_exist == "" or rule.A_exist not in visited) and (rule.A_None == "" or rule.A_None in visited):
            unvisited_candidates = [
                n for n in graph[node]
                if n not in visited and n.name.startswith(rule.B_start) and n.name.endswith(rule.B_end)
            ]
            if rule.C_option == "필승":
                for candidate in unvisited_candidates:
                    candidate.color = "blue"
            elif rule.C_option == "필패":
                for candidate in unvisited_candidates:
                    candidate.color = "red"
            elif isinstance(rule.C_option, int):
                sorted_candidates = sort_candidates(unvisited_candidates)
                rest_candidates = [n for n in graph[node] if n in visited or n not in unvisited_candidates]
                graph[node] = sorted_candidates + rest_candidates
    return graph

def dfs_stream(graph, visited, path, node):
    # DFS 함수에 처음 진입할 때(즉, path가 비어있을 때)만 시작 경로를 출력
    if not path:
        yield f"DFS 시작 경로: [{node.name}]\n"
        
    if node in visited:
        return

    visited.add(node)
    path.append(node)

    if node.color == "blue":
        result_paths.append(path.copy())
        path.pop()
        visited.remove(node)
        return

    graph = apply_user_custom_rules(node, visited, graph)
    unvisited_neighbors = [neighbor for neighbor in graph[node] if neighbor not in visited]

    if not unvisited_neighbors:
        result_paths.append(path.copy())
        path.pop()
        visited.remove(node)
        return

    if any(neighbor.color == "red" for neighbor in unvisited_neighbors):
        result_paths.append(path.copy())
        path.pop()
        visited.remove(node)
        return

    for neighbor in unvisited_neighbors:
        if neighbor.color == "red":
            continue
        yield from dfs_stream(graph, visited, path, neighbor)

    path.pop()
    visited.remove(node)

def find_with_dfs(requested_word):
    yield f"요청 단어: {requested_word}\n"
    dfs_setup()
    for word in word_list:
        if word.name == requested_word:
            yield from dfs_stream(word_graph, set(), [], word)
            break
    final_paths = [[n.name for n in path] for path in result_paths]
    yield f"탐색 결과 경로: {final_paths}\n"
    if result_paths:
        lengths = [len(path) for path in result_paths]
        if all(l % 2 == 1 for l in lengths):
            yield "최종 결과: 필승\n"
        elif all(l % 2 == 0 for l in lengths):
            yield "최종 결과: 필패\n"
        else:
            yield "최종 결과: 미정\n"
    else:
        yield "최종 결과: 필패\n"
