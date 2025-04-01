import gradio as gr

def input_user_custom_ui() :
    A_exist = gr.Textbox(label="~이(가) 있고", placeholder="예시) 가족", lines=1)
    A_None = gr.Textbox(label="~이(가) 제외된 경우", placeholder="예시) 회사", lines=1)
    B_start = gr.Textbox(label="~로 시작하고", placeholder="예시) 가", lines=1)
    B_end = gr.Textbox(label="~로 끝나는 모든 단어는", placeholder="예시) 수", lines=1)
    C_option = gr.Textbox(label="필승, 필패, 글자 계산 우선순위에서 숫자 N으로 계산", placeholder="예시) 필승, 필패, 10", lines=1)
    return A_exist, A_None, B_start, B_end, C_option


def create_user_custom_ui():
    # 이 함수는 유저 커스텀 영역 UI와 관련된 컴포넌트를 생성합니다.
    with gr.Blocks() as UI_show_user_custom:
        # container를 별도로 반환하기 위해 inner container 사용
        with gr.Column(visible=False) as container:
            gr.Markdown("### 유저 커스텀 추가 영역")
            A_exist, A_None, B_start, B_end, C_option = input_user_custom_ui()
            with gr.Row():
                with gr.Column(scale=1):
                    button_confirm_user_custom = gr.Button(value="추가")
                with gr.Column(scale=1):
                    button_cancel_user_custom = gr.Button(value="취소")
            gr.Markdown('---')

    button_confirm_user_custom.click(lambda: gr.update(visible=False), outputs=container)
    button_cancel_user_custom.click(lambda: gr.update(visible=False), outputs=container)
    
    # 필요한 컴포넌트를 반환합니다.
    return container, button_confirm_user_custom, button_cancel_user_custom, A_exist, A_None, B_start, B_end, C_option
