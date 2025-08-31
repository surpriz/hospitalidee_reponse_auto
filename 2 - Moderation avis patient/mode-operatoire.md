# Mode Opératoire - Intégration du Système de Modération d'Avis Clients (Version 2)

**Dernière mise à jour : 31 Août 2025**

http://83.147.36.59:8503/

## 🆕 Nouveautés de la Version 2 (Mise à jour 31 Août 2025)

Cette version 2 apporte des améliorations majeures :

- **🤖 API Mistral comme filtre principal** : L'IA gère maintenant 90% de la modération
- **📚 Dictionnaire enrichi** : 320+ mots interdits (contre 9 initialement) comme filet de sécurité
- **👤 Détection étendue des noms propres** : Reconnaissance de 30+ titres professionnels et civilités
- **🔍 Détection intelligente des sources** : Savoir exactement qui a modéré quoi
- **⚡ Ajout rapide de mots** : Interface pour ajouter facilement les mots manqués par l'IA
- **🎯 Seuil par défaut optimisé** : Réglé à 1.0 (très permissif) pour éviter la sur-modération
- **📅 Indicateur de version** : Affichage de la date de dernière mise à jour du code

## Table des matières

1. [Présentation du système](#1-présentation-du-système)
2. [Prérequis](#2-prérequis)
3. [Installation](#3-installation)
4. [Configuration](#4-configuration)
5. [Utilisation de l'API de modération](#5-utilisation-de-lapi-de-modération)
6. [Gestion des mots interdits](#6-gestion-des-mots-interdits)
7. [Personnalisation du seuil de modération](#7-personnalisation-du-seuil-de-modération)
8. [Nouveautés Version 2 - Intégration avancée](#8-nouveautés-version-2---intégration-avancée)
9. [Déploiement en production](#9-déploiement-en-production)
10. [Dépannage](#10-dépannage)
11. [FAQ](#11-faq)

## 1. Présentation du système

Le système de modération d'avis clients est une solution intelligente qui utilise l'API Mistral AI comme **filtre principal** pour détecter et filtrer les contenus inappropriés dans les avis clients.

### 🔄 Architecture Version 2 (Optimisée)

1. **🤖 API Mistral AI (90% - Filtre principal)**
   - Détecte automatiquement les contenus inappropriés via l'intelligence artificielle
   - Modère une liste exhaustive de ~25 mots/expressions grossiers courants
   - Se déclenche quand le score de détection dépasse le seuil configuré

2. **📚 Dictionnaire de mots interdits (10% - Filet de sécurité)**
   - Capture les mots spécifiques que l'IA pourrait manquer
   - Modération systématique indépendamment de l'IA
   - Facilement personnalisable selon vos besoins

3. **👤 Détection étendue de noms propres (30+ titres reconnus)**
   - Protection automatique de l'identité (Dr Durant → Dr *****)
   - Titres médicaux : Médecin, Infirmier, Chirurgien, Pharmacien, etc.
   - Civilités complètes : Monsieur, Madame, M., Mr., Mme., etc.
   - Titres professionnels : Directeur, Responsable, Chef, Maître, etc.
   - Fonctionne indépendamment des autres filtres

### 🎯 Avantages de la Version 2

- **Plus intelligent** : L'IA s'adapte au contexte
- **Moins de faux positifs** : Seuil par défaut optimisé à 1.0
- **Traçabilité complète** : Savoir qui a modéré quoi
- **Auto-amélioration** : Ajout facile des mots manqués

Le système est développé en Python avec Flask pour la partie API et peut être facilement intégré à votre site web existant.

## 2. Prérequis

- Python 3.9 ou supérieur
- Accès à un terminal/ligne de commande
- Une clé API Mistral AI (à obtenir sur [https://console.mistral.ai/](https://console.mistral.ai/))
- Connaissance de base des requêtes HTTP (GET/POST)

## 3. Installation

### 3.1. Téléchargement du code

Clonez le dépôt ou téléchargez les fichiers suivants dans un même dossier :
- `app.py` (API Flask)
- `mots_interdits.txt` (Liste des mots interdits)
- `requirements.txt` (Dépendances)

### 3.2. Création d'un environnement virtuel (recommandé)

```bash
# Création de l'environnement virtuel
python -m venv venv

# Activation de l'environnement virtuel
# Sur Windows
venv\Scripts\activate
# Sur MacOS/Linux
source venv/bin/activate
```

### 3.3. Installation des dépendances

```bash
pip install -r requirements.txt
```

## 4. Configuration

### 4.1. Configuration de la clé API Mistral

Créez un fichier `.env` à la racine du projet avec le contenu suivant :

```
MISTRAL_API_KEY=votre_clé_api_mistral
```

Remplacez `votre_clé_api_mistral` par la clé que vous avez obtenue sur la console Mistral AI.

### 4.2. Vérification du fichier des mots interdits

Le fichier `mots_interdits.txt` contient une liste enrichie de **320+ mots interdits** à modérer automatiquement, incluant :
- Insultes courantes et leurs variantes
- Termes vulgaires et sexuels
- Expressions composées (fils de pute, va te faire, etc.)
- Abréviations (fdp, ntm, tg, vtf, etc.)
- Termes discriminatoires
- Variantes orthographiques

Vérifiez son contenu et ajustez-le selon vos besoins. Un mot par ligne.

## 5. Utilisation de l'API de modération

### 5.1. Démarrage du serveur API

```bash
python app.py
```

Le serveur démarre par défaut sur `http://localhost:5004`. Vous pouvez modifier le port dans le fichier `app.py` si nécessaire.

### 5.2. Intégration à votre site web

Voici un exemple d'intégration avec JavaScript :

```javascript
// Fonction pour modérer un texte
async function modererTexte(texte, seuil = 0.5) {
  try {
    const response = await fetch('http://localhost:5004/moderate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: texte,
        moderation_threshold: seuil
      }),
    });
    
    return await response.json();
  } catch (error) {
    console.error('Erreur lors de la modération :', error);
    return null;
  }
}

// Exemple d'utilisation
document.getElementById('formulaire-avis').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const texteAvis = document.getElementById('texte-avis').value;
  
  // Appel à l'API de modération
  const resultat = await modererTexte(texteAvis);
  
  if (resultat && resultat.status === 'success') {
    // Utilisation du texte modéré
    if (resultat.is_moderated) {
      // Si le texte a été modéré, afficher un message et/ou utiliser la version modérée
      alert('Votre avis contient des termes inappropriés qui ont été filtrés.');
      document.getElementById('texte-avis').value = resultat.moderated_text;
    } else {
      // Si aucune modération n'a été appliquée, soumettre le formulaire
      // Exemple : enregistrement en base de données
      alert('Avis soumis avec succès !');
    }
  } else {
    alert('Erreur lors de la modération. Veuillez réessayer.');
  }
});
```

### 5.3. Exemple d'intégration en PHP

```php
<?php
function modererTexte($texte, $seuil = 0.5) {
    $url = 'http://localhost:5004/moderate';
    $data = json_encode([
        'text' => $texte,
        'moderation_threshold' => $seuil
    ]);
    
    $options = [
        'http' => [
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => $data
        ]
    ];
    
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    
    if ($result === FALSE) {
        return null;
    }
    
    return json_decode($result, true);
}

// Exemple d'utilisation
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $avis = $_POST['texte_avis'];
    $resultat = modererTexte($avis);
    
    if ($resultat && $resultat['status'] === 'success') {
        if ($resultat['is_moderated']) {
            echo "Votre avis contient des termes inappropriés qui ont été filtrés.";
            // Utiliser le texte modéré pour l'enregistrement
            $avis_modere = $resultat['moderated_text'];
            // Enregistrement en base de données...
        } else {
            echo "Avis soumis avec succès !";
            // Enregistrement en base de données...
        }
    } else {
        echo "Erreur lors de la modération. Veuillez réessayer.";
    }
}
?>
```

## 6. Gestion des mots interdits

L'API propose des endpoints pour gérer dynamiquement la liste des mots interdits.

### 6.1. Récupérer la liste des mots interdits

```javascript
// JavaScript
async function getMotsInterdits() {
  const response = await fetch('http://localhost:5004/forbidden_words');
  return await response.json();
}
```

### 6.2. Ajouter un mot interdit

```javascript
// JavaScript
async function ajouterMotInterdit(mot) {
  const response = await fetch('http://localhost:5004/add_forbidden_word', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ word: mot }),
  });
  
  return await response.json();
}
```

### 6.3. Supprimer un mot interdit

```javascript
// JavaScript
async function supprimerMotInterdit(mot) {
  const response = await fetch('http://localhost:5004/remove_forbidden_word', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ word: mot }),
  });
  
  return await response.json();
}
```

## 7. Personnalisation du seuil de modération

Le seuil de modération détermine la sensibilité de la détection des contenus inappropriés. Plus la valeur est basse, plus la modération sera stricte.

- **0.1 = Très strict** (modère presque tous les contenus potentiellement inappropriés)
- **0.3 = Strict**
- **0.5 = Modéré** (équilibré)
- **0.7 = Permissif**
- **0.9 = Très permissif** (modère uniquement les contenus très clairement inappropriés)

Vous pouvez ajuster ce seuil en fonction de votre audience et du niveau de modération souhaité.

## 8. Nouveautés Version 2 - Intégration avancée

### 8.1. Nouvelle réponse API enrichie

La Version 2 retourne des informations détaillées sur les sources de modération :

```json
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

### 8.2. Intégration JavaScript avancée

Voici comment exploiter les nouvelles fonctionnalités :

```javascript
// Fonction de modération Version 2
async function modererTexteV2(texte, seuil = 1.0) {
  try {
    const response = await fetch('http://localhost:5004/moderate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: texte,
        moderation_threshold: seuil
      }),
    });
    
    const result = await response.json();
    
    if (result.status === 'success') {
      // Afficher les sources de modération
      displayModerationSources(result.moderation_details);
      
      return result;
    }
    
    return null;
  } catch (error) {
    console.error('Erreur lors de la modération :', error);
    return null;
  }
}

// Affichage des sources de modération
function displayModerationSources(details) {
  const sources = details.sources || [];
  
  if (sources.length > 0) {
    console.log('🔍 Sources de modération:');
    
    sources.forEach(source => {
      switch(source) {
        case 'API Mistral':
          console.log('🤖 API Mistral - Mots détectés:', details.mistral_api_applied);
          break;
        case 'Dictionnaire de mots interdits':
          console.log('📚 Dictionnaire - Mots détectés:', details.forbidden_words_applied);
          break;
        case 'Détection de noms propres':
          console.log('👤 Noms propres - Détectés:', details.proper_names_applied);
          break;
      }
    });
  }
}

// Exemple d'utilisation avec interface utilisateur
document.getElementById('formulaire-avis').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const texteAvis = document.getElementById('texte-avis').value;
  const resultat = await modererTexteV2(texteAvis);
  
  if (resultat && resultat.status === 'success') {
    if (resultat.is_moderated) {
      // Afficher un message informatif selon la source
      const sources = resultat.moderation_details.sources;
      let message = 'Votre avis a été modéré par : ' + sources.join(', ');
      
      // Proposer le texte modéré
      if (confirm(message + '\n\nVoulez-vous utiliser la version modérée ?')) {
        document.getElementById('texte-avis').value = resultat.moderated_text;
      }
    } else {
      // Aucune modération nécessaire
      alert('Avis soumis avec succès !');
      // Soumettre le formulaire...
    }
  } else {
    alert('Erreur lors de la modération. Veuillez réessayer.');
  }
});
```

### 8.3. Gestion intelligente des mots non détectés

La Version 2 permet de détecter automatiquement les mots que l'IA a manqués :

```javascript
// Fonction pour détecter les mots potentiellement non modérés
function detectUnmoderatedWords(original, moderated) {
  const suspectWords = [
    'connasse', 'salope', 'pute', 'putain', 'merde', 'con', 'connard',
    'enculé', 'bite', 'couille', 'crétin', 'imbécile', 'débile'
  ];
  
  const originalWords = original.toLowerCase().match(/\b\w+\b/g) || [];
  const moderatedWords = moderated.toLowerCase().match(/\b\w+\b/g) || [];
  
  const unmoderated = [];
  suspectWords.forEach(word => {
    if (originalWords.includes(word) && moderatedWords.includes(word)) {
      unmoderated.push(word);
    }
  });
  
  return unmoderated;
}

// Ajout automatique des mots manqués
async function handleUnmoderatedWords(original, moderated) {
  const unmoderatedWords = detectUnmoderatedWords(original, moderated);
  
  if (unmoderatedWords.length > 0) {
    const shouldAdd = confirm(
      `Mots non modérés détectés: ${unmoderatedWords.join(', ')}\n` +
      'Voulez-vous les ajouter à la liste des mots interdits ?'
    );
    
    if (shouldAdd) {
      for (const word of unmoderatedWords) {
        await ajouterMotInterdit(word);
      }
      
      alert(`${unmoderatedWords.length} mot(s) ajouté(s) avec succès !`);
    }
  }
}

// Utilisation complète
async function processReviewWithSmartDetection(texte) {
  const resultat = await modererTexteV2(texte);
  
  if (resultat && resultat.status === 'success') {
    // Vérifier les mots non modérés
    await handleUnmoderatedWords(resultat.original_text, resultat.moderated_text);
    
    return resultat;
  }
  
  return null;
}
```

### 8.4. Interface de gestion avancée

Créez une interface d'administration pour gérer la modération :

```html
<!-- Interface d'administration -->
<div id="moderation-admin">
  <h3>🔧 Administration de la modération</h3>
  
  <!-- Test de modération -->
  <div class="test-section">
    <h4>Test de modération</h4>
    <textarea id="test-text" placeholder="Texte à tester..."></textarea>
    <button onclick="testModeration()">Tester</button>
    
    <div id="test-results" style="display:none;">
      <h5>Résultats :</h5>
      <div id="original-text"></div>
      <div id="moderated-text"></div>
      <div id="moderation-sources"></div>
    </div>
  </div>
  
  <!-- Gestion des mots interdits -->
  <div class="words-management">
    <h4>Gestion des mots interdits</h4>
    <input type="text" id="new-word" placeholder="Nouveau mot...">
    <button onclick="addWord()">Ajouter</button>
    
    <div id="words-list"></div>
  </div>
</div>

<script>
async function testModeration() {
  const text = document.getElementById('test-text').value;
  const result = await modererTexteV2(text);
  
  if (result) {
    document.getElementById('original-text').innerHTML = 
      `<strong>Original:</strong> ${result.original_text}`;
    document.getElementById('moderated-text').innerHTML = 
      `<strong>Modéré:</strong> ${result.moderated_text}`;
    
    const sources = result.moderation_details.sources.join(', ') || 'Aucune';
    document.getElementById('moderation-sources').innerHTML = 
      `<strong>Sources:</strong> ${sources}`;
    
    document.getElementById('test-results').style.display = 'block';
  }
}

async function addWord() {
  const word = document.getElementById('new-word').value;
  if (word) {
    await ajouterMotInterdit(word);
    document.getElementById('new-word').value = '';
    loadWordsList();
  }
}

async function loadWordsList() {
  const words = await getMotsInterdits();
  const list = document.getElementById('words-list');
  
  list.innerHTML = Object.keys(words.forbidden_words)
    .map(word => `
      <div class="word-item">
        <span>${word}</span>
        <button onclick="removeWord('${word}')">Supprimer</button>
      </div>
    `).join('');
}
</script>
```

### 8.5. Intégration avec frameworks modernes

#### React/Next.js

```jsx
import { useState, useEffect } from 'react';

function ModerationHook() {
  const [moderationResult, setModerationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const moderateText = async (text, threshold = 1.0) => {
    setIsLoading(true);
    
    try {
      const response = await fetch('/api/moderate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, moderation_threshold: threshold })
      });
      
      const result = await response.json();
      setModerationResult(result);
      
      return result;
    } catch (error) {
      console.error('Erreur de modération:', error);
      return null;
    } finally {
      setIsLoading(false);
    }
  };
  
  return { moderateText, moderationResult, isLoading };
}

// Composant d'affichage des sources
function ModerationSources({ details }) {
  if (!details || !details.sources.length) return null;
  
  return (
    <div className="moderation-sources">
      <h4>🔍 Sources de modération</h4>
      {details.sources.map((source, index) => (
        <div key={index} className="source-item">
          {source === 'API Mistral' && (
            <div className="api-source">
              🤖 <strong>API Mistral</strong>
              {details.mistral_api_applied.length > 0 && (
                <span> - Mots: {details.mistral_api_applied.join(', ')}</span>
              )}
            </div>
          )}
          {source === 'Dictionnaire de mots interdits' && (
            <div className="dict-source">
              📚 <strong>Dictionnaire</strong>
              <span> - Mots: {details.forbidden_words_applied.join(', ')}</span>
            </div>
          )}
          {source === 'Détection de noms propres' && (
            <div className="names-source">
              👤 <strong>Noms propres</strong>
              <span> - Détectés: {details.proper_names_applied.join(', ')}</span>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
```

#### Vue.js

```vue
<template>
  <div class="moderation-component">
    <textarea 
      v-model="reviewText" 
      placeholder="Votre avis..."
      @blur="moderateText"
    ></textarea>
    
    <div v-if="moderationResult && moderationResult.is_moderated" class="moderation-info">
      <p>✅ Texte modéré par: {{ moderationSources }}</p>
      <button @click="acceptModeration">Accepter la modération</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      reviewText: '',
      moderationResult: null
    }
  },
  computed: {
    moderationSources() {
      return this.moderationResult?.moderation_details?.sources?.join(', ') || '';
    }
  },
  methods: {
    async moderateText() {
      if (!this.reviewText.trim()) return;
      
      try {
        const response = await this.$http.post('/api/moderate', {
          text: this.reviewText,
          moderation_threshold: 1.0
        });
        
        this.moderationResult = response.data;
      } catch (error) {
        console.error('Erreur de modération:', error);
      }
    },
    
    acceptModeration() {
      this.reviewText = this.moderationResult.moderated_text;
      this.moderationResult = null;
    }
  }
}
</script>
```

## 9. Déploiement en production

### 8.1. Utilisation d'un serveur WSGI

Pour un déploiement en production, il est recommandé d'utiliser un serveur WSGI comme Gunicorn :

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5004 app:app
```

### 8.2. Configuration avec Nginx

Exemple de configuration Nginx :

```nginx
server {
    listen 80;
    server_name moderation.votredomaine.com;

    location / {
        proxy_pass http://127.0.0.1:5004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 8.3. Sécurisation de l'API

Pour sécuriser l'API en production, envisagez d'ajouter :

- Un système d'authentification (clé API ou token JWT)
- HTTPS pour les communications
- Des limites de taux (rate limiting)

## 9. Dépannage

### 9.1. Logs et diagnostics

L'API enregistre les logs dans le fichier `moderation.log`. Consultez ce fichier en cas de problème :

```bash
tail -f moderation.log
```

### 9.2. Problèmes courants

**Erreur de connexion à l'API :**
- Vérifiez que le serveur Flask est bien démarré
- Vérifiez le port et l'adresse d'accès
- Vérifiez les règles de pare-feu

**Erreur d'authentification Mistral :**
- Vérifiez votre clé API dans le fichier `.env`
- Assurez-vous que la clé est valide et active

**Performances lentes :**
- L'appel à l'API Mistral peut prendre quelques secondes
- Envisagez de mettre en cache les résultats de modération pour les textes fréquents

## 10. Interface Streamlit - Indicateur de version

L'interface Streamlit affiche désormais en haut à droite un badge vert avec la date et l'heure de la dernière mise à jour du code :

**✓ Last update : 31 Août 2025 - 14h32**

Cette date est définie dans le fichier `streamlit_moderation.py` (ligne 109) :

```python
# Date et heure de dernière mise à jour du code (à modifier manuellement lors des mises à jour)
LAST_UPDATE = "31 Août 2025 - 14h32"
```

Cette fonctionnalité permet aux utilisateurs de vérifier qu'ils utilisent bien la dernière version de l'application.

## 11. FAQ

**Q : Puis-je utiliser le système de modération sans l'API Mistral ?**  
R : Oui, mais uniquement avec la modération par liste de mots interdits. Il faudra modifier le code pour désactiver les appels à l'API Mistral.

**Q : Comment puis-je ajouter de nouvelles catégories de modération ?**  
R : Les catégories sont définies par l'API Mistral. Vous pouvez ajuster les seuils par catégorie dans la fonction `check_moderation_api`.

**Q : Est-ce que le système fonctionne pour d'autres langues que le français ?**  
R : Oui, l'API Mistral prend en charge plusieurs langues. Vous devrez cependant adapter votre liste de mots interdits.

**Q : Comment puis-je tester l'intégration avant de la déployer ?**  
R : Utilisez l'interface Streamlit fournie (`streamlit_moderation.py`) pour tester le fonctionnement du système avant l'intégration :
```bash
streamlit run streamlit_moderation.py
```
