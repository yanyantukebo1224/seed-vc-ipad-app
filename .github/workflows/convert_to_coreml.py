#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed-VC CoreML Model Converter
Converts PyTorch models to CoreML format for iOS deployment

Usage:
    python convert_to_coreml.py

Requirements:
    pip install torch torchaudio transformers coremltools munch audiotools dac huggingface_hub
"""

import os
import sys
from pathlib import Path

# Setup paths for GitHub Actions environment
WORKSPACE = "/Users/runner/workspace/seed-vc-ipad-app"
SEED_VC_PATH = os.path.join(WORKSPACE, "seed-vc")
OUTPUT_DIR = os.path.join(WORKSPACE, "SeedVC/CoreMLModels")

sys.path.insert(0, SEED_VC_PATH)
os.chdir(SEED_VC_PATH)

import torch
import yaml
from munch import Munch
from transformers import AutoFeatureExtractor, WhisperModel
from coremltools import convert as ct_convert

def setup_environment():
    """Set up Hugging Face environment"""
    cache_dir = os.path.join(SEED_VC_PATH, "checkpoints/hf_cache")
    os.makedirs(cache_dir, exist_ok=True)
    
    # Set environment variables
    os.environ["HF_HOME"] = cache_dir
    os.environ["HF_HUB_CACHE"] = cache_dir
    
    print(f"Using HF cache directory: {cache_dir}")

def load_model_from_hf(repo_id, filename):
    """Load model from Hugging Face Hub"""
    from huggingface_hub import hf_hub_download
    
    cache_dir = os.path.join(SEED_VC_PATH, "checkpoints/hf_cache")
    
    return hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        cache_dir=cache_dir
    )

def convert_whisper_to_coreml():
    """Convert Whisper feature extractor to CoreML"""
    print("\n[1/3] Converting Whisper Feature Extractor...")
    
    whisper_name = "openai/whisper-small"
    
    try:
        print(f"  Loading {whisper_name}...")
        whisper_model = WhisperModel.from_pretrained(whisper_name, torch_dtype=torch.float16)
        
        # Move to CPU and set eval mode
        whisper_model.to('cpu')
        whisper_model.eval()
        
        # Create dummy input
        batch_size = 1
        num_features = 80
        seq_len = 1500
        
        print(f"  Converting model with input shape: ({batch_size}, {num_features}, {seq_len})...")
        
        mlmodel_path = Path(OUTPUT_DIR) / "WhisperFeatureExtractor.mlmodel"
        mlmodel_path.parent.mkdir(parents=True, exist_ok=True)
        
        converted_model = ct_convert(
            whisper_model,
            inputs=[torch.TensorType(shape=(batch_size, num_features, seq_len))]
        )
        
        converted_model.save(str(mlmodel_path))
        print(f"  OK Whisper model saved to {mlmodel_path}")
        
    except Exception as e:
        print(f"  ERROR converting Whisper model: {e}")
        import traceback
        traceback.print_exc()

def convert_dit_to_coreml():
    """Convert DiT Voice Converter to CoreML"""
    print("\n[2/3] Converting DiT Voice Converter...")
    
    try:
        # Load checkpoint and config from Hugging Face
        checkpoint_path = load_model_from_hf(
            "Plachta/Seed-VC",
            "DiT_seed_v2_uvit_whisper_small_wavenet_bigvgan_pruned.pth"
        )
        
        config_path = load_model_from_hf(
            "Plachta/Seed-VC",
            "config_dit_mel_seed_uvit_whisper_small_wavenet.yml"
        )
        
        print(f"  Loaded checkpoint: {checkpoint_path}")
        print(f"  Loaded config: {config_path}")
        
        # Load config
        config = yaml.safe_load(open(config_path, "r"))
        model_params = Munch(config["model_params"])
        model_params.dit_type = 'DiT'
        
        # Build model
        from modules.commons import build_model, load_checkpoint
        
        print("  Building DiT model...")
        model = build_model(model_params, stage="DiT")
        
        print("  Loading checkpoint weights...")
        model, _, _, _ = load_checkpoint(
            model, None, checkpoint_path,
            load_only_params=True, ignore_modules=[], is_distributed=False
        )
        
        # Move to CPU and set eval mode
        for key in model:
            model[key].eval()
            model[key].to('cpu')
        
        print("  Converting to CoreML...")
        mlmodel_path = Path(OUTPUT_DIR) / "DiTVoiceConverter.mlmodel"
        
        # Create dummy input: (batch, time_steps, mel_bins)
        batch_size = 1
        time_steps = 512
        mel_bins = 80
        
        converted_model = ct_convert(
            model,
            inputs=[torch.TensorType(shape=(batch_size, time_steps, mel_bins))]
        )
        
        converted_model.save(str(mlmodel_path))
        print(f"  OK DiT model saved to {mlmodel_path}")
        
    except Exception as e:
        print(f"  ERROR converting DiT model: {e}")
        import traceback
        traceback.print_exc()

def convert_vocoder_to_coreml():
    """Convert BigVGAN Vocoder to CoreML"""
    print("\n[3/3] Converting BigVGAN Vocoder...")
    
    try:
        from modules.bigvgan import bigvgan
        
        # Load vocoder
        print("  Loading BigVGAN model...")
        vocoder = bigvgan.BigVGAN.from_pretrained("bigvgan_256m_unistft", use_cuda_kernel=False)
        vocoder.remove_weight_norm()
        vocoder.eval()
        vocoder.to('cpu')
        
        print("  Converting to CoreML...")
        mlmodel_path = Path(OUTPUT_DIR) / "BigVGANVocoder.mlmodel"
        
        # Create dummy input: (batch, mel_bins, time_steps)
        batch_size = 1
        mel_bins = 80
        time_steps = 256
        
        converted_model = ct_convert(
            vocoder,
            inputs=[torch.TensorType(shape=(batch_size, mel_bins, time_steps))]
        )
        
        converted_model.save(str(mlmodel_path))
        print(f"  OK BigVGAN model saved to {mlmodel_path}")
        
    except Exception as e:
        print(f"  ERROR converting Vocoder model: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    print("=" * 60)
    print("Seed-VC CoreML Model Converter")
    print("=" * 60)
    
    # Setup environment
    setup_environment()
    
    # Ensure output directory exists
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Convert models
    convert_whisper_to_coreml()
    convert_dit_to_coreml()
    convert_vocoder_to_coreml()
    
    print("\n" + "=" * 60)
    print("CoreML conversion complete!")
    print(f"Models saved to: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
