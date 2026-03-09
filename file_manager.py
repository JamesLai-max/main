import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

import keyboard
import pyautogui

pyautogui.FAILSAFE = True  # 滑鼠快速移到左上角可中止


class AutoClickApp:
    def __init__(self, root):
        self.root = root
        self.root.title("固定位置自動點擊器")
        self.root.geometry("320x240")
        self.root.resizable(False, False)

        self.running = False
        self.click_thread = None

        self.x_var = tk.StringVar(value="500")
        self.y_var = tk.StringVar(value="500")
        self.interval_var = tk.StringVar(value="1.0")
        self.status_var = tk.StringVar(value="狀態：停止")

        self.build_ui()
        self.bind_hotkeys()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="X 座標").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.x_var, width=15).grid(row=0, column=1, pady=4)

        ttk.Label(frame, text="Y 座標").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.y_var, width=15).grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="間隔秒數").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.interval_var, width=15).grid(row=2, column=1, pady=4)

        ttk.Button(frame, text="讀取目前滑鼠位置 (F9)", command=self.capture_mouse_position).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=8
        )

        ttk.Button(frame, text="開始點擊 (F8)", command=self.start_clicking).grid(
            row=4, column=0, sticky="ew", pady=6, padx=(0, 4)
        )

        ttk.Button(frame, text="停止點擊 (F8)", command=self.stop_clicking).grid(
            row=4, column=1, sticky="ew", pady=6, padx=(4, 0)
        )

        ttk.Label(frame, textvariable=self.status_var, foreground="blue").grid(
            row=5, column=0, columnspan=2, sticky="w", pady=10
        )

        tips = (
            "提示：\n"
            "F8 = 開始/停止\n"
            "F9 = 取得目前滑鼠座標\n"
            "Esc = 關閉程式\n"
            "滑鼠移到左上角可緊急中止"
        )
        ttk.Label(frame, text=tips, justify="left").grid(
            row=6, column=0, columnspan=2, sticky="w"
        )

    def bind_hotkeys(self):
        keyboard.add_hotkey("F8", self.toggle_clicking)
        keyboard.add_hotkey("F9", self.capture_mouse_position)
        keyboard.add_hotkey("esc", self.safe_close)

    def capture_mouse_position(self):
        x, y = pyautogui.position()
        self.x_var.set(str(x))
        self.y_var.set(str(y))
        self.status_var.set(f"狀態：已讀取座標 ({x}, {y})")

    def click_loop(self):
        while self.running:
            try:
                x = int(self.x_var.get())
                y = int(self.y_var.get())
                interval = float(self.interval_var.get())

                pyautogui.click(x, y)
                time.sleep(interval)

            except pyautogui.FailSafeException:
                self.running = False
                self.status_var.set("狀態：已緊急中止")
                return
            except Exception as e:
                self.running = False
                self.status_var.set("狀態：錯誤，已停止")
                messagebox.showerror("錯誤", f"執行失敗：{e}")
                return

    def start_clicking(self):
        if self.running:
            return

        try:
            int(self.x_var.get())
            int(self.y_var.get())
            interval = float(self.interval_var.get())
            if interval <= 0:
                raise ValueError("間隔秒數必須大於 0")
        except Exception as e:
            messagebox.showwarning("輸入錯誤", f"請確認輸入值正確：{e}")
            return

        self.running = True
        self.status_var.set("狀態：執行中")
        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()

    def stop_clicking(self):
        self.running = False
        self.status_var.set("狀態：停止")

    def toggle_clicking(self):
        if self.running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def safe_close(self):
        self.running = False
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickApp(root)
    root.protocol("WM_DELETE_WINDOW", app.safe_close)
    root.mainloop()
