"""
香港粵語文字轉語音工具 (GUI 離線版本 - 簡化版)
功能說明：
1. 提供圖形用戶界面 (GUI)
2. 支援系統自帶的離線TTS引擎
3. 可調整音量和語速
4. 可選擇保存語音文件
5. 直接使用pyttsx3，不依賴pygame

作者：
日期：2026-06-17（修復粵語語音選擇問題，簡化播放）
"""

import sys
import os
import warnings
import threading
import tempfile
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyttsx3

# ==============================
# 初始化設定
# ==============================
warnings.filterwarnings("ignore", category=UserWarning)

class CantoneseTTSApp:
    """
    粵語 TTS 應用程式主類別 (離線版本 - 簡化)
    """
    def __init__(self, root):
        """
        初始化應用程式
        """
        self.root = root
        self.root.title("粵語朗讀 (離線版)")
        self.root.geometry("600x500")
        
        # 設定預設值
        self.settings = {
            "language": "粵語",
            "gender": "女聲",
            "volume": 60,
            "speed": 75,
            "save_file": False
        }
        
        # 播放狀態
        self.is_playing = False
        self.is_paused = False
        self.current_audio_file = None
        self.play_thread = None
        self.tts_engine = None
        
        # 建立介面
        self.create_main_ui()
    
    def create_main_ui(self):
        """
        建立主視窗介面
        """
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 設定視窗縮放權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # 標題
        title_label = ttk.Label(main_frame, text="請在下方輸入要朗讀的文本：", font=("Microsoft JhengHei", 12))
        title_label.grid(row=0, column=0, sticky=tk.W, pady=(0,5))
        
        # 文本框
        self.text_input = scrolledtext.ScrolledText(
            main_frame, 
            width=60, 
            height=18,
            font=("Microsoft JhengHei", 12)
        )
        self.text_input.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 按鈕框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # 按鈕
        self.btn_read = ttk.Button(button_frame, text="朗讀", command=self.start_reading)
        self.btn_read.grid(row=0, column=0, padx=5)
        
        self.btn_stop = ttk.Button(button_frame, text="停止", command=self.stop_reading, state=tk.DISABLED)
        self.btn_stop.grid(row=0, column=1, padx=5)
        
        self.btn_settings = ttk.Button(button_frame, text="設置", command=self.open_settings)
        self.btn_settings.grid(row=0, column=2, padx=5)
        
        self.btn_exit = ttk.Button(button_frame, text="退出", command=self.exit_app)
        self.btn_exit.grid(row=0, column=3, padx=5)
        
        # 狀態標籤
        self.status_label = ttk.Label(main_frame, text="就緒", font=("Microsoft JhengHei", 9), foreground="gray")
        self.status_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
    
    def open_settings(self):
        """
        打開設置視窗
        """
        # 建立設置視窗
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("設置")
        self.settings_window.geometry("500x300")
        self.settings_window.transient(self.root)
        self.settings_window.grab_set()
        
        # 設置視窗框架
        settings_frame = ttk.Frame(self.settings_window, padding="20")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 語言選擇
        ttk.Label(settings_frame, text="語言：", font=("Microsoft JhengHei", 10)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.language_var = tk.StringVar(value=self.settings["language"])
        language_combo = ttk.Combobox(
            settings_frame, 
            textvariable=self.language_var,
            values=["粵語", "普通話"],
            state="readonly",
            width=15
        )
        language_combo.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        # 音量控制
        ttk.Label(settings_frame, text="音量：", font=("Microsoft JhengHei", 10)).grid(row=1, column=0, sticky=tk.W, pady=10)
        
        volume_frame = ttk.Frame(settings_frame)
        volume_frame.grid(row=1, column=1, sticky=tk.W, pady=10, columnspan=2)
        
        self.volume_var = tk.IntVar(value=self.settings["volume"])
        volume_scale = ttk.Scale(
            volume_frame,
            from_=0,
            to=100,
            variable=self.volume_var,
            orient=tk.HORIZONTAL,
            length=200,
            command=self.update_volume_label
        )
        volume_scale.grid(row=0, column=0)
        
        self.volume_label = ttk.Label(volume_frame, text=str(self.settings["volume"]), font=("Microsoft JhengHei", 10))
        self.volume_label.grid(row=0, column=1, padx=10)
        
        # 語速控制
        ttk.Label(settings_frame, text="語速：", font=("Microsoft JhengHei", 10)).grid(row=2, column=0, sticky=tk.W, pady=10)
        
        speed_frame = ttk.Frame(settings_frame)
        speed_frame.grid(row=2, column=1, sticky=tk.W, pady=10, columnspan=2)
        
        self.speed_var = tk.IntVar(value=self.settings["speed"])
        speed_scale = ttk.Scale(
            speed_frame,
            from_=0,
            to=100,
            variable=self.speed_var,
            orient=tk.HORIZONTAL,
            length=200,
            command=self.update_speed_label
        )
        speed_scale.grid(row=0, column=0)
        
        self.speed_label = ttk.Label(speed_frame, text=str(self.settings["speed"]), font=("Microsoft JhengHei", 10))
        self.speed_label.grid(row=0, column=1, padx=10)
        
        # 保存選項
        self.save_file_var = tk.BooleanVar(value=self.settings["save_file"])
        save_check = ttk.Checkbutton(
            settings_frame,
            text="保存語音文件",
            variable=self.save_file_var
        )
        save_check.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=20)
        
        # 返回按鈕
        return_btn = ttk.Button(
            settings_frame,
            text="返回",
            command=self.save_settings_and_close
        )
        return_btn.grid(row=4, column=0, columnspan=3, pady=10)
    
    def update_volume_label(self, value):
        """
        更新音量顯示標籤
        """
        self.volume_label.config(text=str(int(float(value))))
    
    def update_speed_label(self, value):
        """
        更新語速顯示標籤
        """
        self.speed_label.config(text=str(int(float(value))))
    
    def save_settings_and_close(self):
        """
        保存設置並關閉視窗
        """
        self.settings["language"] = self.language_var.get()
        self.settings["gender"] = self.gender_var.get() if hasattr(self, 'gender_var') else "女聲"
        self.settings["volume"] = self.volume_var.get()
        self.settings["speed"] = self.speed_var.get()
        self.settings["save_file"] = self.save_file_var.get()
        
        self.settings_window.destroy()
    
    def get_output_filename(self):
        """
        生成輸出文件名
        """
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_talk.wav"
        output_dir = r"D:\PythonFiles\Output\TTS"
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, filename)
    
    def text_to_speech(self, text, output_file):
        """
        離線文字轉語音
        """
        # 初始化 TTS 引擎
        engine = pyttsx3.init()
        
        # 將0-100的語速轉換為pyttsx3的50-200範圍
        # 0 → 50 (很慢), 50 → 125 (正常), 100 → 200 (很快)
        speed_value = self.settings["speed"]
        rate = 50 + (speed_value * 1.5)
        engine.setProperty('rate', rate)
        
        # 設置音量 (0.0-1.0)
        engine.setProperty('volume', self.settings["volume"] / 100)
        
        # 嘗試設置語音（取決於系統安裝的語音包）
        voices = engine.getProperty('voices')
        
        try:
            selected_voice = None
            if self.settings["language"] == "粵語":
                # 優先查找粵語語音 - 使用多種匹配方式
                for voice in voices:
                    voice_id_lower = voice.id.lower()
                    voice_name_lower = voice.name.lower()
                    
                    if ('zh-hk' in voice_id_lower or 
                        'zh_hk' in voice_id_lower or 
                        'hongkong' in voice_name_lower or 
                        'hong kong' in voice_name_lower or
                        'hk' in voice_name_lower or
                        'tracy' in voice_name_lower):
                        selected_voice = voice
                        break
                
                if selected_voice:
                    engine.setProperty('voice', selected_voice.id)
                    print(f"已選擇粵語語音：{selected_voice.name}")
                    self.status_label.config(text=f"正在使用：{selected_voice.name}", foreground="green")
                else:
                    print("警告：未找到粵語語音包，將使用默認語音")
                    self.status_label.config(text="警告：未找到粵語語音包", foreground="orange")
            else:
                # 普通話
                for voice in voices:
                    voice_id_lower = voice.id.lower()
                    voice_name_lower = voice.name.lower()
                    
                    if ('zh-cn' in voice_id_lower or 
                        'zh_cn' in voice_id_lower or 
                        'chinese' in voice_name_lower or
                        'simplified' in voice_name_lower or
                        'huihui' in voice_name_lower):
                        selected_voice = voice
                        break
                
                if selected_voice:
                    engine.setProperty('voice', selected_voice.id)
                    print(f"已選擇普通話語音：{selected_voice.name}")
                    self.status_label.config(text=f"正在使用：{selected_voice.name}", foreground="green")
                else:
                    print("警告：未找到普通話語音包，將使用默認語音")
                    self.status_label.config(text="警告：未找到普通話語音包", foreground="orange")
        except Exception as e:
            print(f"設置語音時發生錯誤：{str(e)}")
            pass
        
        if self.settings["save_file"]:
            # 保存語音文件
            engine.save_to_file(text, output_file)
            engine.runAndWait()
        
        return engine
    
    def start_reading(self):
        """
        開始朗讀
        """
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("提示", "請先輸入要朗讀的文本！")
            return
        
        # 更新按鈕狀態
        self.btn_read.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.btn_settings.config(state=tk.DISABLED)
        self.status_label.config(text="正在朗讀...", foreground="blue")
        
        self.is_playing = True
        self.is_paused = False
        
        # 在新線程中執行
        self.play_thread = threading.Thread(target=self._read_text_thread, args=(text,))
        self.play_thread.daemon = True
        self.play_thread.start()
    
    def _read_text_thread(self, text):
        """
        朗讀文本的線程函數
        """
        try:
            if self.settings["save_file"]:
                output_file = self.get_output_filename()
                self.current_audio_file = output_file
            else:
                output_file = None
            
            # 創建TTS引擎並直接朗讀
            engine = self.text_to_speech(text, output_file)
            
            # 如果不保存文件，直接朗讀
            if not self.settings["save_file"] and self.is_playing:
                engine.say(text)
                engine.runAndWait()
            
            engine.stop()
            
            # 播放完成後更新UI
            self.root.after(0, self._playback_complete)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("錯誤", f"朗讀過程中發生錯誤：{str(e)}"))
            self.root.after(0, self.reset_buttons)
    
    def _playback_complete(self):
        """
        播放完成
        """
        self.status_label.config(text="朗讀完成", foreground="gray")
        self.reset_buttons()
    
    def stop_reading(self):
        """
        停止朗讀
        """
        self.is_playing = False
        self.is_paused = False
        
        self.status_label.config(text="已停止", foreground="red")
        self.reset_buttons()
    
    def reset_buttons(self):
        """
        重置按鈕狀態
        """
        self.is_playing = False
        self.is_paused = False
        self.btn_read.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_settings.config(state=tk.NORMAL)
    
    def exit_app(self):
        """
        退出應用
        """
        self.is_playing = False
        self.root.destroy()
        sys.exit(0)

def main():
    """
    主函數
    """
    root = tk.Tk()
    app = CantoneseTTSApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
