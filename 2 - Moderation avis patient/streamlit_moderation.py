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

# Fonction pour récupérer la configuration des flags
def get_flag_config():
    try:
        response = requests.get(
            f"{API_URL}/get_flag_config",
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json().get('flag_config', {})
        else:
            st.error(f"Erreur API ({response.status_code}): {response.text}")
            return {}
    except Exception as e:
        st.error(f"Erreur lors de la récupération de la configuration des flags: {str(e)}")
        return {}

# Fonction pour mettre à jour la configuration des flags
def update_flag_config(config):
    try:
        response = requests.post(
            f"{API_URL}/update_flag_config",
            json={"flag_config": config},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la mise à jour de la configuration des flags: {str(e)}")
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

# Date et heure de dernière mise à jour du code (à modifier manuellement lors des mises à jour)
# Format : "Jour Mois Année - HHhMM"
LAST_UPDATE = "31 Août 2025 - 17h51"

# Afficher avec un badge de mise à jour
col_title, col_update = st.columns([3, 1])
with col_update:
    st.markdown(
        f"""
        <div style="text-align: right; padding: 10px 0;">
            <span style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 5px; font-size: 12px;">
                ✓ Last update : {LAST_UPDATE}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# Créer des onglets pour organiser l'interface
tab1, tab2, tab3 = st.tabs(["🔍 Test de modération", "📋 Gestion des mots", "⚙️ Configuration des flags"])

with tab1:

    # Section de test de modération
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
                    # Afficher le flag en premier avec une mise en forme visuelle
                    flag = result.get('flag', 'UNKNOWN')
                    flag_reasons = result.get('flag_reasons', [])
                    
                    st.subheader("🚦 Décision de filtrage automatique")
                    
                    flag_col, reason_col = st.columns([1, 2])
                    
                    with flag_col:
                        if flag == "RED":
                            st.markdown(
                                """
                                <div style="text-align: center; padding: 20px; background-color: #ffebee; border-radius: 10px; border-left: 5px solid #f44336;">
                                    <h2 style="color: #d32f2f; margin: 0;">🔴 FLAG RED</h2>
                                    <p style="margin: 5px 0 0 0; color: #d32f2f;"><strong>Vérification humaine requise</strong></p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        elif flag == "GREEN":
                            st.markdown(
                                """
                                <div style="text-align: center; padding: 20px; background-color: #e8f5e8; border-radius: 10px; border-left: 5px solid #4caf50;">
                                    <h2 style="color: #2e7d32; margin: 0;">🟢 FLAG GREEN</h2>
                                    <p style="margin: 5px 0 0 0; color: #2e7d32;"><strong>Publication automatique possible</strong></p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.warning(f"Flag inconnu: {flag}")
                    
                    with reason_col:
                        st.markdown("**Raisons de la décision :**")
                        if flag_reasons:
                            for reason in flag_reasons:
                                if flag == "RED":
                                    st.markdown(f"• ⚠️ {reason}")
                                else:
                                    st.markdown(f"• ✅ {reason}")
                        else:
                            st.markdown("Aucune raison fournie")
                    
                    st.markdown("---")
                    
                    # Afficher les résultats avec mise en forme
                    st.subheader("📝 Détails de la modération")
                    
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
    

with tab2:
    st.header("📋 Gestion des mots interdits")
    
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

with tab3:
    st.header("⚙️ Configuration des flags RED/GREEN")
    
    # Information sur le système de flags
    st.info(
        """
        🚦 **Système de flags automatiques** :
        - **🔴 FLAG RED** : L'avis nécessite une vérification humaine avant publication
        - **🟢 FLAG GREEN** : L'avis peut être publié automatiquement
        
        Ajustez les seuils ci-dessous pour calibrer le comportement du système.
        """
    )
    
    # Récupérer la configuration actuelle
    current_config = get_flag_config()
    
    if current_config:
        st.subheader("🎯 Configuration des seuils")
        
        with st.form("flag_config_form"):
            # Seuil API Mistral
            api_threshold = st.slider(
                "Seuil API Mistral (score maximum acceptable)",
                min_value=0.0,
                max_value=1.0,
                value=float(current_config.get('mistral_api_score_threshold', 0.3)),
                step=0.05,
                help="Si le score de l'API Mistral dépasse ce seuil, l'avis aura un FLAG RED"
            )
            
            col_checkboxes1, col_checkboxes2 = st.columns(2)
            
            with col_checkboxes1:
                # Mots interdits
                forbidden_words_trigger = st.checkbox(
                    "Mots interdits → FLAG RED",
                    value=current_config.get('forbidden_words_trigger_red', True),
                    help="Si des mots interdits sont détectés, l'avis aura un FLAG RED"
                )
                
                # Noms propres
                proper_names_trigger = st.checkbox(
                    "Noms propres → FLAG RED",
                    value=current_config.get('proper_names_trigger_red', True),
                    help="Si des noms propres sont détectés (RGPD), l'avis aura un FLAG RED"
                )
            
            with col_checkboxes2:
                # Modification du texte
                text_modification_trigger = st.checkbox(
                    "Texte modifié → FLAG RED",
                    value=current_config.get('text_modification_trigger_red', True),
                    help="Si le texte a été modifié par la modération, l'avis aura un FLAG RED"
                )
            
            # Affichage prévisionnel du comportement
            st.markdown("---")
            st.subheader("🔮 Prévision du comportement")
            
            behavior_col1, behavior_col2 = st.columns(2)
            
            with behavior_col1:
                st.markdown("🔴 **FLAG RED sera attribué si :**")
                red_conditions = []
                if api_threshold < 1.0:
                    red_conditions.append(f"• Score API Mistral > {api_threshold}")
                if forbidden_words_trigger:
                    red_conditions.append("• Mots interdits détectés")
                if proper_names_trigger:
                    red_conditions.append("• Noms propres détectés")
                if text_modification_trigger:
                    red_conditions.append("• Texte a été modifié")
                
                if red_conditions:
                    for condition in red_conditions:
                        st.markdown(condition)
                else:
                    st.markdown("• Aucune condition activée (tous les avis seront GREEN)")
            
            with behavior_col2:
                st.markdown("🟢 **FLAG GREEN sera attribué si :**")
                st.markdown("• Aucune des conditions RED n'est remplie")
                st.markdown("• Score API Mistral faible")
                st.markdown("• Pas de contenu problématique détecté")
            
            # Bouton de sauvegarde
            submitted = st.form_submit_button("💾 Sauvegarder la configuration", type="primary")
            
            if submitted:
                new_config = {
                    'mistral_api_score_threshold': api_threshold,
                    'forbidden_words_trigger_red': forbidden_words_trigger,
                    'proper_names_trigger_red': proper_names_trigger,
                    'text_modification_trigger_red': text_modification_trigger
                }
                
                result = update_flag_config(new_config)
                if result and result.get('status') in ['success', 'warning']:
                    st.success("✅ Configuration sauvegardée avec succès !")
                    st.rerun()
                else:
                    st.error("❌ Échec de la sauvegarde de la configuration.")
        
        # Statistiques et informations supplémentaires
        st.markdown("---")
        st.subheader("📊 Conseils d'utilisation")
        
        col_tips1, col_tips2 = st.columns(2)
        
        with col_tips1:
            st.markdown(
                """
                **📈 Pour un filtrage plus strict :**
                - Réduire le seuil API Mistral (ex: 0.2)
                - Activer tous les triggers
                - Tester avec différents exemples
                """
            )
        
        with col_tips2:
            st.markdown(
                """
                **📉 Pour un filtrage plus permissif :**
                - Augmenter le seuil API Mistral (ex: 0.5)
                - Désactiver certains triggers
                - Surveiller les faux négatifs
                """
            )
    
    else:
        st.error("Impossible de récupérer la configuration actuelle des flags.")

# Pied de page
st.markdown("---")
st.markdown("**Application de modération** - Développée pour la modération automatique d'avis clients")