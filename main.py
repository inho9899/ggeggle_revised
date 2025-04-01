import gradio as gr
from utility.usercustom import *
from utility.wordrank import *
from utility.textinput import *
from ui.user_custom_ui import *
from utility.dfs import *

# 전역에서 매니저 인스턴스를 생성합니다.
custom_manager = UserCustomManager()

def process_user_custom_data_class(A_exist, A_None, B_start, B_end, C_option):
    # custom_manager.add_entry()를 통해 누적된 결과를 반환받습니다.
    result = custom_manager.add_entry(A_exist, A_None, B_start, B_end, C_option)
    # UI 영역(컨테이너)는 숨기고, 텍스트박스에는 누적된 결과를 표시합니다.
    return gr.update(visible=False), result

# DFS의 제너레이터 출력들을 모두 모아서 단일 문자열로 반환하는 wrapper 함수
def find_with_dfs_final(requested_word):
    output = []
    for msg in find_with_dfs(requested_word):
        output.append(msg)
    return "".join(output)

# 조건 초기화 함수 정의
def reset_conditions():
    # 글자순위 영역 초기화: 텍스트박스 비우고, 마크다운도 초기화하며, 영역은 숨김 처리
    reset_word_rank_input = gr.update(value="")
    reset_show_word_rank = gr.update(value="")
    reset_UI_add_word_rank = gr.update(visible=False)
    
    # 유저커스텀 영역 초기화: 입력값을 비우고, 마크다운 및 UI 영역도 숨김 처리
    reset_UI_show_user_custom = gr.update(visible=False)
    reset_A_exist = gr.update(value="")
    reset_A_None = gr.update(value="")
    reset_B_start = gr.update(value="")
    reset_B_end = gr.update(value="")
    reset_C_option = gr.update(value="")
    reset_show_user_custom = gr.update(value="")
    
    return (reset_word_rank_input, reset_show_word_rank, reset_UI_add_word_rank,
            reset_UI_show_user_custom, reset_A_exist, reset_A_None, reset_B_start,
            reset_B_end, reset_C_option, reset_show_user_custom)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=3):
            upload_file = gr.File(show_label=False, file_types=[".txt"])
            show_file = gr.Text(label="입력된 단어수")
            upload_file.change(fn=read_input_data, inputs=upload_file, outputs=show_file)

            # 글자순위 추가 영역
            with gr.Blocks():
                with gr.Column(visible=False) as UI_add_word_rank:
                    gr.Markdown("### 글자순위 추가 영역")
                    word_rank_input = gr.Textbox(label="글자 입력", 
                                                 placeholder="예시) 가 : 각 1 그 3 트 10", 
                                                 lines=3)
                    with gr.Row():
                        with gr.Column(scale=1):
                            button_confirm_word_rank = gr.Button(value="추가")
                        with gr.Column(scale=1):
                            button_cancel_word_rank = gr.Button(value="취소")
                    gr.Markdown('---')
                button_cancel_word_rank.click(lambda: gr.update(visible=False), outputs=UI_add_word_rank)

            # 유저 커스텀 추가 영역 (ui/user_custom_ui.py에 정의한 함수)
            UI_show_user_custom, button_confirm_user_custom, button_cancel_user_custom, \
                A_exist, A_None, B_start, B_end, C_option = create_user_custom_ui()

            with gr.Row():
                with gr.Column(scale=1):
                    button_add_word_rank = gr.Button(value="글자순위추가")
                with gr.Column(scale=1):
                    button_add_user_custom = gr.Button(value="유저커스텀추가")
                
            with gr.Row():
                with gr.Column(scale=1):
                    word_input = gr.Textbox(label="시작단어", elem_id="start_word")
                with gr.Column(scale=1):
                    button_find_with_dfs = gr.Button(value="탐색시작", elem_id="start_button")
            
            # 조건 초기화 버튼 추가
            with gr.Row():
                button_reset_conditions = gr.Button(value="조건 초기화")

        with gr.Column(scale=2):
            gr.Markdown('### 글자순위표')
            with gr.Blocks():
                show_word_rank = gr.Markdown()
            gr.Markdown('---')

            gr.Markdown('### 유저커스텀목록표')
            with gr.Blocks():
                show_user_custom = gr.Markdown()
            gr.Markdown('---')
            dfs_result = gr.Textbox(label="탐색결과")

    # 글자순위 추가 버튼 이벤트 (기존 함수 사용)
    button_confirm_word_rank.click(
        fn=confirm_word_rank, 
        inputs=[word_rank_input, gr.State("")],
        outputs=[UI_add_word_rank, show_word_rank]
    )

    # 각 영역을 보이도록 업데이트하는 버튼 이벤트
    button_add_word_rank.click(lambda: gr.update(visible=True), outputs=UI_add_word_rank)
    button_add_user_custom.click(lambda: gr.update(visible=True), outputs=UI_show_user_custom)
    
    # 유저 커스텀 추가 버튼 클릭 시, 클래스를 활용해 데이터를 누적
    button_confirm_user_custom.click(
        fn=process_user_custom_data_class,
        inputs=[A_exist, A_None, B_start, B_end, C_option],
        outputs=[UI_show_user_custom, show_user_custom]
    )

    # 탐색시작 버튼 이벤트: 스트리밍 대신 wrapper 함수를 사용하여 최종 결과를 반환
    button_find_with_dfs.click(
         fn=find_with_dfs_final,
         inputs=word_input,
         outputs=dfs_result
    )

    # 조건 초기화 버튼 이벤트: 리셋 함수 호출하여 컴포넌트 초기화
    button_reset_conditions.click(
        fn=reset_conditions,
        inputs=[],
        outputs=[word_rank_input, show_word_rank, UI_add_word_rank, UI_show_user_custom,
                 A_exist, A_None, B_start, B_end, C_option, show_user_custom]
    )

    # Add custom CSS to style the elements
    demo.css = """
    #start_button {
        background-color: #ffe400;
    }
    """

if __name__ == "__main__":
    demo.launch()
