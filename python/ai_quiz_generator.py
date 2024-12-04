# ai_quiz_generator.py
import bardapi
from config import BARD_API_KEY

def generate_quiz(content):
    input_text = (
        f"다음 주제에 관련된 문제를 영어로 생성해주세요: {content}. "
        "이 문제는 4개의 보기를 포함해야 하며, 그중 정답은 1개여야 합니다. "
        "그리고 출력 형태는 Question: who are you? Answer Choices: 1. a. 2. b. 3. c. 4. d. Correct Answer: 4. d."
    )
    return bardapi.core.Bard(BARD_API_KEY).get_answer(input_text)['content']
# 프롬포트를 통해 원하는 값만 출력되도록