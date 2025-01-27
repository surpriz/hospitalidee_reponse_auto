# Testeur API Mistral

Une interface web simple pour tester l'API Mistral AI, permettant de générer des réponses à des avis clients en utilisant l'intelligence artificielle.

## 🚀 Fonctionnalités

- Interface utilisateur intuitive
- Personnalisation du prompt système
- Visualisation de la réponse générée
- Affichage des informations détaillées de l'API
- Génération de commandes cURL
- Statistiques d'utilisation des tokens

## 📋 Prérequis

- Python 3.7+
- Flask
- Compte Mistral AI avec une clé API valide
- Accès à l'API Mistral AI

## 🛠 Installation

1. Clonez le repository :
```bash
git clone https://github.com/votre-username/testeur-api-mistral.git
cd testeur-api-mistral
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Créez un fichier `.env` à la racine du projet :
```
MISTRAL_API_KEY=votre_clé_api_mistral
```

## 🚦 Démarrage

1. Lancez l'application :
```bash
python app.py
```

2. Ouvrez votre navigateur et accédez à :
```
http://localhost:5000
```

## 💻 Utilisation

1. Personnalisez le prompt système selon vos besoins
2. Entrez l'avis client à traiter
3. Cliquez sur "Générer la réponse"
4. Visualisez la réponse générée et les informations détaillées de l'API

## 🔒 Configuration

Les paramètres de l'API peuvent être ajustés dans le fichier `app.py` :
- Modèle utilisé : `mistral-small-latest`
- Température : 0.7
- Tokens maximum : 500
- Top P : 0.9
- Presence penalty : 0.2
- Frequency penalty : 0.2

## 📦 Structure du projet

```
testeur-api-mistral/
│
├── app.py             # Application Flask principale
├── templates/         # Dossier des templates
│   └── index.html    # Interface utilisateur
├── .env              # Variables d'environnement
└── README.md         # Documentation
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Push sur la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ⚠️ Note importante

N'oubliez pas de ne jamais partager votre clé API Mistral publiquement et de la garder sécurisée dans votre fichier `.env`.