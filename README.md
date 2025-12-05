# 🌱 Chat'Bruti - Interface Streamlit

Interface web interactive pour dialoguer avec Chat'Bruti, le philosophe permaculturel absurde, via Ollama.

## 🌐 Accès en ligne

**Application déployée :** [http://162.38.112.231/](http://162.38.112.231/)

## 📋 Description

Chat'Bruti est un chatbot philosophe qui ne répond jamais directement aux questions et mélange constamment plusieurs langues (grec, cyrillique, arabe, chinois, etc.) dans ses réponses. Il est obsédé par les timbres et transforme chaque question en réflexion absurde.

Ce projet a été développé dans le cadre de la **Nuit de l'Info 2025** pour le défi **Chat'bruti** proposé par Viveris.

## 🔄 Démarche

Dans un premier temps, nous avons tenté une approche de **fine-tuning** en utilisant un **ADAPTER** dans la directive `FROM` du Modelfile. Cette méthode permettait théoriquement d'adapter un modèle de base avec des paramètres spécifiques pour obtenir le comportement désiré de Chat'Bruti.

Cependant, après plusieurs essais, les résultats obtenus n'étaient pas satisfaisants : le modèle ne respectait pas suffisamment les contraintes de personnalité (mélange de langues, obsession des timbres, non-réponse directe aux questions, etc.).

Nous avons donc opté pour une **démarche plus simple et plus efficace** :

- Utilisation directe du modèle **mistral-small:22b** dans la directive `FROM`
- Spécification détaillée de toutes les consignes de personnalité, de style et de comportement dans la section `SYSTEM` du Modelfile

Cette approche s'est révélée beaucoup plus facile, permettant d'obtenir un Chat'Bruti fidèle à sa personnalité absurde et multilingue, tout en restant simple à maintenir et à ajuster.

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

3. **Pull le modèle mistral-small:22b** :

```bash
ollama pull mistral-small:22b
```

4. **Créer le modèle** :

```bash
ollama create blablabruti2 -f Modelfile
```

## 🎯 Utilisation

### Lancer l'application en local

**Option 1 : Port par défaut (8501)**

```bash
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

## 🔗 Ressources

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation Ollama Python](https://github.com/ollama/ollama-python)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)

## 👥 Équipe

**DISTRACTED/DEFIANT TOUGH NEWTS**

Projet réalisé dans le cadre de la Nuit de l'Info 2025.
