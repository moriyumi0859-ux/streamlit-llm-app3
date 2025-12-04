from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from openai import OpenAI

api_key = st.secrets.get("OPENAI_API_KEY", None)

# 2. なければ環境変数（ローカル .env 用）
if api_key is None:
    api_key = os.environ.get("OPENAI_API_KEY")

# 3. それでも無ければエラー表示して止める
if api_key is None:
    st.error("OPENAI_API_KEY が設定されていません。Secrets か .env を確認してください。")
    st.stop()

client = OpenAI(api_key=api_key)

# 定義 

SYSTEM_PROMPT_LOVE_COUNSELOR = """
あなたは恋愛相談の専門家です。
ユーザーの気持ちに寄り添いながら、恋愛の悩みや不安に対して優しく丁寧に答えてください。
相手の心理、コミュニケーションのコツ、関係改善のポイントなどを具体的に示しながら、
ユーザーが前向きな一歩を踏み出せるようにアドバイスを行います。
言い切りすぎず、選択肢や可能性を提示する形で解説してください。
"""

SYSTEM_PROMPT_COMM_COACH = """
あなたは人間関係・コミュニケーションの専門コーチです。
恋愛に限らず、職場・友人・家族など幅広い場面の対人関係に対して、
論理的かつ実践的なコミュニケーション改善アドバイスを行います。
具体的な行動提案、会話のコツ、相手のタイプ別のアプローチなどを中心に、
ユーザーがすぐに使えるテクニックを分かりやすく説明してください。
感情的になりすぎず、落ち着いたコーチングの口調で答えてください。
"""

# Streamlit

st.title("恋愛相談 & コミュニケーション相談 AI")

st.write("ラジオボタンで相談したい専門家のタイプを選んでください。")

role = st.radio(
    "専門家のタイプを選択",
    (
        "A：恋愛カウンセラー（恋愛相談の専門家）",
        "B：コミュニケーションコーチ（人間関係・コミュ力の専門家）",
    ),
)

user_input = st.text_area(
    "相談内容を入力してください",
    placeholder="例）気になる人と距離を縮めるにはどうしたらいいですか？",
    height=150,
)

if st.button("相談する"):
    if not user_input.strip():
        st.warning("相談内容を入力してください。")
    else:
        # ラジオボタンの選択に応じて system メッセージを切り替える
        if role.startswith("A"):
            system_message = SYSTEM_PROMPT_LOVE_COUNSELOR
            expert_label = "恋愛カウンセラー"
        else:
            system_message = SYSTEM_PROMPT_COMM_COACH
            expert_label = "コミュニケーションコーチ"

        with st.spinner(f"{expert_label}として回答を生成しています..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_input},
                    ],
                )

                answer = response.choices[0].message.content

                st.markdown(f"### {expert_label}からの回答")
                st.write(answer)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")