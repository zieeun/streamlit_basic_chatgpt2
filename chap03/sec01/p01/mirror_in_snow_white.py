from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# ② 
response = client.chat.completions.create(
  model="gpt-4o",
  temperature=0.9,  # ③
  messages=[
    {"role": "system", "content": "너는 백설공주 이야기 속의 거울이야. 그 이야기 속의 마법 거울의 캐릭터에 부합하게 답변해줘."},
    {"role": "user", "content": "세상에서 누가 제일 아름답니?"},
  ]		# ④
)

print(response)

print('----')	# ⑤
print(response.choices[0].message.content) 
