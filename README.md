# 🌱 Chat'Bruti - Interface Streamlit

Interface web interactive pour dialoguer avec Chat'Bruti, le philosophe permaculturel absurde, via Ollama.

## 📋 Description

Chat'Bruti est un chatbot philosophe qui ne répond jamais directement aux questions et mélange constamment plusieurs langues (grec, cyrillique, arabe, chinois, etc.) dans ses réponses. Il est obsédé par la permaculture et transforme chaque question en réflexion absurde.

## 🚀 Installation

### Prérequis

1. **Python 3.8+** installé
2. **Ollama** installé et lancé
3. **Modèle Chat'Bruti** créé dans Ollama

### Étapes d'installation

1. **Installer les dépendances** :

```bash
pip install -r requirements.txt
```

2. **Vérifier qu'Ollama est lancé** :

```bash
# Dans un terminal séparé
ollama serve
```

3. **Vérifier que le modèle existe** :

```bash
ollama list | grep -i chatbruti
```

Si le modèle n'existe pas, créez-le avec :

```bash
ollama create chatbruti -f Modelfile
```

## 🎯 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

### Fonctionnalités

- **Chat interactif** : Dialoguez avec Chat'Bruti en temps réel
- **Historique persistant** : Les conversations sont conservées pendant la session
- **Paramètres ajustables** :
  - Temperature (0.0 - 1.0)
  - Top P (0.0 - 1.0)
  - Max tokens (50 - 1000)
- **Support Unicode** : Affichage correct des caractères multilingues
- **Nouvelle conversation** : Bouton pour réinitialiser l'historique

## 🎨 Interface

### Page principale

- **Header** : Titre et sous-titre multilingue
- **Zone de chat** : Messages utilisateur (bleu) et Chat'Bruti (vert)
- **Input** : Champ de texte avec placeholder amusant

### Sidebar

- **Paramètres du modèle** : Sliders pour ajuster le comportement
- **Informations** : Statut de connexion, modèle actif, nombre de messages
- **À propos** : Description de Chat'Bruti
- **Bouton de réinitialisation** : Nouvelle conversation

## 🛠️ Stack technique

- **Frontend** : Streamlit
- **Backend LLM** : Ollama (API locale)
- **Modèle** : `chatbruti` ou `chatbruiti`
- **Python** : 3.8+

## 🐛 Dépannage

### Ollama non connecté

Si vous voyez "🔴 Ollama non connecté" :

1. Vérifiez qu'Ollama est lancé : `ollama serve`
2. Vérifiez que le service écoute sur le port 11434
3. Redémarrez l'application Streamlit

### Modèle introuvable

Si le modèle n'est pas trouvé :

1. Vérifiez les modèles disponibles : `ollama list`
2. Créez le modèle si nécessaire : `ollama create chatbruti -f Modelfile`
3. L'interface détectera automatiquement les modèles disponibles

### Caractères Unicode non affichés

Streamlit gère nativement l'UTF-8. Si vous avez des problèmes :

1. Vérifiez que votre terminal/navigateur supporte UTF-8
2. Utilisez une police qui supporte Unicode (Noto Sans, Arial, etc.)

## 📝 Notes

- **Port par défaut** : Streamlit utilise le port 8501, Ollama le port 11434
- **Historique** : Les conversations sont stockées en mémoire (session Streamlit) et ne persistent pas après fermeture
- **Performance** : Les réponses dépendent de la puissance de votre machine et du modèle utilisé

## 🔗 Ressources

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation Ollama Python](https://github.com/ollama/ollama-python)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)

## 📄 Licence

Ce projet fait partie de la Nuit de l'Info 2025.

---

**Créé avec 💚 et un peu de compost philosophique**
