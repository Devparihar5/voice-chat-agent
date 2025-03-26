# Voice Chat Agent

## Overview
Voice Chat Agent is an interactive Streamlit application designed to simulate conversations specifically related to **Devendra Parihar**. The application supports two-way communication, leveraging **OpenAI's GPT-4** model for intelligent responses and **edge-tts** for text-to-speech capabilities. Users can input queries via text or voice and receive context-aware responses.

## Features

- **Text-to-Audio Mode**: Converts text-based queries into voice responses.
- **Audio-to-Audio Mode**: Records and transcribes voice queries, processes them, and provides voice responses.
- **Know More About Devendra**: Showcases a PDF viewer for detailed information.
- **Vector Store Search**: Uses FAISS for efficient similarity search in textual data.
- **GPT-4 Integration**: Provides intelligent, context-aware responses.

## Installation

### Prerequisites
Ensure you have the following installed on your machine:

- **Python 3.8 or higher**
- **Streamlit**
- **OpenAI API Key**
- **edge-tts**

### Setup

1. **Clone the Repository**
```bash
git clone https://github.com/Devparihar5/voice-chat-agent.git
cd voice-chat-agent
```

2. **Create a Virtual Environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up the Required Files**
- Place your information file at `files/my_info.txt`.
- Place your resume PDF at `files/Devendra-Parihar-Resume.pdf`.

5. **Run the Application**
```bash
streamlit run app.py
```

## Usage

1. Open the URL provided by Streamlit in your browser.
2. Select the mode from the sidebar:
   - **Text-to-Audio**: Type a question and receive audio responses.
   - **Audio-to-Audio**: Record a voice query and receive audio responses.
   - **Know More About Devendra**: View or download Devendra Parihar's resume.
3. Ensure you provide your **OpenAI API key** in the sidebar.

## Project Structure
```
voice-chat-agent/
├── files/
│   ├── my_info.txt
│   ├── Devendra-Parihar-Resume.pdf
├── app.py
├── requirements.txt
├── README.md
```

## Technologies Used

- **Streamlit**: Web interface.
- **OpenAI GPT-4**: Intelligent responses.
- **edge-tts**: Text-to-speech audio generation.
- **FAISS**: Vector store for document similarity search.
- **LangChain**: Prompt templates and chain handling.

## Contributing
Contributions are welcome! Feel free to fork the repository and create a pull request with suggested improvements or new features.

## Contact
For any queries, reach out to **Devendra Parihar**:

- **GitHub**: [Devparihar5](https://github.com/Devparihar5)
- **LinkedIn**: [Devendra Parihar](https://www.linkedin.com/in/devendra-parihar/)