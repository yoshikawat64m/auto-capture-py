# Auto Capture CLI テストガイド

このガイドでは、Auto Capture CLIツールの様々なテスト方法を説明します。

## 前提条件

### ビルド済み実行ファイルのテスト
```bash
# ビルドが完了していることを確認
ls -la dist/auto-capture
```

### Pythonスクリプトとしてのテスト
```bash
# 依存関係がインストールされていることを確認
pip install -r requirements.txt
```

## 基本機能テスト

### 1. ヘルプメッセージの確認

```bash
# ビルド版
./dist/auto-capture --help

# Python版
python main.py --help
```

**期待される結果**: 使用方法とオプションの説明が表示される

### 2. 単一フレームキャプチャ（GUI無し）

```bash
# ビルド版
./dist/auto-capture --no-gui --single --output-prefix test_single

# Python版
python main.py --no-gui --single --output-prefix test_single
```

**期待される結果**: 
- `test_single_single.jpg` ファイルが作成される
- 全画面のスクリーンショットが保存される

### 3. 範囲指定キャプチャ

```bash
# ビルド版
./dist/auto-capture --area 100,100,600,400 --single --output-prefix test_area

# Python版
python main.py --area 100,100,600,400 --single --output-prefix test_area
```

**期待される結果**:
- `test_area_single.jpg` ファイルが作成される
- 指定した範囲（500x300ピクセル）のスクリーンショットが保存される

### 4. 連続キャプチャ（短時間）

```bash
# ビルド版
./dist/auto-capture --no-gui --fps 2 --duration 3 --output-prefix test_continuous

# Python版
python main.py --no-gui --fps 2 --duration 3 --output-prefix test_continuous
```

**期待される結果**:
- 6枚の画像ファイルが作成される（2fps × 3秒）
- ファイル名に連番とタイムスタンプが含まれる

## エラーハンドリングテスト

### 1. 無効なFPS値

```bash
./dist/auto-capture --fps -1
```

**期待される結果**: `エラー: FPSは0より大きい値を指定してください`

### 2. 無効な継続時間

```bash
./dist/auto-capture --duration -5
```

**期待される結果**: `エラー: 継続時間は0より大きい値を指定してください`

### 3. 無効な範囲指定

```bash
./dist/auto-capture --area 100,100,50
```

**期待される結果**: `エラー: 範囲は x1,y1,x2,y2 の形式で指定してください`

### 4. 存在しないオプション

```bash
./dist/auto-capture --invalid-option
```

**期待される結果**: ヘルプメッセージとエラーが表示される

## パフォーマンステスト

### 1. 高頻度キャプチャ

```bash
# 10fps で 5秒間（50フレーム）
./dist/auto-capture --no-gui --fps 10 --duration 5 --output-prefix perf_high
```

**確認項目**:
- フレームドロップが発生しないか
- メモリ使用量が適切か
- CPU使用率が過度に高くないか

### 2. 長時間キャプチャ

```bash
# 1fps で 60秒間（60フレーム）
./dist/auto-capture --no-gui --fps 1 --duration 60 --output-prefix perf_long
```

**確認項目**:
- メモリリークが発生しないか
- ファイルサイズが適切か
- 処理が安定して継続するか

### 3. 大きな範囲キャプチャ

```bash
# 全画面キャプチャ
./dist/auto-capture --no-gui --single --output-prefix perf_fullscreen
```

**確認項目**:
- 処理時間が適切か
- ファイルサイズが適切か
- 画質が保たれているか

## GUI機能テスト（ローカル環境のみ）

### 1. ウィンドウ選択機能

```bash
# ブラウザなどのウィンドウを開いてからテスト
python main.py --fps 1 --duration 5 --output-prefix gui_window
```

**テスト手順**:
1. コマンド実行
2. 5秒のカウントダウン中にブラウザウィンドウを準備
3. カウントダウン後、ブラウザウィンドウをクリック
4. 範囲選択画面でドラッグして範囲を指定
5. キャプチャが開始されることを確認

### 2. 範囲選択機能

```bash
python main.py --single --output-prefix gui_area
```

**テスト手順**:
1. ウィンドウを選択
2. オーバーレイ画面でマウスドラッグ
3. 選択した範囲が正確にキャプチャされることを確認

### 3. ESCキーでのキャンセル

```bash
python main.py --single --output-prefix gui_cancel
```

**テスト手順**:
1. ウィンドウを選択
2. 範囲選択画面でESCキーを押す
3. プログラムが正常に終了することを確認

## Docker環境でのテスト

### 1. Docker環境での基本テスト

```bash
# Dockerイメージをビルド
docker-compose build

# 単一フレームキャプチャ
docker-compose run auto-capture python main.py --no-gui --single --output-prefix docker_test

# 連続キャプチャ
docker-compose run auto-capture python main.py --no-gui --fps 1 --duration 5 --output-prefix docker_continuous
```

### 2. 事前定義サービスのテスト

```bash
# 単一フレームキャプチャサービス
docker-compose run single-capture

# ヘルプ表示サービス
docker-compose run help
```

## 自動テストスクリプト

### テスト実行スクリプトの作成

```bash
#!/bin/bash
# test_cli.sh

echo "=== Auto Capture CLI テスト開始 ==="

# 1. ヘルプテスト
echo "1. ヘルプメッセージテスト"
./dist/auto-capture --help > /dev/null && echo "✅ ヘルプ表示成功" || echo "❌ ヘルプ表示失敗"

# 2. 単一フレームテスト
echo "2. 単一フレームキャプチャテスト"
./dist/auto-capture --no-gui --single --output-prefix test_auto
if [ -f "test_auto_single.jpg" ]; then
    echo "✅ 単一フレームキャプチャ成功"
    rm test_auto_single.jpg
else
    echo "❌ 単一フレームキャプチャ失敗"
fi

# 3. 範囲指定テスト
echo "3. 範囲指定キャプチャテスト"
./dist/auto-capture --area 100,100,300,200 --single --output-prefix test_area_auto
if [ -f "test_area_auto_single.jpg" ]; then
    echo "✅ 範囲指定キャプチャ成功"
    rm test_area_auto_single.jpg
else
    echo "❌ 範囲指定キャプチャ失敗"
fi

# 4. 連続キャプチャテスト
echo "4. 連続キャプチャテスト"
./dist/auto-capture --no-gui --fps 2 --duration 2 --output-prefix test_cont_auto
count=$(ls test_cont_auto_*.jpg 2>/dev/null | wc -l)
if [ $count -ge 3 ]; then
    echo "✅ 連続キャプチャ成功 ($count フレーム)"
    rm test_cont_auto_*.jpg
else
    echo "❌ 連続キャプチャ失敗 ($count フレーム)"
fi

# 5. エラーハンドリングテスト
echo "5. エラーハンドリングテスト"
output=$(./dist/auto-capture --fps -1 2>&1)
if [[ $output == *"エラー"* ]]; then
    echo "✅ エラーハンドリング成功"
else
    echo "❌ エラーハンドリング失敗"
fi

echo "=== テスト完了 ==="
```

### テストスクリプトの実行

```bash
chmod +x test_cli.sh
./test_cli.sh
```

## 品質確認項目

### 1. 画像品質
- 解像度が正しく保たれているか
- 色彩が正確に再現されているか
- ノイズや歪みがないか

### 2. ファイル出力
- ファイル名の形式が正しいか
- タイムスタンプが正確か
- ファイルサイズが適切か

### 3. パフォーマンス
- 指定したFPSが維持されているか
- メモリ使用量が適切か
- CPU使用率が過度に高くないか

### 4. エラーハンドリング
- 無効な入力に対して適切なエラーメッセージが表示されるか
- プログラムがクラッシュしないか
- リソースが適切に解放されるか

## トラブルシューティング

### よくある問題と解決方法

#### 1. 権限エラー（macOS）
```bash
# 実行権限を付与
chmod +x dist/auto-capture

# セキュリティ設定で許可
# システム環境設定 → セキュリティとプライバシー → 一般
```

#### 2. 画面キャプチャ権限エラー（macOS）
```bash
# システム環境設定 → セキュリティとプライバシー → プライバシー → 画面収録
# アプリケーションを許可リストに追加
```

#### 3. Docker環境でのX11エラー
```bash
# XQuartzの設定を確認
xhost +localhost
export DISPLAY=:0
```

#### 4. ファイルが作成されない
```bash
# 書き込み権限を確認
ls -la ./
# ディスク容量を確認
df -h
```

## 継続的テスト

### GitHub Actionsでの自動テスト

```yaml
# .github/workflows/test.yml
name: Test Auto Capture CLI

on: [push, pull_request]

jobs:
  test:
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
    
    - name: Build executable
      run: pyinstaller auto-capture.spec
    
    - name: Test help command
      run: ./dist/auto-capture --help
    
    - name: Test single capture
      run: ./dist/auto-capture --no-gui --single --output-prefix ci_test
    
    - name: Verify output file
      run: ls ci_test_single.jpg
```

このテストガイドを使用して、CLIツールの品質と信頼性を確保してください。
