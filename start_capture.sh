#!/bin/bash

# 仮想ディスプレイを起動
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
XVFB_PID=$!

# 少し待ってからコマンドを実行
sleep 2

# 引数をそのまま渡してPythonスクリプトを実行
python main.py "$@"

# 終了時にXvfbを停止
kill $XVFB_PID 2>/dev/null || true
