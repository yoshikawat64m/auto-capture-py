# ローカル環境での実行手順

実際の画面（ブラウザの動画など）をキャプチャするには、ローカル環境で実行する必要があります。

## 1. 必要なライブラリのインストール

### macOSの場合
```bash
# Python依存関係をインストール
pip install -r requirements.txt

# 必要に応じてアクセシビリティ権限を許可
# システム環境設定 → セキュリティとプライバシー → プライバシー → アクセシビリティ
# ターミナルまたはPythonを追加
```

### Windowsの場合
```bash
# Python依存関係をインストール
pip install -r requirements.txt
```

### Linuxの場合
```bash
# システムパッケージをインストール
sudo apt-get update
sudo apt-get install python3-tk x11-apps libx11-dev libxext-dev

# Python依存関係をインストール
pip install -r requirements.txt
```

## 2. 実行方法

### 基本的な使用方法（GUIモード）
```bash
# インタラクティブモードで実行
python main.py

# カスタム設定で実行
python main.py --fps 2 --duration 30 --output-prefix captures/browser_video
```

### 実行手順
1. **コマンド実行**: 上記のコマンドを実行
2. **ウィンドウ選択**: 5秒のカウントダウン後、キャプチャしたいウィンドウ（ブラウザなど）をクリック
3. **範囲選択**: マウスをドラッグして動画の範囲を選択
4. **キャプチャ開始**: 指定した設定でキャプチャが自動開始

### 単一フレーム（スクリーンショット）
```bash
python main.py --single --output-prefix captures/screenshot
```

### 高頻度キャプチャ（動画用）
```bash
# 10fps で60秒間キャプチャ（600フレーム）
python main.py --fps 10 --duration 60 --output-prefix captures/video_capture
```

## 3. 使用例：ブラウザ動画のキャプチャ

### ステップ1: ブラウザで動画を開く
- YouTubeやその他の動画サイトで動画を再生
- 動画を全画面表示にするか、適切なサイズに調整

### ステップ2: キャプチャツールを実行
```bash
python main.py --fps 5 --duration 120 --output-prefix captures/youtube_video
```

### ステップ3: ウィンドウと範囲を選択
1. カウントダウン後、ブラウザウィンドウをクリック
2. 動画の範囲をマウスドラッグで選択
3. 自動的にキャプチャが開始される

### ステップ4: キャプチャ完了
- 指定した時間が経過すると自動停止
- Ctrl+Cで途中停止も可能
- `captures/`フォルダに連番ファイルが保存される

## 4. 高品質キャプチャのコツ

### フレームレートの選択
- **動画キャプチャ**: 5-10fps（滑らかな動画用）
- **スライドショー**: 1-2fps（プレゼンテーション用）
- **高速変化**: 15-30fps（ゲームやアニメーション用）

### 範囲選択のコツ
- 動画プレイヤーの制御バーを除外
- 広告やサイドバーを除外
- 動画コンテンツのみを正確に選択

### パフォーマンス最適化
```bash
# 低解像度で高頻度キャプチャ
python main.py --fps 15 --duration 30 --output-prefix captures/high_fps

# 高解像度で低頻度キャプチャ
python main.py --fps 2 --duration 300 --output-prefix captures/long_capture
```

## 5. トラブルシューティング

### アクセシビリティ権限エラー（macOS）
```
システム環境設定 → セキュリティとプライバシー → プライバシー → 画面収録
ターミナルまたはPythonアプリケーションを追加
```

### ウィンドウが選択できない
- 他のアプリケーションが最前面にないか確認
- フルスクリーンモードを解除
- ウィンドウが最小化されていないか確認

### キャプチャが開始されない
- 選択した範囲が有効か確認
- 十分なディスク容量があるか確認
- 他のアプリケーションがカメラ/画面を使用していないか確認

## 6. 動画ファイルへの変換

キャプチャした連番画像を動画ファイルに変換する場合：

### FFmpegを使用（別途インストール必要）
```bash
# MP4動画に変換（5fps）
ffmpeg -r 5 -i captures/video_capture_%04d.jpg -c:v libx264 -pix_fmt yuv420p output.mp4

# GIFアニメーションに変換
ffmpeg -r 5 -i captures/video_capture_%04d.jpg -vf "scale=800:-1" output.gif
```

## 注意事項

- **著作権**: 動画コンテンツのキャプチャは著作権法に注意
- **プライバシー**: 個人情報が含まれる画面のキャプチャに注意
- **パフォーマンス**: 高頻度キャプチャは大量のファイルを生成
- **ストレージ**: 長時間キャプチャは十分なディスク容量を確保
