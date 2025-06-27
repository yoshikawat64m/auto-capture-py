import time
import threading
from datetime import datetime
from typing import Tuple, Optional
import mss
from PIL import Image


class CaptureManager:
    def __init__(self):
        self.is_capturing = False
        self.capture_thread = None
        
    def start_capture(
        self,
        area: Tuple[int, int, int, int],
        fps: float,
        duration: float,
        output_prefix: str = "capture"
    ) -> None:
        """キャプチャを開始"""
        if self.is_capturing:
            print("既にキャプチャが実行中です。")
            return
            
        self.is_capturing = True
        
        # キャプチャスレッドを開始
        self.capture_thread = threading.Thread(
            target=self._capture_loop,
            args=(area, fps, duration, output_prefix),
            daemon=True
        )
        self.capture_thread.start()
        
    def stop_capture(self) -> None:
        """キャプチャを停止"""
        self.is_capturing = False
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join()
            
    def _capture_loop(
        self,
        area: Tuple[int, int, int, int],
        fps: float,
        duration: float,
        output_prefix: str
    ) -> None:
        """キャプチャのメインループ"""
        x1, y1, x2, y2 = area
        
        # mssの座標形式に変換
        monitor = {
            "top": y1,
            "left": x1,
            "width": x2 - x1,
            "height": y2 - y1
        }
        
        interval = 1.0 / fps
        start_time = time.time()
        frame_count = 0
        
        print(f"キャプチャ開始: {fps}fps, {duration}秒間")
        print(f"範囲: ({x1}, {y1}) - ({x2}, {y2})")
        print("Ctrl+Cで停止できます")
        
        # スレッド内で新しいmssインスタンスを作成
        with mss.mss() as sct:
            try:
                while self.is_capturing:
                    current_time = time.time()
                    if (current_time - start_time) >= duration:
                        break
                    frame_start = current_time
                    
                    # スクリーンショットを取得
                    screenshot = sct.grab(monitor)
                    
                    # PILイメージに変換
                    img = Image.frombytes(
                        "RGB",
                        screenshot.size,
                        screenshot.bgra,
                        "raw",
                        "BGRX"
                    )
                    
                    # ファイル名を生成
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = (f"{output_prefix}_{timestamp}_"
                                f"{frame_count:04d}.jpg")
                    
                    # JPEG形式で保存
                    img.save(filename, "JPEG", quality=85)
                    
                    frame_count += 1
                    
                    # 進捗表示
                    elapsed = time.time() - start_time
                    remaining = duration - elapsed
                    print(f"\rフレーム: {frame_count}, "
                          f"経過時間: {elapsed:.1f}s, "
                          f"残り時間: {remaining:.1f}s", end="")
                    
                    # フレームレート調整
                    frame_time = time.time() - frame_start
                    sleep_time = max(0, interval - frame_time)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                        
            except KeyboardInterrupt:
                print("\nキャプチャが中断されました。")
            except Exception as e:
                print(f"\nキャプチャエラー: {e}")
            finally:
                self.is_capturing = False
                print(f"\nキャプチャ完了: {frame_count}フレーム保存")
            
    def capture_single_frame(
        self,
        area: Tuple[int, int, int, int],
        filename: Optional[str] = None
    ) -> str:
        """単一フレームをキャプチャ"""
        x1, y1, x2, y2 = area
        
        # mssの座標形式に変換
        monitor = {
            "top": y1,
            "left": x1,
            "width": x2 - x1,
            "height": y2 - y1
        }
        
        # mssインスタンスを作成してスクリーンショットを取得
        with mss.mss() as sct:
            screenshot = sct.grab(monitor)
        
        # PILイメージに変換
        img = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.bgra,
            "raw",
            "BGRX"
        )
        
        # ファイル名を生成
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.jpg"
            
        # JPEG形式で保存
        img.save(filename, "JPEG", quality=85)
        
        return filename
