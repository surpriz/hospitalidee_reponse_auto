# app.py
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Récupérer la clé API depuis les variables d'environnement
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.json
    review = data.get('review')
    system_prompt = data.get('system_prompt')
    
    # Préparer la requête pour Mistral API
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {MISTRAL_API_KEY}'
    }
    
    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Voici l'avis client à traiter : {review}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 0.9,
        "presence_penalty": 0.2,
        "frequency_penalty": 0.2
    }
    
    try:
        # Faire l'appel à l'API Mistral
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            
            # Générer la commande cURL correspondante
            curl_command = f"""curl --location "https://api.mistral.ai/v1/chat/completions" \\
--header 'Content-Type: application/json' \\
--header 'Accept: application/json' \\
--header "Authorization: Bearer $MISTRAL_API_KEY" \\
--data '{{
    "model": "mistral-small-latest",
    "messages": [
        {{
            "role": "system",
            "content": "{system_prompt}"
        }},
        {{
            "role": "user",
            "content": "Voici l'\\'avis client à traiter : {review}"
        }}
    ],
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 0.9,
    "presence_penalty": 0.2,
    "frequency_penalty": 0.2
}}'"""
            
            return jsonify({
                'status': 'success',
                'response': generated_text,
                'curl_command': curl_command
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Erreur API: {response.status_code}'
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)