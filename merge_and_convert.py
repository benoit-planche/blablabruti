"""
Script pour fusionner le LoRA avec le modèle de base et convertir en GGUF
À exécuter sur la VM après l'entraînement
"""
from unsloth import FastLanguageModel
import torch

print("🚀 Fusion du LoRA avec le modèle de base...")

# Charger le modèle avec l'adapter LoRA
print("📥 Chargement du modèle avec l'adapter LoRA...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="./blablabruti-lora-final",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# Fusionner le LoRA avec le modèle de base et sauvegarder
print("🔗 Fusion du LoRA et sauvegarde...")
# Utiliser la méthode Unsloth qui fusionne et sauvegarde en une seule étape
# Si save_pretrained_merged ne fonctionne pas, essayez avec merge_and_unload d'abord
try:
    # Méthode 1 : Utiliser save_pretrained_merged (recommandé)
    model.save_pretrained_merged(
        "blablabruti-merged",
        tokenizer,
        save_method="merged_16bit",  # Sauvegarde en 16-bit pour économiser l'espace
    )
except AttributeError:
    # Méthode 2 : Fusionner d'abord, puis sauvegarder
    print("⚠️  Utilisation de la méthode alternative...")
    from peft import PeftModel
    if isinstance(model, PeftModel):
        model = model.merge_and_unload()
    model.save_pretrained("blablabruti-merged")
    tokenizer.save_pretrained("blablabruti-merged")

print("✅ Modèle fusionné sauvegardé dans ./blablabruti-merged")
print("\n📝 Prochaines étapes :")
print("1. Le modèle fusionné est dans ./blablabruti-merged")
print("2. Vous pouvez maintenant convertir en GGUF avec llama.cpp")
print("3. Ou utiliser directement avec transformers/Unsloth")

