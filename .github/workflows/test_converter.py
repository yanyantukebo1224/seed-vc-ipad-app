#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified Seed-VC CoreML Converter for GitHub Actions
Usage: python test_converter.py (from seed-vc directory)
"""

import os
import sys
from pathlib import Path

# Setup paths
SEED_VC_PATH = os.getcwd()  # Current directory is seed-vc
OUTPUT_DIR = Path(SEED_VC_PATH) / "SeedVC/CoreMLModels"

sys.path.insert(0, SEED_VC_PATH)

import torch
from munch import Munch
from coremltools import convert as ct_convert

def main():
    print("=" * 60)
    print("Seed-VC CoreML Model Converter (Test)")
    print("=" * 60)
    
    # Setup Hugging Face cache
    cache_dir = Path(SEED_VC_PATH) / "checkpoints/hf_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HOME"] = str(cache_dir)
    os.environ["HF_HUB_CACHE"] = str(cache_dir)
    
    print(f"Cache directory: {cache_dir}")
    
    # Try to load Whisper model first (simplest test)
    print("\n[1/3] Testing Whisper model...")
    try:
        from transformers import AutoFeatureExtractor, WhisperModel
        
        whisper_name = "openai/whisper-small"
        print(f"  Downloading {whisper_name}...")
        
        whisper_model = WhisperModel.from_pretrained(whisper_name, torch_dtype=torch.float16)
        whisper_model.to('cpu')
        whisper_model.eval()
        
        # Convert to CoreML
        mlmodel_path = OUTPUT_DIR / "WhisperFeatureExtractor.mlmodel"
        print(f"  Converting to CoreML...")
        
        converted_model = ct_convert(
            whisper_model,
            inputs=[torch.TensorType(shape=(1, 80, 1500))]
        )
        
        converted_model.save(str(mlmodel_path))
        print(f"  OK Whisper model saved: {mlmodel_path}")
        
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nConversion test complete!")

if __name__ == "__main__":
    main()
