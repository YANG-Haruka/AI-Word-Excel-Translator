import json
import ollama
from ollama._types import Options
import os

LANGUAGE_MAP = {
    "日本語": "ja",
    "中文": "zh",
    "English": "en"
}

def load_prompt(dest_lang):
    """Load the translation prompt from a JSON file based on the target language."""
    lang_code = LANGUAGE_MAP.get(dest_lang, "en")
    prompt_path = f"prompts/{lang_code}.json"  # Assume JSON files are stored in 'prompts' directory
    
    if not os.path.exists(prompt_path):
        print(f"Prompt file not found: {prompt_path}")
        return "Translate the following text:"
    
    try:
        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt_data = json.load(file)
            system_prompt = prompt_data.get("system_prompt", "")
            user_prompt = prompt_data.get("user_prompt", "Translate the following text:")
            return system_prompt, user_prompt
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        return "Translate the following text:", ""

def translate_text(segments, model, src_lang, dest_lang):
    """Translate text segments using the Ollama API."""
    # Load dynamic prompts based on the destination language
    system_prompt, user_prompt = load_prompt(dest_lang)
    
    # Join segments to create the full text to translate
    text_to_translate = segments
    
    messages = [
        {"role": "user", "content": f"{text_to_translate}{user_prompt}"},
        {"role": "system", "content": system_prompt}
    ]
    
    # Send the prompt to Ollama for translation
    response = ollama.chat(
        model=model,
        messages=messages,
        options=Options(num_ctx=10240, num_predict=-1)
    )

    # Check and return translated text
    if response.get('done', False):
        translated_text = response['message']['content']
        return translated_text
    else:
        print("Failed to translate text.")
        return None

def populate_sum_model():
    """Check local Ollama models and return a list of model names."""
    try:
        models = ollama.list()
        if models and 'models' in models:
            model_names = [model['name'] for model in models['models']]
            return model_names
        else:
            return None
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        return None
