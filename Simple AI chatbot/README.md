# Simple AI Chatbot using OpenAI, Langchain and Firestore

This project is simple conversational chatbot built with:
- **OpenAI's gpt-4o-mini**
- **LangChain** for conversation flow
- **Firestore** for saving chat history

---

## How to Run

1. Open the notebook in [Google Colab](https://colab.research.google.com)
2. Follow the steps:
    - Install dependencies
    - Set API keys
    - Authenticate Firestore
    - Interact with the chatbot

---

## Requirements

- OpenAI API key
- Google Firestore setup  (with 'serviceAccountKey.json')
- Python librarires:
    ```bash
    pip install langchain openai firebase-admin google-cloud-firestore