FROM python:3.11-slim

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    libx11-dev \
    libxext-dev \
    libxrandr-dev \
    libxss1 \
    libgconf-2-4 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# 実行権限を付与
RUN chmod +x main.py start_capture.sh

# デフォルトコマンド
CMD ["python", "main.py", "--help"]
