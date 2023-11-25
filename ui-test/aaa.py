import uuid

import gradio as gr

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])


    def respond(message, chat_history):
        bot_message = ["你好", ("1.webp", (str(uuid.UUID.bytes))), ("111.wav", (str(uuid.UUID.bytes)))]
        for i, e in enumerate(bot_message):
            if i == 0:
                chat_history.append((message, e))
            else:
                chat_history.append((None, e))
        return "", chat_history


    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()
