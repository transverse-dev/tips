
import gradio as gr
import numpy as np

def flip(im):
    
    return np.flipud(im)

with gr.Blocks() as demo:
    with gr.Row():
        input_img = gr.Image(sources=["webcam"])
        output_img = gr.Image()
        input_img.stream(lambda x:flip(x), input_img, output_img)

demo.launch()