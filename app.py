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
        
        # Création d'un dictionnaire pour stocker les informations de la réponse
        api_response_info = {
            'status_code': response.status_code,
            'is_success': response.status_code == 200,
            'headers': dict(response.headers),
            'raw_response': None,
            'error_message': None
        }

        if response.status_code == 200:
            result = response.json()
            api_response_info['raw_response'] = result
            api_response_info['generated_text'] = result['choices'][0]['message']['content']
            api_response_info['model_used'] = result.get('model')
            api_response_info['usage'] = result.get('usage')
            api_response_info['conversation_id'] = result.get('id')
            api_response_info['created_timestamp'] = result.get('created')
            api_response_info['finish_reason'] = result['choices'][0].get('finish_reason')
            
            # Générer la commande cURL (comme avant)
            curl_command = f"""curl --location "https://api.mistral.ai/v1/chat/completions" \\
--header 'Content-Type: application/json' \\
--header 'Accept: application/json' \\
--header "Authorization: Bearer $MISTRAL_API_KEY" \\
--data '{
    "model": "mistral-small-latest",
    "messages": [
        {
            "role": "system",
            "content": "{system_prompt}"
        },
        {
            "role": "user",
            "content": "Voici l\\'avis client à traiter : {review}"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 0.9,
    "presence_penalty": 0.2,
    "frequency_penalty": 0.2
}'"""
            
            return jsonify({
                'status': 'success',
                'api_info': api_response_info,
                'curl_command': curl_command
            })
        else:
            api_response_info['error_message'] = f'Erreur API: {response.status_code}'
            try:
                api_response_info['error_details'] = response.json()
            except:
                api_response_info['error_details'] = response.text

            return jsonify({
                'status': 'error',
                'api_info': api_response_info
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'error_type': type(e).__name__
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)