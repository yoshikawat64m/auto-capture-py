# 画面キャプチャツール

任意のウィンドウの任意の範囲を指定した間隔で画面キャプチャを行うPythonツールです。

## 機能

- マウスクリックによるウィンドウ選択
- マウスドラッグによる範囲選択
- 指定したFPS（秒間フレーム数）での連続キャプチャ
- 指定した時間での自動停止
- JPEG形式での画像保存
- 単一フレームキャプチャモード

## インストール

### 方法1: Docker環境（推奨）

既存のPython環境を壊さずに実行できます。

#### macOSでの事前準備

1. **XQuartzをインストール**
```bash
# Homebrewでインストール
brew install --cask xquartz

# または公式サイトからダウンロード
# https://www.xquartz.org/
```

2. **XQuartzを起動して設定**
- XQuartzを起動
- 環境設定 → セキュリティ → "ネットワーククライアントからの接続を許可" にチェック
- XQuartzを再起動

3. **X11転送を許可**
```bash
# X11転送を許可
xhost +localhost

# DISPLAYを設定
export DISPLAY=:0
```

#### Dockerの使用方法

```bash
# Dockerイメージをビルド
docker-compose build

# ヘルプを表示
docker-compose run help

# GUI無しモード（全画面キャプチャ）
docker-compose run auto-capture python main.py --no-gui --fps 1 --duration 10 --output-prefix captures/my_capture

# 範囲を直接指定してキャプチャ
docker-compose run auto-capture python main.py --area 100,100,800,600 --fps 1 --duration 10 --output-prefix captures/my_capture

# 単一フレーム（GUI無し）
docker-compose run auto-capture python main.py --no-gui --single --output-prefix captures/screenshot
```

### 方法2: ローカル環境（実際の画面キャプチャ用）

**実際の画面（ブラウザの動画など）をキャプチャする場合は、ローカル環境で実行してください。**

#### インストール手順

**macOS:**
```bash
pip install -r requirements.txt
# アクセシビリティ権限の設定が必要な場合があります
# システム環境設定 → セキュリティとプライバシー → プライバシー → 画面収録
```

**Windows:**
```bash
pip install -r requirements.txt
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3-tk x11-apps libx11-dev libxext-dev
pip install -r requirements.txt
```

#### 実行方法

```bash
# 基本的な使用方法
python main.py

# ブラウザ動画のキャプチャ例
python main.py --fps 5 --duration 120 --output-prefix captures/youtube_video

# 高頻度キャプチャ（動画用）
python main.py --fps 10 --duration 60 --output-prefix captures/video_capture
```

詳細な手順は `LOCAL_SETUP.md` を参照してください。

### 必要なライブラリ

- `mss`: 高速画面キャプチャ
- `Pillow`: 画像処理
- `pygetwindow`: ウィンドウ情報取得

## 使用方法

### Docker環境での使用方法（推奨）

#### 基本的な使用方法

```bash
# インタラクティブモードで起動
docker-compose run auto-capture

# コンテナ内でコマンド実行
python main.py --fps 1 --duration 10 --output-prefix captures/my_capture
```

#### 単一フレームキャプチャ

```bash
# 事前定義されたサービスを使用
docker-compose run single-capture

# または、カスタムオプションで実行
docker-compose run auto-capture python main.py --single --output-prefix captures/screenshot
```

#### カスタムオプションでの実行

```bash
# 高頻度キャプチャ
docker-compose run auto-capture python main.py --fps 5 --duration 30 --output-prefix captures/high_freq

# 低頻度長時間キャプチャ
docker-compose run auto-capture python main.py --fps 0.5 --duration 120 --output-prefix captures/monitoring
```

### ローカル環境での使用方法

#### 基本的な使用方法

```bash
python main.py
```

デフォルト設定（1fps、10秒間）でキャプチャを実行します。

#### オプション指定

```bash
python main.py --fps 2.0 --duration 30 --output-prefix "my_capture"
```

#### 単一フレームキャプチャ

```bash
python main.py --single --output-prefix "screenshot"
```

### コマンドラインオプション

- `--fps`: キャプチャのフレームレート（秒間フレーム数、デフォルト: 1.0）
- `--duration`: キャプチャ継続時間（秒、デフォルト: 10.0）
- `--output-prefix`: 出力ファイル名のプレフィックス（デフォルト: "capture"）
- `--single`: 単一フレームのみキャプチャ

## 実行手順

1. **ウィンドウ選択**
   - コマンド実行後、5秒のカウントダウンが始まります
   - カウントダウン後、キャプチャしたいウィンドウをクリックしてください

2. **範囲選択**
   - 全画面にオーバーレイが表示されます
   - マウスをドラッグしてキャプチャしたい範囲を選択してください
   - ESCキーでキャンセルできます

3. **キャプチャ実行**
   - 指定した設定でキャプチャが開始されます
   - Ctrl+Cで途中停止できます

## 出力ファイル

キャプチャされた画像は以下の形式で保存されます：

```
{output-prefix}_{timestamp}_{frame_number}.jpg
```

例：
- `capture_20240627_191530_0001.jpg`
- `capture_20240627_191530_0002.jpg`
- ...

## 使用例

### 例1: 高頻度キャプチャ
```bash
python main.py --fps 5 --duration 60 --output-prefix "high_freq"
```
5fps で60秒間キャプチャ（300枚の画像）

### 例2: 低頻度長時間キャプチャ
```bash
python main.py --fps 0.5 --duration 300 --output-prefix "monitoring"
```
0.5fps（2秒に1回）で300秒間キャプチャ（150枚の画像）

### 例3: スクリーンショット
```bash
python main.py --single --output-prefix "screenshot"
```
単一フレームのスクリーンショット

## 注意事項

- macOSでは、アクセシビリティ権限が必要な場合があります
- 高いFPSでの長時間キャプチャは大量のファイルを生成します
- キャプチャ範囲が大きいほど、処理時間とファイルサイズが増加します

## トラブルシューティング

### ウィンドウが選択できない場合
- アクセシビリティ権限を確認してください
- 他のアプリケーションが画面を占有していないか確認してください

### キャプチャが開始されない場合
- 選択した範囲が有効かどうか確認してください
- 十分なディスク容量があることを確認してください

## ビルドと配布

### スタンドアロン実行ファイルの作成

PyInstallerを使用してスタンドアロンの実行ファイルを作成できます。

#### ビルド手順

**Linux/macOS:**
```bash
# 基本的なビルド
./build.sh

# 仮想環境を使用してビルド（推奨）
./build.sh --venv
```

**Windows:**
```cmd
REM 基本的なビルド
build.bat

REM 仮想環境を使用してビルド（推奨）
build.bat --venv
```

#### ビルド結果

ビルドが成功すると、`dist/` ディレクトリに実行ファイルが作成されます：
- **Linux/macOS**: `dist/auto-capture`
- **Windows**: `dist/auto-capture.exe`

#### 配布

作成された実行ファイルは、Pythonがインストールされていない環境でも動作します。

詳細なビルド手順は `BUILD_GUIDE.md` を参照してください。

### GitHub Releases

タグをプッシュすると、GitHub Actionsが自動的にクロスプラットフォーム向けのビルドを実行し、リリースを作成します：

```bash
# バージョンタグを作成してプッシュ
git tag v1.0.0
git push origin v1.0.0
```

以下のプラットフォーム向けのビルドが自動作成されます：
- Linux x64 (tar.gz)
- macOS x64 (tar.gz)  
- Windows x64 (zip)

## ライセンス

MIT License
