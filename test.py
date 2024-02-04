import openai
from dotenv import load_dotenv, find_dotenv
from langchain.chains import OpenAIChain

_ = load_dotenv(find_dotenv())  # read local .env file


# OpenAI API 키 설정 (환경 변수에서 불러오거나 직접 지정)
openai.api_key = 'your_openai_api_key_here'

# LangChain을 사용하여 OpenAI GPT-4 체인 초기화
gpt_chain = OpenAIChain(model="gpt-4")

def classify_items(items, categories):
    classified_results = []
    reasons = []

    for item in items:
        # 각 항목에 대해 GPT-4를 사용하여 분류 질문 생성 및 호출
        prompt = f"{item}은(는) 다음 중 어떤 카테고리에 속하나요? {', '.join(categories)}"
        response = gpt_chain.run(prompt)
        
        # 분류 결과 추출
        classified_category = response.choices[0].text.strip()
        classified_results.append(classified_category)
        
        # 분류 사유 질문 생성 및 호출
        reason_prompt = f"왜 {item}은(는) {classified_category}인가요?"
        reason_response = gpt_chain.run(reason_prompt)
        
        # 분류 사유 추출
        reason = reason_response.choices[0].text.strip()
        reasons.append(reason)

    return classified_results, reasons

# 입력 데이터
items = ["사과", "호랑이", "배", "곰"]
categories = ["과일", "동물"]

# 분류 실행
classified_results, reasons = classify_items(items, categories)

# 결과 출력
print("분류 값:", classified_results)
print("분류 사유:", reasons)
