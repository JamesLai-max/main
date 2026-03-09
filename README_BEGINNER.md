# AutoClicker 程式碼庫新手導覽

## 1. 整體結構

目前這個專案是一個單檔案桌面工具：

- `autoclicker.py`：主程式，包含 UI、熱鍵、自動點擊迴圈與錯誤處理。

你可以把它想成三層：

1. **UI 層（Tkinter）**：建立輸入框、按鈕、狀態文字。
2. **控制層（AutoClickApp 類別方法）**：處理按鈕事件、熱鍵、啟停狀態。
3. **執行層（背景執行緒）**：按固定間隔呼叫 `pyautogui.click(x, y)`。

## 2. 新手必懂重點

### 啟動與主流程

- 程式從 `if __name__ == "__main__":` 開始。
- 建立 `Tk()` 視窗後，把控制邏輯包進 `AutoClickApp`，最後進入 `mainloop()` 等待使用者操作。

### 狀態管理

- `self.running` 是核心狀態旗標：
  - `True`：背景執行緒會持續點擊。
  - `False`：背景迴圈停止。
- `start_clicking()` / `stop_clicking()` / `toggle_clicking()` 共同維護這個旗標。

### UI 與資料綁定

- `self.x_var`, `self.y_var`, `self.interval_var` 都是 `tk.StringVar`，UI 的輸入欄位與程式邏輯共用這些變數。
- `self.status_var` 用來更新「目前狀態」文字。

### 並行（Thread）

- 點擊動作跑在 `threading.Thread(..., daemon=True)`，避免卡住主視窗。
- 背景函式是 `click_loop()`，每次讀取座標與間隔並點擊一次，然後 `sleep(interval)`。

### 安全與錯誤處理

- `pyautogui.FAILSAFE = True`：滑鼠移到左上角會丟出 `FailSafeException`，可緊急停止。
- `start_clicking()` 先驗證輸入合法（座標整數、間隔 > 0）。
- `click_loop()` 包含例外處理，錯誤時會停止並彈出訊息框。

## 3. 你接下來應該學什麼

### 第一階段（先能看懂）

1. **Python class 與方法呼叫關係**
2. **Tkinter 基本元件**（`Label`/`Entry`/`Button`/`StringVar`）
3. **事件驅動觀念**（按鈕 callback、主迴圈）

### 第二階段（能改功能）

1. **threading 基礎**：為什麼 UI 與工作執行緒要分離
2. **輸入驗證與錯誤訊息設計**
3. **熱鍵生命週期管理**（綁定、取消、關閉程式時清理）

### 第三階段（做成可發佈工具）

1. 設定檔（記住上次座標與間隔）
2. 日誌（logging）與除錯資訊
3. 打包（PyInstaller）與跨平台注意事項

## 4. 建議的下一步練習

1. 新增「點擊次數上限」功能（例如 100 次後自動停止）。
2. 新增「倒數 3 秒開始」功能，避免馬上點錯位置。
3. 把熱鍵改為可自訂（例如 F6/F7）。
4. 新增「啟動前預覽目前座標」與「測試點擊一次」按鈕。

這四個練習會讓你完整走過：UI 改動、狀態管理、執行緒控制與錯誤處理。
