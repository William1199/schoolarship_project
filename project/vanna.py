import time
import streamlit as st
from googletrans import Translator  # Thêm thư viện Google Translate
from vanna_calls import (
    generate_questions_cached,
    generate_sql_cached,
    run_sql_cached,
    generate_plotly_code_cached,
    generate_plot_cached,
    generate_followup_cached,
    should_generate_chart_cached,
    is_sql_valid_cached,
    generate_summary_cached
)

avatar_url = "http://127.0.0.1:8000/static/assets/scholarnest.png"

st.set_page_config(
    page_title="ScholarNest AI",
    page_icon="http://127.0.0.1:8000/static/assets/scholarnest.png",
    layout="wide"
)

# Sidebar Settings
st.sidebar.title("Output Settings")
st.sidebar.checkbox("Show SQL", value=True, key="show_sql")
st.sidebar.checkbox("Show Table", value=True, key="show_table")
st.sidebar.checkbox("Show Plotly Code", value=True, key="show_plotly_code")
st.sidebar.checkbox("Show Chart", value=True, key="show_chart")
st.sidebar.checkbox("Show Summary", value=True, key="show_summary")
st.sidebar.checkbox("Show Follow-up Questions", value=True, key="show_followup")
st.sidebar.button("Reset", on_click=lambda: st.session_state.clear(), use_container_width=True)

# Tạo nút HTML với kiểu dáng giống nút Reset
st.sidebar.markdown(
    '<a href="http://127.0.0.1:8000" target="_self" style="font-size:16px; color: #007bff; text-decoration: none;">Go back to Homepage</a>',
    unsafe_allow_html=True
)

# Header Design
st.markdown(f"""
    <style>
        .title-container {{
            display: flex;
            align-items: center;
        }}
        .title-container h1 {{
            font-size: 50px;
            color: #b08864;
        }}
        .title-container img {{
            width: 100px;
            height: auto;
        }}
    </style>
    <div class="title-container">
        <img src="{avatar_url}" alt="Scholarnest Avatar">
        <h1>Scholarnest AI</h1>
    </div>
""", unsafe_allow_html=True)

# Hàm để dịch văn bản sang tiếng Anh
def translate_to_english(text):
    translator = Translator()
    translated = translator.translate(text, src='auto', dest='en')  # Dịch sang tiếng Anh
    return translated.text

# Hàm để xử lý câu hỏi khi người dùng bấm vào câu hỏi đề xuất
def set_question(question):
    st.session_state["my_question"] = question

# Tạo phần câu hỏi gợi ý luôn được hiển thị khi chương trình bắt đầu
if "show_questions" not in st.session_state:
    st.session_state["show_questions"] = True  # Mặc định hiển thị câu hỏi gợi ý ngay khi bắt đầu

# Hiển thị câu hỏi gợi ý ngay từ đầu mà không cần bấm nút
if st.session_state["show_questions"]:
    with st.expander("Suggested questions"):
        questions = generate_questions_cached()  # Tạo câu hỏi gợi ý một lần
        for question in questions:
            # Tạo button cho mỗi câu hỏi gợi ý
            if st.button(question, on_click=set_question, args=(question,)):  # Khi bấm vào, câu hỏi sẽ được lưu vào session_state
                break

# Chat Input
my_question = st.chat_input("Ask me a question about scholarship")
if my_question:
    # Dịch câu hỏi sang tiếng Anh
    my_question = translate_to_english(my_question)  # Chỉnh sửa: dịch câu hỏi trước khi xử lý
    set_question(my_question)  # Lưu câu hỏi vào session_state
    st.session_state["my_question"] = my_question
    user_message = st.chat_message("user")
    user_message.write(my_question)

# Kiểm tra nếu có câu hỏi trong session_state và xử lý
if "my_question" in st.session_state and st.session_state["my_question"]:
    my_question = st.session_state["my_question"]

    # Generate SQL
    sql = generate_sql_cached(question=my_question)

    if sql:
        if is_sql_valid_cached(sql=sql):
            if st.session_state.get("show_sql", True):
                assistant_message_sql = st.chat_message("assistant", avatar=avatar_url)
                assistant_message_sql.code(sql, language="sql", line_numbers=True)
        else:
            assistant_message_error = st.chat_message("assistant", avatar=avatar_url)
            assistant_message_error.error("Sorry I cannot generate SQL query through your question.")
            st.session_state["my_question"] = None
            st.stop()

        # Run SQL and fetch data
        df = run_sql_cached(sql=sql)
        if df is not None:
            st.session_state["df"] = df

            # Display table
            if st.session_state.get("show_table", True):
                assistant_message_table = st.chat_message("assistant", avatar=avatar_url)
                if len(df) > 10:
                    assistant_message_table.text("First 10 rows of data")
                    assistant_message_table.dataframe(df.head(10))
                else:
                    assistant_message_table.dataframe(df)

            # Generate Chart
            if should_generate_chart_cached(question=my_question, sql=sql, df=df):
                code = generate_plotly_code_cached(question=my_question, sql=sql, df=df)
                if st.session_state.get("show_plotly_code", False):
                    assistant_message_plotly_code = st.chat_message("assistant", avatar=avatar_url)
                    assistant_message_plotly_code.code(code, language="python", line_numbers=True)
                if code:
                    if st.session_state.get("show_chart", True):
                        assistant_message_chart = st.chat_message("assistant", avatar=avatar_url)
                        fig = generate_plot_cached(code=code, df=df)
                        if fig:
                            assistant_message_chart.plotly_chart(fig)
                        else:
                            assistant_message_chart.error("Could not generate chart.")

            # Generate Summary
            if st.session_state.get("show_summary", True):
                summary = generate_summary_cached(question=my_question, df=df)
                if summary:
                    assistant_message_summary = st.chat_message("assistant", avatar=avatar_url)
                    assistant_message_summary.text(summary)

            # Generate Follow-up Questions
            if st.session_state.get("show_followup", True):
                followup_questions = generate_followup_cached(question=my_question, sql=sql, df=df)
                if followup_questions:
                    assistant_message_followup = st.chat_message("assistant", avatar=avatar_url)
                    assistant_message_followup.text("Here are some follow-up questions:")
                    for question in followup_questions[:5]:
                        st.button(question, on_click=set_question, args=(question,))
                else:
                    assistant_message_followup = st.chat_message("assistant", avatar=avatar_url)
                    assistant_message_followup.text("No follow-up questions available.")
    else:
        assistant_message_error = st.chat_message("assistant", avatar=avatar_url)
        assistant_message_error.error("Failed to generate SQL for the given question.")

    # Reset question for next input
    st.session_state["my_question"] = None
