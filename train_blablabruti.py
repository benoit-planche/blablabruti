from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# Configuration
max_seq_length = 2048
# Utilise Mistral 7B quantizée pour économiser la VRAM
# Pour Mistral 22B, changez en "unsloth/mistral-22b-v0.3-bnb-4bit" (nécessite 16GB+ VRAM)
model_name = "unsloth/mistral-7b-v0.3-bnb-4bit"

print(f"🚀 Chargement du modèle {model_name}...")

# Charger le modèle
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    dtype=None,  # Auto-détection
    load_in_4bit=True,  # Utilise la quantization 4-bit pour économiser VRAM
)

# Configurer LoRA
print("🔧 Configuration LoRA...")
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # Rang LoRA (16-32 est un bon équilibre, augmentez à 32 pour plus de capacité)
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
)

# Charger le dataset
print("📚 Chargement du dataset...")
dataset = load_dataset("json", data_files="chatbruti_dataset.json", split="train")

# Formater les conversations pour Mistral
def format_prompts(examples):
    texts = []
    for conversation in examples["conversations"]:
        text = ""
        for message in conversation:
            if message["from"] == "human":
                text += f"<|im_start|>user\n{message['value']}<|im_end|>\n"
            else:
                text += f"<|im_start|>assistant\n{message['value']}<|im_end|>\n"
        texts.append(text)
    return {"text": texts}

dataset = dataset.map(format_prompts, batched=True)

print(f"✅ Dataset chargé : {len(dataset)} exemples")

# Configuration de l'entraînement
training_args = TrainingArguments(
    output_dir="./blablabruti-lora",
    per_device_train_batch_size=2,  # Réduisez à 1 si vous manquez de VRAM
    gradient_accumulation_steps=4,  # Augmentez à 8 si batch_size=1
    warmup_steps=10,
    max_steps=500,  # Augmentez à 1000-2000 si vous avez beaucoup de données
    learning_rate=2e-4,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    logging_steps=10,
    optim="adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="linear",
    seed=3407,
    save_strategy="steps",
    save_steps=100,
    report_to="none",  # Désactive wandb/tensorboard
)

# Entraîner
print("🎓 Début de l'entraînement...")
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    args=training_args,
)

trainer.train()

# Sauvegarder le modèle LoRA
print("💾 Sauvegarde du modèle...")
model.save_pretrained("blablabruti-lora-final")
tokenizer.save_pretrained("blablabruti-lora-final")

print("✅ Entraînement terminé ! Adapter sauvegardé dans ./blablabruti-lora-final")
print("\n📝 Prochaines étapes :")
print("1. Testez le modèle avec le script test_model.py")
print("2. Si satisfait, utilisez-le avec Ollama ou exportez-le en GGUF")

