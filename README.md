---
title: Chatbot PDF
emoji: 🏆
colorFrom: pink
colorTo: blue
sdk: streamlit
sdk_version: 1.33.0
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Chatbot-PDF

Chatbot-PDF is a conversational application that allows users to interact with PDF documents using natural language. It utilizes Hugging Face's open-source models to understand and respond to user queries related to the content of PDF files.

## Features

- **Streamlit Interface**: Built with Streamlit, providing an intuitive and interactive user interface.
- **PDF Integration**: Chatbot is capable of processing PDF documents and extracting relevant information.
- **Natural Language Understanding**: Powered by Hugging Face's models, the chatbot understands and responds to user queries in natural language.

## Usage

To use the Chatbot-PDF application, follow these steps:

1. **Clone the Repository**: Begin by cloning this repository to your local machine. Open your terminal or command prompt and use the following command:
```bash
git clone https://github.com/theSuriya/RAG-LLAMA-INDEX
```
2. **Open in Your Favorite IDE**: Open the cloned directory in your preferred Integrated Development Environment (IDE) such as Visual Studio Code, PyCharm, or any other IDE of your choice.
   
4. **HuggingFace Account login**:If you don't have a Hugging Face account, create one. You'll need an account to generate an authentication token. Follow the steps outlined in this [guid](https://huggingface.co/docs/hub/security-tokens) to generate your token. Once you have the token, locate the .env file in your project directory. Open it and paste your token like this:
  ```bash
  HF_TOkEN = "paste the token here"
  ```
4. **Install Dependencies**: Make sure you have Python installed on your system. Then, In your terminal or command prompt within the project directory, run:
```bash
pip install -r requirements.txt
```
4. **Run the Application**: Navigate to the project directory and run the following command:
 ```bash
 streamlit run app.py
 ```
6. **Interact with the Chatbot**: Once the application is running, open a web browser and go to http://localhost:8501 to access the chat interface. You can now interact with the chatbot by asking questions related to the provided PDF documents.

## Demo

For a live demo of the Chatbot-PDF application, visit [here](https://huggingface.co/spaces/suriya7/Chatbot-PDF).

## Contributing

Contributions are welcome! If you have any ideas for improvements or encounter any issues, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).




