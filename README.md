
# 香港粵語文字轉語音工具 (Cantonese TTS Tool)

一個基於 Python 的圖形用戶界面工具，提供香港粵語和普通話的文字轉語音功能。

## 功能特點

- 🎯 **支持多種語音引擎**
  - 在線版本 (使用 Microsoft Edge TTS) - 完美支持粵語
  

- 🎙️ **多樣語音選擇**
  - 粵語 (香港) - 女聲/男聲
  - 普通話 - 女聲/男聲

- ⚙️ **個性化設置**
  - 音量調節 (0-100)
  - 語速控制 (0-100)
  - 保存語音文件選項

- 🎛️ **播放控制**
  - 朗讀
  - 暫停/繼續
  - 停止

## 文件說明

| 文件名 | 說明 |
|--------|------|
| `CantoneseTTS_GUI.py` | 基礎在線版本 - 支持語言選擇 |
| `CantoneseTTS_GUI02.py` | 完整在線版本 - 支持語言+男女聲選擇 |
| `CantoneseTTS_GUI03.py` | 離線版本 - 使用系統自帶TTS |
| `Cantonese_tts_loud.py` | 簡單版本 - 自動朗讀 |
| `Cantonese_tts_loud_remark.py` | 帶註釋的簡單版本 |
| `cantonese_tts.py` | 原始版本 |
| `dist/` | 打包好的可執行文件 (exe) |

## 安裝與使用

### 方式一：直接運行 EXE 文件 (推薦)

1. 進入 `dist/` 文件夾
2. 雙擊運行對應的 EXE 文件：
   - `CantoneseTTS_GUI02.exe` - 完整功能在線版本
   - `CantoneseTTS_GUI.exe` - 基礎在線版本

### 方式二：運行 Python 腳本

#### 前置要求

- Python 3.7+
- pip 包管理器

#### 安裝依賴

```bash
pip install edge-tts pygame
```

#### 運行程序

```bash
# 運行完整在線版本 (推薦)
python CantoneseTTS_GUI02.py

# 或運行其他版本
python CantoneseTTS_GUI.py
python CantoneseTTS_GUI03.py
```

## 使用說明

### 在線版本 (推薦使用 GUI02)

1. 打開程序
2. 在文本框中粘貼要朗讀的文字
3. 點擊「設置」按鈕配置：
   - 選擇語言 (粵語/普通話)
   - 選擇語音 (女聲/男聲)
   - 調整音量和語速
   - 選擇是否保存語音文件
4. 點擊「朗讀」按鈕開始播放

**注意**：在線版本需要聯網使用。

### 離線版本 (GUI03)

1. 確保系統已安裝對應語言的語音包
2. 運行步驟與在線版本相同
3. 無需聯網即可使用

**注意**：離線版本對粵語的支持取決於系統是否安裝了香港中文語音包。

## 語音模型說明

### 在線版本使用的語音

| 語言 | 性別 | 模型名稱 |
|------|------|----------|
| 粵語 | 女聲 | `zh-HK-HiuMaanNeural` |
| 粵語 | 男聲 | `zh-HK-WanLungNeural` |
| 普通話 | 女聲 | `zh-CN-XiaoxiaoNeural` |
| 普通話 | 男聲 | `zh-CN-YunxiNeural` |

## 輸出文件

- 如果勾選了「保存語音文件」，文件將保存到：`D:\PythonFiles\Output\TTS\`
- 文件名格式：`YYYYMMDD_HHMMSS_talk.mp3` (或 .wav)

## 打包成 EXE

如需自己打包成 EXE 文件：

```bash
# 安裝 PyInstaller
pip install pyinstaller

# 打包 (以 GUI02 為例)
pyinstaller --onefile --noconsole --name CantoneseTTS_GUI02 CantoneseTTS_GUI02.py
```

打包好的文件將位於 `dist/` 文件夾中。

## 系統要求

- Windows 10/11
- 在線版本需要網絡連接
- 離線版本需要系統安裝對應的語音包

## 開發技術

- **GUI 框架**：tkinter
- **在線 TTS**：edge-tts
- **離線 TTS**：pyttsx3
- **音頻播放**：pygame
- **打包工具**：PyInstaller

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 許可證

本項目僅供學習和個人使用。

---

**注意**：請確保遵守相關服務的使用條款。

