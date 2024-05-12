import streamlit as st
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex, SimpleDirectoryReader, ChatPromptTemplate
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import os
from youtube_transcript_api import YouTubeTranscriptApi
import shutil
import time

# Load environment variables
load_dotenv()

icons = {"assistant": "robot.png", "user": "man-kddi.png"}

# Configure the Llama index settings
Settings.llm = HuggingFaceInferenceAPI(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    tokenizer_name="mistralai/Mistral-7B-Instruct-v0.2",
    context_window=3000,
    token=os.getenv("HF_TOKEN"),
    max_new_tokens=512,
    generate_kwargs={"temperature": 0.1},
)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Define the directory for persistent storage and data
PERSIST_DIR = "./db"
DATA_DIR = "data"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PERSIST_DIR, exist_ok=True)

def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def data_ingestion():
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    print(documents)
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(documents,show_progress=True)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
       
        return transcript

    except Exception as e:
        st.error(e)

def remove_old_files():
    # Specify the directory path you want to clear
    directory_path = "data"

    # Remove all files and subdirectories in the specified directory
    shutil.rmtree(directory_path)

    # Recreate an empty directory if needed
    os.makedirs(directory_path)
    
def handle_query(query):
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    chat_text_qa_msgs = [
    (
        "user",
        """You are a Q&A assistant named CHATTO, created by Suriya. your main goal is to provide answers as accurately as possible, based on the instructions and context you have been given. If a question does not match the provided context or is outside the scope of the document, kindly advise the user to ask questions within the context of the document.
        Context:
        {context_str}
        Question:
        {query_str}
        """
    )
    ]
    text_qa_template = ChatPromptTemplate.from_messages(chat_text_qa_msgs)
    
    query_engine = index.as_query_engine(text_qa_template=text_qa_template)
    answer = query_engine.query(query)

    final_ans = []
    if hasattr(answer, 'response'):
        final_ans.append(answer.response)
    elif isinstance(answer, dict) and 'response' in answer:
        final_ans.append(answer['response'])
    else:
        final_ans.append("Sorry, I couldn't find an answer.")

    ans = " ".join(final_ans)
    for i in ans:
        yield str(i)
        time.sleep(0.01)


# Streamlit app initialization
st.title("Chat with your PDF📄")
st.markdown("Built by [Suriya❤️](https://github.com/theSuriya)")
st.markdown("chat here👇")

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', "content": 'Hello! Upload a PDF and ask me anything about its content.'}]
    
# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"],avatar=icons[message["role"]]):
        st.write(message["content"])
        
with st.sidebar:
    st.title("Menu:")
    uploaded_file = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button")
    video_url = st.text_input("Enter Youtube Video Link: ")
    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            if len(os.listdir("data")) !=0:
                remove_old_files()
                
            if uploaded_file:
                filepath = "data/saved_pdf.pdf"
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
        
            if video_url:
                extracted_text = extract_transcript_details(video_url)
                with open("data/saved_text.txt", "w") as file:
                    file.write(extracted_text)
                
            data_ingestion()  # Process PDF every time new file is uploaded
            st.success("Done")

user_prompt = st.chat_input("Ask me anything about the content of the PDF:")
if user_prompt and (video_url or uploaded_file):
    st.session_state.messages.append({'role': 'user', "content": user_prompt})
    with st.chat_message("user", avatar="man-kddi.png"):
        st.write(user_prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant",avatar="robot.png"):
        response = handle_query(user_prompt)
        full_response = st.write_stream(response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
