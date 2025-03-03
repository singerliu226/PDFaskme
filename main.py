import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import qa_agent


st.title("📖唱子的文件问答智能体")

with st.sidebar:
    openai_api_key = st.text_input("请输入您的密钥：", type="password")
    st.markdown("[获取你的密钥](http://platform.openai.com/account/api-key")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,memory_key="chat history",
        output_key="answer"
    )

uploaded_file = st.file_uploader("上传你的文件：",type="pdf,word")
question = st.text_input("对PDF的内容进行提问",disabled=not uploaded_file)

if uploaded_file and question and not openai_api_key:
    st.info("请输入您的密钥")

if uploaded_file and not question and openai_api_key:
    st.info("请输入您想询问的问题")

if question and openai_api_key and not uploaded_file:
    st.info("请上传文件")

if uploaded_file and question and openai_api_key:
    with st.spinner("AI正在思考中，请稍等..."):
        response = qa_agent(openai_api_key,st.session_state["memory"],
                            uploaded_file,question)
    st.write("### 答案")
    st.write(response["answer"])
    st.session_state["chat_history"] = response["chat_history"]

if "chat_history" in st.session_state:
    with st.expander("历史消息"):
        for i in range(0, len(st.session_state["chat_history"]),2):
            if i+1 >= len(st.session_state["chat_history"]):
                break
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.markdown(f"**您**：{human_message.content}")
            st.markdown(f"*AI*：{ai_message.content}")
