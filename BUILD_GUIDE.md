# Auto Capture CLI ビルドガイド

このガイドでは、Auto Capture ツールをスタンドアロンの実行ファイルとしてビルドし、配布する方法を説明します。

## 概要

PyInstallerを使用して、Pythonの依存関係を含む単一の実行ファイルを作成します。これにより、Pythonがインストールされていない環境でもツールを実行できます。

## 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）
- Git（ソースコードの取得用）

## ビルド手順

### 1. ソースコードの準備

```bash
# リポジトリをクローン（または既存のディレクトリに移動）
cd auto-capture-py
```

### 2. ビルド実行

#### Linux/macOS の場合

```bash
# 基本的なビルド
./build.sh

# 仮想環境を使用してビルド（推奨）
./build.sh --venv
```

#### Windows の場合

```cmd
REM 基本的なビルド
build.bat

REM 仮想環境を使用してビルド（推奨）
build.bat --venv
```

### 3. ビルド結果の確認

ビルドが成功すると、`dist/` ディレクトリに実行ファイルが作成されます：

- **Linux/macOS**: `dist/auto-capture`
- **Windows**: `dist/auto-capture.exe`

## 配布方法

### 1. 単一ファイル配布

```bash
# 実行ファイルのみを配布
cp dist/auto-capture /path/to/distribution/
```

### 2. アーカイブ配布

```bash
# Linux/macOS
tar -czf auto-capture-linux.tar.gz -C dist auto-capture

# Windows (PowerShell)
Compress-Archive -Path dist\auto-capture.exe -DestinationPath auto-capture-windows.zip
```

### 3. インストーラー作成（オプション）

#### macOS用 (.dmg)

```bash
# create-dmg をインストール
brew install create-dmg

# DMGファイルを作成
create-dmg \
  --volname "Auto Capture" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --app-drop-link 425 120 \
  "auto-capture.dmg" \
  "dist/"
```

#### Windows用 (.msi)

Windows Installer XML (WiX) toolsetを使用してMSIファイルを作成できます。

## 使用方法（配布後）

### 基本的な使用方法

```bash
# ヘルプを表示
./auto-capture --help

# 基本的なキャプチャ
./auto-capture

# カスタム設定でキャプチャ
./auto-capture --fps 5 --duration 30 --output-prefix my_capture

# 単一フレームキャプチャ
./auto-capture --single
```

### 高度な使用例

```bash
# 高頻度キャプチャ（動画用）
./auto-capture --fps 10 --duration 60 --output-prefix video_capture

# 低頻度長時間キャプチャ（監視用）
./auto-capture --fps 0.5 --duration 3600 --output-prefix monitoring

# 範囲指定キャプチャ
./auto-capture --area 100,100,800,600 --fps 2 --duration 30
```

## トラブルシューティング

### ビルドエラー

#### 依存関係エラー
```bash
# 依存関係を再インストール
pip install --upgrade -r requirements.txt -r build_requirements.txt
```

#### PyInstaller エラー
```bash
# PyInstallerをアップデート
pip install --upgrade pyinstaller

# キャッシュをクリア
pyinstaller --clean auto-capture.spec
```

### 実行時エラー

#### 権限エラー（macOS）
```bash
# 実行権限を付与
chmod +x auto-capture

# セキュリティ設定で許可
# システム環境設定 → セキュリティとプライバシー → 一般
# "このまま開く" をクリック
```

#### DLLエラー（Windows）
- Visual C++ Redistributable をインストール
- Windows Defender の除外設定を確認

### パフォーマンス最適化

#### ファイルサイズの削減

```bash
# UPX圧縮を有効化（auto-capture.spec で設定済み）
# より小さなファイルサイズが必要な場合：

# 不要なモジュールを除外
pyinstaller --exclude-module matplotlib --exclude-module numpy auto-capture.spec
```

#### 起動時間の改善

```bash
# 事前コンパイル済みライブラリを使用
pip install --only-binary=all -r requirements.txt
```

## 配布チェックリスト

### ビルド前
- [ ] すべての依存関係が requirements.txt に記載されている
- [ ] コードが正常に動作することを確認
- [ ] バージョン番号を更新（setup.py）

### ビルド後
- [ ] 実行ファイルが正常に動作する
- [ ] ヘルプメッセージが表示される
- [ ] 基本的なキャプチャ機能が動作する
- [ ] エラーハンドリングが適切に動作する

### 配布前
- [ ] README.md を更新
- [ ] ライセンス情報を確認
- [ ] 配布パッケージにドキュメントを含める
- [ ] 異なるOS環境でテスト

## 配布パッケージの構成例

```
auto-capture-v1.0.0/
├── auto-capture(.exe)          # 実行ファイル
├── README.md                   # 使用方法
├── LICENSE                     # ライセンス
└── examples/                   # 使用例
    ├── basic_usage.md
    └── advanced_usage.md
```

## 継続的インテグレーション（CI）

GitHub Actions を使用した自動ビルドの例：

```yaml
# .github/workflows/build.yml
name: Build Auto Capture

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r build_requirements.txt
    
    - name: Build with PyInstaller
      run: pyinstaller auto-capture.spec
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v2
      with:
        name: auto-capture-${{ matrix.os }}
        path: dist/
```

## サポート

ビルドや配布に関する問題が発生した場合：

1. このドキュメントのトラブルシューティングセクションを確認
2. GitHub Issues で報告
3. ログファイルを添付して詳細を提供

## 更新履歴

- v1.0.0: 初回リリース
  - PyInstaller ベースのビルドシステム
  - クロスプラットフォーム対応
  - 自動ビルドスクリプト
