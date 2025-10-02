import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError, APIStatusError

load_dotenv()

API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("API Key가 비어있습니다. Streamlit Secrets 또는 .env를 확인하세요.")
    st.stop()
    
client = OpenAI(api_key=API_KEY)

st.title("2조 변학균 최지은")

# (1) st.session_state에 "messages"가 없으면 초기값을 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "뭘봐?"}]

#기록 렌더링
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

#입력 처리
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # 먼저 접근 쉬운 모델로 테스트
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        reply = resp.choices[0].message.content

    except AuthenticationError as e:
        st.error(f"[Auth] 인증 오류: {e}")
        st.stop()
    except RateLimitError as e:
        st.error(f"[429] 호출 제한: {e}")
        st.stop()
    except APIConnectionError as e:
        st.error(f"[네트워크] 연결 실패: {e}")
        st.stop()
    except APIStatusError as e:
        st.error(f"[{e.status_code}] API 오류: {e.message}")
        st.stop()
    except Exception as e:
        st.error(f"[기타] {type(e).name}: {e}")
        st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

