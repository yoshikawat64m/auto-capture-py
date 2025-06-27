@echo off
REM ビルドスクリプト for auto-capture CLI tool (Windows)

echo === Auto Capture CLI ビルドスクリプト (Windows) ===

REM 仮想環境の作成（オプション）
if "%1"=="--venv" (
    echo 仮想環境を作成中...
    python -m venv build_env
    call build_env\Scripts\activate.bat
    echo 仮想環境をアクティベート済み
)

REM 依存関係のインストール
echo 依存関係をインストール中...
pip install -r requirements.txt
pip install -r build_tools\build_requirements.txt

REM 既存のビルドファイルをクリーンアップ
echo 既存のビルドファイルをクリーンアップ中...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
del /q *.pyc 2>nul

REM PyInstallerでビルド
echo PyInstallerでビルド中...
cd build_tools
pyinstaller auto-capture.spec
cd ..

REM ビルド結果の確認
if exist "dist\auto-capture.exe" (
    echo ✅ ビルド成功！
    echo 実行ファイルの場所: dist\
    dir dist\
    
    echo.
    echo 使用方法:
    echo   dist\auto-capture.exe --help
    echo   dist\auto-capture.exe --fps 5 --duration 30
    
) else (
    echo ❌ ビルド失敗
    exit /b 1
)

echo === ビルド完了 ===
pause
