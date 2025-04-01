from collections import defaultdict
from src.vars import *
from utility.usercustom import UserCustom

# 결과 경로들을 저장할 전역 리스트
result_paths = []

def dfs_setup():
    global word_list, word_graph, priority_map, user_custom_map
    print("priority_map: ", priority_map)
    # 혹시 기존에 user_custom_map이 남아있다면 초기화
    user_custom_map.clear()
    # priority_map을 기반으로 user_custom_map 초기화
    for key, value in priority_map.items():
        user_custom_map.append(UserCustom(None, None, key[0], key[1], value))
    print("user_custom_map: ", user_custom_map)

def apply_user_custom_rules(node, visited, graph):
    """
    1) 먼저 모든 규칙에 대해 '필승'(blue), '필패'(red) 색칠만 적용.
    2) 이후 우선순위(priority_map)에 따라 unvisited 후보들을 한 번만 정렬.
    """

    # ========== (1) 색칠(필승/필패) 먼저 적용 ==========
    for rule in user_custom_map:
        # 조건 확인
        if (rule.A_exist is None or rule.A_exist not in visited) \
           and (rule.A_None is None or rule.A_None in visited):

            # rule.B_start / rule.B_end 조건에 맞는 후보(아직 방문 안 한)
            unvisited_candidates = [
                n for n in graph[node]
                if n not in visited
                and n.name.startswith(rule.B_start)
                and n.name.endswith(rule.B_end)
            ]
            # 색칠 처리
            if rule.C_option == "필승":
                for candidate in unvisited_candidates:
                    candidate.color = "blue"
            elif rule.C_option == "필패":
                for candidate in unvisited_candidates:
                    candidate.color = "red"
            # 숫자(int)인 경우(우선순위)는 여기서는 정렬하지 않고, 일단 패스
            # 정렬은 마지막에 한 번만 수행

    # ========== (2) 우선순위 정렬은 마지막에 한 번만 실행 ==========
    def sort_candidates(candidates):
        prioritized = []
        non_prioritized = []
        for candidate in candidates:
            key = (candidate.name[0], candidate.name[-1])
            if key in priority_map:
                # priority_map[key]가 작을수록 더 높은 우선순위
                prioritized.append((priority_map[key], candidate))
            else:
                non_prioritized.append(candidate)

        # priority_map 값이 작은 순 → 이름 순으로 오름차순 정렬
        prioritized.sort(key=lambda x: (x[0], x[1].name))
        return [cand for _, cand in prioritized] + non_prioritized

    # 현재 노드의 unvisited 후보들을 한 번에 정렬
    unvisited_all = [n for n in graph[node] if n not in visited]
    sorted_candidates = sort_candidates(unvisited_all)
    visited_or_not_candidates = [n for n in graph[node] if n in visited or n not in unvisited_all]

    # 최종적으로 정렬된 후보들 + 나머지를 합쳐서 그래프에 반영
    graph[node] = sorted_candidates + visited_or_not_candidates

    return graph

def dfs_stream(graph, visited, path, node):
    # DFS 함수에 처음 진입할 때(즉, path가 비어있을 때)만 시작 경로를 출력
    if not path:
        yield f"DFS 시작 경로: [{node.name}]\n"

    if node in visited:
        return

    visited.add(node)
    path.append(node)

    # 만약 노드가 'blue'라면 경로를 result_paths에 저장하고 탐색 중단
    if node.color == "blue":
        result_paths.append(path.copy())
        path.pop()
        visited.remove(node)
        return

    # 규칙 적용(색칠 + 우선순위 정렬)
    graph = apply_user_custom_rules(node, visited, graph)

    # 정렬된 순서대로 unvisited인 이웃 노드들 확인
    unvisited_neighbors = [neighbor for neighbor in graph[node] if neighbor not in visited]

    # 만약 방문할 후보가 없다면 경로를 결과에 추가
    if not unvisited_neighbors:
        result_paths.append(path.copy())
        path.pop()
        visited.remove(node)
        return

    # 후보 중에 하나라도 'red'가 있으면 거기서도 경로 종료
    if any(neighbor.color == "red" for neighbor in unvisited_neighbors):
        result_paths.append(path.copy())
        path.pop()
        visited.remove(node)
        return

    # 'red'가 아닌 후보들만 DFS 진행
    for neighbor in unvisited_neighbors:
        if neighbor.color != "red":
            yield from dfs_stream(graph, visited, path, neighbor)

    path.pop()
    visited.remove(node)

def find_with_dfs(requested_word):
    yield f"요청 단어: {requested_word}\n"
    # 매번 결과 경로 초기화
    result_paths.clear()
    # DFS 세팅
    dfs_setup()

    # requested_word로 시작하는 word를 찾아 DFS 시작
    for word in word_list:
        if word.name == requested_word:
            yield from dfs_stream(word_graph, set(), [], word)
            break

    # 결과 경로 정리
    final_paths = [[n.name for n in path] for path in result_paths]
    yield f"탐색 결과 경로: {final_paths}\n"

    # 경로 길이에 따른 최종 결과 판단
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
