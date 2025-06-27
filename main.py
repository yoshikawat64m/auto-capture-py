#!/usr/bin/env python3
"""
画面キャプチャツール

任意のウィンドウの任意の範囲を指定した間隔でキャプチャするツール
"""

import argparse
import sys
import signal
from window_selector import WindowSelector
from area_selector import AreaSelector
from capture_tool import CaptureManager


def signal_handler(sig, frame):
    """Ctrl+Cハンドラ"""
    print("\n\nキャプチャを停止しています...")
    sys.exit(0)


def main():
    """メイン関数"""
    # シグナルハンドラを設定
    signal.signal(signal.SIGINT, signal_handler)
    
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(
        description="画面キャプチャツール - ウィンドウの指定範囲を連続キャプチャ"
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=1.0,
        help="キャプチャのフレームレート（秒間フレーム数、デフォルト: 1.0）"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=10.0,
        help="キャプチャ継続時間（秒、デフォルト: 10.0）"
    )
    parser.add_argument(
        "--output-prefix",
        type=str,
        default="capture",
        help="出力ファイル名のプレフィックス（デフォルト: capture）"
    )
    parser.add_argument(
        "--single",
        action="store_true",
        help="単一フレームのみキャプチャ"
    )
    parser.add_argument(
        "--area",
        type=str,
        help="キャプチャ範囲を直接指定 (x1,y1,x2,y2の形式、例: 100,100,800,600)"
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="GUI無しモード（全画面キャプチャ）"
    )
    
    args = parser.parse_args()
    
    # 引数の検証
    if args.fps <= 0:
        print("エラー: FPSは0より大きい値を指定してください")
        sys.exit(1)
        
    if args.duration <= 0:
        print("エラー: 継続時間は0より大きい値を指定してください")
        sys.exit(1)
    
    print("=== 画面キャプチャツール ===")
    print(f"設定: FPS={args.fps}, 継続時間={args.duration}秒")
    print(f"出力プレフィックス: {args.output_prefix}")
    print()
    
    try:
        # 範囲指定の処理
        if args.area:
            # コマンドライン引数で範囲を直接指定
            try:
                coords = [int(x.strip()) for x in args.area.split(',')]
                if len(coords) != 4:
                    raise ValueError("座標は4つ必要です")
                capture_area = tuple(coords)
                print(f"指定されたキャプチャ範囲: {capture_area}")
            except ValueError as e:
                print(f"エラー: 範囲指定が無効です ({e})")
                print("正しい形式: --area x1,y1,x2,y2 (例: --area 100,100,800,600)")
                sys.exit(1)
        elif args.no_gui:
            # GUI無しモード（全画面）
            print("GUI無しモード: 全画面をキャプチャします")
            import tkinter as tk
            try:
                root = tk.Tk()
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                root.destroy()
                capture_area = (0, 0, screen_width, screen_height)
            except Exception:
                # フォールバック
                capture_area = (0, 0, 1920, 1080)
            print(f"キャプチャ範囲: {capture_area}")
        else:
            # 通常のGUIモード
            # Step 1: ウィンドウ選択
            print("Step 1: ウィンドウ選択")
            window_selector = WindowSelector()
            window_bounds = window_selector.select_window_by_click()
            
            if not window_bounds:
                print("ウィンドウが選択されませんでした。終了します。")
                sys.exit(1)
                
            print(f"選択されたウィンドウ範囲: {window_bounds}")
            print()
            
            # Step 2: 範囲選択
            print("Step 2: キャプチャ範囲選択")
            area_selector = AreaSelector()
            capture_area = area_selector.select_area()
            
            if not capture_area:
                print("キャプチャ範囲が選択されませんでした。終了します。")
                sys.exit(1)
                
            print(f"キャプチャ範囲: {capture_area}")
            print()
        
        # Step 3: キャプチャ実行
        print("Step 3: キャプチャ実行")
        capture_manager = CaptureManager()
        
        if args.single:
            # 単一フレームキャプチャ
            filename = capture_manager.capture_single_frame(
                capture_area,
                f"{args.output_prefix}_single.jpg"
            )
            print(f"スクリーンショットを保存しました: {filename}")
        else:
            # 連続キャプチャ
            capture_manager.start_capture(
                capture_area,
                args.fps,
                args.duration,
                args.output_prefix
            )
            
            # キャプチャ完了まで待機
            try:
                while capture_manager.is_capturing:
                    import time
                    time.sleep(0.1)
            except KeyboardInterrupt:
                capture_manager.stop_capture()
                print("\nキャプチャが中断されました。")
        
        print("処理が完了しました。")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
