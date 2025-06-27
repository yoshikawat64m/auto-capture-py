#!/bin/bash

# ビルドスクリプト for auto-capture CLI tool

set -e

echo "=== Auto Capture CLI ビルドスクリプト ==="

# 仮想環境の作成（オプション）
if [ "$1" = "--venv" ]; then
    echo "仮想環境を作成中..."
    python -m venv build_env
    source build_env/bin/activate
    echo "仮想環境をアクティベート済み"
fi

# 依存関係のインストール
echo "依存関係をインストール中..."
pip install -r requirements.txt
pip install -r build_tools/build_requirements.txt

# 既存のビルドファイルをクリーンアップ
echo "既存のビルドファイルをクリーンアップ中..."
rm -rf build/
rm -rf dist/
rm -rf __pycache__/
rm -rf *.pyc

# PyInstallerでビルド
echo "PyInstallerでビルド中..."
cd build_tools
pyinstaller auto-capture.spec
cd ..

# ビルド結果の確認
if [ -f "dist/auto-capture" ] || [ -f "dist/auto-capture.exe" ]; then
    echo "✅ ビルド成功！"
    echo "実行ファイルの場所: dist/"
    ls -la dist/
    
    # 実行ファイルのサイズを表示
    if [ -f "dist/auto-capture" ]; then
        echo "ファイルサイズ: $(du -h dist/auto-capture | cut -f1)"
    elif [ -f "dist/auto-capture.exe" ]; then
        echo "ファイルサイズ: $(du -h dist/auto-capture.exe | cut -f1)"
    fi
    
    echo ""
    echo "使用方法:"
    echo "  ./dist/auto-capture --help"
    echo "  ./dist/auto-capture --fps 5 --duration 30"
    
else
    echo "❌ ビルド失敗"
    exit 1
fi

echo "=== ビルド完了 ==="
