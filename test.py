# Next steps: label data; RAG, 파인튜닝

from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = OpenAI()

SYSTEM_MESSAGE = """
**Instruction Prompt for Classifying Emergency Room Medical Descriptions:**

When given a medical description from an emergency department context, 
classify the description according to the following categories. 
Provide the rationale for your classification(s), and note that multiple classifications are possible.
Additionally, you may summarize any supplementary information, only if it is deemed to be helpful.
Do the thinking process in English, then translate the final output into Korean.

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
참조: 상황을 가장 잘 분류하기 위해 설명된 손상의 기전이나 근본적인 원인을 고려하세요. 예를 들어, 기억상실은 종종 머리 부상으로 인해 발생하는데, 이는 낙상, 폭행, 또는 교통사고로 인해 발생할 수 있습니다. 찰과상은 일반적으로 날카로운 부상과 관련이 있으며, 이는 외상과 관련된 분류를 지원할 수 있습니다.
"""

def categorize_and_explain(text):
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": text}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        temperature=0
    )
    return(response.choices[0].message.content)

print(categorize_and_explain("ABDO PAIN DIFFICULITY USING BOWELS REPORTS"))
