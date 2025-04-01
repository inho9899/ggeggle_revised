import gradio as gr
from src.vars import *

# button_confirm_word_rank.click(fn = confirm_word_rank ,inputs = (button_confirm_word_rank, word_rank_input), outputs=UI_add_word_rank)

def confirm_word_rank(word_rank_input_value, prev_word_list):
    res = ""
    try:
        lines = word_rank_input_value.strip().split("\n")
        for line in lines:
            if not line or ":" not in line:
                raise Exception("Invalid format")
            start_part, rest_part = line.split(":", 1)
            start = start_part.strip()
            tokens = rest_part.strip().split()
            # tokens 예시: ["권", "1", "식", "100", ...]
            for i in range(0, len(tokens), 2):
                end = tokens[i]
                priority = int(tokens[i + 1])
                # priority_map이 전역 혹은 외부에 정의되어 있다고 가정
                priority_map[(start, end)] = priority
            res += line + "\n\n"
        updated_result = prev_word_list + res
        return gr.update(visible = False), updated_result
    
    except Exception as e:
        print("Error:", e)
        return prev_word_list


    
def sort_candidates(candidates):
    prioritized = []
    non_prioritized = []
    for node in candidates:
        key = (node.word[0], node.word[-1])
        if key in priority_map:
            prioritized.append((priority_map[key], node))
        else:
            non_prioritized.append(node)
    # 우선순위가 지정된 후보는 우선순위 값과 단어 알파벳 순으로 정렬
    prioritized.sort(key=lambda x: (x[0], x[1].word))
    # non_prioritized는 원래 순서를 유지 (또는 sorted(non_prioritized, key=lambda x: x.word))
    return [node for _, node in prioritized] + non_prioritized
