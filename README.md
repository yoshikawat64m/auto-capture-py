# Auto Capture CLI

任意のウィンドウ画面の任意の範囲、任意の時間、任意の間隔で画面キャプチャができるPythonコマンドラインツールです。

## 📁 プロジェクト構造

```
auto-capture-py/
├── src/                    # ソースコード
│   ├── main.py            # メインスクリプト
│   ├── area_selector.py   # 範囲選択GUI
│   └── window_selector.py # ウィンドウ選択GUI
├── docs/                  # ドキュメント
│   ├── README.md          # このファイル
│   ├── LOCAL_SETUP.md     # ローカル環境セットアップガイド
│   ├── BUILD_GUIDE.md     # ビルドガイド
│   ├── TEST_GUIDE.md      # テストガイド
│   └── LICENSE            # ライセンス
├── scripts/               # スクリプト
│   ├── start_capture.sh   # Docker用起動スクリプト
│   └── test_cli.sh        # 自動テストスクリプト
├── build_tools/           # ビルド関連
│   ├── build.sh           # Unix/Linux用ビルドスクリプト
│   ├── build.bat          # Windows用ビルドスクリプト
│   ├── auto-capture.spec  # PyInstaller設定
│   ├── setup.py           # Python setuptools設定
│   └── build_requirements.txt # ビルド用依存関係
├── tests/                 # テストファイル（将来用）
├── captures/              # キャプチャ画像保存先
├── dist/                  # ビルド済み実行ファイル
├── .github/workflows/     # GitHub Actions CI/CD
├── requirements.txt       # 実行時依存関係
├── Dockerfile            # Docker設定
└── docker-compose.yml    # Docker Compose設定
```

## 🚀 クイックスタート

### 1. 実行ファイルを使用（推奨）

最新のリリースから実行ファイルをダウンロード：

```bash
# ヘルプを表示
./auto-capture --help

# 基本的なキャプチャ（5fps、30秒間）
./auto-capture --fps 5 --duration 30

# 単一フレームキャプチャ
./auto-capture --single

# 範囲指定キャプチャ
./auto-capture --area 100,100,800,600 --fps 2 --duration 10
```

### 2. Pythonスクリプトとして実行

```bash
# 依存関係をインストール
pip install -r requirements.txt

# 実行
python src/main.py --fps 5 --duration 30
```

### 3. Dockerを使用

```bash
# ヘルプを表示
docker-compose run help

# 単一フレームキャプチャ
docker-compose run single-capture
```

## 📖 詳細ドキュメント

- **[ローカル環境セットアップ](docs/LOCAL_SETUP.md)** - 開発環境の構築方法
- **[ビルドガイド](docs/BUILD_GUIDE.md)** - 実行ファイルの作成方法
- **[テストガイド](docs/TEST_GUIDE.md)** - テスト方法と品質保証

## ⚡ 主な機能

- **ウィンドウ選択**: 特定のアプリケーションウィンドウを選択
- **範囲選択**: マウスドラッグで任意の範囲を指定
- **連続キャプチャ**: 指定したFPSで連続撮影
- **単一フレーム**: 1枚だけのスクリーンショット
- **クロスプラットフォーム**: Windows、macOS、Linux対応
- **GUI/CLI両対応**: GUIモードとコマンドラインモード

## 🛠️ 開発者向け

### ビルド

```bash
# Unix/Linux/macOS
./build_tools/build.sh

# Windows
build_tools\build.bat
```

### テスト

```bash
# 自動テスト実行
./scripts/test_cli.sh

# 手動テスト
python src/main.py --no-gui --single --output-prefix test
```

### Docker開発環境

```bash
# 開発用コンテナ起動
docker-compose run auto-capture

# 仮想ディスプレイでテスト
docker-compose run capture-headless
```

## 📋 使用例

### 基本的な使用方法

```bash
# 5fps で 30秒間キャプチャ
./auto-capture --fps 5 --duration 30

# 特定の範囲を 2fps で 10秒間
./auto-capture --area 100,100,800,600 --fps 2 --duration 10

# 単一フレームキャプチャ
./auto-capture --single

# GUIなしモード（全画面）
./auto-capture --no-gui --fps 1 --duration 60
```

### 高度な使用方法

```bash
# カスタムファイル名プレフィックス
./auto-capture --fps 5 --duration 30 --output-prefix my_capture

# 高頻度キャプチャ
./auto-capture --fps 30 --duration 5

# 長時間低頻度キャプチャ
./auto-capture --fps 0.5 --duration 3600  # 1時間、2秒に1回
```

## 🔧 システム要件

- **Python**: 3.11以上
- **OS**: Windows 10+、macOS 10.14+、Ubuntu 18.04+
- **メモリ**: 最低512MB、推奨1GB以上
- **ディスク**: 100MB以上の空き容量

### 必要な権限

- **macOS**: 画面収録権限、アクセシビリティ権限
- **Windows**: 管理者権限（初回実行時）
- **Linux**: X11アクセス権限

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](docs/LICENSE) ファイルを参照してください。

## 🐛 バグレポート・機能要望

[GitHub Issues](https://github.com/your-username/auto-capture-py/issues) でバグレポートや機能要望をお寄せください。

## 📞 サポート

- **ドキュメント**: [docs/](docs/) フォルダ内の各種ガイド
- **テスト**: `./scripts/test_cli.sh` で動作確認
- **トラブルシューティング**: [TEST_GUIDE.md](docs/TEST_GUIDE.md#トラブルシューティング)

---

**Auto Capture CLI** - 効率的な画面キャプチャツール 🎯
