#!/usr/bin/env python3
import os, sys, torch
from pathlib import Path
from munch import Munch
from coremltools import convert as ct_convert

cache_dir = Path("checkpoints/hf_cache")
cache_dir.mkdir(parents=True, exist_ok=True)
os.environ["HF_HOME"] = str(cache_dir)
os.environ["HF_HUB_CACHE"] = str(cache_dir)

print("=" * 60)
print("Seed-VC CoreML Converter (Test)")
print("=" * 60)
print(f"PyTorch version: {torch.__version__}")

from transformers import WhisperModel

print("\n[1/3] Testing Whisper model...")
try:
    print("  Loading whisper-small...")
    model = WhisperModel.from_pretrained("openai/whisper-small", torch_dtype=torch.float16)
    model.to('cpu')
    model.eval()
    
    OUTPUT_DIR = Path("SeedVC/CoreMLModels")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("  Converting to CoreML...")
    # Use classifier_inputs instead of inputs for Whisper
    mlmodel = ct_convert(model, inputs=[torch.TensorType(shape=(1, None))])
    mlmodel.save(str(OUTPUT_DIR / "WhisperFeatureExtractor.mlmodel"))
    print(f"  OK: {OUTPUT_DIR}/WhisperFeatureExtractor.mlmodel")
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nDone!")
