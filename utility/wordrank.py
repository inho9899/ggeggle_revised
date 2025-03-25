import gradio as gr

def confirm_word_rank(button_value, word_rank_input_value):
    print("Button clicked:", button_value)
    print("Word rank input:", word_rank_input_value)
    return f"입력된 글자순위: {word_rank_input_value}"
