import gradio as gr
from currans_idea.api import app as fastapi_app
from currans_idea.engine import CurransIdeaEngine

engine = CurransIdeaEngine()

def simulate_ui(post_text):
    if not post_text.strip():
        return "Inserisci il testo di un post o evento."
    reactions = engine.simulate_mock_reactions(post_text)
    out = []
    for r in reactions:
        out.append(f"[+{r['delay_seconds']}s] {r['persona_name']}:\n   > {r['message']}\n")
    return "\n".join(out)

def thread_ui(post_text):
    if not post_text.strip():
        return "Inserisci il testo di un post o evento."
    thread = engine.simulate_thread(post_text)
    out = []
    for t in thread:
        reply_info = f" (in risposta a #{t['in_reply_to_id']} {t['in_reply_to_persona']})" if t['in_reply_to_id'] else " (Post Canale)"
        out.append(f"[#{t['id']} | +{t['delay_seconds']}s]{reply_info} {t['persona_name']}:\n   > {t['message']}\n")
    return "\n".join(out)

with gr.Blocks(title="Humans as Curran's Idea") as demo:
    gr.Markdown("# ⚽ Humans as Curran's Idea — Live Playground & API")
    gr.Markdown("Motore comportamentale ed euristico per commenti realistici Telegram (calibrato su oltre 45k messaggi reali).")
    gr.Markdown("📖 **REST API Docs:** Visita [`/docs`](/docs) per testare direttamente gli endpoint REST.")

    with gr.Tab("💬 Reazioni dei 5 Archetipi"):
        input_post = gr.Textbox(
            label="Incolla il Post del Canale",
            lines=4,
            value="GOAL! ⚽️ Lautaro Martinez 👟 Barella ⏱️ 34' Inter 🆚 Milan #SerieA"
        )
        btn = gr.Button("Simula Reazioni", variant="primary")
        output_reactions = gr.Textbox(label="Risposte Simulate con Delay", lines=10)
        btn.click(fn=simulate_ui, inputs=[input_post], outputs=[output_reactions])

    with gr.Tab("🧵 Thread Multi-Turno (Discussione Bot-to-Bot)"):
        input_thread = gr.Textbox(
            label="Incolla il Post del Canale",
            lines=4,
            value="GOAL! ⚽️ Vlahovic ⏱️ 89' Juventus 🆚 Napoli"
        )
        btn_thread = gr.Button("Genera Discussione a Catena", variant="primary")
        output_thread = gr.Textbox(label="Discussione nei Commenti", lines=10)
        btn_thread.click(fn=thread_ui, inputs=[input_thread], outputs=[output_thread])

app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
