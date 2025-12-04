# Guide complet : Entraîner un adapter LoRA pour Blablabruti

Ce guide vous permettra de créer un adapter LoRA qui forcera Mistral 7B (ou 22B) à incarner parfaitement **Blablabruti**, le chatbot philosophe du dimanche passionné de timbres.

**Temps estimé : 2-4 heures selon votre matériel**

---

## 📋 Étape 1 : Préparer l'environnement

### 1.1 Vérifier les prérequis

**Matériel nécessaire :**

- GPU NVIDIA avec au moins **8 GB VRAM** (Mistral 7B) ou **16 GB+** (Mistral 22B)
- **50 GB** d'espace disque libre
- Linux, macOS, ou Windows avec WSL2

**Vérifier votre GPU :**

```bash
nvidia-smi
```

### 1.2 Installer les dépendances

```bash
# Créer un environnement virtuel
python3 -m venv blablabruti-env
source blablabruti-env/bin/activate  # Sur Windows: blablabruti-env\Scripts\activate

# Installer unsloth (le plus simple pour débuter)
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
pip install --no-deps trl peft accelerate bitsandbytes
```

---

## 📚 Étape 2 : Créer le dataset d'entraînement

### 2.1 Le fichier `chatbruti_dataset.json`

Le fichier `chatbruti_dataset.json` contient **30 exemples** de conversations avec Blablabruti. Chaque exemple montre :

- Le mélange de langues (grec, cyrillique, hébreu, chinois, etc.)
- La passion pour les timbres (même quand la question n'est pas liée)
- Le style absurde et philosophique

**Format :**

```json
[
  {
    "conversations": [
      {"from": "human", "value": "Question"},
      {"from": "gpt", "value": "Réponse de Blablabruti avec mélange de langues et référence aux timbres"}
    ]
  }
]
```

**⚠️ IMPORTANT :** Plus vous avez d'exemples (100-500+), meilleur sera votre adapter. Les 30 exemples fournis sont un début. Idéalement, créez 100-200 exemples en variant les questions tout en gardant le style Blablabruti.

**Conseils pour créer plus d'exemples :**

- Variez les types de questions (techniques, philosophiques, pratiques, absurdes)
- Toujours détourner vers les timbres
- Toujours mélanger plusieurs langues
- Garder le ton absurde et sûr de soi

---

## 🎓 Étape 3 : Script de fine-tuning

### 3.1 Le fichier `train_blablabruti.py`

Le script est déjà créé et configuré. Il utilise :

- **Mistral 7B** par défaut (changeable pour 22B)
- **LoRA** avec rang 16
- **Quantization 4-bit** pour économiser la VRAM
- **Format Mistral** (`<|im_start|>user/assistant<|im_end|>`)

### 3.2 Lancer l'entraînement

```bash
python train_blablabruti.py
```

**Temps estimé :** 30 minutes à 2 heures selon votre GPU et la quantité de données.

**Paramètres ajustables dans le script :**

- `r=16` : Rang LoRA (augmentez à 32 pour plus de capacité, mais plus de VRAM)
- `max_steps=500` : Nombre d'étapes (augmentez à 1000-2000 pour plus de données)
- `per_device_train_batch_size=2` : Réduisez à 1 si vous manquez de VRAM
- `gradient_accumulation_steps=4` : Augmentez à 8 si batch_size=1

**Pour utiliser Mistral 22B :**
Changez dans le script :

```python
model_name = "unsloth/mistral-22b-v0.3-bnb-4bit"
```

---

## 🧪 Étape 4 : Tester le modèle

### 4.1 Créer un script de test

Créez `test_model.py` :

```python
from unsloth import FastLanguageModel
from transformers import TextStreamer

# Charger le modèle entraîné
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="./blablabruti-lora-final",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

FastLanguageModel.for_inference(model)

# Tester
prompt = "<|im_start|>user\nBonjour<|im_end|>\n<|im_start|>assistant\n"
inputs = tokenizer([prompt], return_tensors="pt").to("cuda")

text_streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
_ = model.generate(**inputs, streamer=text_streamer, max_new_tokens=256, temperature=0.9)
```

Lancez :

```bash
python test_model.py
```

---

## 🔄 Étape 5 : Utiliser avec Ollama (Option 1)

### 5.1 Exporter en format Ollama

Ollama peut utiliser les adapters LoRA directement. Créez un Modelfile :

```dockerfile
FROM mistral:7b

ADAPTER ./blablabruti-lora-final

PARAMETER temperature 0.9
PARAMETER num_ctx 8192
```

Puis :

```bash
ollama create blablabruti -f Modelfile
ollama run blablabruti
```

---

## 🔄 Étape 6 : Convertir en GGUF (Option 2)

### 6.1 Installer llama.cpp

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
```

### 6.2 Fusionner le LoRA avec le modèle de base

```bash
# D'abord, télécharger le modèle Mistral 7B complet
# Puis fusionner avec le LoRA
python llama.cpp/convert_lora_to_gguf.py \
  --base-model-path /path/to/mistral-7b \
  --lora-path ./blablabruti-lora-final \
  --outfile blablabruti.gguf
```

---

## 🎯 Étape 7 : Optimisations et conseils

### 7.1 Améliorer les performances

**Si le modèle ne suit pas assez le style :**

- Augmentez `r=32` (rang LoRA)
- Augmentez `max_steps=1000-2000`
- Ajoutez plus d'exemples au dataset (100-200+)

**Si vous manquez de VRAM :**

- Réduisez `per_device_train_batch_size=1`
- Augmentez `gradient_accumulation_steps=8`
- Utilisez Mistral 7B au lieu de 22B

### 7.2 Créer plus d'exemples

Utilisez votre Modelfile actuel avec Ollama pour générer des exemples :

```bash
ollama run blablabruti
```

Posez des questions variées et sauvegardez les réponses dans le format JSON du dataset.

---

## 📊 Résultats attendus

Après l'entraînement, Blablabruti devrait :

- ✅ Toujours détourner vers les timbres
- ✅ Mélanger plusieurs langues dans chaque réponse
- ✅ Avoir un ton absurde et sûr de soi
- ✅ Ne jamais répondre directement aux questions
- ✅ Être inutile mais attachant

---

## 🐛 Dépannage

**Erreur "Out of memory" :**

- Réduisez `per_device_train_batch_size=1`
- Utilisez Mistral 7B au lieu de 22B
- Fermez les autres applications utilisant le GPU

**Le modèle ne suit pas le style :**

- Augmentez le nombre d'exemples (100+)
- Augmentez `max_steps=1000-2000`
- Vérifiez que vos exemples sont cohérents avec le style

**Erreur d'import :**

- Vérifiez que vous êtes dans l'environnement virtuel
- Réinstallez les dépendances : `pip install --upgrade unsloth`

---

## 🎉 C'est parti

Vous avez maintenant tout ce qu'il faut pour entraîner Blablabruti. Bon entraînement ! 🚀
