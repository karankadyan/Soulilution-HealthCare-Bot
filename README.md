# Healthcare Chatbot

This is a healthcare chatbot built using Streamlit that interacts with users via voice. The bot listens to user symptoms, searches a predefined database, and provides a response through both voice and text.

## Features

- Voice interaction: The bot listens to user input and responds accordingly.
- Textual and voice responses: Users receive feedback both as text and via speech.
- Continual interaction: Users can continue interacting with the bot until they choose to exit.

## Prerequisites

- Python 3.6+
- Necessary Python packages (see below)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/karankadyan/healthcare-chatbot.git
    cd healthcare-chatbot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure you have the required NLTK data packages:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('wordnet')
    ```

5. Place your `intents.json`, `words.pkl`, `classes.pkl`, and `chatbot_model.h5` files in the project directory.

## Running the Application

To start the chatbot application, run:
```bash
streamlit run web.py
```

## Usage

1. When the application starts, the bot will introduce itself.
2. The bot will ask whether you want to continue with a male or female voice.
3. Speak your symptoms clearly to the microphone when prompted.
4. The bot will process your symptoms and provide a response.
5. If you want to continue, say "true". To exit, say "false".

## OS Compatibility

This application currently works with macOS only, as it uses the `os.system("say ...")` command for text-to-speech functionality.

### Using on Windows or Other Operating Systems

For Windows or other operating systems, you can use the `pyttsx3` module for text-to-speech functionality. Here's how you can modify the code to use `pyttsx3`:

1. Install `pyttsx3`:
    ```bash
    pip install pyttsx3
    ```

2. Replace the `os.system("say ...")` commands with `pyttsx3` functions in `web.py`. Here is an example:

    ```python
    import pyttsx3

    engine = pyttsx3.init()

    def speak(text):
        engine.say(text)
        engine.runAndWait()
    ```

3. Replace the `os.system("say '...'")` calls with `speak('...')`.

## Code Explanation

- `web.py`: The main Streamlit application file.
  - Loads the trained model and necessary data.
  - Manages voice interaction using the `speech_recognition` library.
  - Continuously listens to user input and provides responses.

- `intents.json`: Contains the predefined intents and responses.
- `words.pkl` and `classes.pkl`: Pickled files containing the words and classes used by the model.
- `chatbot_model.h5`: The trained model file.

## Troubleshooting

- Ensure your microphone is working correctly.
- If the bot doesn't recognize your voice, speak clearly and ensure there is minimal background noise.
- If you encounter any errors, check the console logs for more details.

## Contributing

Feel free to fork this repository and make improvements. Pull requests are welcome!
