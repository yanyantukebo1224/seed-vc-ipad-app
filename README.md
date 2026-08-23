# Seed-VC iPad App 🎤

音声変換（Voice Conversion）の Seed-VC を iPad アプリとして実装したプロジェクトです。

## ✨ 機能

- 🎵 音声ファイルのアップロード
- 🔄 音声変換（ターゲットボイスに音声を転換）
- ⚡ CoreML モデルを使用した高速推論
- 💾 結果の保存・再生
- 🔒 オフライン動作・プライバシー保護

## 📦 プロジェクト構成

```
seed-vc-ipad-app/
├── SeedVC/
│   ├── CoreMLModels/          # CoreML モデルファイル（ビルド時に生成）
│   │   ├── WhisperFeatureExtractor.mlmodel
│   │   ├── DiTVoiceConverter.mlmodel
│   │   └── BigVGANVocoder.mlmodel
│   ├── App/                    # SwiftUI アプリコード
│   │   ├── VoiceConverterApp.swift
│   │   ├── ContentView.swift
│   │   ├── AudioRecorder.swift
│   │   └── ModelLoader.swift
│   └── Models/                 # モデル定義
├── VoiceConverterApp.xcodeproj/  # Xcode プロジェクト
├── .github/workflows/          # GitHub Actions ワークフロー
│   ├── build.yml               # ビルドワークフロー
│   ├── release.yml             # リリースワークフロー
│   └── convert_to_coreml.py    # CoreML 変換スクリプト
├── LICENSE                     # MIT ライセンス
└── README.md
```

## 🚀 クイックスタート

### 1. リポジトリをクローン

```bash
git clone https://github.com/YOUR_USERNAME/seed-vc-ipad-app.git
cd seed-vc-ipad-app
```

### 2. Xcode プロジェクトを開く

```bash
# macOS で Xcode を起動
open VoiceConverterApp.xcodeproj
```

### 3. ビルドと実行

1. Xcode でプロジェクトを開く
2. シミュレータまたは iPad デバイスを選択
3. `Cmd + B` でビルド
4. アプリを実行

## 🛠️ GitHub Actions で自動ビルド

このリポジトリは GitHub Actions を使用しています。プッシュやタグ作成時に自動的に：

1. **CoreML モデルの生成**: PyTorch → CoreML 変換
2. **iOS アプリのビルド**: Xcode でアプリを構築
3. **リリースパッケージの作成**: `.app` ファイルとモデルファイルを ZIP

### ワークフロー

- `build.yml`: プッシュ時のビルド
- `release.yml`: タグ（v*）作成時のリリース

## 📋 要件

### ローカル開発

- macOS (Xcode 14.0+)
- Xcode Command Line Tools
- Python 3.10+

### CI/CD

- GitHub アカウント
- Hugging Face API Token（オプション）

## 🔧 設定

### Hugging Face Token（推奨）

CoreML モデルの生成を高速化するために Hugging Face Token を設定します：

```bash
# ローカル開発用
export HF_TOKEN="your_huggingface_token"

# GitHub Actions で設定（GitHub Secrets）
# Settings → Secrets → Actions → New repository secret
# Name: HF_TOKEN, Value: your_token
```

## 📱 アプリの使い方

1. **音声ファイルを選択**: 「Source Audio」ボタンから音声ファイルを選択
2. **ターゲットボイスを選択**: 「Target Voice」ボタンから目標音声を選択
3. **変換実行**: 「Convert Voice」ボタンをタップ
4. **結果を確認**: 変換された音声を再生・保存

## 🧪 ローカルでテスト

```bash
# CoreML モデルを生成（macOS 環境が必要）
python .github/workflows/convert_to_coreml.py

# Xcode でビルド
xcodebuild -scheme VoiceConverterApp -destination 'platform=iOS Simulator,name=iPad Pro' build
```

## 📊 テクノロジースタック

| カテゴリ | テクノロジー |
|---------|-------------|
| **iOS** | SwiftUI, CoreML, AVFoundation |
| **モデル** | Whisper (音声認識), DiT (音声変換), BigVGAN (再生) |
| **CI/CD** | GitHub Actions + macOS |
| **ライセンス** | MIT |

## 🤝 貢献

このプロジェクトに貢献したい方は、プルリクエストを歓迎します！

1. Fork このリポジトリ
2. 新しいブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更を加える (`git commit -m 'Add some AmazingFeature'`)
4. ブランチをプッシュ (`git push origin feature/AmazingFeature`)
5. Pull Request を作成

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) のもとで利用可能です。

## 🙏 謝辞

- [Seed-VC](https://github.com/plachta/seed-vc) - 音声変換モデルの原作
- Hugging Face - モデルホスティング

---

Made with ❤️ using Seed-VC and CoreML

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-iOS%2015.0+-blue.svg)](https://developer.apple.com/iphone/index.action)
[![Swift](https://img.shields.io/badge/Swift-5.7-orange.svg)](https://swift.org/download/)
