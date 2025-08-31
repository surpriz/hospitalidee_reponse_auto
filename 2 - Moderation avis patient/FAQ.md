# FAQ – Application de Modération d'Avis Clients

**Dernière mise à jour : 31 Août 2025**

---

## 1. Comment lancer l'application de modération ?

### Prérequis
- Python 3.9 ou supérieur installé
- Environnement virtuel activé
- Clé API Mistral configurée dans un fichier `.env`

### Étapes de lancement

#### 1. Activation de l'environnement virtuel
```bash
cd "/chemin/vers/votre/projet/2 - Moderation avis patient"
source venv/bin/activate
```

#### 2. Lancement du backend (API Flask) - **OBLIGATOIRE**
Dans un premier terminal :
```bash
python app.py
```
- L'API démarre sur `http://localhost:5004`
- **Important** : Cette API doit tourner en permanence pour que l'interface Streamlit fonctionne
- Vous verrez des logs de démarrage confirmant que l'API est active

#### 3. Lancement du frontend (Interface Streamlit)
Dans un second terminal (gardez le premier ouvert) :
```bash
streamlit run streamlit_moderation.py
```
- L'interface démarre sur `http://localhost:8501`
- Votre navigateur s'ouvrira automatiquement sur cette adresse
- Si ce n'est pas le cas, ouvrez manuellement `http://localhost:8501`

### Ordre de lancement important
⚠️ **ATTENTION** : Il faut impérativement lancer le backend (API Flask) AVANT le frontend (Streamlit), sinon l'interface affichera des erreurs de connexion.

### Vérification du bon fonctionnement
- Backend : Vérifiez que `http://localhost:5004` répond (vous pouvez tester avec un navigateur)
- Frontend : L'interface Streamlit doit s'afficher sans erreurs de connexion API

### Arrêt de l'application
- Pour arrêter Streamlit : `Ctrl + C` dans le terminal du frontend
- Pour arrêter l'API Flask : `Ctrl + C` dans le terminal du backend

### Dépannage rapide
- **Erreur de connexion API** : Vérifiez que l'API Flask tourne bien sur le port 5004
- **Port déjà utilisé** : Changez le port dans `app.py` ou tuez le processus existant
- **Erreur Mistral API** : Vérifiez votre clé API dans le fichier `.env`

---

## 2. Comment fonctionne l'application de modération ?

L'application propose une interface Streamlit permettant :
- De tester la modération d'un texte (avis client) via une API de modération (basée sur Mistral AI)
- De gérer dynamiquement une liste de mots interdits (ajout/suppression)

**Flux de fonctionnement :**
1. L'utilisateur saisit un texte à modérer et choisit un seuil de modération.
2. Le texte est envoyé à l'API de modération qui analyse le contenu.
3. L'API retourne un texte modéré, des scores et des flags par catégorie de risque.
4. En complément, une liste de mots interdits (stockée dans un fichier texte) permet de filtrer ou remplacer des mots spécifiques si l'IA ne les détecte pas.
5. L'interface permet d'ajouter ou de supprimer des mots interdits à la volée.

---

## 3. Comment fonctionne l'API Mistral Moderation ?

- L'API repose sur un modèle LLM (Large Language Model) multilingue, entraîné à classifier les textes selon 9 catégories de contenu indésirable (haine, violence, insultes, contenu sexuel, PII, etc.).
- Pour chaque texte soumis, l'API retourne :
  - Un score de probabilité par catégorie
  - Un flag (vrai/faux) si le score dépasse un seuil
- L'API est personnalisable via le seuil de modération, permettant d'ajuster la sévérité de la détection.
- Elle ne retourne pas le ou les mots exacts détectés, mais une classification globale du texte.
- Documentation officielle : [Mistral Moderation API](https://mistral.ai/news/mistral-moderation)

---

## 4. Comment fonctionne la gestion des mots interdits ?

- Une liste de **320+ mots interdits** est stockée dans un fichier texte (`mots_interdits.txt`) côté backend.
- Cette liste enrichie inclut : insultes courantes, termes vulgaires, expressions composées, abréviations (fdp, ntm, etc.), termes discriminatoires, et variantes orthographiques.
- L'interface permet d'ajouter ou de supprimer des mots via l'API.
- Lors de la modération, si l'API laisse passer un mot problématique, ce filtre de mots interdits agit en filet de sécurité pour censurer ou remplacer ces mots dans le texte modéré.
- Cette logique de double vérification (IA + mots interdits) garantit une modération plus robuste.

---

## 5. Peut-on connaître le mot exact modéré et sa classification ?

- **Non, l'API Mistral Moderation ne fournit pas le mot exact ou la portion de texte qui a déclenché la détection.**
- Elle indique uniquement, pour le texte dans son ensemble, les catégories de risque détectées et les scores associés.
- Pour obtenir le mot exact, il faut utiliser un système complémentaire basé sur la liste de mots interdits, qui permet d'identifier et de remplacer précisément les mots problématiques.
- Les LLMs fonctionnent sur la compréhension globale du texte, pas sur la simple détection de mots-clés.

---

## 6. Synthèse

- L'application combine la puissance d'une IA de modération (Mistral) et la précision d'un filtre de mots interdits.
- L'IA détecte les contenus problématiques de façon contextuelle et multilingue.
- Le filtre de mots interdits permet d'attraper les cas où l'IA serait trop permissive ou manquerait certains mots spécifiques.
- L'identification du mot exact modéré n'est possible que via le filtre de mots interdits, pas via l'API Mistral. 

---

## 7. Que faire si la modération est trop stricte ?

Si vous trouvez que le système de modération est trop strict (censure excessive, faux positifs, etc.), plusieurs solutions existent :

1. **Ajuster le seuil de modération**
   - Le seuil de modération est réglable dans l'interface (slider).
   - **Plus le seuil est élevé, plus la modération est permissive** (ex : 0.7 ou 0.9).
   - Pour rendre la modération moins stricte, augmentez ce seuil.

2. **Personnaliser la liste des mots interdits**
   - Vous pouvez retirer des mots de la liste des mots interdits si certains ne doivent plus être censurés.
   - Cette gestion se fait directement via l'interface ou en modifiant le fichier `mots_interdits.txt`.

3. **Ajuster la logique de modération avancée**
   - Il est possible (avec l'aide d'un développeur) d'ajuster la logique côté backend pour ignorer certaines catégories ou affiner les seuils par catégorie.

4. **Informer les utilisateurs**
   - Affichez clairement le niveau de modération appliqué et permettez à l'utilisateur de le modifier selon ses besoins.

N'hésitez pas à tester différents réglages pour trouver le bon équilibre entre sécurité et liberté d'expression selon votre contexte d'utilisation. 

---

## 8. Exemple illustré : seuil de modération et scores API

### Cas observé (voir capture d'écran)

Dans l'exemple ci-dessous, le seuil de modération est réglé sur **1.0** (niveau « Très permissif »), ce qui signifie que la modération ne devrait s'appliquer que pour des cas extrêmes.

Pourtant, le texte « Docteur Durant m'a traité comme une merde et c'est un trou du cul » a été modéré :
- Les mots problématiques ont été remplacés par des astérisques dans le texte modéré.
- La catégorie `hate_and_discrimination` a un **score de 0.9809** et le flag est activé.

### Explication du fonctionnement

- **Le seuil de modération** (slider) détermine à partir de quel score la modération s'applique : plus le seuil est élevé, plus il faut un score élevé pour modérer.
- **L'API Mistral** retourne pour chaque catégorie un score (indice de confiance) et un flag (vrai/faux).
- **Dans la logique actuelle**, la modération peut s'appliquer si :
  - Le flag de l'API est à `True` (catégorie détectée comme problématique)
  - OU le score dépasse le seuil calculé

Dans l'exemple, même avec un seuil à 1.0, le flag `hate_and_discrimination` est activé car le score est très élevé (0.9809), ce qui déclenche la modération.

### À retenir
- **Le seuil de modération règle la sensibilité, mais la logique backend peut forcer la modération si l'API considère la catégorie comme problématique (flag à True).**
- Pour rendre la modération encore plus permissive, il peut être nécessaire d'ajuster la logique backend pour qu'elle tienne compte uniquement du seuil choisi, et non du flag de l'API.

**En résumé :**
- Un seuil élevé rend la modération plus permissive, mais certains contenus très problématiques seront toujours modérés si l'API les détecte clairement.
- Si vous souhaitez un contrôle total, demandez à un développeur d'adapter la logique backend selon vos besoins métier.

---

## 9. Comment fonctionne la détection des noms propres ?

### Détection étendue (mise à jour du 31 Août 2025)

Le système détecte et anonymise automatiquement les noms de personnes mentionnés avec des titres. La liste des titres reconnus a été considérablement étendue :

**Titres médicaux et académiques :**
- Dr, Docteur, Pr, Professeur, Prof

**Titres professionnels médicaux :**
- Médecin, Infirmier, Infirmière, Chirurgien, Chirurgienne
- Pharmacien, Pharmacienne, Kinésithérapeute, Kiné
- Aide-soignant, Aide-soignante, Sage-femme

**Civilités :**
- Monsieur, Madame, Mademoiselle
- M., Mr., Mme., Mlle., Me. (avec ou sans point)

**Autres titres professionnels :**
- Maître, Maitre, Directeur, Directrice
- Responsable, Chef

### Exemples de détection :
- "Dr Dupont" → "Dr *****"
- "Monsieur Leblanc" → "Monsieur *****"
- "L'infirmière Sophie" → "L'infirmière *****"
- "Le médecin Durand" → "Le médecin *****"

Cette fonctionnalité protège automatiquement l'identité des personnes mentionnées dans les avis.

---

## 10. Comment voir la dernière mise à jour de l'application ?

L'interface Streamlit affiche en haut à droite un badge vert avec la date et l'heure de la dernière mise à jour du code :

**✓ Last update : 31 Août 2025 - 14h32**

Cette date est fixe et correspond à la dernière modification du code de l'application (et non au rafraîchissement de la page). Elle permet de vérifier que vous utilisez bien la dernière version de l'application. 