#!/bin/bash
# Seed-VC iPad App - GitHub Setup Script

echo "=========================================="
echo "Seed-VC iPad App - GitHub 公開設定"
echo "=========================================="

# Step 1: Check if Git is configured
echo ""
echo "Step 1: Git 設定を確認..."
git config --global user.name
git config --global user.email

if [ $? -ne 0 ]; then
    echo "⚠️  Git 設定が必要です。以下のコマンドを実行してください:"
    echo "   git config --global user.name "YOUR_NAME""
    echo "   git config --global user.email "your@email.com""
    exit 1
fi

# Step 2: Create GitHub repository (manual step)
echo ""
echo "Step 2: GitHub リポジトリを作成してください"
echo "------------------------------------------"
echo "1. https://github.com/new を開く"
echo "2. リポジトリ名：seed-vc-ipad-app"
echo "3. Public に設定"
echo "4. このリポジトリを fork する（または新規作成）"
echo ""

# Step 3: Add remote and push
echo "Step 3: GitHub にプッシュ..."
echo "------------------------------------------"

# Get GitHub username
GITHUB_USER=$(git config --global user.name)
echo "ユーザー名：$GITHUB_USER"

# Ask for repository URL
read -p "GitHub リポジトリの URL を入力してください (例：https://github.com/YOUR_USERNAME/seed-vc-ipad-app.git): " REPO_URL

# Add remote
git remote add origin $REPO_URL

# Push to GitHub
echo "プッシュ中..."
git push -u origin main --force-with-lease

echo ""
echo "=========================================="
echo "✅ 完了！リポジトリが公開されました"
echo "=========================================="
echo ""
echo "確認 URL: https://github.com/$GITHUB_USER/seed-vc-ipad-app"
echo ""
echo "GitHub Actions が自動的に実行されます:"
echo "  - CoreML モデルの生成"
echo "  - Xcode プロジェクトのビルド"
echo "  - リリースパッケージの作成"
