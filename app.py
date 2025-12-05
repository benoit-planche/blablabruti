import streamlit as st
import ollama
import time
from typing import List, Dict

# Configuration de la page
st.set_page_config(
    page_title="Chat'Bruti - Philosophe Permaculturel",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fonction pour générer le CSS selon le thème
def get_css(theme):
    if theme == "light":
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,700;1,400&family=Noto+Sans+Arabic:wght@400;700&family=Noto+Sans+Devanagari:wght@400;700&family=Noto+Sans+Hebrew:wght@400;700&family=Noto+Sans+SC:wght@400;700&family=Noto+Sans+TC:wght@400;700&display=swap');
            
            * {
                font-family: 'Noto Sans', 'Noto Sans Arabic', 'Noto Sans Devanagari', 'Noto Sans Hebrew', 'Noto Sans SC', 'Noto Sans TC', 'Arial Unicode MS', 'Segoe UI', sans-serif !important;
            }
            
            body, .stApp {
                color: #2C3E50 !important;
            }
            
            .main {
                background-color: #FFFFFF;
            }
            
            .stApp {
                background-color: #FFFFFF;
            }
            
            .stTextInput > div > div > input {
                background-color: #FFFFFF;
                font-family: 'Noto Sans', 'Noto Sans Arabic', 'Noto Sans Devanagari', 'Noto Sans Hebrew', 'Noto Sans SC', 'Noto Sans TC', 'Arial Unicode MS', sans-serif !important;
            }
            
            h1 {
                color: #6B8E23;
                font-family: 'Comic Sans MS', 'Noto Sans', cursive;
            }
            
            .user-message {
                background-color: #E3F2FD;
                color: #1A237E;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                text-align: right;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                font-family: 'Noto Sans', 'Noto Sans Arabic', 'Noto Sans Devanagari', 'Noto Sans Hebrew', 'Noto Sans SC', 'Noto Sans TC', 'Arial Unicode MS', sans-serif !important;
                font-size: 17px;
                line-height: 1.8;
                word-wrap: break-word;
                direction: ltr;
                letter-spacing: 0.3px;
            }
            
            .bot-message {
                background-color: #FFFFFF;
                color: #2C3E50;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                text-align: left;
                border-left: 4px solid #6B8E23;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                font-family: 'Noto Sans', 'Noto Sans Arabic', 'Noto Sans Devanagari', 'Noto Sans Hebrew', 'Noto Sans SC', 'Noto Sans TC', 'Arial Unicode MS', sans-serif !important;
                font-size: 17px;
                line-height: 1.8;
                word-wrap: break-word;
                direction: ltr;
                white-space: pre-wrap;
                letter-spacing: 0.3px;
            }
            
            .stChatInput {
                background-color: #FFFFFF;
            }
            
            /* Support pour les caractères RTL (arabe, hébreu) */
            .rtl-text {
                direction: rtl;
                text-align: right;
            }
            
            /* Masquer le bouton de toggle de la sidebar par défaut de Streamlit */
            button[kind="header"] {
                display: none !important;
            }
            
            [data-testid="stSidebarCollapseButton"],
            [data-testid="stSidebarExpandButton"],
            button[data-testid="baseButton-header"],
            .stApp > header button {
                display: none !important;
            }
            
            /* Améliorer l'apparence de la sidebar */
            section[data-testid="stSidebar"] {
                background-color: #FFFFFF;
            }
        </style>
        """
    else:  # dark mode
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,700;1,400&family=Noto+Sans+Arabic:wght@400;700&family=Noto+Sans+Devanagari:wght@400;700&family=Noto+Sans+Hebrew:wght@400;700&family=Noto+Sans+SC:wght@400;700&family=Noto+Sans+TC:wght@400;700&display=swap');
            
            * {
                font-family: 'Noto Sans', 'Noto Sans Arabic', 'Noto Sans Devanagari', 'Noto Sans Hebrew', 'Noto Sans SC', 'Noto Sans TC', 'Arial Unicode MS', 'Segoe UI', sans-serif !important;
            }
            
            .main {
                background-color: #1E1E1E;
            }
            
            .stApp {
                background-color: #1E1E1E;
            }
            
            .stTextInput > div > div > input {
                background-color: #2D2D2D;
                color: #FFFFFF;
                font-family: 'Noto Sans', 'Noto Sans Arabic', 'Noto Sans Devanagari', 'Noto Sans Hebrew', 'Noto Sans SC', 'Noto Sans TC', 'Arial Unicode MS', sans-serif !important;
            }
            
            h1 {
                color: #8BC34A;
                font-family: 'Comic Sans MS', 'Noto Sans', cursive;
            }
            
            .user-message {
                background-color: #1E3A5F;
                color: #FFFFFF;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                text-align: right;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                font-family: 'Noto Sans', 'Noto Sans Arabic', 'Noto Sans Devanagari', 'Noto Sans Hebrew', 'Noto Sans SC', 'Noto Sans TC', 'Arial Unicode MS', sans-serif !important;
                font-size: 16px;
                line-height: 1.6;
                word-wrap: break-word;
                direction: ltr;
            }
            
            .bot-message {
                background-color: #2D2D2D;
                color: #E0E0E0;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                text-align: left;
                border-left: 4px solid #8BC34A;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                font-family: 'Noto Sans', 'Noto Sans Arabic', 'Noto Sans Devanagari', 'Noto Sans Hebrew', 'Noto Sans SC', 'Noto Sans TC', 'Arial Unicode MS', sans-serif !important;
                font-size: 16px;
                line-height: 1.6;
                word-wrap: break-word;
                direction: ltr;
                white-space: pre-wrap;
            }
            
            .stChatInput {
                background-color: #2D2D2D;
            }
            
            /* Masquer le bouton de toggle de la sidebar par défaut de Streamlit */
            button[kind="header"] {
                display: none !important;
            }
            
            [data-testid="stSidebarCollapseButton"],
            [data-testid="stSidebarExpandButton"],
            button[data-testid="baseButton-header"],
            .stApp > header button {
                display: none !important;
            }
            
            /* Améliorer l'apparence de la sidebar */
            section[data-testid="stSidebar"] {
                background-color: #1E1E1E;
            }
        </style>
        """

# Initialisation de l'historique de conversation et du thème
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # light ou dark

# Appliquer le CSS selon le thème
st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# Titre principal
st.title("🌱 Chat'Bruti - Le Philosophe Permaculturel Absurde")
st.markdown("*Αχ, Bonjour! Готов говорить о комpost ? 🍄*")

# Configuration par défaut du modèle
try:
    models = ollama.list()
    available_models = [model['name'] for model in models.get('models', [])]
    blablabruti_models = [m for m in available_models if 'blablabruti' in m.lower() or 'chatbruti' in m.lower() or 'chatbruiti' in m.lower()]
    
    if blablabruti_models:
        blablabruti_models.sort(key=lambda x: (x.lower() != 'blablabruti2', x.lower()))
        model_name = blablabruti_models[0]
    elif available_models:
        model_name = available_models[0]
    else:
        model_name = "blablabruti2"
except Exception:
    model_name = "blablabruti2"

# Paramètres par défaut
temperature = 0.9
top_p = 0.9
max_tokens = 512

# Sidebar - Options simples
with st.sidebar:
    # Toggle pour le thème
    theme_options = {"light": "☀️ Mode clair", "dark": "🌙 Mode sombre"}
    current_theme_label = theme_options[st.session_state.theme]
    
    if st.button(current_theme_label, use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()
    
    st.divider()
    
    if st.button("🔄 Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Zone de chat - Affichage de l'historique
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.info("💬 Commencez une conversation avec Chat'Bruti ! Il vous parlera de permaculture... ou pas !")
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            # Échapper le HTML pour éviter les problèmes de sécurité
            content = message["content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            st.markdown(f'<div class="user-message">👤 <strong>Vous :</strong><br>{content}</div>', 
                       unsafe_allow_html=True)
        else:
            # Échapper le HTML et préserver les sauts de ligne
            content = message["content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            st.markdown(f'<div class="bot-message">🌱 <strong>Chat\'Bruti :</strong><br>{content}</div>', 
                       unsafe_allow_html=True)

# Input utilisateur
user_input = st.chat_input("Pose ta question (ou ne la pose pas, je parlerai de permaculture quand même...)")

if user_input:
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Afficher le message utilisateur immédiatement
    with chat_container:
        # Échapper le HTML
        escaped_input = user_input.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(f'<div class="user-message">👤 <strong>Vous :</strong><br>{escaped_input}</div>', 
                   unsafe_allow_html=True)
    
    # Préparer les messages pour Ollama
    messages_for_ollama = [{"role": msg["role"], "content": msg["content"]} 
                           for msg in st.session_state.messages]
    
    # Générer la réponse
    with st.spinner("Chat'Bruti réfléchit... ou pas... 🤔"):
        try:
            response = ollama.chat(
                model=model_name,
                messages=messages_for_ollama,
                options={
                    "temperature": temperature,
                    "top_p": top_p,
                    "num_predict": max_tokens
                }
            )
            
            bot_response = response['message']['content']
            
            # Ajouter la réponse du bot
            st.session_state.messages.append({
                "role": "assistant", 
                "content": bot_response
            })
            
            # Recharger pour afficher la réponse
            st.rerun()
            
        except Exception as e:
            error_msg = f"❌ Erreur lors de la génération : {str(e)}"
            st.error(error_msg)
            st.info("💡 Vérifie que Ollama est lancé (`ollama serve`) et que le modèle existe (`ollama list`).")
            
            # Ajouter un message d'erreur à l'historique pour informer l'utilisateur
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Αχ, une erreur technique ! {str(e)}. Peut-être que les vers de terre ont mangé les câbles ? 🪱"
            })
            st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B8E23; padding: 20px;'>
    <small>Créé avec 💚 et un peu de compost philosophique | Powered by Ollama & Streamlit</small>
</div>
""", unsafe_allow_html=True)

