# PDF Querying Chatbot
A chatbot designed to handle PDF documents by summarizing their content or answering any queries related to the PDF. The project utilizes LangChain for backend logic, a FastAPI deployment for the LLM, and Chainlit for the frontend interface. It supports any LLaMA model for natural language processing.
## Features

- **PDF Upload**: Users can upload PDF documents.
- **Summarization**: Automatically generates concise summaries of uploaded PDFs.
- **Query Handling**: Allows users to ask questions related to the uploaded PDF and get accurate answers.
- **User-Friendly Interface**: An interactive and intuitive chatbot interface built using Chainlit.

---

## Tech Stack

- **Backend**: [LangChain](https://www.langchain.com/) for document processing and logic.
- **LLM**: LLaMA model deployed via [FastAPI](https://fastapi.tiangolo.com/).
- **Frontend**: [Chainlit](https://www.chainlit.io/) for the user interface.
- **Model**: Any LLaMA variant for text understanding.

---

## Guide

- [Installation](
    - create a virtual environment
    - activate the environment
    - Install the requirements.txt file using the command "pip install -r requirements.txt"
    - note the dependancies will only be installed on Linux or MacOS systems 
)
- [Usage](
    - run the main_api.py file using the command "python final_api.py"
    - run the chainlit application using the command "chainlit run app.py --port 5001"
)

