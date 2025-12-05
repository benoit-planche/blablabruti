import streamlit as st
import ollama
import time
from typing import List, Dict

# Configuration de la page
st.set_page_config(
    page_title="Chat'Bruti - Philosophe Permaculturel",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main {
        background-color: #F0F4EF;
    }
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
    }
    h1 {
        color: #6B8E23;
        font-family: 'Comic Sans MS', cursive;
    }
    .user-message {
        background-color: #E3F2FD;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: right;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .bot-message {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: left;
        border-left: 4px solid #6B8E23;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stChatInput {
        background-color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.title("🌱 Chat'Bruti - Le Philosophe Permaculturel Absurde")
st.markdown("*Αχ, Bonjour! Готов говорить о комpost ? 🍄*")

# Initialisation de l'historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar - Paramètres
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Vérifier la connexion Ollama
    try:
        models = ollama.list()
        st.success("🟢 Ollama connecté")
        
        # Extraire les noms de modèles disponibles
        available_models = [model['name'] for model in models.get('models', [])]
        
        # Filtrer pour trouver les modèles blablabruti (priorité à blablabruti2)
        blablabruti_models = [m for m in available_models if 'blablabruti' in m.lower() or 'chatbruti' in m.lower() or 'chatbruiti' in m.lower()]
        
        # Trier pour mettre blablabruti2 en premier s'il existe
        if blablabruti_models:
            blablabruti_models.sort(key=lambda x: (x.lower() != 'blablabruti2', x.lower()))
            model_name = st.selectbox(
                "Modèle",
                blablabruti_models,
                index=0
            )
        else:
            # Si aucun modèle blablabruti trouvé, proposer les modèles disponibles ou des valeurs par défaut
            if available_models:
                model_name = st.selectbox(
                    "Modèle",
                    available_models,
                    index=0
                )
                st.warning("⚠️ Aucun modèle blablabruti trouvé. Utilisez un modèle disponible.")
            else:
                model_name = st.selectbox(
                    "Modèle",
                    ["blablabruti2", "blablabruti", "chatbruti", "chatbruiti"],
                    index=0
                )
                st.warning("⚠️ Modèle non trouvé. Assurez-vous que le modèle existe.")
    except Exception as e:
        st.error("🔴 Ollama non connecté")
        st.error(f"Erreur : {str(e)}")
        model_name = st.selectbox(
            "Modèle",
            ["blablabruti2", "blablabruti", "chatbruti", "chatbruiti"],
            index=0
        )
        st.info("💡 Assurez-vous qu'Ollama est lancé : `ollama serve`")
    
    st.divider()
    
    temperature = st.slider("Temperature", 0.0, 1.0, 0.85, 0.05)
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Max tokens", 50, 1000, 512, 50)
    
    st.divider()
    
    st.header("📊 Informations")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Modèle actif", model_name)
    
    st.divider()
    
    st.header("ℹ️ À propos")
    st.markdown("""
    **Chat'Bruti** est un philosophe absurde obsédé par la permaculture.
    
    Il ne répond JAMAIS directement aux questions et mélange constamment les langues.
    
    Profite de sa sagesse... discutable ! 🌿
    """)
    
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
            st.markdown(f'<div class="user-message">👤 <strong>Vous :</strong><br>{message["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🌱 <strong>Chat\'Bruti :</strong><br>{message["content"]}</div>', 
                       unsafe_allow_html=True)

# Input utilisateur
user_input = st.chat_input("Pose ta question (ou ne la pose pas, je parlerai de permaculture quand même...)")

if user_input:
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Afficher le message utilisateur immédiatement
    with chat_container:
        st.markdown(f'<div class="user-message">👤 <strong>Vous :</strong><br>{user_input}</div>', 
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

