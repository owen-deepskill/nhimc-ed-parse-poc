from openai import OpenAI
import streamlit as st
import hashlib
# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv())

client = OpenAI()

MODEL = "gpt-4-0125-preview"

SYSTEM_MESSAGE = """
**Instruction Prompt for Classifying Emergency Room Medical Descriptions:**

When given a medical description from an emergency department context, 
classify the description according to the following categories. 
Provide the rationale for your classification(s), and note that multiple classifications are possible.
Keep the classification in English, and provide the rationale in Korean.
If none of the categories can be applied, output "해당 분류 없음" and provide the rationale.

Categories:
1. Alcohol related
2. Accommodation or food
3. Assault or trauma
4. Abdominal pain
5. Headache
6. Chest pain
7. Allergy
8. Shortness of breath
9. Falls
10. Poisoning
11. Motor vehicle accident
12. Abnormal heart beat
13. Suicide

**Example Input:**
AA AMNESIC TO EVENTS SMALL LACERATION TO RI

**Example Output:**

분류 1: 3 Assault or trauma (사건에 대한 기억상실("AMNESIC TO EVENTS") 언급은 기억 손실을 일으킨 가능한 외상을 제안합니다. "RI에 대한 작은 찰과상"은 폭행이나 외상으로 인해 발생할 수 있는 신체적 손상을 나타냅니다.)

분류 2: 9 Falls (찰과상은 특히 기억상실이 환자가 넘어져 부상을 입은 사건과 관련이 있는 경우, 낙상을 나타낼 수도 있습니다.)
"""


def check_password():
    """비밀번호 입력 및 검증"""
    with st.form(key="password_form"):
        password = st.text_input("비밀번호를 입력하세요", type="password")
        login_button = st.form_submit_button(label="로그인")

        if login_button:
            if (
                hashlib.sha256(password.encode()).hexdigest()
                == "c6bdd43e330236f231858fee9102a72b4ee4dea3ca78d9f7015b0311d470ffed"
            ):
                st.session_state.password_verified = True
                st.rerun()
            else:
                st.error("비밀번호가 틀렸습니다.")

def show_main_content():
    st.title("일산병원 응급실 적요 분류 앱 (POC)")

    st.caption(
        """
적요 텍스트를 입력하면 분류와 이유를 출력합니다. 분류는 복수일 수 있습니다.

주어진 분류 값:
1. Alcohol related
2. Accommodation or food
3. Assault or trauma
4. Abdominal pain
5. Headache
6. Chest pain
7. Allergy
8. Shortness of breath
9. Falls
10. Poisoning
11. Motor vehicle accident
12. Abnormal heart beat
13. Suicide
"""
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "응급실 적요를 입력하세요"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        client = OpenAI()
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE}
            ] + st.session_state.messages,
            temperature=0
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

if "password_verified" not in st.session_state:
    st.session_state.password_verified = False

if not st.session_state.password_verified:
    check_password()
else:
    show_main_content()
