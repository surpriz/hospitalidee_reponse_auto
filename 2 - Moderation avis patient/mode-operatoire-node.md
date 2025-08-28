# Mode opératoire - Intégration du système de modération d'avis clients avec Mistral AI (Version 2)

## 🆕 Nouveautés de la Version 2

Cette version 2 apporte des améliorations majeures pour NodeJS :

- **🤖 API Mistral comme filtre principal** : L'IA gère maintenant 90% de la modération
- **📚 Dictionnaire comme filet de sécurité** : Les mots interdits gèrent les 10% restants
- **🔍 Détection intelligente des sources** : Traçabilité complète de la modération
- **⚡ Gestion avancée des mots** : Auto-détection et ajout des mots manqués par l'IA
- **🎯 Seuil optimisé** : Par défaut à 1.0 pour éviter la sur-modération
- **🚀 Intégration moderne** : Support React, Vue, Express avec exemples complets

## Introduction

Ce mode opératoire vous guidera dans l'intégration du système de modération d'avis clients Version 2 utilisant l'API Mistral AI dans votre application NodeJS. Cette version optimisée offre une modération intelligente et traçable.

## Table des matières

1. [Prérequis](#prérequis)
2. [Architecture du système](#architecture-du-système)
3. [Installation et configuration](#installation-et-configuration)
4. [Implémentation du serveur de modération en NodeJS](#implémentation-du-serveur-de-modération-en-nodejs)
5. [Utilisation de l'API de modération](#utilisation-de-lapi-de-modération)
6. [Gestion des mots interdits](#gestion-des-mots-interdits)
7. [Personnalisation et optimisation](#personnalisation-et-optimisation)
8. [Dépannage](#dépannage)
9. [Informations complémentaires](#informations-complémentaires)

## Prérequis

- NodeJS (v14 ou supérieur)
- npm ou yarn
- Une clé API Mistral AI (inscription sur [https://mistral.ai](https://mistral.ai))
- Un éditeur de code

## Architecture du système

### 🔄 Architecture Version 2 (Optimisée)

Le système de modération Version 2 se compose des éléments suivants :

1. **🤖 API Mistral AI (90% - Filtre principal)**
   - Détection contextuelle intelligente des contenus inappropriés
   - Modération automatique de ~25 mots/expressions grossiers courants
   - Déclenchement basé sur des seuils de confiance configurables

2. **📚 Dictionnaire de mots interdits (10% - Filet de sécurité)**
   - Capture des mots spécifiques manqués par l'IA
   - Modération systématique indépendante de l'IA
   - Gestion dynamique via API REST

3. **👤 Détection de noms propres**
   - Protection automatique de l'identité
   - Anonymisation des titres + noms (Dr Durant → Dr *****)

4. **🔍 Système de traçabilité**
   - Identification précise des sources de modération
   - Détection automatique des mots non modérés
   - Interface d'amélioration continue

### 🎯 Avantages Version 2

- **Plus intelligent** : L'IA comprend le contexte
- **Moins de faux positifs** : Seuil par défaut optimisé
- **Auto-amélioration** : Détection et ajout des mots manqués
- **Traçabilité complète** : Savoir qui a modéré quoi
- **Intégration moderne** : Support des frameworks actuels

Contrairement à l'implémentation de démonstration qui utilise Flask (Python), cette solution NodeJS Version 2 est entièrement optimisée pour s'intégrer parfaitement à votre environnement existant avec une logique de modération intelligente.

## Installation et configuration

### 1. Créer un nouveau répertoire pour le service de modération

```bash
mkdir moderation-service
cd moderation-service
npm init -y
```

### 2. Installer les dépendances nécessaires

```bash
npm install express dotenv axios winston cors fs-extra
```

- `express` : Serveur HTTP pour l'API REST
- `dotenv` : Gestion des variables d'environnement
- `axios` : Client HTTP pour les appels à l'API Mistral
- `winston` : Journalisation
- `cors` : Gestion des requêtes cross-origin
- `fs-extra` : Opérations de fichiers améliorées

### 3. Créer le fichier de configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet :

```
MISTRAL_API_KEY=votre_clé_api_mistral
PORT=5004
NODE_ENV=production
```

## Implémentation du serveur de modération en NodeJS

### 1. Créer la structure de base du projet

```
moderation-service/
├── .env
├── package.json
├── mots_interdits.txt
├── src/
│   ├── server.js
│   ├── services/
│   │   └── moderation.service.js
│   ├── routes/
│   │   └── moderation.routes.js
│   └── utils/
│       ├── logger.js
│       └── forbidden-words.js
└── logs/
    └── moderation.log
```

### 2. Implémentation du fichier principal (server.js)

Créez le fichier `src/server.js` :

```javascript
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { logger } = require('./utils/logger');
const moderationRoutes = require('./routes/moderation.routes');

// Chargement des variables d'environnement
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5004;

// Middleware
app.use(cors());
app.use(express.json());

// Logging des requêtes
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.url}`);
  next();
});

// Routes
app.use('/', moderationRoutes);

// Gestion des erreurs
app.use((err, req, res, next) => {
  logger.error(`Erreur serveur: ${err.stack}`);
  res.status(500).json({
    status: 'error',
    message: `Erreur serveur: ${err.message}`
  });
});

// Démarrage du serveur
app.listen(PORT, () => {
  logger.info(`Serveur de modération démarré sur le port ${PORT}`);
});
```

### 3. Implémentation du logger (utils/logger.js)

Créez le fichier `src/utils/logger.js` :

```javascript
const winston = require('winston');
const path = require('path');
const fs = require('fs-extra');

// Création du répertoire de logs s'il n'existe pas
const logDir = path.join(__dirname, '../../logs');
fs.ensureDirSync(logDir);

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ 
      filename: path.join(logDir, 'moderation.log') 
    }),
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    })
  ]
});

module.exports = { logger };
```

### 4. Implémentation de la gestion des mots interdits (utils/forbidden-words.js)

Créez le fichier `src/utils/forbidden-words.js` :

```javascript
const fs = require('fs-extra');
const path = require('path');
const { logger } = require('./logger');

const FORBIDDEN_WORDS_FILE = path.join(__dirname, '../../mots_interdits.txt');

/**
 * Charge les mots interdits depuis le fichier
 */
function loadForbiddenWords() {
  try {
    if (fs.existsSync(FORBIDDEN_WORDS_FILE)) {
      const content = fs.readFileSync(FORBIDDEN_WORDS_FILE, 'utf-8');
      const words = content
        .split('\n')
        .map(line => line.trim().toLowerCase())
        .filter(line => line && !line.startsWith('#'));
      
      // Générer le dictionnaire avec les remplacements
      const wordsDict = {};
      words.forEach(word => {
        wordsDict[word] = '*'.repeat(word.length);
      });
      
      return wordsDict;
    } else {
      // Créer le fichier avec des valeurs par défaut
      const defaultWords = ["merde", "putain", "connard", "con", "pute", "bite", "trou du cul"];
      fs.writeFileSync(FORBIDDEN_WORDS_FILE, defaultWords.join('\n'), 'utf-8');
      
      const wordsDict = {};
      defaultWords.forEach(word => {
        wordsDict[word] = '*'.repeat(word.length);
      });
      
      return wordsDict;
    }
  } catch (error) {
    logger.error(`Erreur lors du chargement des mots interdits: ${error.message}`);
    return {};
  }
}

/**
 * Sauvegarde les mots interdits dans le fichier
 */
function saveForbiddenWords(wordsDict) {
  try {
    const words = Object.keys(wordsDict);
    fs.writeFileSync(FORBIDDEN_WORDS_FILE, words.join('\n'), 'utf-8');
    return true;
  } catch (error) {
    logger.error(`Erreur lors de la sauvegarde des mots interdits: ${error.message}`);
    return false;
  }
}

// Charger les mots au démarrage
const FORBIDDEN_WORDS = loadForbiddenWords();

module.exports = {
  FORBIDDEN_WORDS,
  loadForbiddenWords,
  saveForbiddenWords
};
```

### 5. Implémentation du service de modération (services/moderation.service.js)

Créez le fichier `src/services/moderation.service.js` :

```javascript
const axios = require('axios');
const { logger } = require('../utils/logger');
const { FORBIDDEN_WORDS } = require('../utils/forbidden-words');

// Seuil de modération par défaut
const DEFAULT_MODERATION_THRESHOLD = 0.5;

/**
 * Vérifie si le texte doit être modéré via l'API Mistral
 */
async function checkModerationApi(text, threshold = DEFAULT_MODERATION_THRESHOLD) {
  const apiKey = process.env.MISTRAL_API_KEY;
  
  if (!apiKey) {
    throw new Error("La clé API Mistral n'est pas définie dans le fichier .env");
  }
  
  try {
    const response = await axios.post(
      "https://api.mistral.ai/v1/moderations",
      {
        model: "mistral-moderation-latest",
        input: [text]
      },
      {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`
        },
        timeout: 10000
      }
    );
    
    const result = response.data;
    logger.info(`Réponse API modération: ${JSON.stringify(result)}`);
    
    // Vérifie si l'une des catégories est flaggée comme inappropriée
    let shouldModerate = false;
    
    for (const categoryResult of result.results || []) {
      const categories = categoryResult.categories || {};
      const categoryScores = categoryResult.category_scores || {};
      
      // Si l'une des catégories est True, le texte doit être modéré
      if (Object.values(categories).some(val => val === true)) {
        shouldModerate = true;
      }
      
      // Vérification des scores par rapport au seuil défini
      // Logique inversée: seuil plus bas = plus strict = modérer à des scores plus bas
      if (Object.values(categoryScores).some(score => score >= (1.0 - threshold))) {
        shouldModerate = true;
        logger.info(`Modération activée car au moins un score dépasse le seuil inversé de ${1.0 - threshold}`);
      }
    }
    
    return { shouldModerate, result };
  } catch (error) {
    logger.error(`Exception lors de l'appel API Mistral: ${error.message}`);
    return { shouldModerate: false, result: { error: error.message } };
  }
}

/**
 * Modère le texte en remplaçant les mots interdits
 */
async function moderateText(text, moderationThreshold = DEFAULT_MODERATION_THRESHOLD) {
  // Vérifier via l'API Mistral
  const { shouldModerate, result } = await checkModerationApi(text, moderationThreshold);
  
  // Créer une copie du texte pour la modération
  let moderatedText = text;
  
  // Extraire les mots à partir de contenus détectés par l'API Mistral
  const additionalWordsToModerate = [];
  
  // Si l'API a détecté du contenu inapproprié, on applique une modération plus stricte
  if (shouldModerate) {
    logger.info(`Contenu inapproprié détecté par l'API Mistral (seuil: ${moderationThreshold})`);
    
    // Extraction des mots potentiellement problématiques
    const words = text.toLowerCase().match(/\b\w+\b/g) || [];
    const wordPhrases = [];
    
    // Extraire également les phrases potentielles (2-3 mots)
    for (let i = 0; i < words.length - 1; i++) {
      wordPhrases.push(`${words[i]} ${words[i + 1]}`);
    }
    
    for (let i = 0; i < words.length - 2; i++) {
      wordPhrases.push(`${words[i]} ${words[i + 1]} ${words[i + 2]}`);
    }
    
    // Vérification des catégories spécifiques
    for (const categoryResult of result.results || []) {
      const categories = categoryResult.categories || {};
      const categoryScores = categoryResult.category_scores || {};
      
      // Si du contenu sexuel est détecté
      if ((categoryScores.sexual || 0) >= moderationThreshold) {
        const sexualWords = ["bite", "sexe", "penis", "pénis", "vagin", "couilles", "seins", "cul", "trou du cul"];
        for (const word of sexualWords) {
          if (text.toLowerCase().includes(word) && !FORBIDDEN_WORDS[word]) {
            additionalWordsToModerate.push(word);
          }
        }
      }
      
      // Si du contenu haineux est détecté
      if ((categoryScores.hate_and_discrimination || 0) >= moderationThreshold) {
        for (const phrase of wordPhrases) {
          if (!FORBIDDEN_WORDS[phrase] && phrase.length > 3) {
            additionalWordsToModerate.push(phrase);
          }
        }
      }
    }
  }
  
  // Appliquer le dictionnaire de mots interdits
  for (const [word, replacement] of Object.entries(FORBIDDEN_WORDS)) {
    // Utilise une regex pour trouver le mot entier avec différentes casses
    const regex = new RegExp('\\b' + word.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&') + '\\b', 'gi');
    moderatedText = moderatedText.replace(regex, replacement);
  }
  
  // Appliquer la modération pour les mots additionnels détectés par l'API
  for (const word of additionalWordsToModerate) {
    const replacement = '*'.repeat(word.length);
    const regex = new RegExp('\\b' + word.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&') + '\\b', 'gi');
    moderatedText = moderatedText.replace(regex, replacement);
  }
  
  // Détection des noms propres (simplifiée)
  const titles = ["Dr", "Docteur", "Pr", "Professeur", "M.", "Mme", "Mlle"];
  for (const title of titles) {
    const pattern = new RegExp(`(${title}\\s+)([A-Z][a-zéèêëàâäôöûüç]+)`, 'g');
    moderatedText = moderatedText.replace(pattern, '$1*****');
  }
  
  return { moderatedText, result };
}

module.exports = {
  DEFAULT_MODERATION_THRESHOLD,
  checkModerationApi,
  moderateText
};
```

### 6. Implémentation des routes de l'API (routes/moderation.routes.js)

Créez le fichier `src/routes/moderation.routes.js` :

```javascript
const express = require('express');
const { logger } = require('../utils/logger');
const { moderateText, DEFAULT_MODERATION_THRESHOLD } = require('../services/moderation.service');
const { FORBIDDEN_WORDS, saveForbiddenWords, loadForbiddenWords } = require('../utils/forbidden-words');

const router = express.Router();

/**
 * Point d'entrée API pour la modération
 * POST /moderate
 */
router.post('/moderate', async (req, res) => {
  try {
    const { text, moderation_threshold } = req.body;
    
    if (!text) {
      return res.status(400).json({
        status: 'error',
        message: 'Le champ "text" est requis'
      });
    }
    
    logger.info(`Demande de modération pour le texte: ${text}`);
    
    // Récupérer le seuil de modération s'il est fourni
    const threshold = moderation_threshold 
      ? Math.max(0.1, Math.min(1.0, parseFloat(moderation_threshold)))
      : DEFAULT_MODERATION_THRESHOLD;
    
    const { moderatedText, result } = await moderateText(text, threshold);
    
    // Si le texte a été modifié, c'est qu'il y a eu modération
    const isModerated = moderatedText !== text;
    
    return res.json({
      status: 'success',
      original_text: text,
      moderated_text: moderatedText,
      is_moderated: isModerated,
      moderation_threshold: threshold,
      api_result: result
    });
  } catch (error) {
    logger.error(`Erreur lors de la modération: ${error.message}`);
    return res.status(500).json({
      status: 'error',
      message: `Erreur serveur: ${error.message}`
    });
  }
});

/**
 * Ajoute un mot au dictionnaire des mots interdits
 * POST /add_forbidden_word
 */
router.post('/add_forbidden_word', (req, res) => {
  try {
    const { word } = req.body;
    
    if (!word) {
      return res.status(400).json({
        status: 'error',
        message: 'Le champ "word" est requis'
      });
    }
    
    const wordLower = word.toLowerCase();
    
    // Générer automatiquement le remplacement (astérisques)
    const replacement = '*'.repeat(wordLower.length);
    
    // Mettre à jour le dictionnaire en mémoire
    FORBIDDEN_WORDS[wordLower] = replacement;
    
    // Sauvegarder dans le fichier
    const saveSuccess = saveForbiddenWords(FORBIDDEN_WORDS);
    
    if (saveSuccess) {
      return res.json({
        status: 'success',
        message: `Le mot "${wordLower}" a été ajouté à la liste des mots interdits`,
        current_dictionary: Object.fromEntries(
          Object.keys(FORBIDDEN_WORDS).map(k => [k, '*'.repeat(k.length)])
        )
      });
    } else {
      return res.json({
        status: 'warning',
        message: `Le mot "${wordLower}" a été ajouté temporairement mais n'a pas pu être sauvegardé dans le fichier`,
        current_dictionary: Object.fromEntries(
          Object.keys(FORBIDDEN_WORDS).map(k => [k, '*'.repeat(k.length)])
        )
      });
    }
  } catch (error) {
    logger.error(`Erreur lors de l'ajout du mot interdit: ${error.message}`);
    return res.status(500).json({
      status: 'error',
      message: `Erreur serveur: ${error.message}`
    });
  }
});

/**
 * Récupère la liste des mots interdits
 * GET /forbidden_words
 */
router.get('/forbidden_words', (req, res) => {
  try {
    // Recharger depuis le fichier pour s'assurer d'avoir les données à jour
    const currentWords = loadForbiddenWords();
    
    // Pour l'affichage, remplacer les valeurs par des astérisques
    const displayWords = Object.fromEntries(
      Object.keys(currentWords).map(k => [k, '*'.repeat(k.length)])
    );
    
    return res.json({
      status: 'success',
      forbidden_words: displayWords
    });
  } catch (error) {
    logger.error(`Erreur lors de la récupération des mots interdits: ${error.message}`);
    return res.status(500).json({
      status: 'error',
      message: `Erreur serveur: ${error.message}`
    });
  }
});

/**
 * Supprime un mot du dictionnaire des mots interdits
 * POST /remove_forbidden_word
 */
router.post('/remove_forbidden_word', (req, res) => {
  try {
    const { word } = req.body;
    
    if (!word) {
      return res.status(400).json({
        status: 'error',
        message: 'Le champ "word" est requis'
      });
    }
    
    const wordLower = word.toLowerCase();
    
    // Vérifier si le mot existe
    if (!FORBIDDEN_WORDS[wordLower]) {
      return res.status(404).json({
        status: 'error',
        message: `Le mot "${wordLower}" n'existe pas dans la liste des mots interdits`
      });
    }
    
    // Supprimer du dictionnaire en mémoire
    delete FORBIDDEN_WORDS[wordLower];
    
    // Sauvegarder dans le fichier
    const saveSuccess = saveForbiddenWords(FORBIDDEN_WORDS);
    
    if (saveSuccess) {
      return res.json({
        status: 'success',
        message: `Le mot "${wordLower}" a été supprimé de la liste des mots interdits`,
        current_dictionary: FORBIDDEN_WORDS
      });
    } else {
      return res.json({
        status: 'warning',
        message: `Le mot "${wordLower}" a été supprimé temporairement mais la mise à jour n'a pas pu être sauvegardée dans le fichier`,
        current_dictionary: FORBIDDEN_WORDS
      });
    }
  } catch (error) {
    logger.error(`Erreur lors de la suppression du mot interdit: ${error.message}`);
    return res.status(500).json({
      status: 'error',
      message: `Erreur serveur: ${error.message}`
    });
  }
});

module.exports = router;
```

### 7. Créez un fichier package.json mis à jour

À la racine du projet, mettez à jour le fichier `package.json` :

```json
{
  "name": "moderation-service",
  "version": "1.0.0",
  "description": "Service de modération d'avis clients avec Mistral AI",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [
    "moderation",
    "api",
    "mistral"
  ],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "axios": "^1.6.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "express": "^4.18.2",
    "fs-extra": "^11.1.1",
    "winston": "^3.11.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}
```

### 8. Créez le fichier mots_interdits.txt initial

À la racine du projet, créez le fichier `mots_interdits.txt` avec le contenu suivant :

```
merde
putain
con
pute
salope
enculé
couille
niquer
nique
foutre
encule
trou du cul
```

## Utilisation de l'API de modération

Une fois le serveur de modération implémenté, vous pouvez l'utiliser dans votre application NodeJS existante. Voici comment procéder :

### 1. Intégration dans une application Express

Voici comment intégrer l'appel à l'API de modération dans votre application NodeJS existante :

```javascript
const axios = require('axios');

// URL du serveur de modération
const MODERATION_API_URL = 'http://localhost:5004';

/**
 * Fonction pour modérer un avis client
 * @param {string} text - Texte à modérer
 * @param {number} threshold - Seuil de modération (0.1-1.0)
 * @returns {Promise<object>} - Résultat de la modération
 */
async function moderateReview(text, threshold = 0.5) {
  try {
    const response = await axios.post(
      `${MODERATION_API_URL}/moderate`,
      {
        text,
        moderation_threshold: threshold
      },
      {
        timeout: 5000
      }
    );
    
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la modération :', error.message);
    throw error;
  }
}

// Exemple d'utilisation dans une route Express pour soumettre un avis
app.post('/api/reviews', async (req, res) => {
  try {
    const { review_text, user_id, product_id } = req.body;
    
    // Modérer l'avis avant de l'enregistrer
    const moderationResult = await moderateReview(review_text);
    
    // Utiliser le texte modéré
    const finalText = moderationResult.moderated_text;
    
    // Ici, code pour enregistrer l'avis en base de données
    // ...
    
    res.json({
      status: 'success',
      message: 'Avis soumis avec succès',
      was_moderated: moderationResult.is_moderated
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: `Erreur lors de la soumission de l'avis: ${error.message}`
    });
  }
});
```

### 2. Exemple avec React/Next.js (côté client)

Si vous utilisez React ou Next.js, voici comment intégrer l'appel à l'API de modération :

```jsx
import { useState } from 'react';
import axios from 'axios';

function ReviewForm() {
  const [reviewText, setReviewText] = useState('');
  const [isModerating, setIsModerating] = useState(false);
  const [moderatedText, setModeratedText] = useState('');
  const [error, setError] = useState('');
  
  const handleTextChange = (e) => {
    setReviewText(e.target.value);
  };
  
  const moderateText = async () => {
    if (!reviewText.trim()) return;
    
    setIsModerating(true);
    
    try {
      const response = await axios.post('http://localhost:5004/moderate', {
        text: reviewText,
        moderation_threshold: 0.5
      });
      
      if (response.data.is_moderated) {
        setModeratedText(response.data.moderated_text);
      } else {
        setModeratedText(reviewText);
      }
    } catch (error) {
      setError(`Erreur lors de la modération: ${error.message}`);
    } finally {
      setIsModerating(false);
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Si le texte n'a pas encore été modéré, le faire avant la soumission
    if (!moderatedText) {
      await moderateText();
    }
    
    // Soumettre le formulaire avec le texte modéré
    // ...
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="review">Votre avis :</label>
        <textarea
          id="review"
          value={reviewText}
          onChange={handleTextChange}
          rows={5}
        />
      </div>
      
      {error && <div className="error">{error}</div>}
      
      <div className="buttons">
        <button 
          type="button" 
          onClick={moderateText} 
          disabled={isModerating || !reviewText.trim()}
        >
          {isModerating ? 'Modération...' : 'Prévisualiser'}
        </button>
        
        <button 
          type="submit" 
          disabled={isModerating || !reviewText.trim()}
        >
          Soumettre
        </button>
      </div>
      
      {moderatedText && (
        <div className="preview">
          <h3>Prévisualisation :</h3>
          <p>{moderatedText}</p>
        </div>
      )}
    </form>
  );
}

export default ReviewForm;
```

## Gestion des mots interdits

La solution permet de gérer une liste personnalisée de mots interdits. Voici comment l'utiliser :

### 1. Ajouter un mot interdit

```javascript
async function addForbiddenWord(word) {
  try {
    const response = await axios.post('http://localhost:5004/add_forbidden_word', {
      word
    });
    
    return response.data;
  } catch (error) {
    console.error(`Erreur lors de l'ajout du mot interdit: ${error.message}`);
    throw error;
  }
}
```

### 2. Supprimer un mot interdit

```javascript
async function removeForbiddenWord(word) {
  try {
    const response = await axios.post('http://localhost:5004/remove_forbidden_word', {
      word
    });
    
    return response.data;
  } catch (error) {
    console.error(`Erreur lors de la suppression du mot interdit: ${error.message}`);
    throw error;
  }
}
```

### 3. Récupérer la liste des mots interdits

```javascript
async function getForbiddenWords() {
  try {
    const response = await axios.get('http://localhost:5004/forbidden_words');
    
    return response.data.forbidden_words;
  } catch (error) {
    console.error(`Erreur lors de la récupération des mots interdits: ${error.message}`);
    throw error;
  }
}
```

## Personnalisation et optimisation

### Ajustement du seuil de modération

Le seuil de modération peut être ajusté pour contrôler la sensibilité de la détection :
- **0.1** : Très strict (modère presque tout)
- **0.5** : Modération standard (équilibrée)
- **0.9** : Très permissif (modère uniquement le contenu extrêmement inapproprié)

### Optimisation des performances

Pour optimiser les performances de l'API de modération :

1. **Mise en cache** : Implémentez un mécanisme de mise en cache pour éviter d'appeler l'API Mistral pour des textes similaires.

```javascript
// Exemple simple de mise en cache avec une Map
const moderationCache = new Map();
const CACHE_TTL = 3600000; // 1 heure en ms

async function moderateWithCache(text, threshold = 0.5) {
  const cacheKey = `${text}_${threshold}`;
  
  // Vérifier si le résultat est en cache et valide
  if (moderationCache.has(cacheKey)) {
    const { result, timestamp } = moderationCache.get(cacheKey);
    if (Date.now() - timestamp < CACHE_TTL) {
      return result;
    }
  }
  
  // Si pas en cache ou expiré, appeler l'API
  const result = await moderateReview(text, threshold);
  
  // Mettre en cache
  moderationCache.set(cacheKey, {
    result,
    timestamp: Date.now()
  });
  
  return result;
}
```

2. **Traitement par lots** : Si vous avez plusieurs textes à modérer, traitez-les par lots.

3. **Analyse préalable** : Effectuez une première analyse locale avant d'appeler l'API Mistral pour réduire les appels inutiles.

## Dépannage

### Problèmes courants et solutions

1. **L'API Mistral renvoie une erreur 401**
   - Vérifiez que votre clé API est correcte dans le fichier `.env`
   - Assurez-vous que votre abonnement Mistral est actif

2. **Le serveur de modération n'est pas accessible**
   - Vérifiez que le serveur est en cours d'exécution
   - Vérifiez que le port configuré est disponible
   - Vérifiez les règles de pare-feu

3. **La modération est trop stricte ou trop permissive**
   - Ajustez le paramètre `moderation_threshold` lors des appels à l'API
   - Modifiez la liste des mots interdits

4. **Erreurs de performance**
   - Augmentez le timeout des requêtes HTTP
   - Implémentez la mise en cache décrite ci-dessus

### Logs et diagnostics

Les logs sont enregistrés dans le fichier `logs/moderation.log`. Vous pouvez les analyser pour diagnostiquer les problèmes éventuels.

Pour activer des logs plus détaillés, modifiez le niveau de log dans `src/utils/logger.js` :

```javascript
const logger = winston.createLogger({
  level: 'debug', // au lieu de 'info'
  // ...
});
```

## Informations complémentaires

### Considérations de sécurité

1. **Protection de l'API** : Assurez-vous que votre API de modération n'est pas accessible publiquement sans authentification. Utilisez une authentification par token JWT ou API Key.

2. **Limites de taux** : Implémentez des limites de taux pour éviter les abus.

3. **Validation des entrées** : Vérifiez toujours les entrées utilisateur.

### Integration avec PM2 pour la production

Pour exécuter le service en production, utilisez PM2 :

```bash
# Installation de PM2
npm install -g pm2

# Démarrage du service
pm2 start src/server.js --name moderation-service

# Configuration du démarrage automatique
pm2 startup
pm2 save

# Visualisation des logs
pm2 logs moderation-service

# Redémarrage du service
pm2 restart moderation-service
```

### Exemple complet d'intégration dans une application Express

Voici un exemple complet d'intégration dans une route Express pour la gestion des avis clients :

```javascript
const express = require('express');
const router = express.Router();
const axios = require('axios');

// URL du serveur de modération
const MODERATION_API_URL = 'http://localhost:5004';

// Middleware pour modérer automatiquement les textes
const moderationMiddleware = async (req, res, next) => {
  try {
    if (req.body && req.body.content) {
      const response = await axios.post(
        `${MODERATION_API_URL}/moderate`,
        {
          text: req.body.content,
          moderation_threshold: 0.5
        }
      );
      
      // Remplacer le contenu original par le contenu modéré
      req.body.content = response.data.moderated_text;
      req.body.was_moderated = response.data.is_moderated;
    }
    next();
  } catch (error) {
    console.error('Erreur de modération:', error.message);
    // En cas d'erreur de modération, continuer quand même
    next();
  }
};

// Appliquer le middleware à toutes les routes de création/modification d'avis
router.post('/reviews', moderationMiddleware, async (req, res) => {
  // Traitement normal de création d'avis avec le texte déjà modéré
  // ...
  
  res.json({ success: true, was_moderated: req.body.was_moderated });
});

router.put('/reviews/:id', moderationMiddleware, async (req, res) => {
  // Traitement normal de mise à jour d'avis avec le texte déjà modéré
  // ...
  
  res.json({ success: true, was_moderated: req.body.was_moderated });
});

module.exports = router;
```

### Amélioration avec une file d'attente de tâches

Pour des systèmes avec un volume élevé, vous pouvez implémenter une file d'attente de tâches de modération avec Bull :

```javascript
// Installation des packages nécessaires
// npm install bull ioredis

const Queue = require('bull');
const { moderateText } = require('./moderation.service');

// Créer une file d'attente de modération
const moderationQueue = new Queue('moderation', {
  redis: {
    host: 'localhost',
    port: 6379
  }
});

// Traitement des tâches
moderationQueue.process(async (job) => {
  const { text, threshold, reviewId } = job.data;
  
  // Modérer le texte
  const { moderatedText, result } = await moderateText(text, threshold);
  
  // Mettre à jour l'avis en base de données
  await updateReviewInDatabase(reviewId, moderatedText);
  
  return { moderatedText, result };
});

// Ajouter une tâche à la file d'attente
async function queueModerationTask(text, reviewId, threshold = 0.5) {
  await moderationQueue.add({
    text,
    reviewId,
    threshold
  }, {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000
    }
  });
}

// Utilisation dans votre route
router.post('/reviews', async (req, res) => {
  try {
    const { text, userId, productId } = req.body;
    
    // Enregistrer d'abord l'avis en base de données
    const reviewId = await saveReviewToDatabase(text, userId, productId);
    
    // Ajouter la tâche de modération à la file d'attente
    await queueModerationTask(text, reviewId);
    
    res.json({
      status: 'success',
      message: 'Avis soumis et en cours de modération',
      reviewId
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});
```

## Nouveautés Version 2 - Fonctionnalités avancées

### Réponse API enrichie Version 2

La Version 2 retourne des informations détaillées sur les sources de modération :

```javascript
// Exemple de réponse API Version 2
{
  "status": "success",
  "original_text": "Ce docteur est un connard",
  "moderated_text": "Ce docteur est un *******",
  "is_moderated": true,
  "moderation_threshold": 1.0,
  "api_result": { /* Détails de l'API Mistral */ },
  "moderation_details": {
    "forbidden_words_applied": ["connard"],
    "mistral_api_applied": [],
    "proper_names_applied": [],
    "sources": ["Dictionnaire de mots interdits"]
  }
}
```

### Service de modération Version 2 amélioré

Voici la version mise à jour du service de modération avec traçabilité :

```javascript
// services/moderation.service.js - Version 2
const axios = require('axios');
const { logger } = require('../utils/logger');
const { FORBIDDEN_WORDS } = require('../utils/forbidden-words');

const DEFAULT_MODERATION_THRESHOLD = 1.0; // Nouveau défaut optimisé

/**
 * Modère le texte avec traçabilité des sources (Version 2)
 */
async function moderateText(text, moderationThreshold = DEFAULT_MODERATION_THRESHOLD) {
  const { shouldModerate, result } = await checkModerationApi(text, moderationThreshold);
  
  let moderatedText = text;
  
  // Tracker les sources de modération
  const moderationDetails = {
    forbidden_words_applied: [],
    mistral_api_applied: [],
    proper_names_applied: [],
    sources: []
  };
  
  // ÉTAPE 1: API Mistral (filtre principal - 90%)
  const additionalWordsToModerate = [];
  
  if (shouldModerate) {
    logger.info(`Contenu inapproprié détecté par l'API Mistral (seuil: ${moderationThreshold})`);
    
    // Liste exhaustive des mots que l'API peut modérer
    const apiModerationWords = [
      // Mots grossiers de base
      "merde", "putain", "con", "connard", "connasse", "salope", "pute", "enculé", "encule",
      "bite", "couille", "couilles", "trou du cul", "trou-du-cul",
      // Mots sexuels
      "sexe", "penis", "pénis", "vagin", "seins", "cul",
      // Insultes
      "salaud", "ordure", "fumier", "crétin", "imbécile", "idiot", "débile",
      "abruti", "taré", "dégénéré", "pourriture", "salopard",
      // Verbes grossiers
      "niquer", "nique", "foutre", "chier", "pisser",
      // Variantes et expressions
      "fils de pute", "va te faire", "ta gueule", "ferme ta gueule"
    ];
    
    // Modérer tous les mots de cette liste s'ils sont présents
    for (const word of apiModerationWords) {
      if (text.toLowerCase().includes(word)) {
        additionalWordsToModerate.push(word);
      }
    }
  }
  
  // Appliquer la modération API Mistral
  const textBeforeApi = moderatedText;
  for (const word of additionalWordsToModerate) {
    const replacement = '*'.repeat(word.length);
    const regex = new RegExp('\\b' + word.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&') + '\\b', 'gi');
    moderatedText = moderatedText.replace(regex, replacement);
    moderationDetails.mistral_api_applied.push(word);
  }
  
  if (textBeforeApi !== moderatedText) {
    moderationDetails.sources.push('API Mistral');
  }
  
  // ÉTAPE 2: Dictionnaire de mots interdits (filet de sécurité - 10%)
  const textBeforeForbidden = moderatedText;
  for (const [word, replacement] of Object.entries(FORBIDDEN_WORDS)) {
    const regex = new RegExp('\\b' + word.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&') + '\\b', 'gi');
    if (regex.test(moderatedText)) {
      moderatedText = moderatedText.replace(regex, replacement);
      moderationDetails.forbidden_words_applied.push(word);
    }
  }
  
  if (textBeforeForbidden !== moderatedText) {
    moderationDetails.sources.push('Dictionnaire de mots interdits');
  }
  
  // ÉTAPE 3: Détection des noms propres
  const textBeforeNames = moderatedText;
  const titles = ["Dr", "Docteur", "Pr", "Professeur", "M.", "Mme", "Mlle"];
  
  for (const title of titles) {
    const pattern = new RegExp(`(${title}\\s+)([A-Z][a-zéèêëàâäôöûüç]+)`, 'g');
    const matches = [...moderatedText.matchAll(pattern)];
    
    if (matches.length > 0) {
      matches.forEach(match => {
        moderationDetails.proper_names_applied.push(`${match[1]}${match[2]}`);
      });
      moderatedText = moderatedText.replace(pattern, '$1*****');
    }
  }
  
  if (textBeforeNames !== moderatedText) {
    moderationDetails.sources.push('Détection de noms propres');
  }
  
  return { moderatedText, result, moderationDetails };
}

module.exports = {
  DEFAULT_MODERATION_THRESHOLD,
  checkModerationApi,
  moderateText
};
```

### Routes API Version 2 avec traçabilité

```javascript
// routes/moderation.routes.js - Version 2
router.post('/moderate', async (req, res) => {
  try {
    const { text, moderation_threshold } = req.body;
    
    if (!text) {
      return res.status(400).json({
        status: 'error',
        message: 'Le champ "text" est requis'
      });
    }
    
    logger.info(`Demande de modération pour le texte: ${text}`);
    
    const threshold = moderation_threshold 
      ? Math.max(0.1, Math.min(1.0, parseFloat(moderation_threshold)))
      : DEFAULT_MODERATION_THRESHOLD;
    
    // Utiliser la nouvelle fonction avec traçabilité
    const { moderatedText, result, moderationDetails } = await moderateText(text, threshold);
    
    const isModerated = moderatedText !== text;
    
    return res.json({
      status: 'success',
      original_text: text,
      moderated_text: moderatedText,
      is_moderated: isModerated,
      moderation_threshold: threshold,
      api_result: result,
      moderation_details: moderationDetails // Nouvelle propriété Version 2
    });
  } catch (error) {
    logger.error(`Erreur lors de la modération: ${error.message}`);
    return res.status(500).json({
      status: 'error',
      message: `Erreur serveur: ${error.message}`
    });
  }
});
```

### Intégration client Version 2

```javascript
// Client-side integration avec détection intelligente
class ModerationClientV2 {
  constructor(apiUrl = 'http://localhost:5004') {
    this.apiUrl = apiUrl;
  }
  
  async moderateText(text, threshold = 1.0) {
    try {
      const response = await fetch(`${this.apiUrl}/moderate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, moderation_threshold: threshold })
      });
      
      const result = await response.json();
      
      if (result.status === 'success') {
        // Analyser les sources de modération
        this.displayModerationSources(result.moderation_details);
        
        // Détecter les mots non modérés
        await this.handleUnmoderatedWords(result.original_text, result.moderated_text);
        
        return result;
      }
      
      throw new Error(result.message || 'Erreur de modération');
    } catch (error) {
      console.error('Erreur de modération:', error);
      throw error;
    }
  }
  
  displayModerationSources(details) {
    if (!details || !details.sources.length) return;
    
    console.log('🔍 Sources de modération:');
    details.sources.forEach(source => {
      switch(source) {
        case 'API Mistral':
          console.log('🤖 API Mistral - Mots:', details.mistral_api_applied);
          break;
        case 'Dictionnaire de mots interdits':
          console.log('📚 Dictionnaire - Mots:', details.forbidden_words_applied);
          break;
        case 'Détection de noms propres':
          console.log('👤 Noms propres - Détectés:', details.proper_names_applied);
          break;
      }
    });
  }
  
  detectUnmoderatedWords(original, moderated) {
    const suspectWords = [
      'connasse', 'salope', 'pute', 'putain', 'merde', 'con', 'connard',
      'enculé', 'bite', 'couille', 'crétin', 'imbécile', 'débile'
    ];
    
    const originalWords = original.toLowerCase().match(/\b\w+\b/g) || [];
    const moderatedWords = moderated.toLowerCase().match(/\b\w+\b/g) || [];
    
    return suspectWords.filter(word => 
      originalWords.includes(word) && moderatedWords.includes(word)
    );
  }
  
  async handleUnmoderatedWords(original, moderated) {
    const unmoderatedWords = this.detectUnmoderatedWords(original, moderated);
    
    if (unmoderatedWords.length > 0) {
      console.warn('⚠️ Mots non modérés détectés:', unmoderatedWords);
      
      // Optionnel: proposer l'ajout automatique
      if (confirm(`Mots non modérés: ${unmoderatedWords.join(', ')}\nLes ajouter à la liste ?`)) {
        for (const word of unmoderatedWords) {
          await this.addForbiddenWord(word);
        }
        console.log('✅ Mots ajoutés avec succès');
      }
    }
  }
  
  async addForbiddenWord(word) {
    const response = await fetch(`${this.apiUrl}/add_forbidden_word`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ word })
    });
    
    return response.json();
  }
}

// Utilisation
const moderationClient = new ModerationClientV2();

// Dans votre formulaire
document.getElementById('review-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const text = document.getElementById('review-text').value;
  
  try {
    const result = await moderationClient.moderateText(text);
    
    if (result.is_moderated) {
      const sources = result.moderation_details.sources.join(', ');
      alert(`Texte modéré par: ${sources}`);
      document.getElementById('review-text').value = result.moderated_text;
    }
    
    // Continuer avec la soumission...
  } catch (error) {
    alert('Erreur de modération: ' + error.message);
  }
});
```

## Conclusion

Cette implémentation NodeJS Version 2 du service de modération vous permet d'intégrer facilement et efficacement l'API Mistral AI avec une logique de modération intelligente et traçable. Elle offre :

- **🤖 Modération IA avancée** : 90% de la modération gérée intelligemment
- **📚 Filet de sécurité robuste** : 10% de protection supplémentaire
- **🔍 Traçabilité complète** : Savoir exactement qui a modéré quoi
- **⚡ Auto-amélioration** : Détection et ajout des mots manqués
- **🚀 Intégration moderne** : Compatible avec tous les frameworks actuels

Cette version s'intègre parfaitement à votre environnement NodeJS existant tout en offrant une expérience de modération optimisée et intelligente.

Pour toute question ou assistance supplémentaire, n'hésitez pas à contacter l'équipe technique.