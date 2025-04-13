import gradio as gr
from interviewer import Interviewer
from openrouter_utils import ask_llm
from whisper_transcriber import transcribe_audio
from history_db import init_db, store_history, get_history

interviewer = Interviewer("questions.json")

def calculate_stars(score):
    if score >= 90:
        return 5
    elif score >= 75:
        return 4
    elif score >= 60:
        return 3
    elif score >= 45:
        return 2
    elif score >= 30:
        return 1
    else:
        return 0

def get_badge(score):
    if score >= 90:
        return "🏆 Gold Badge"
    elif score >= 75:
        return "🥈 Silver Badge"
    elif score >= 60:
        return "🥉 Bronze Badge"
    return "❌ No Badge"

# def format_history_html():
#     rows = get_history()
#     table = "<table border='1' style='width:100%; border-collapse: collapse;'>"
#     table += "<tr><th>Question</th><th>Your Answer</th><th>Correct</th><th>Difficulty</th></tr>"
#     for q, a, correct, diff in rows:
#         table += f"<tr><td>{q}</td><td>{a}</td><td>{'✅' if correct else '❌'}</td><td>{diff}</td></tr>"
#     table += "</table>"
#     return table
def format_history_html():
    rows = get_history()
    rows = rows[-10:][::-1]  # Get last 10 entries, then reverse the order
    table = "<table border='1' style='width:100%; border-collapse: collapse;'>"
    table += "<tr><th>Question</th><th>Your Answer</th><th>Correct</th><th>Difficulty</th></tr>"
    for q, a, correct, diff in rows:
        table += f"<tr><td>{q}</td><td>{a}</td><td>{'✅' if correct else '❌'}</td><td>{diff}</td></tr>"
    table += "</table>"
    return table


# 🟢 First-time session setup
def start_session():
    q = interviewer.get_question()
    history_html = format_history_html()
    stars = calculate_stars(interviewer.accuracy)
    badge = get_badge(interviewer.accuracy)
    return f"Difficulty: {interviewer.difficulty}", q, "", 0, history_html, f"{stars} ⭐", badge

def submit_answer(answer, last_question):
    evaluation_prompt = f"User was asked: '{last_question}'\nThey answered: '{answer}'\nWas this correct? Answer only 'yes' or 'no'."
    result = ask_llm(evaluation_prompt)
    is_correct = "yes" in result.lower()
    acc, diff = interviewer.update_score(is_correct)

    store_history(last_question, answer, is_correct, diff)

    history_html = format_history_html()
    stars = calculate_stars(acc)
    badge = get_badge(acc)

    if acc < 30:
        return f"Session Ended. Accuracy: {acc:.2f}%", "Thank you!", "", acc, history_html, f"{stars} ⭐", badge

    q = interviewer.get_question()
    return f"Difficulty: {diff}", q, "", acc, history_html, f"{stars} ⭐", badge

def handle_voice_input(audio):
    return transcribe_audio(audio)

with gr.Blocks() as demo:
    gr.Markdown("# 🎯 LLM Interviewer")

    diff_display = gr.Text(label="Current Difficulty")
    score_display = gr.Number(label="Score (%)")
    question_display = gr.Text(label="Current Question", interactive=False)

    answer_in = gr.Textbox(label="Your Answer")
    voice_input = gr.Audio(label="🎙️ Voice Answer (optional)", type="filepath")

    with gr.Row():
        submit_btn = gr.Button("Submit Answer")
        record_btn = gr.Button("Transcribe Voice")

    with gr.Row():
        star_display = gr.Text(label="⭐ Stars Earned")
        badge_display = gr.Text(label="🏅 Badge")

    gr.Markdown("## 🧾 Answer History")

    with gr.Row():
        refresh_btn = gr.Button("🔄 Refresh History")

    history_html = gr.HTML()

    refresh_btn.click(
        fn=format_history_html,
        outputs=history_html
    )

    submit_btn.click(
        fn=submit_answer,
        inputs=[answer_in, question_display],
        outputs=[
            diff_display,
            question_display,
            answer_in,
            score_display,
            history_html,
            star_display,
            badge_display
        ]
    )

    record_btn.click(
        fn=handle_voice_input,
        inputs=voice_input,
        outputs=answer_in
    )

    demo.load(
        fn=start_session,
        inputs=[],
        outputs=[
            diff_display,
            question_display,
            answer_in,
            score_display,
            history_html,
            star_display,
            badge_display
        ]
    )

    init_db()
    demo.launch()
