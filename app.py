import streamlit as st
from google import genai

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Maths AI Solver",
    page_icon="📐",
    layout="centered"
)

# ----------------------------------
# GEMINI CONFIGURATION
# ----------------------------------

MODEL = "gemini-3.8-flash"

@st.cache_resource
def get_client():
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

# ----------------------------------
# SIDEBAR SETTINGS
# ----------------------------------

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

# Apply selected theme
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

# ----------------------------------
# HELPER FUNCTION
# ----------------------------------

def ask_gemini(prompt):

    client = get_client()

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text


# ----------------------------------
# TABS
# ----------------------------------

tab_1, tab_2 = st.tabs(["Assistant", "Practice"])


# ==================================
# TAB 1: MATHS ASSISTANT
# ==================================

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

            st.warning("Please enter a maths problem first.")

        else:

            with st.spinner("Solving your problem..."):

                try:

                    question = f"""
                    You are an expert mathematics tutor.

                    The student's level is: {level}.

                    Solve the following mathematical problem.

                    Instructions:
                    1. Explain the solution step by step.
                    2. Show all relevant calculations.
                    3. Explain the mathematical concepts.
                    4. Clearly highlight the final answer.
                    5. Check your calculations.
                    6. Use LaTeX formatting for equations.
                    7. Adjust your explanation to the student's level.

                    Mathematical problem:
                    {prompt}
                    """

                    answer = ask_gemini(question)

                    st.success("Solution generated!")

                    st.markdown("### Solution")
                    st.markdown(answer)

                except Exception as e:

                    st.error(f"Something went wrong: {e}")


# ==================================
# TAB 2: PRACTICE
# ==================================

with tab_2:

    st.title("Maths Practice ✏️")

    st.subheader("Test your mathematical knowledge!")

    st.write(
        f"Current difficulty: **{level}**"
    )

    # Generate a practice question

    if st.button("Generate question", type="primary"):

        with st.spinner("Generating a maths question..."):

            try:

                question = f"""
                Generate ONE mathematics practice question.

                Difficulty: {level}

                Requirements:
                - Make the question suitable for this difficulty.
                - Only generate one question.
                - Do not reveal the answer.
                - Keep the question clear and understandable.
                """

                generated = ask_gemini(question)

                st.session_state.practice_question = generated
                st.session_state.practice_feedback = None

            except Exception as e:

                st.error(f"Something went wrong: {e}")

    # Display generated question

    if "practice_question" in st.session_state:

        st.markdown("### Your question")

        st.markdown(st.session_state.practice_question)

        user_answer = st.text_input(
            "Your answer",
            key="practice_answer"
        )

        if st.button("Check answer"):

            if not user_answer.strip():

                st.warning("Please enter your answer.")

            else:

                with st.spinner("Checking your answer..."):

                    try:

                        check_prompt = f"""
                        You are a mathematics teacher.

                        Difficulty: {level}

                        Mathematics question:
                        {st.session_state.practice_question}

                        Student's answer:
                        {user_answer}

                        Check whether the answer is mathematically correct.

                        Explain:
                        1. Whether the answer is correct.
                        2. Why it is correct or incorrect.
                        3. The correct solution, step by step.
                        4. The correct final answer.

                        Be encouraging and educational.
                        """

                        feedback = ask_gemini(check_prompt)

                        st.session_state.practice_feedback = feedback

                    except Exception as e:

                        st.error(f"Something went wrong: {e}")

        # Display feedback

        if st.session_state.practice_feedback:

            st.markdown("### Feedback")

            st.markdown(
                st.session_state.practice_feedback
            )