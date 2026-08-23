#!/usr/bin/env python3
import os, sys, torch, yaml
from pathlib import Path
from munch import Munch
from coremltools import convert as ct_convert
from huggingface_hub import hf_hub_download

cache_dir = Path("checkpoints/hf_cache")
cache_dir.mkdir(parents=True, exist_ok=True)
os.environ["HF_HOME"] = str(cache_dir)
os.environ["HF_HUB_CACHE"] = str(cache_dir)

print("=" * 60)
print("Seed-VC CoreML Converter")
print("=" * 60)

from transformers import WhisperModel

def load_from_hf(repo_id, filename):
    return hf_hub_download("Plachta/seed-vc", filename, cache_dir=str(cache_dir))

OUTPUT_DIR = Path("SeedVC/CoreMLModels")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n[1/3] Whisper...")
try:
    model = WhisperModel.from_pretrained("openai/whisper-small", torch_dtype=torch.float16)
    model.to('cpu')
    model.eval()
    mlmodel = ct_convert(model, inputs=[torch.TensorType(shape=(1, 80, 1500))])
    mlmodel.save(str(OUTPUT_DIR / "WhisperFeatureExtractor.mlmodel"))
    print(f"  OK: Whisper")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n[2/3] DiT...")
try:
    checkpoint = load_from_hf("DiT_seed_v2_uvit_whisper_small_wavenet_bigvgan_pruned.pth")
    config_path = load_from_hf("config_dit_mel_seed_uvit_whisper_small_wavenet.yml")
    
    config = yaml.safe_load(open(config_path, "r"))
    model_params = Munch(config["model_params"])
    model_params.dit_type = 'DiT'
    
    from modules.commons import build_model, load_checkpoint
    model = build_model(model_params, stage="DiT")
    model, _, _, _ = load_checkpoint(model, None, checkpoint, load_only_params=True, ignore_modules=[], is_distributed=False)
    
    for key in model:
        model[key].eval()
        model[key].to('cpu')
    
    mlmodel = ct_convert(model, inputs=[torch.TensorType(shape=(1, 512, 80))])
    mlmodel.save(str(OUTPUT_DIR / "DiTVoiceConverter.mlmodel"))
    print(f"  OK: DiT")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n[3/3] BigVGAN...")
try:
    from modules.bigvgan import bigvgan
    vocoder = bigvgan.BigVGAN.from_pretrained("bigvgan_256m_unistft", use_cuda_kernel=False)
    vocoder.remove_weight_norm()
    vocoder.eval()
    vocoder.to('cpu')
    
    mlmodel = ct_convert(vocoder, inputs=[torch.TensorType(shape=(1, 80, 256))])
    mlmodel.save(str(OUTPUT_DIR / "BigVGANVocoder.mlmodel"))
    print(f"  OK: BigVGAN")
except Exception as e:
    print(f"  ERROR: {e}")

print("\nDone!")
