import streamlit as st

st.set_page_config(page_title="AI Smart IQ Analyzer", page_icon="🧠", layout="centered")

QUESTIONS = [
    {"category": "Logical Reasoning", "question": "Which number comes next: 2, 4, 8, 16, __?", "options": ["18", "24", "32", "36"], "answer": "32", "explanation": "Each number is multiplied by 2."},
    {"category": "Numerical Reasoning", "question": "If 5 pens cost Rs. 100, how much do 2 pens cost?", "options": ["Rs. 20", "Rs. 30", "Rs. 40", "Rs. 50"], "answer": "Rs. 40", "explanation": "One pen costs Rs. 20, so two cost Rs. 40."},
    {"category": "Pattern Recognition", "question": "Which item is different from the others?", "options": ["Triangle", "Square", "Circle", "Carrot"], "answer": "Carrot", "explanation": "The first three are geometric shapes; a carrot is a vegetable."},
    {"category": "Verbal Reasoning", "question": "A book is used for reading. A fork is used for what?", "options": ["Writing", "Eating", "Running", "Sleeping"], "answer": "Eating", "explanation": "A fork is generally used for eating."},
    {"category": "Logical Reasoning", "question": "Ali is taller than Sara. Sara is taller than Ahmed. Who is shortest?", "options": ["Ali", "Sara", "Ahmed", "Cannot tell"], "answer": "Ahmed", "explanation": "Ali > Sara > Ahmed, so Ahmed is shortest."}
]

def performance(score):
    if score <= 1:
        return "Needs Practice", "Practice more reasoning and pattern questions to improve your quiz performance."
    if score <= 3:
        return "Developing", "Good effort. Keep practising different types of reasoning questions."
    if score == 4:
        return "Strong Performance", "You performed very well on this short quiz."
    return "Excellent Performance", "Excellent result on this five-question challenge!"

st.title("🧠 AI Smart IQ Analyzer")
st.caption("A short reasoning and aptitude challenge")

st.info(
    "Educational note: This five-question quiz is not a standardized or clinical IQ test. "
    "It cannot determine actual IQ. Your result is a score for this quiz only."
)

if "started" not in st.session_state:
    st.session_state.started = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.started:
    st.subheader("Welcome!")
    name = st.text_input("Enter your name", placeholder="Your name")
    st.write("Answer all five multiple-choice questions. Each correct answer earns one point.")
    if st.button("Start Test", type="primary", use_container_width=True):
        if not name.strip():
            st.warning("Please enter your name first.")
        else:
            st.session_state.name = name.strip()
            st.session_state.started = True
            st.rerun()

elif not st.session_state.submitted:
    st.subheader(f"Good luck, {st.session_state.name}!")
    with st.form("quiz_form"):
        answers = []
        for i, q in enumerate(QUESTIONS, start=1):
            st.markdown(f"**Question {i} of 5 · {q['category']}**")
            answers.append(st.radio(q["question"], q["options"], index=None, key=f"q{i}"))
            if i < 5:
                st.divider()
        submitted = st.form_submit_button("Submit Answers", type="primary", use_container_width=True)

    if submitted:
        if any(answer is None for answer in answers):
            st.warning("Please answer all five questions before submitting.")
        else:
            st.session_state.answers = answers
            st.session_state.submitted = True
            st.rerun()

else:
    answers = st.session_state.answers
    score = sum(answer == q["answer"] for answer, q in zip(answers, QUESTIONS))
    label, feedback = performance(score)

    st.subheader(f"Your Result, {st.session_state.name}")
    st.metric("Quiz Score", f"{score} / 5")
    st.progress(score / 5)
    st.header(label)
    st.write(feedback)

    st.subheader("Answer Review")
    for i, (q, answer) in enumerate(zip(QUESTIONS, answers), start=1):
        correct = answer == q["answer"]
        st.markdown(f"**Q{i}. {q['question']}**")
        st.write(f"Your answer: {answer}")
        st.write(f"Correct answer: {q['answer']}")
        st.write(("✅ Correct" if correct else "❌ Incorrect") + f" — {q['explanation']}")
        if i < 5:
            st.divider()

    st.warning(
        "This category describes performance on this mini-quiz only. "
        "It is not an actual IQ score, diagnosis, or measure of a person's overall intelligence."
    )
    if st.button("Retake Test", use_container_width=True):
        for key in ["started", "submitted", "answers", "name"]:
            st.session_state.pop(key, None)
        st.rerun()
