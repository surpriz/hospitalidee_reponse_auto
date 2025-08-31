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
- **🔴🟢 Système de flags automatiques** : Classification RED/GREEN pour optimiser la vérification humaine
- **⚙️ Configuration flexible** : Seuils ajustables via interface et API
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

## 8. Nouveautés Version 2 - Système de flags RED/GREEN

### 8.1. Introduction au système de flags automatiques

La Version 2 intègre un système de **flags automatiques** pour optimiser le workflow de modération :

- **🔴 FLAG RED** : Vérification humaine requise avant publication
- **🟢 FLAG GREEN** : Publication automatique possible

#### Critères de classification

**FLAG RED déclenché si :**
- Score API Mistral > seuil configurable (défaut: 0.3)
- Mots interdits détectés
- Noms propres détectés (RGPD)
- Texte modifié pendant la modération

**FLAG GREEN déclenché si :**
- Aucun des critères RED n'est rempli
- Score API faible
- Pas de modification nécessaire

### 8.2. Configuration des seuils de flags

#### Récupérer la configuration actuelle

```javascript
// JavaScript
async function getFlagConfig() {
  const response = await fetch('http://localhost:5004/get_flag_config');
  return await response.json();
}
```

```php
<?php
// PHP
function getFlagConfig() {
    $url = 'http://localhost:5004/get_flag_config';
    $response = file_get_contents($url);
    return json_decode($response, true);
}
?>
```

#### Mettre à jour la configuration

```javascript
// JavaScript
async function updateFlagConfig(config) {
  const response = await fetch('http://localhost:5004/update_flag_config', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ flag_config: config })
  });
  
  return await response.json();
}

// Exemple d'usage
const newConfig = {
  mistral_api_score_threshold: 0.3,
  forbidden_words_trigger_red: true,
  proper_names_trigger_red: true,
  text_modification_trigger_red: true
};

await updateFlagConfig(newConfig);
```

```php
<?php
// PHP
function updateFlagConfig($config) {
    $url = 'http://localhost:5004/update_flag_config';
    $data = json_encode(['flag_config' => $config]);
    
    $options = [
        'http' => [
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => $data
        ]
    ];
    
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    
    return json_decode($result, true);
}

// Exemple d'usage
$newConfig = [
    'mistral_api_score_threshold' => 0.3,
    'forbidden_words_trigger_red' => true,
    'proper_names_trigger_red' => true,
    'text_modification_trigger_red' => true
];

$result = updateFlagConfig($newConfig);
?>
```

### 8.3. Nouvelle réponse API enrichie avec flags

La Version 2 retourne des informations détaillées sur les sources de modération :

```json
{
  "status": "success",
  "original_text": "Dr Durant est un trou du cul",
  "moderated_text": "Dr ***** est un ***********",
  "is_moderated": true,
  "moderation_threshold": 1.0,
  "api_result": { /* Détails de l'API Mistral */ },
  "moderation_details": {
    "forbidden_words_applied": ["trou du cul"],
    "mistral_api_applied": [],
    "proper_names_applied": ["Dr Durant"],
    "sources": ["Dictionnaire de mots interdits", "Détection de noms propres"]
  },
  "flag": "RED",
  "flag_reasons": [
    "Mots interdits détectés (1 mot(s))",
    "Noms propres détectés (1 nom(s)) - RGPD",
    "Texte modifié pendant la modération"
  ]
}
```

### 8.4. Intégration JavaScript avec gestion des flags

Voici comment exploiter les nouvelles fonctionnalités :

```javascript
// Fonction de modération avec flags Version 2
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
      // Afficher le flag et les raisons
      displayFlagResult(result.flag, result.flag_reasons);
      
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

// Affichage du flag et des raisons
function displayFlagResult(flag, reasons) {
  const flagEmoji = flag === 'RED' ? '🔴' : '🟢';
  const flagText = flag === 'RED' ? 'Vérification humaine requise' : 'Publication automatique possible';
  
  console.log(`${flagEmoji} FLAG ${flag}: ${flagText}`);
  
  if (reasons && reasons.length > 0) {
    console.log('Raisons:');
    reasons.forEach(reason => console.log(`  • ${reason}`));
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
    // Traitement selon le flag
    if (resultat.flag === 'RED') {
      // Vérification humaine requise
      const reasons = resultat.flag_reasons.join('\n• ');
      alert(`🔴 Vérification humaine requise\n\nRaisons:\n• ${reasons}\n\nL'avis sera envoyé pour validation avant publication.`);
      
      // Envoyer vers la file de vérification humaine
      await sendForHumanReview({
        original_text: resultat.original_text,
        moderated_text: resultat.moderated_text,
        flag_reasons: resultat.flag_reasons
      });
      
    } else if (resultat.flag === 'GREEN') {
      // Publication automatique possible
      if (resultat.is_moderated) {
        const sources = resultat.moderation_details.sources.join(', ');
        if (confirm(`🟢 Avis validé automatiquement\n\nModération appliquée par: ${sources}\n\nVoulez-vous publier la version modérée ?`)) {
          await publishAutomatically(resultat.moderated_text);
        }
      } else {
        // Aucune modération nécessaire
        alert('🟢 Avis validé et publié automatiquement !');
        await publishAutomatically(resultat.original_text);
      }
    }
  } else {
    alert('Erreur lors de la modération. Veuillez réessayer.');
  }
});

// Fonctions de traitement des flags
async function sendForHumanReview(data) {
  // Logique d'envoi vers système de vérification humaine
  try {
    const response = await fetch('/api/moderation-queue', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...data,
        status: 'pending_human_review',
        timestamp: new Date().toISOString()
      })
    });
    
    if (response.ok) {
      console.log('✅ Avis envoyé pour vérification humaine');
    }
  } catch (error) {
    console.error('Erreur envoi vérification:', error);
  }
}

async function publishAutomatically(text) {
  // Logique de publication automatique
  try {
    const response = await fetch('/api/reviews', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        status: 'published',
        publication_type: 'automatic',
        timestamp: new Date().toISOString()
      })
    });
    
    if (response.ok) {
      console.log('✅ Avis publié automatiquement');
    }
  } catch (error) {
    console.error('Erreur publication automatique:', error);
  }
}
```

### 8.5. Intégration PHP avec gestion des flags

```php
<?php
function traiterAvisAvecFlags($texteAvis, $seuil = 1.0) {
    $url = 'http://localhost:5004/moderate';
    $data = json_encode([
        'text' => $texteAvis,
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
        return ['error' => 'Erreur de connexion API'];
    }
    
    $resultat = json_decode($result, true);
    
    if ($resultat && $resultat['status'] === 'success') {
        // Traitement selon le flag
        if ($resultat['flag'] === 'RED') {
            // Vérification humaine requise
            return envoyerPourVerificationHumaine($resultat);
        } elseif ($resultat['flag'] === 'GREEN') {
            // Publication automatique possible
            return publierAutomatiquement($resultat);
        }
    }
    
    return ['error' => 'Erreur de modération'];
}

function envoyerPourVerificationHumaine($resultat) {
    // Insertion en base pour vérification humaine
    $pdo = getPDOConnection();
    $stmt = $pdo->prepare(
        "INSERT INTO moderation_queue (original_text, moderated_text, flag_reasons, status, created_at) 
         VALUES (?, ?, ?, 'pending_human_review', NOW())"
    );
    
    $stmt->execute([
        $resultat['original_text'],
        $resultat['moderated_text'],
        json_encode($resultat['flag_reasons'])
    ]);
    
    return [
        'status' => 'queued_for_review',
        'message' => '🔴 Avis envoyé pour vérification humaine',
        'reasons' => $resultat['flag_reasons']
    ];
}

function publierAutomatiquement($resultat) {
    // Publication directe en base
    $pdo = getPDOConnection();
    $stmt = $pdo->prepare(
        "INSERT INTO reviews (text, status, publication_type, moderation_applied, created_at) 
         VALUES (?, 'published', 'automatic', ?, NOW())"
    );
    
    $stmt->execute([
        $resultat['moderated_text'],
        $resultat['is_moderated'] ? 1 : 0
    ]);
    
    return [
        'status' => 'published',
        'message' => '🟢 Avis publié automatiquement',
        'moderation_applied' => $resultat['is_moderated']
    ];
}

// Exemple d'utilisation
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $avis = $_POST['texte_avis'] ?? '';
    
    if (!empty($avis)) {
        $resultat = traiterAvisAvecFlags($avis);
        
        // Retourner le résultat en JSON pour AJAX
        header('Content-Type: application/json');
        echo json_encode($resultat);
    }
}
?>
```

### 8.6. Gestion intelligente des mots non détectés

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

### 8.7. Interface de gestion avancée avec flags

Créez une interface d'administration pour gérer la modération :

```html
<!-- Interface d'administration -->
<div id="moderation-admin">
  <h3>🔧 Administration de la modération avec flags</h3>
  
  <!-- Test de modération -->
  <div class="test-section">
    <h4>Test de modération</h4>
    <textarea id="test-text" placeholder="Texte à tester..."></textarea>
    <button onclick="testModeration()">Tester</button>
    
    <div id="test-results" style="display:none;">
      <h5>Résultats :</h5>
      <div id="flag-result"></div>
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
    // Afficher le flag avec couleur
    const flagEmoji = result.flag === 'RED' ? '🔴' : '🟢';
    const flagColor = result.flag === 'RED' ? '#dc3545' : '#28a745';
    const flagText = result.flag === 'RED' ? 'Vérification humaine' : 'Publication automatique';
    
    document.getElementById('flag-result').innerHTML = 
      `<div style="color: ${flagColor}; font-weight: bold; margin-bottom: 10px;">
         ${flagEmoji} FLAG ${result.flag}: ${flagText}
         ${result.flag_reasons && result.flag_reasons.length > 0 ? 
           '<br><small>Raisons: ' + result.flag_reasons.join(', ') + '</small>' : ''}
       </div>`;
    
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

### 8.8. Configuration des flags en temps réel

```html
<!-- Interface de configuration des flags -->
<div class="flag-config-section">
  <h4>⚙️ Configuration des flags RED/GREEN</h4>
  
  <div class="config-form">
    <div class="form-group">
      <label>Seuil API Mistral:</label>
      <input type="range" id="api-threshold" min="0" max="1" step="0.05" value="0.3">
      <span id="threshold-value">0.3</span>
    </div>
    
    <div class="form-group">
      <label>
        <input type="checkbox" id="forbidden-words-red" checked>
        Mots interdits → FLAG RED
      </label>
    </div>
    
    <div class="form-group">
      <label>
        <input type="checkbox" id="proper-names-red" checked>
        Noms propres → FLAG RED (RGPD)
      </label>
    </div>
    
    <div class="form-group">
      <label>
        <input type="checkbox" id="text-modified-red" checked>
        Texte modifié → FLAG RED
      </label>
    </div>
    
    <button onclick="saveFlags Configuration()">Sauvegarder</button>
  </div>
  
  <div id="config-preview" class="preview-section"></div>
</div>

<script>
// Gestion de la configuration des flags
const thresholdSlider = document.getElementById('api-threshold');
const thresholdValue = document.getElementById('threshold-value');

thresholdSlider.addEventListener('input', function() {
  thresholdValue.textContent = this.value;
  updateConfigPreview();
});

function updateConfigPreview() {
  const config = getCurrentConfig();
  const preview = document.getElementById('config-preview');
  
  const redConditions = [];
  if (config.mistral_api_score_threshold < 1.0) {
    redConditions.push(`Score API > ${config.mistral_api_score_threshold}`);
  }
  if (config.forbidden_words_trigger_red) {
    redConditions.push('Mots interdits détectés');
  }
  if (config.proper_names_trigger_red) {
    redConditions.push('Noms propres détectés');
  }
  if (config.text_modification_trigger_red) {
    redConditions.push('Texte modifié');
  }
  
  preview.innerHTML = `
    <h5>Prévision du comportement :</h5>
    <div style="color: #dc3545;">
      <strong>🔴 FLAG RED si :</strong><br>
      ${redConditions.length > 0 ? redConditions.map(c => `• ${c}`).join('<br>') : '• Aucune condition (tous GREEN)'}
    </div>
    <div style="color: #28a745; margin-top: 10px;">
      <strong>🟢 FLAG GREEN si :</strong><br>
      • Aucune condition RED remplie
    </div>
  `;
}

function getCurrentConfig() {
  return {
    mistral_api_score_threshold: parseFloat(thresholdSlider.value),
    forbidden_words_trigger_red: document.getElementById('forbidden-words-red').checked,
    proper_names_trigger_red: document.getElementById('proper-names-red').checked,
    text_modification_trigger_red: document.getElementById('text-modified-red').checked
  };
}

async function saveFlagsConfiguration() {
  const config = getCurrentConfig();
  
  try {
    const response = await fetch('http://localhost:5004/update_flag_config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ flag_config: config })
    });
    
    const result = await response.json();
    
    if (result.status === 'success') {
      alert('✅ Configuration sauvegardée avec succès !');
    } else {
      alert('❌ Erreur lors de la sauvegarde');
    }
  } catch (error) {
    alert('❌ Erreur de connexion: ' + error.message);
  }
}

// Charger la configuration au démarrage
async function loadFlagsConfiguration() {
  try {
    const response = await fetch('http://localhost:5004/get_flag_config');
    const result = await response.json();
    
    if (result.status === 'success') {
      const config = result.flag_config;
      
      thresholdSlider.value = config.mistral_api_score_threshold;
      thresholdValue.textContent = config.mistral_api_score_threshold;
      document.getElementById('forbidden-words-red').checked = config.forbidden_words_trigger_red;
      document.getElementById('proper-names-red').checked = config.proper_names_trigger_red;
      document.getElementById('text-modified-red').checked = config.text_modification_trigger_red;
      
      updateConfigPreview();
    }
  } catch (error) {
    console.error('Erreur lors du chargement de la config:', error);
  }
}

// Charger au démarrage de la page
document.addEventListener('DOMContentLoaded', loadFlagsConfiguration);
</script>
```

### 8.9. Intégration avec frameworks modernes

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
      
      // Traitement automatique selon le flag
      if (result.flag === 'RED') {
        console.log('🔴 Avis en attente de vérification humaine');
        // Logique pour envoi en file d'attente
      } else if (result.flag === 'GREEN') {
        console.log('🟢 Avis validé pour publication automatique');
        // Logique de publication automatique
      }
      
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

// Composant d'affichage des flags
function FlagDisplay({ flag, reasons }) {
  if (!flag) return null;
  
  const isRed = flag === 'RED';
  const emoji = isRed ? '🔴' : '🟢';
  const color = isRed ? '#dc3545' : '#28a745';
  const text = isRed ? 'Vérification humaine requise' : 'Publication automatique possible';
  
  return (
    <div className={`flag-display flag-${flag.toLowerCase()}`} style={{ color, padding: '15px', borderRadius: '8px', backgroundColor: isRed ? '#fff5f5' : '#f0fff4', border: `2px solid ${color}` }}>
      <div style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '8px' }}>
        {emoji} FLAG {flag}: {text}
      </div>
      {reasons && reasons.length > 0 && (
        <div style={{ fontSize: '14px', opacity: 0.8 }}>
          <strong>Raisons:</strong>
          <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
            {reasons.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
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

**✓ Last update : 31 Août 2025 - 17h51**

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
