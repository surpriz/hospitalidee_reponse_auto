#!/bin/bash

# Script de déploiement vers le serveur de production
# Usage: ./deploy.sh

echo "🚀 Déploiement de l'application de modération..."

# Variables
SERVER="83.147.36.59"
USER="administrator"
REMOTE_PATH="/var/www/surpriz.io/Hospitalidee/moderation_2"
LOCAL_PATH="/Users/jerome_laval/Desktop/Projects/Hospitalidee/Generer_reponse/2 - Moderation avis patient"

echo "📦 Synchronisation des fichiers vers $SERVER..."
echo "   (Le mot de passe ne sera demandé qu'une seule fois)"
echo ""

# Utiliser rsync pour copier tous les fichiers en une seule connexion
rsync -avz --progress \
    --exclude 'venv/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '*.log' \
    --exclude '.DS_Store' \
    --exclude 'Archives/' \
    --exclude '*.png' \
    --exclude '*.jpg' \
    --exclude '.env.local' \
    --exclude 'test_*.py' \
    --include '.gitignore' \
    --include 'app.py' \
    --include 'streamlit_moderation.py' \
    --include 'requirements.txt' \
    --include 'mots_interdits.txt' \
    --include '*.md' \
    "$LOCAL_PATH/app.py" \
    "$LOCAL_PATH/streamlit_moderation.py" \
    "$LOCAL_PATH/requirements.txt" \
    "$LOCAL_PATH/mots_interdits.txt" \
    "$LOCAL_PATH/"*.md \
    "$LOCAL_PATH/.gitignore" \
    "$USER@$SERVER:$REMOTE_PATH/"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Déploiement réussi!"
    echo ""
    echo "📝 Pour finaliser la mise à jour sur le serveur :"
    echo ""
    echo "1️⃣  Connectez-vous au serveur :"
    echo "    ssh $USER@$SERVER"
    echo ""
    echo "2️⃣  Allez dans le dossier de l'application :"
    echo "    cd $REMOTE_PATH"
    echo ""
    echo "3️⃣  Vérifiez/créez le fichier .env avec votre clé API :"
    echo "    echo 'MISTRAL_API_KEY=votre_clé_ici' > .env"
    echo ""
    echo "4️⃣  Redémarrez les services :"
    echo "    # Arrêter les anciens processus"
    echo "    pkill -f 'python.*app.py' || true"
    echo "    pkill -f 'streamlit.*streamlit_moderation.py' || true"
    echo ""
    echo "    # Redémarrer l'API Flask (en arrière-plan)"
    echo "    nohup python app.py > api.log 2>&1 &"
    echo ""
    echo "    # Redémarrer Streamlit (en arrière-plan)"
    echo "    nohup streamlit run streamlit_moderation.py --server.port 8503 > streamlit.log 2>&1 &"
    echo ""
    echo "5️⃣  Vérifiez que tout fonctionne :"
    echo "    - Interface Streamlit : http://83.147.36.59:8503"
    echo "    - API Flask : http://83.147.36.59:5004"
    echo ""
    echo "💡 Astuce : Utilisez 'screen' ou 'tmux' pour des sessions persistantes"
else
    echo ""
    echo "❌ Erreur lors du déploiement"
    echo "   Vérifiez votre connexion et vos identifiants"
fi