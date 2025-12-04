from unsloth import FastLanguageModel
from transformers import TextStreamer

print("🚀 Chargement du modèle entraîné...")

# Charger le modèle entraîné
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="./blablabruti-lora-final",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# Activer le mode inférence
FastLanguageModel.for_inference(model)

print("✅ Modèle chargé !")
print("\n" + "="*50)
print("Test de Blablabruti")
print("="*50 + "\n")

# Questions de test
test_questions = [
    "Bonjour",
    "Quelle heure est-il ?",
    "Comment faire cuire des pâtes ?",
    "Qu'est-ce qu'une blockchain ?",
    "Quel est le sens de la vie ?",
]

for question in test_questions:
    print(f"👤 Question: {question}")
    print("🤖 Blablabruti:")
    
    # Formater la prompt pour Mistral
    prompt = f"<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n"
    inputs = tokenizer([prompt], return_tensors="pt").to("cuda")
    
    # Générer la réponse
    text_streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    _ = model.generate(
        **inputs,
        streamer=text_streamer,
        max_new_tokens=256,
        temperature=0.9,
        do_sample=True,
    )
    
    print("\n" + "-"*50 + "\n")

print("✅ Tests terminés !")

