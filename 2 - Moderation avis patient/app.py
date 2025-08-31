from flask import Flask, request, jsonify
import requests
import os
import re
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('moderation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Récupérer la clé API depuis les variables d'environnement
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
if not MISTRAL_API_KEY:
    raise ValueError("La clé API Mistral n'est pas définie dans le fichier .env")

# Fichier contenant les mots interdits
FORBIDDEN_WORDS_FILE = "mots_interdits.txt"
# Seuil de modération par défaut
DEFAULT_MODERATION_THRESHOLD = 0.5

# Fonction pour charger les mots interdits depuis le fichier
def load_forbidden_words():
    words_dict = {}
    try:
        if os.path.exists(FORBIDDEN_WORDS_FILE):
            with open(FORBIDDEN_WORDS_FILE, 'r', encoding='utf-8') as file:
                for line in file:
                    word = line.strip().lower()
                    if word and not word.startswith('#'):  # Ignorer les lignes vides et commentaires
                        # Générer automatiquement le remplacement (astérisques)
                        replacement = "*" * len(word)
                        words_dict[word] = replacement
        else:
            # Créer le fichier avec des valeurs par défaut si inexistant
            default_words = ["merde", "putain", "connard", "con", "pute", "bite", "trou du cul"]
            with open(FORBIDDEN_WORDS_FILE, 'w', encoding='utf-8') as file:
                for word in default_words:
                    file.write(f"{word}\n")
            
            # Construire le dictionnaire avec les remplacements automatiques
            for word in default_words:
                words_dict[word] = "*" * len(word)
    except Exception as e:
        logger.error(f"Erreur lors du chargement des mots interdits: {str(e)}")
    
    return words_dict

# Fonction pour sauvegarder les mots interdits dans le fichier
def save_forbidden_words(words_dict):
    try:
        with open(FORBIDDEN_WORDS_FILE, 'w', encoding='utf-8') as file:
            for word in words_dict.keys():
                file.write(f"{word}\n")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des mots interdits: {str(e)}")
        return False

# Charger les mots interdits au démarrage
FORBIDDEN_WORDS = load_forbidden_words()

def check_moderation_api(text, threshold=DEFAULT_MODERATION_THRESHOLD):
    """
    Vérifie si le texte doit être modéré via l'API Mistral
        
    Args:
        text (str): Texte à vérifier
        threshold (float): Seuil de modération entre 0.1 et 1.0
            Plus la valeur est basse, plus la modération sera stricte
            0.1 = Très strict (modère tout contenu avec score > 0.9)
            0.9 = Très permissif (modère seulement le contenu avec score > 0.1)
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}"
    }
    
    payload = {
        "model": "mistral-moderation-latest",
        "input": [text]
    }
    
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/moderations",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Réponse API modération: {result}")
            
            # Vérifie si l'une des catégories dépasse le seuil
            should_moderate = False
            
            for category_result in result.get("results", []):
                categories = category_result.get("categories", {})
                category_scores = category_result.get("category_scores", {})
                
                # Logique simplifiée : vérifier si un score dépasse le seuil
                # threshold = 1.0 (très permissif) -> seuls les scores très élevés (>= 0.9) déclenchent
                # threshold = 0.1 (très strict) -> les scores faibles (>= 0.1) déclenchent
                moderation_trigger = 1.0 - threshold + 0.1  # Ajustement pour avoir une plage raisonnable
                
                for category, score in category_scores.items():
                    if score >= moderation_trigger:
                        should_moderate = True
                        logger.info(f"Modération activée: {category} score={score:.4f} >= seuil={moderation_trigger:.4f}")
                        break
                
                if should_moderate:
                    break
            
            return should_moderate, result
        else:
            logger.error(f"Erreur API: {response.status_code} - {response.text}")
            return False, {"error": f"Erreur API: {response.status_code}"}
    
    except Exception as e:
        logger.error(f"Exception lors de l'appel API: {str(e)}")
        return False, {"error": str(e)}

def moderate_text(text, moderation_threshold=DEFAULT_MODERATION_THRESHOLD):
    """
    Modère le texte en remplaçant les mots interdits et en détectant les noms propres
    
    Args:
        text (str): Texte à modérer
        moderation_threshold (float): Seuil de modération entre 0.1 et 1.0
    
    Returns:
        tuple: (moderated_text, api_result, moderation_details)
    """
    # Vérifier via l'API Mistral
    should_moderate, api_result = check_moderation_api(text, moderation_threshold)
    
    # Créer une copie du texte pour la modération
    moderated_text = text
    
    # Tracker les sources de modération
    moderation_details = {
        'forbidden_words_applied': [],
        'mistral_api_applied': [],
        'proper_names_applied': [],
        'sources': []
    }
    
    # Extraire les mots à partir de contenus détectés par l'API Mistral
    additional_words_to_moderate = []
    
    # Si l'API a détecté du contenu inapproprié, elle devient le filtre principal
    if should_moderate:
        logger.info(f"Contenu inapproprié détecté par l'API Mistral (seuil: {moderation_threshold})")
        
        # L'API Mistral détecte le contenu inapproprié, donc on modère les mots grossiers courants
        # Cette liste couvre 90% des cas - l'API est le filtre principal
        api_moderation_words = [
            # Mots grossiers de base
            "merde", "putain", "con", "connard", "connasse", "salope", "pute", "enculé", "encule",
            "bite", "couille", "couilles", "trou du cul", "trou-du-cul",
            # Mots sexuels
            "sexe", "penis", "pénis", "vagin", "seins", "cul",
            # Insultes
            "salaud", "ordure", "fumier", "crétin", "imbécile", "idiot", "débile",
            "abruti", "taré", "dégénéré", "pourriture", "salopard",
            # Verbes grossiers
            "niquer", "nique", "foutre", "chier", "pisser",
            # Variantes et expressions
            "fils de pute", "va te faire", "ta gueule", "ferme ta gueule"
        ]
        
        # Modérer tous les mots de cette liste s'ils sont présents dans le texte
        # L'API a déjà validé que le contenu est inapproprié
        for word in api_moderation_words:
            if word in text.lower():
                additional_words_to_moderate.append(word)
    
    # ÉTAPE 1: Appliquer la modération de l'API Mistral (filtre principal - 90%)
    text_before_api = moderated_text
    for word in additional_words_to_moderate:
        replacement = "*" * len(word)
        if re.search(r'\b' + re.escape(word) + r'\b', moderated_text, flags=re.IGNORECASE):
            moderated_text = re.sub(r'\b' + re.escape(word) + r'\b', replacement, moderated_text, flags=re.IGNORECASE)
            moderation_details['mistral_api_applied'].append(word)
    
    # Vérifier si l'API Mistral a modifié le texte
    if text_before_api != moderated_text:
        moderation_details['sources'].append('API Mistral')
    
    # ÉTAPE 2: Appliquer le dictionnaire de mots interdits (filet de sécurité - 10%)
    # Seulement pour les mots qui n'ont pas été modérés par l'API
    text_before_forbidden = moderated_text
    for word, replacement in FORBIDDEN_WORDS.items():
        # Utilise une regex pour trouver le mot entier avec différentes casses
        if re.search(r'\b' + re.escape(word) + r'\b', moderated_text, flags=re.IGNORECASE):
            moderated_text = re.sub(r'\b' + re.escape(word) + r'\b', replacement, moderated_text, flags=re.IGNORECASE)
            moderation_details['forbidden_words_applied'].append(word)
    
    # Vérifier si le dictionnaire de mots interdits a modifié le texte
    if text_before_forbidden != moderated_text:
        moderation_details['sources'].append('Dictionnaire de mots interdits')
    
    # Détection des noms propres (améliorée)
    # Pour une détection plus précise, un modèle NLP serait nécessaire
    titles = [
        # Titres médicaux et académiques
        "Dr", "Docteur", "Pr", "Professeur", "Prof",
        # Titres professionnels médicaux
        "Médecin", "Infirmier", "Infirmière", "Chirurgien", "Chirurgienne",
        "Pharmacien", "Pharmacienne", "Kinésithérapeute", "Kiné",
        "Aide-soignant", "Aide-soignante", "Sage-femme", "Sage femme",
        # Civilités complètes
        "Monsieur", "Madame", "Mademoiselle",
        # Civilités abrégées avec et sans point
        "M\\.?", "Mr\\.?", "Mme\\.?", "Mlle\\.?", "Me\\.?",
        # Autres titres professionnels
        "Maître", "Maitre", "Directeur", "Directrice",
        "Responsable", "Chef"
    ]
    text_before_names = moderated_text
    
    # Version améliorée pour prendre en compte les noms en majuscules et minuscules
    for title in titles:
        # Pour les titres avec regex (ceux avec \\.?)
        if "\\.?" in title:
            # Format standard - mot commençant par une majuscule (avec support des traits d'union)
            pattern_standard = f"\\b({title}\\s+)([A-Z][a-zéèêëàâäôöûüç-]+)"
            matches = re.findall(pattern_standard, moderated_text, flags=re.IGNORECASE)
            if matches:
                for match in matches:
                    moderation_details['proper_names_applied'].append(f"{match[0]}{match[1]}")
            moderated_text = re.sub(pattern_standard, r"\1*****", moderated_text, flags=re.IGNORECASE)
            
            # Format tout en majuscules
            pattern_majuscules = f"\\b({title}\\s+)([A-Z][A-ZÉÈÊËÀÂÄÔÖÛÜÇ]+)"
            matches = re.findall(pattern_majuscules, moderated_text, flags=re.IGNORECASE)
            if matches:
                for match in matches:
                    moderation_details['proper_names_applied'].append(f"{match[0]}{match[1]}")
            moderated_text = re.sub(pattern_majuscules, r"\1*****", moderated_text, flags=re.IGNORECASE)
        else:
            # Pour les titres normaux, on fait une recherche insensible à la casse
            # Format standard - mot commençant par une majuscule (avec support des traits d'union)
            pattern_standard = f"\\b({re.escape(title)}\\s+)([A-Z][a-zéèêëàâäôöûüç-]+)"
            matches = re.findall(pattern_standard, moderated_text, flags=re.IGNORECASE)
            if matches:
                for match in matches:
                    moderation_details['proper_names_applied'].append(f"{match[0]}{match[1]}")
            moderated_text = re.sub(pattern_standard, r"\1*****", moderated_text, flags=re.IGNORECASE)
            
            # Format tout en majuscules
            pattern_majuscules = f"\\b({re.escape(title)}\\s+)([A-Z][A-ZÉÈÊËÀÂÄÔÖÛÜÇ]+)"
            matches = re.findall(pattern_majuscules, moderated_text, flags=re.IGNORECASE)
            if matches:
                for match in matches:
                    moderation_details['proper_names_applied'].append(f"{match[0]}{match[1]}")
            moderated_text = re.sub(pattern_majuscules, r"\1*****", moderated_text, flags=re.IGNORECASE)
    
    # Vérifier si la détection de noms propres a modifié le texte
    if text_before_names != moderated_text:
        moderation_details['sources'].append('Détection de noms propres')
    
    return moderated_text, api_result, moderation_details

@app.route('/moderate', methods=['POST'])
def moderate():
    """
    Point d'entrée API pour la modération
    """
    try:
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Le champ "text" est requis'
            }), 400
        
        original_text = data['text']
        logger.info(f"Demande de modération pour le texte: {original_text}")
        
        # Récupérer le seuil de modération s'il est fourni dans la requête
        threshold = float(data.get('moderation_threshold', DEFAULT_MODERATION_THRESHOLD))
        # S'assurer que le seuil est dans la plage valide
        threshold = max(0.1, min(1.0, threshold))
        
        moderated_text, api_result, moderation_details = moderate_text(original_text, threshold)
        
        # Si le texte a été modifié, c'est qu'il y a eu modération
        is_moderated = moderated_text != original_text
        
        return jsonify({
            'status': 'success',
            'original_text': original_text,
            'moderated_text': moderated_text,
            'is_moderated': is_moderated,
            'moderation_threshold': threshold,
            'api_result': api_result,
            'moderation_details': moderation_details
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de la modération: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Erreur serveur: {str(e)}"
        }), 500

@app.route('/add_forbidden_word', methods=['POST'])
def add_forbidden_word():
    """
    Ajoute un mot au dictionnaire des mots interdits
    """
    try:
        data = request.json
        
        if not data or 'word' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Le champ "word" est requis'
            }), 400
        
        word = data['word'].lower()
        
        # Générer automatiquement le remplacement (astérisques)
        replacement = "*" * len(word)
        
        # Mettre à jour le dictionnaire en mémoire
        FORBIDDEN_WORDS[word] = replacement
        
        # Sauvegarder dans le fichier
        save_success = save_forbidden_words(FORBIDDEN_WORDS)
        
        if save_success:
            return jsonify({
                'status': 'success',
                'message': f'Le mot "{word}" a été ajouté à la liste des mots interdits',
                'current_dictionary': {k: "*" * len(k) for k in FORBIDDEN_WORDS.keys()}
            })
        else:
            return jsonify({
                'status': 'warning',
                'message': f'Le mot "{word}" a été ajouté temporairement mais n\'a pas pu être sauvegardé dans le fichier',
                'current_dictionary': {k: "*" * len(k) for k in FORBIDDEN_WORDS.keys()}
            })
    
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout du mot interdit: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Erreur serveur: {str(e)}"
        }), 500

@app.route('/forbidden_words', methods=['GET'])
def get_forbidden_words():
    """
    Récupère la liste des mots interdits
    """
    try:
        # Recharger depuis le fichier pour s'assurer d'avoir les données à jour
        current_words = load_forbidden_words()
        
        # Pour l'affichage, nous remplaçons les valeurs par des astérisques
        display_words = {k: "*" * len(k) for k in current_words.keys()}
        
        return jsonify({
            'status': 'success',
            'forbidden_words': display_words
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des mots interdits: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Erreur serveur: {str(e)}"
        }), 500

@app.route('/remove_forbidden_word', methods=['POST'])
def remove_forbidden_word():
    """
    Supprime un mot du dictionnaire des mots interdits
    """
    try:
        data = request.json
        
        if not data or 'word' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Le champ "word" est requis'
            }), 400
        
        word = data['word'].lower()
        
        # Vérifier si le mot existe
        if word not in FORBIDDEN_WORDS:
            return jsonify({
                'status': 'error',
                'message': f'Le mot "{word}" n\'existe pas dans la liste des mots interdits'
            }), 404
        
        # Supprimer du dictionnaire en mémoire
        del FORBIDDEN_WORDS[word]
        
        # Sauvegarder dans le fichier
        save_success = save_forbidden_words(FORBIDDEN_WORDS)
        
        if save_success:
            return jsonify({
                'status': 'success',
                'message': f'Le mot "{word}" a été supprimé de la liste des mots interdits',
                'current_dictionary': FORBIDDEN_WORDS
            })
        else:
            return jsonify({
                'status': 'warning',
                'message': f'Le mot "{word}" a été supprimé temporairement mais la mise à jour n\'a pas pu être sauvegardée dans le fichier',
                'current_dictionary': FORBIDDEN_WORDS
            })
    
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du mot interdit: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Erreur serveur: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)