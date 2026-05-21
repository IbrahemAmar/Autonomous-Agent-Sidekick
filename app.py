import gradio as gr
from sidekick import Sidekick



def award_xp(amount: int, reason: str = ""):
    # If you aren't using the database/leaderboard for now, 
    # just print to terminal to avoid the error.
    print(f"DEBUG: Awarding {amount} XP for: {reason}")

async def setup():
    sidekick = Sidekick()
    try:
        await sidekick.setup()
    except Exception as e:
        print(f"Sidekick setup failed: {e}")
        raise gr.Error(
            f"Failed to start Sidekick: {e}. "
            "Check your .env API keys and that Playwright is installed (run: playwright install chromium)."
        ) from e
    return sidekick


async def ensure_sidekick(sidekick):
    if sidekick is not None:
        return sidekick
    return await setup()


async def process_message(sidekick, message, success_criteria, history):
    sidekick = await ensure_sidekick(sidekick)
    try:
        results = await sidekick.run_superstep(message, success_criteria, history)
    except Exception as e:
        print(f"run_superstep failed: {e}")
        raise gr.Error(f"Sidekick failed while processing your request: {e}") from e
    return results, sidekick


async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", None, new_sidekick


def free_resources(sidekick):
    print("Cleaning up")
    try:
        if sidekick:
            sidekick.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Sidekick Personal Co-Worker")
    sidekick = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300)
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Sidekick")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success critiera?"
            )
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")

    ui.load(setup, [], [sidekick])
    message.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    success_criteria.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    go_button.click(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])


ui.launch(inbrowser=True)
