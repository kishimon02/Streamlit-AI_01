import requests
import streamlit as st

dify_api_key = st.secrets["DIFY_API_KEY"]   # Streamlitのsecrets機能を使って、Dify APIのAPIキーを安全に取得
url = 'https://api.dify.ai/v1/chat-messages'    # Dify APIのエンドポイント（APIの機能が利用できるURL）

st.title('Kishimon AIのお悩み相談室')   # タイトルを表示

if "conversation_id" not in st.session_state:   # 会話IDがセッションステートにない場合
    st.session_state.conversation_id = ""   # 空文字列をセット

if "messages" not in st.session_state:  # メッセージがセッションステートにない場合
    st.session_state.messages = []  # 空リストをセット

for message in st.session_state.messages:   # セッションステートのメッセージを表示
    with st.chat_message(message["role"]):  # チャットメッセージを表示（ユーザーとAIのメッセージをそれぞれのロール（役割）に応じて左右どちらかに表示）
        st.markdown(message["content"]) # メッセージの内容を表示

prompt = st.chat_input("Kishimon AIに何か質問してみよう!")  # チャット入力欄を表示

if prompt:  # ユーザーが何か入力した場合
    with st.chat_message("user"):   #ユーザーのメッセージをチャット欄に表示
        st.markdown(prompt) # コンテンツがプロンプトの場合

    st.session_state.messages.append({"role": "user", "content": prompt})   # ユーザーのプロンプトメッセージをセッションステートに追加

with st.chat_message("assistant"):  # AIのメッセージをチャット欄に表示
    message_placeholder = st.empty()    # AIの応答を一時的に表示するための空のプレースホルダーを作成

    headers = {
        'Authorization': 'Bearer {dify_api_key}',  # Dify APIのAPIキーをヘッダーにセット
        'Content-Type': 'application/json'  # コンテンツタイプをJSONにセット
    }

    payload = {
        "inputs": {},   # 入力を空にセット
        "query": prompt,        # プロンプトをセット
        "response_mode": "streaming",    # レスポンスモードをブロッキング（チャットボットからの返信が出来上がってからしか返ってこない設定）にセット
        "conversation_id": st.session_state.conversation_id,    # 会話IDをセット（Dify APIが会話履歴を管理するために使用）
        "user": "kishimon-01",    # ユーザーをセット（Dify APIがユーザーを識別するために使用）
        "files": []   # ファイルを空にセット
    }

try:    # APIリクエストを送信
    response = requests.post(url, headers=headers, json=payload)    # POSTリクエストを送信
    response.raise_for_status() # ステータスコードが200番台以外の場合は例外を発生させる

    response_data = response.json() # レスポンスデータをJSON形式で取得

    full_response = response_data.get("answer", "")   # レスポンスデータから回答を取得
    new_conversation_id = response_data.get("conversation_id", st.session_state.conversation_id)    # レスポンスデータから会話IDを取得

    st.session_state.conversation_id = new_conversation_id  # 新しい会話IDをセッションステートにセット

except requests.exceptions.RequestException as e:   # リクエストエラーが発生した場合
    st.error(f"An error occurred: {e}") # エラーメッセージを表示
    full_response = "An error occurred while fetching the response."    # エラーが発生したことをユーザーに伝えるためのメッセージをセット

message_placeholder.markdown(full_response)  # プレースホルダー（一時的に格納しておく場所）にチャットボットからの最終的な応答を表示
st.session_state.messages.append({"role": "assistant", "content": full_response})   # チャットボットからの最終的な応答をセッションステートに追加








