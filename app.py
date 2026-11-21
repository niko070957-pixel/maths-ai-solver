
import streamlit as st
from groq import Groq
import sympy as sp

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Maths AI Solver",
    page_icon="📐",
    layout="centered"
)

# ==========================================
# GROQ CONFIGURATION
# ==========================================

MODEL = "openai/gpt-oss-120b"


@st.cache_resource
def get_client():
    return Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )


def ask_ai(prompt):

    client = get_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert mathematics tutor.

                Your job is to solve mathematical problems
                and explain them clearly.

                Instructions:
                - Explain every step.
                - Show relevant calculations.
                - Use LaTeX for equations.
                - Check your answers.
                - Adapt explanations to the student's level.
                - Be accurate and educational.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=2500,
        reasoning_effort="medium"
    )

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError("The AI returned an empty response.")

    return answer


# ==========================================
# SIDEBAR SETTINGS
# ==========================================

st.sidebar.header("Assistant settings")
st.sidebar.write("Experimental features")

level = st.sidebar.selectbox(
    "Choose level",
    ["Beginner", "Intermediate", "Advanced"]
)

theme = st.sidebar.selectbox(
    "Theme",
    ["Light", "Dark"]
)


# ==========================================
# THEME
# ==========================================

if theme == "Dark":

    st.markdown("""
        <style>

        [data-testid="stAppViewContainer"] {
            background-color: #171923;
            color: white;
        }

        [data-testid="stSidebar"] {
            background-color: #202333;
        }

        [data-testid="stHeader"] {
            background-color: transparent;
        }

        </style>
    """, unsafe_allow_html=True)


# ==========================================
# MATHEMATICAL CALCULATOR
# ==========================================

def calculate_math(expression):

    try:

        x = sp.symbols("x")

        expression = expression.strip()

        # Handle equations
        if "=" in expression:

            left, right = expression.split("=", 1)

            equation = sp.Eq(
                sp.sympify(left),
                sp.sympify(right)
            )

            result = sp.solve(equation, x)

            return result

        # Handle ordinary expressions
        else:

            result = sp.sympify(expression)

            return sp.simplify(result)

    except Exception:

        return None


# ==========================================
# TABS
# ==========================================

tab_1, tab_2 = st.tabs(
    ["Assistant", "Practice"]
)


# ==========================================
# TAB 1: ASSISTANT
# ==========================================

with tab_1:

    st.title("Maths AI Solver 📐")

    st.subheader(
        "Solve equations and perform algebraic operations with ease!"
    )

    st.write(
        "Enter a maths problem and let AI explain how to solve it."
    )

    prompt = st.text_area(
        "Your equation or question",
        placeholder="Example: 2x + 7 = 23",
        height=120
    )

    if st.button("Answer", type="primary"):

        if not prompt.strip():

            st.warning(
                "Please enter a mathematical problem."
            )

        else:

            with st.spinner("Solving your problem..."):

                try:

                    # Ask AI for an explanation
                    question = f"""
                    Student level: {level}

                    Solve this mathematical problem.

                    Explain the solution step by step.
                    Show all calculations.
                    Use LaTeX formatting.
                    Check your final answer.

                    Problem: {prompt}
                    """

                    answer = ask_ai(question)

                    st.success("Solution generated!")

                    st.markdown("### AI Explanation")

                    st.markdown(answer)

                    # Try to calculate using SymPy
                    result = calculate_math(prompt)

                    if result is not None:

                        st.markdown("### Python verification")

                        st.latex(
                            sp.latex(result)
                        )

                        st.caption(
                            "Calculated independently using SymPy."
                        )

                except Exception as e:

                    st.error(
                        f"An error occurred: {e}"
                    )


# ==========================================
# TAB 2: PRACTICE
# ==========================================

with tab_2:

    st.title("Maths Practice ✏️")

    st.subheader(
        "Test your mathematical knowledge!"
    )

    st.write(
        f"Current difficulty: **{level}**"
    )

    # Generate question
    if st.button(
        "Generate question",
        type="primary"
    ):

        with st.spinner("Generating question..."):

            try:

                question = f"""
                Generate ONE mathematics practice question.

                Difficulty: {level}

                Requirements:
                - Generate one clear question.
                - Make it suitable for the selected level.
                - Do not reveal the answer.
                - Do not include the solution.
                """

                generated = ask_ai(question)

                st.session_state.practice_question = generated

                st.session_state.practice_feedback = None

                st.session_state.practice_answer = ""

            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )

    # Display question
    if "practice_question" in st.session_state:

        st.markdown("### Your question")

        st.markdown(
            st.session_state.practice_question
        )

        user_answer = st.text_input(
            "Your answer",
            key="practice_answer"
        )

        if st.button("Check answer"):

            if not user_answer.strip():

                st.warning(
                    "Please enter your answer."
                )

            else:

                with st.spinner("Checking your answer..."):

                    try:

                        check_prompt = f"""
                        You are a mathematics teacher.

                        Difficulty: {level}

                        Question:
                        {st.session_state.practice_question}

                        Student's answer:
                        {user_answer}

                        Assess the answer.

                        Explain:
                        1. Whether it is correct.
                        2. Why it is correct or incorrect.
                        3. The correct solution step by step.
                        4. The final answer.

                        Be encouraging and educational.
                        """

                        feedback = ask_ai(check_prompt)

                        st.session_state.practice_feedback = feedback

                    except Exception as e:

                        st.error(
                            f"An error occurred: {e}"
                        )

        # Show feedback
        if st.session_state.get("practice_feedback"):

            st.markdown("### Feedback")

            st.markdown(
                st.session_state.practice_feedback
            )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Maths AI Solver | Powered by Groq, GPT-OSS and Python"
)
