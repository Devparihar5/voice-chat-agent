import os
import openai
import asyncio
import edge_tts
import streamlit as st
from pathlib import Path
from streamlit_pdf_viewer import pdf_viewer
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate


# ========== Function to generate TTS audio ==========
async def generate_tts(text, voice, output_file):
    """Generate text-to-speech audio."""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
    except Exception as e:
        st.error(f"Error generating TTS: {e}")


# ========== Load documents and create vector store ==========
def load_vector_store(file_path, api_key):
    """Load documents and create an in-memory FAISS vector store."""
    try:
        loader = TextLoader(file_path)
        documents = loader.load()

        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        
        # Use FAISS as in-memory vector store
        vector_store = FAISS.from_documents(documents, embeddings)
        return vector_store

    except Exception as e:
        st.error(f"Error loading vector store: {e}")
        st.stop()

# ========== Initialize Streamlit App ==========
st.set_page_config(page_title="Voice Chat Agent", layout="wide")

# Sidebar
st.sidebar.title("Settings")
mode = st.sidebar.radio("Choose Mode", ["Text-to-Audio", "Audio-to-Audio", "Know More About Devendra"])
voice_option = st.sidebar.selectbox("Select Voice", ["en-US-GuyNeural", "en-US-JennyNeural"])
file_path = "files/my_info.txt"

# Main UI
st.title("🗣️ Voice Chat Agent")
st.write("Ask any question related to Devendra Parihar.")

# Load API key

openai_api_key = st.sidebar.text_input("OpenAI API Key")

if not openai_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")
    st.stop()

else:
    # Load Vector Store
    if not os.path.isfile(file_path):
        st.error(f"File '{file_path}' not found.")
        st.stop()

    vector_store = load_vector_store(file_path, openai_api_key)

    # User Input
    if mode == "Text-to-Audio":

        user_input = st.text_input("💬 Ask your question:")
        if user_input:
            st.write(f"**You asked:** {user_input}")

            try:
                results = vector_store.similarity_search(user_input, k=1)

                # Combine document content into a single string
                if results:
                    context = "\n".join([res.page_content for res in results])
                else:
                    context = ""

                # GPT-4 Model
                gpt4 = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key, temperature=0.3)

                # Prompt Template
                prompt = PromptTemplate(
                    input_variables=["query", "context"],
                    template="""
                    Assume you are Devendra Parihar. 
                    - Respond to questions only related to Devendra Parihar based on the provided context.
                    - If no related context is found, say: "You can ask me queries only related to Devendra Parihar."

                    User Question:
                    {query}

                    Context:
                    {context}

                    Answer: within 3-4 lines max
                    """
                )

                # Generate response
                chain = prompt | gpt4
                response = chain.invoke({"query": user_input, "context": context})

                # Display response
                st.subheader("💡 Response:")
                st.write(response.content)

                # Generate TTS audio
                output_file = "audio_output.mp3"
                asyncio.run(generate_tts(response.content, voice_option, output_file))

                # Display audio player
                with open(output_file, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")

            except Exception as e:
                st.error(f"An error occurred: {e}")

    # ========== Mode: Audio-to-Audio ==========
    if mode =="Audio-to-Audio":        
        audio_value = st.audio_input("Record a voice message")

        if audio_value:
            st.audio(audio_value)
            audio_path = Path("temp_audio.wav")
            with open(audio_path, "wb") as f:
                f.write(audio_value.getbuffer())
                    
            # Use OpenAI v1.0.0+ API for transcription
            client = openai.Client(api_key=openai_api_key)
            if audio_path.exists():
                with open(audio_path, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )

            st.write("### Transcription:")
            st.write(transcript.text)

            # Clean up the temporary audio file
            os.remove(audio_path)
            user_input = transcript.text
            
            try:
                results = vector_store.similarity_search(user_input, k=1)

                # Combine document content into a single string
                if results:
                    context = "\n".join([res.page_content for res in results])
                else:
                    context = ""

                # GPT-4 Model
                gpt4 = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key, temperature=0.3)

                # Prompt Template
                prompt = PromptTemplate(
                    input_variables=["query", "context"],
                    template="""
                    Assume you are Devendra Parihar. 
                    - Respond to questions only related to Devendra Parihar based on the provided context.
                    - If no related context is found, say: "You can ask me queries only related to Devendra Parihar."

                    User Question:
                    {query}

                    Context:
                    {context}

                    Answer: within 3-4 lines max
                    """
                )

                # Generate response
                chain = prompt | gpt4
                response = chain.invoke({"query": user_input, "context": context})

                # Display response
                st.subheader("💡 Response:")
                st.write(response.content)

                # Generate TTS audio
                output_file = "audio_output.mp3"
                asyncio.run(generate_tts(response.content, voice_option, output_file))

                # Display audio player
                with open(output_file, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")

            except Exception as e:
                st.error(f"An error occurred: {e}")

    if mode=="Know More About Devendra":
        st.write("### Know More About Devendra")

        #show a pdf here 
        pdf_path = "files/Devendra-Parihar-Resume.pdf"
        container_pdf, container_chat = st.columns([250, 250])
        with container_pdf:
            with open(pdf_path, "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            pdf_viewer(input=PDFbyte,
                    width=700)
        
        st.download_button(label="Download PDF", data=PDFbyte, file_name=pdf_path, mime="application/octet-stream")
        