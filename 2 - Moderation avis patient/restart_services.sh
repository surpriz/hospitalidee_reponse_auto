#!/bin/bash

# Script de redémarrage des services de modération
# À exécuter sur le serveur après déploiement
# Usage: ./restart_services.sh

echo "🔄 Redémarrage des services de modération..."
echo ""

# Variables
APP_DIR="/var/www/surpriz.io/Hospitalidee/moderation_2"
STREAMLIT_PORT="8503"
API_PORT="5004"

# Aller dans le dossier de l'application
cd "$APP_DIR" || exit 1

# Vérifier que les fichiers nécessaires existent
echo "📋 Vérification des fichiers..."
if [ ! -f "app.py" ]; then
    echo "❌ Erreur : app.py non trouvé"
    exit 1
fi

if [ ! -f "streamlit_moderation.py" ]; then
    echo "❌ Erreur : streamlit_moderation.py non trouvé"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "⚠️  Attention : Fichier .env non trouvé"
    echo "   Créez-le avec : echo 'MISTRAL_API_KEY=votre_clé' > .env"
    exit 1
fi

echo "✅ Fichiers vérifiés"
echo ""

# Arrêter les anciens processus
echo "🛑 Arrêt des services existants..."
pkill -f "python.*app.py" 2>/dev/null && echo "   - API Flask arrêtée" || echo "   - API Flask n'était pas en cours d'exécution"
pkill -f "streamlit.*streamlit_moderation.py" 2>/dev/null && echo "   - Streamlit arrêté" || echo "   - Streamlit n'était pas en cours d'exécution"

# Attendre un peu pour s'assurer que les ports sont libérés
sleep 2

echo ""
echo "🚀 Démarrage des nouveaux services..."

# Démarrer l'API Flask
echo "   - Démarrage de l'API Flask sur le port $API_PORT..."
nohup python app.py > api.log 2>&1 &
API_PID=$!
echo "     PID: $API_PID"

# Attendre que l'API soit prête
sleep 3

# Démarrer Streamlit
echo "   - Démarrage de Streamlit sur le port $STREAMLIT_PORT..."
nohup streamlit run streamlit_moderation.py \
    --server.port $STREAMLIT_PORT \
    --server.address 0.0.0.0 \
    --server.headless true \
    > streamlit.log 2>&1 &
STREAMLIT_PID=$!
echo "     PID: $STREAMLIT_PID"

# Attendre un peu
sleep 3

echo ""
echo "🔍 Vérification des services..."

# Vérifier que les processus sont en cours d'exécution
if ps -p $API_PID > /dev/null; then
    echo "✅ API Flask est en cours d'exécution (PID: $API_PID)"
else
    echo "❌ API Flask n'a pas démarré correctement"
    echo "   Vérifiez api.log pour plus de détails"
fi

if ps -p $STREAMLIT_PID > /dev/null; then
    echo "✅ Streamlit est en cours d'exécution (PID: $STREAMLIT_PID)"
else
    echo "❌ Streamlit n'a pas démarré correctement"
    echo "   Vérifiez streamlit.log pour plus de détails"
fi

echo ""
echo "📊 Résumé :"
echo "   - Interface Streamlit : http://83.147.36.59:$STREAMLIT_PORT"
echo "   - API Flask : http://83.147.36.59:$API_PORT"
echo ""
echo "📝 Logs disponibles :"
echo "   - API : tail -f $APP_DIR/api.log"
echo "   - Streamlit : tail -f $APP_DIR/streamlit.log"
echo ""
echo "💡 Pour arrêter les services :"
echo "   pkill -f 'python.*app.py'"
echo "   pkill -f 'streamlit.*streamlit_moderation.py'"