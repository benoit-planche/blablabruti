#!/bin/bash
# Script pour convertir le modèle fusionné en GGUF
# À exécuter après merge_and_convert.py

echo "🔄 Conversion du modèle fusionné en GGUF..."

# Vérifier que llama.cpp est compilé
if [ ! -f "llama.cpp/build/bin/llama-convert" ]; then
    echo "❌ llama.cpp n'est pas compilé. Compilez-le d'abord :"
    echo "   cd llama.cpp && mkdir -p build && cd build"
    echo "   cmake .. -DCMAKE_BUILD_TYPE=Release"
    echo "   cmake --build . --config Release -j\$(nproc)"
    exit 1
fi

# Convertir en GGUF
echo "📦 Conversion en GGUF..."
python3 llama.cpp/convert-hf-to-gguf.py \
    ./blablabruti-merged \
    --outfile blablabruti.gguf \
    --outtype f16

echo "✅ Conversion terminée ! Modèle GGUF : blablabruti.gguf"

