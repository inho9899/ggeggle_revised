import gradio as gr
from utility.wordrank import *

def create_word_rank_ui():
    with gr.Blocks() as UI_add_word_rank:
        hidden_ui_data = gr.State("")
        with gr.Column(visible=False) as container:
            gr.Markdown("### 글자순위 추가 영역")
            word_rank_input = gr.Textbox(
                label="글자 입력",
                placeholder="예시) 가 : 각 1 그 3 트 10",
                lines=3
            )
            with gr.Row():
                with gr.Column(scale=1):
                    button_confirm_word_rank = gr.Button(value="추가")
                with gr.Column(scale=1):
                    button_cancel_word_rank = gr.Button(value="취소")
            gr.Markdown('---')
    
    # 버튼 클릭 시 UI_add_word_rank 영역을 숨기도록 이벤트 등록
    button_cancel_word_rank.click(
        lambda: gr.update(visible=False),
        outputs=UI_add_word_rank
    )
    
    # Now pass the hidden state as input instead of the column.
    button_confirm_word_rank.click(
        fn=confirm_word_rank, 
        inputs=[word_rank_input, hidden_ui_data], 
        outputs= [UI_add_word_rank]
    )

    # 필요한 컴포넌트를 반환합니다.
    return UI_add_word_rank, word_rank_input, button_confirm_word_rank, button_cancel_word_rank
