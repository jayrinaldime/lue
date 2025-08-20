import gradio as gr
from openai import OpenAI
import tempfile
from pathlib import Path
state = 0

texts = [""]

def on_play(p):
    if p == "Play":
        return "Stop", {"is_playing":True}
    else:
        return "Play", {"is_playing":False}

def text_display(state, texts):
    r = [(s + "\n", "-" if i == state else None) for i, s in enumerate(texts)]
    return r

def get_current_text():
    global state, texts
    current_text = texts[state]
    display_text = text_display(state, texts)
    state+=1
    if state >= len(texts):
        state = 0


    return current_text, display_text
def on_play_state_changed(play_state):
    global state
    if play_state["is_playing"]:
        t = tempfile.gettempdir()
        d = Path(t)/ f"{state}.mp3"
        text, display_text = get_current_text()
        client = OpenAI(base_url="http://", api_key="1234")
        response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="msa.en-US.BrianMultilingual",
                input=text,
                response_format="mp3",
            )

        # Stream the audio response directly to the file
        response.stream_to_file(str(d))
        return str(d), display_text
    else:
        return None, None
def main():
    with gr.Blocks(title="Lue") as ui:
        p = gr.Button("Play")
        play_state = gr.State({"is_playing":False,})
        p.click(on_play, inputs=[p], outputs=[p,play_state])
        audio_out = gr.Audio(label = "TTS", streaming=True, autoplay=True, show_share_button=False, show_download_button=False, visible=True)
        t2 = gr.HighlightedText(
            label="Hey",
            combine_adjacent=False,
            show_inline_category=False,
            show_legend=False,
            color_map={"+": "red", "-": "green"})
        #t.tick(on_text_change, inputs=[t], outputs=t2)
        play_state.change(on_play_state_changed, inputs=[play_state], outputs=[audio_out, t2])
        audio_out.stop(on_play_state_changed, inputs=[play_state], outputs=[audio_out, t2])

    ui.launch(share=False)

if __name__=="__main__":
    main()