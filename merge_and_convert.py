"""
Script pour fusionner le LoRA avec le modèle de base et convertir en GGUF
À exécuter sur la VM après l'entraînement
"""
from unsloth import FastLanguageModel
from unsloth.is_pytorch_2_0_plus import is_pytorch_2_0_plus
import torch

print("🚀 Fusion du LoRA avec le modèle de base...")

# Charger le modèle de base
print("📥 Chargement du modèle de base...")
base_model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/mistral-7b-v0.3-bnb-4bit",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# Charger l'adapter LoRA
print("📥 Chargement de l'adapter LoRA...")
model = FastLanguageModel.from_pretrained(
    model_name="./blablabruti-lora-final",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# Fusionner le LoRA avec le modèle de base
print("🔗 Fusion du LoRA...")
model = FastLanguageModel.merge_and_unload(model)

# Sauvegarder le modèle fusionné
print("💾 Sauvegarde du modèle fusionné...")
model.save_pretrained_merged(
    "blablabruti-merged",
    tokenizer,
    save_method="merged_16bit",  # Sauvegarde en 16-bit pour économiser l'espace
)
tokenizer.save_pretrained("blablabruti-merged")

print("✅ Modèle fusionné sauvegardé dans ./blablabruti-merged")
print("\n📝 Prochaines étapes :")
print("1. Le modèle fusionné est dans ./blablabruti-merged")
print("2. Vous pouvez maintenant convertir en GGUF avec llama.cpp")
print("3. Ou utiliser directement avec transformers/Unsloth")

