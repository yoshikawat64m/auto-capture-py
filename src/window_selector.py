import time
import platform
from typing import Optional, Tuple
import tkinter as tk


class WindowSelector:
    def __init__(self):
        self.selected_window = None
        self.click_position = None
        self.is_linux = platform.system() == 'Linux'
        
    def get_window_at_position(self, x: int, y: int) -> Optional[object]:
        """指定された座標にあるウィンドウを取得"""
        if self.is_linux:
            # Linuxでは簡易的な実装
            return {
                "left": 0, "top": 0, "right": 1920, 
                "bottom": 1080, "title": "Desktop"
            }
        else:
            try:
                import pygetwindow as gw
                # すべてのウィンドウを取得
                windows = gw.getAllWindows()
                
                # 座標が含まれるウィンドウを探す（最前面から）
                for window in windows:
                    if (window.left <= x <= window.right and
                            window.top <= y <= window.bottom and
                            window.visible):
                        return window
                return None
            except Exception as e:
                print(f"ウィンドウ取得エラー: {e}")
                return None
    
    def select_window_by_click(self) -> Optional[Tuple[int, int, int, int]]:
        """マウスクリックでウィンドウを選択し、ウィンドウの境界を返す"""
        if self.is_linux:
            print("Linux環境では全画面を対象とします。")
            print("画面全体の範囲を使用します...")
            # Linux環境では画面全体を返す
            try:
                root = tk.Tk()
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                root.destroy()
                return (0, 0, screen_width, screen_height)
            except Exception:
                # フォールバック
                return (0, 0, 1920, 1080)
        
        print("ウィンドウを選択してください...")
        print("選択したいウィンドウをクリックしてください（5秒後に開始）")
        
        # カウントダウン
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("ウィンドウをクリックしてください！")
        
        # 簡易的なクリック検出用のGUI
        root = tk.Tk()
        root.withdraw()  # メインウィンドウを隠す
        root.attributes('-fullscreen', True)
        root.attributes('-alpha', 0.01)  # ほぼ透明
        root.attributes('-topmost', True)
        
        self.selected_window = None
        
        def on_click(event):
            # クリック位置のウィンドウを取得
            window = self.get_window_at_position(event.x_root, event.y_root)
            if window:
                self.selected_window = window
                print(f"選択されたウィンドウ: {window.get('title', 'Unknown')}")
                root.quit()
            else:
                print("ウィンドウが見つかりませんでした。もう一度クリックしてください。")
        
        root.bind('<Button-1>', on_click)
        
        # 10秒でタイムアウト
        root.after(10000, lambda: root.quit())
        
        try:
            root.mainloop()
        except Exception:
            pass
        finally:
            root.destroy()
        
        if self.selected_window:
            if isinstance(self.selected_window, dict):
                return (
                    self.selected_window["left"],
                    self.selected_window["top"],
                    self.selected_window["right"],
                    self.selected_window["bottom"]
                )
            else:
                return (
                    self.selected_window.left,
                    self.selected_window.top,
                    self.selected_window.right,
                    self.selected_window.bottom
                )
        else:
            print("ウィンドウが選択されませんでした。")
            return None
