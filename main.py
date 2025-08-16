from flask import Flask, render_template, request, jsonify
from openai import OpenAI  # Updated import
import anthropic
import google.generativeai as genai
import os

appwebChatAI = Flask(__name__)

# Set up API keys (replace with your actual API keys)
openai_api_key = "your_openai_api_key"
anthropic_api_key = "your_anthropic_api_key"
os.environ["GOOGLE_API_KEY"] = "your_google_api_key"

# Initialize OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

@appwebChatAI.route('/')
def index():
    return render_template('index.html')

@appwebChatAI.route('/generate', methods=['POST'])
def generate():
    data = request.json
    model = data['model']
    prompt = data['prompt']
    temperature = float(data['temperature'])

    if model == 'chatgpt':
        response = generate_chatgpt(prompt, temperature)
    elif model == 'claude':
        response = generate_claude(prompt, temperature)
    elif model == 'gemini':
        response = generate_gemini(prompt, temperature)
    else:
        return jsonify({'error': 'Invalid model selected'})

    return jsonify(response)

def generate_chatgpt(prompt, temperature):
    try:
        completion = openai_client.chat.completions.create(
            model="GPT",  # Corrected model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return {
            'text': completion.choices[0].message.content,
            'tokens': completion.usage.total_tokens
        }
    except Exception as e:
        return {'error': str(e)}

def generate_claude(prompt, temperature):
    try:
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        message = client.messages.create(
            model="Claude",
            max_tokens=4000,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return {
            'text': message.content[0].text,
            'tokens': message.usage.input_tokens + message.usage.output_tokens
        }
    except Exception as e:
        return {'error': str(e)}

def generate_gemini(prompt, temperature):
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        model = genai.GenerativeModel("Gemini")
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=temperature))
        return {
            'text': response.text,
            'tokens': len(response.text.split())  # appwebChatAIroximation, as Gemini doesn't provide token count
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    appwebChatAI.run(debug=True)
    appwebChatAI.run(port=5001)