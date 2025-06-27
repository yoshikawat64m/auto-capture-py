import tkinter as tk
from typing import Optional, Tuple


class AreaSelector:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        self.canvas = None
        self.root = None
        
    def select_area(self) -> Optional[Tuple[int, int, int, int]]:
        """マウスドラッグで範囲を選択し、座標を返す"""
        print("キャプチャ範囲を選択してください...")
        print("マウスをドラッグして範囲を選択してください")
        
        # 全画面オーバーレイウィンドウを作成
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        
        # キャンバスを作成
        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0,
            bg='black'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # イベントバインド
        self.canvas.bind('<Button-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # 説明テキスト
        self.canvas.create_text(
            self.root.winfo_screenwidth() // 2,
            50,
            text="ドラッグして範囲を選択してください (ESCでキャンセル)",
            fill='white',
            font=('Arial', 16)
        )
        
        try:
            self.root.mainloop()
        except Exception:
            pass
        finally:
            if self.root:
                self.root.destroy()
        
        if all(coord is not None for coord in [
            self.start_x, self.start_y, self.end_x, self.end_y
        ]):
            # 座標を正規化（左上と右下を確実にする）
            x1 = min(self.start_x, self.end_x)
            y1 = min(self.start_y, self.end_y)
            x2 = max(self.start_x, self.end_x)
            y2 = max(self.start_y, self.end_y)
            
            print(f"選択された範囲: ({x1}, {y1}) - ({x2}, {y2})")
            return (x1, y1, x2, y2)
        else:
            print("範囲が選択されませんでした。")
            return None
    
    def on_button_press(self, event):
        """マウスボタンが押された時"""
        self.start_x = event.x
        self.start_y = event.y
        
        # 既存の矩形があれば削除
        if self.rect:
            self.canvas.delete(self.rect)
    
    def on_mouse_drag(self, event):
        """マウスドラッグ中"""
        if self.start_x is not None and self.start_y is not None:
            # 既存の矩形があれば削除
            if self.rect:
                self.canvas.delete(self.rect)
            
            # 新しい矩形を描画
            self.rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='red', width=2, fill='', stipple='gray50'
            )
    
    def on_button_release(self, event):
        """マウスボタンが離された時"""
        self.end_x = event.x
        self.end_y = event.y
        
        # 最終的な矩形を描画
        if self.rect:
            self.canvas.delete(self.rect)
        
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y,
            outline='green', width=3, fill='', stipple='gray25'
        )
        
        # 1秒後に終了
        self.root.after(1000, self.root.quit)
