import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Modération d'avis clients",
    page_icon="🔍",
    layout="wide"
)

# Définition des variables globales
API_URL = "http://localhost:5004"  # URL de l'API de modération

# Fonction pour appeler l'API de modération
def moderate_text(text, threshold=0.5):
    try:
        response = requests.post(
            f"{API_URL}/moderate",
            json={"text": text, "moderation_threshold": threshold},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API: {str(e)}")
        return None

# Fonction pour ajouter un mot au dictionnaire des mots interdits
def add_forbidden_word(word):
    try:
        response = requests.post(
            f"{API_URL}/add_forbidden_word",
            json={"word": word},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'ajout du mot interdit: {str(e)}")
        return None

# Fonction pour supprimer un mot du dictionnaire des mots interdits
def remove_forbidden_word(word):
    try:
        response = requests.post(
            f"{API_URL}/remove_forbidden_word",
            json={"word": word},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la suppression du mot interdit: {str(e)}")
        return None

# Fonction pour récupérer la liste des mots interdits
def get_forbidden_words():
    try:
        response = requests.get(
            f"{API_URL}/forbidden_words",
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json().get('forbidden_words', {})
        else:
            st.error(f"Erreur API ({response.status_code}): {response.text}")
            return {}
    except Exception as e:
        st.error(f"Erreur lors de la récupération des mots interdits: {str(e)}")
        return {}

# Titre de l'application
st.title("🔍 Modération d'avis clients")
st.markdown("---")

# Créer deux colonnes principales
col1, col2 = st.columns([3, 2])

with col1:
    st.header("Test de modération")
    
    # Zone de texte pour l'avis à modérer
    review = st.text_area(
        "Saisissez un avis à modérer :",
        value="Docteur Durant m'a traité comme une merde et c'est un trou du cul",
        height=150
    )
    
    # Slider pour le seuil de modération
    threshold = st.slider(
        "Seuil de modération (0.1 - 1.0):",
        min_value=0.1,
        max_value=1.0,
        value=1.0,
        step=0.05,
        help="Plus la valeur est basse, plus la modération sera stricte"
    )
    
    # Afficher le niveau de modération de manière plus visuelle
    level_col1, level_col2 = st.columns([1, 3])
    with level_col1:
        st.write("Niveau:")
    with level_col2:
        if threshold <= 0.3:
            st.write("🔴 Très strict")
        elif threshold <= 0.5:
            st.write("🟠 Strict")
        elif threshold <= 0.7:
            st.write("🟡 Modéré")
        elif threshold <= 0.9:
            st.write("🟢 Permissif")
        else:
            st.write("🔵 Très permissif (Recommandé)")
    
    # Bouton pour modérer l'avis
    if st.button("Modérer l'avis", key="moderate_btn"):
        if review:
            with st.spinner("Modération en cours..."):
                result = moderate_text(review, threshold)
                
                if result and result.get('status') == 'success':
                    # Afficher les résultats avec mise en forme
                    st.subheader("Résultat de la modération")
                    
                    col_orig, col_mod = st.columns(2)
                    
                    with col_orig:
                        st.markdown("**Texte original :**")
                        st.info(result.get('original_text', ''))
                    
                    with col_mod:
                        st.markdown("**Texte modéré :**")
                        st.success(result.get('moderated_text', ''))
                    
                    # Informations sur la source de modération
                    moderation_details = result.get('moderation_details', {})
                    sources = moderation_details.get('sources', [])
                    
                    if sources:
                        st.subheader("🔍 Source(s) de modération")
                        for source in sources:
                            if source == 'Dictionnaire de mots interdits':
                                st.info(f"📚 **{source}** - Mots détectés: {', '.join(moderation_details.get('forbidden_words_applied', []))}")
                            elif source == 'API Mistral':
                                st.warning(f"🤖 **{source}** - Contenu détecté par l'IA")
                                if moderation_details.get('mistral_api_applied'):
                                    st.write(f"Mots modérés: {', '.join(moderation_details.get('mistral_api_applied', []))}")
                            elif source == 'Détection de noms propres':
                                st.success(f"👤 **{source}** - Noms détectés: {', '.join(moderation_details.get('proper_names_applied', []))}")
                    
                    # Fonction pour détecter les mots potentiellement non modérés
                    def detect_unmoderated_words(original, moderated):
                        """Détecte les mots potentiellement grossiers non modérés"""
                        import re
                        
                        # Mots suspects à vérifier (liste étendue)
                        suspect_words = [
                            'connasse', 'salope', 'pute', 'putain', 'merde', 'con', 'connard', 
                            'enculé', 'bite', 'couille', 'trou du cul', 'crétin', 'imbécile',
                            'débile', 'abruti', 'taré', 'ordure', 'fumier', 'salopard',
                            'chier', 'pisser', 'niquer', 'foutre', 'salaud'
                        ]
                        
                        original_words = re.findall(r'\b\w+\b', original.lower())
                        moderated_words = re.findall(r'\b\w+\b', moderated.lower())
                        
                        # Trouver les mots suspects qui sont encore présents (non modérés)
                        unmoderated = []
                        for word in suspect_words:
                            if word in original_words and word in moderated_words:
                                unmoderated.append(word)
                        
                        return unmoderated
                    
                    # Détecter les mots non modérés
                    unmoderated_words = detect_unmoderated_words(result.get('original_text', ''), result.get('moderated_text', ''))
                    
                    if unmoderated_words:
                        st.subheader("⚠️ Mots potentiellement non modérés")
                        st.warning(f"Ces mots n'ont pas été modérés : **{', '.join(unmoderated_words)}**")
                        
                        # Interface pour ajouter rapidement à la liste des mots interdits
                        st.write("💡 **Action rapide :** Ajouter ces mots à la liste des mots interdits ?")
                        
                        col_words, col_action = st.columns([3, 1])
                        
                        with col_words:
                            selected_words = st.multiselect(
                                "Sélectionner les mots à ajouter :",
                                options=unmoderated_words,
                                default=unmoderated_words,
                                key="quick_add_words"
                            )
                        
                        with col_action:
                            st.write("")  # Espacement
                            if st.button("➕ Ajouter", key="quick_add_btn", help="Ajouter les mots sélectionnés à la liste des mots interdits"):
                                if selected_words:
                                    success_count = 0
                                    for word in selected_words:
                                        add_result = add_forbidden_word(word)
                                        if add_result and add_result.get('status') in ['success', 'warning']:
                                            success_count += 1
                                    
                                    if success_count > 0:
                                        st.success(f"✅ {success_count} mot(s) ajouté(s) avec succès !")
                                        st.rerun()
                                    else:
                                        st.error("❌ Échec de l'ajout des mots.")
                                else:
                                    st.warning("Veuillez sélectionner au moins un mot.")
                    
                    # Informations supplémentaires
                    with st.expander("Détails techniques de l'API Mistral"):
                        # Afficher le seuil de modération utilisé
                        st.markdown(f"**Seuil de modération appliqué :** {result.get('moderation_threshold', threshold)}")
                        
                        # Présentation plus propre des scores par catégorie
                        api_result = result.get('api_result', {})
                        if 'results' in api_result and len(api_result['results']) > 0:
                            scores = api_result['results'][0].get('category_scores', {})
                            categories = api_result['results'][0].get('categories', {})
                            
                            # Créer un DataFrame pour afficher les scores et les flags
                            scores_df = pd.DataFrame({
                                'Catégorie': list(scores.keys()),
                                'Score': list(scores.values()),
                                'Flag': [categories.get(cat, False) for cat in scores.keys()]
                            })
                            
                            # Tri par score décroissant
                            scores_df = scores_df.sort_values(by='Score', ascending=False)
                            
                            # Affichage sous forme de tableau
                            st.dataframe(scores_df, use_container_width=True)
                        else:
                            st.json(api_result)
                else:
                    st.error("Échec de la modération. Veuillez réessayer.")
        else:
            st.warning("Veuillez saisir un texte à modérer.")
    
    # Espace supplémentaire pour équilibrer l'interface
    st.markdown("&nbsp;")
    st.markdown("&nbsp;")

with col2:
    st.header("Gestion des mots interdits")
    
    # Information sur le fichier des mots interdits
    st.info("Les mots interdits sont stockés dans le fichier 'mots_interdits.txt'. Vous pouvez modifier ce fichier directement ou utiliser cette interface.")
    
    # Récupérer la liste actuelle des mots interdits
    forbidden_words = get_forbidden_words()
    
    # Afficher la liste des mots interdits
    st.subheader("Liste des mots interdits")
    
    if forbidden_words:
        # Convertir en DataFrame pour un affichage plus propre
        forbidden_df = pd.DataFrame({
            'Mot': list(forbidden_words.keys()),
            'Remplacement': list(forbidden_words.values())
        })
        
        # Ajouter des boutons de suppression pour chaque mot
        col_list, col_action = st.columns([3, 1])
        
        with col_list:
            st.dataframe(forbidden_df, use_container_width=True)
        
        with col_action:
            st.markdown("### Actions")
            selected_word = st.selectbox("Sélectionner un mot à supprimer:", 
                                      options=list(forbidden_words.keys()),
                                      index=None,
                                      placeholder="Choisir un mot...")
            
            if selected_word and st.button("Supprimer", key="delete_btn"):
                result = remove_forbidden_word(selected_word)
                if result and result.get('status') == 'success':
                    st.success(f"Mot '{selected_word}' supprimé avec succès !")
                    st.rerun()
                else:
                    st.error("Échec de la suppression du mot.")
    else:
        st.info("Aucun mot interdit défini ou impossible de récupérer la liste.")
    
    # Formulaire pour ajouter un nouveau mot interdit
    st.subheader("Ajouter un mot interdit")
    
    with st.form("add_word_form"):
        new_word = st.text_input("Mot à interdire :")
        
        submitted = st.form_submit_button("Ajouter")
        
        if submitted and new_word:
            result = add_forbidden_word(new_word)
            if result and result.get('status') in ['success', 'warning']:
                st.success(result.get('message', 'Mot ajouté avec succès !'))
                st.rerun()
            else:
                st.error("Échec de l'ajout du mot interdit.")

# Pied de page
st.markdown("---")
st.markdown("**Application de modération** - Développée pour la modération automatique d'avis clients")