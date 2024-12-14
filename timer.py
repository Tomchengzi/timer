import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("计时器")
        self.root.geometry("800x200")
        # 设置窗口置顶
        self.root.attributes('-topmost', True)
        # 设置窗口透明度
        self.root.attributes('-alpha', 0.9)
        
        # 记录鼠标位置用于拖动
        self.x = 0
        self.y = 0
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 绑定鼠标事件
        self.main_frame.bind('<Button-1>', self.start_drag)
        self.main_frame.bind('<B1-Motion>', self.on_drag)
        
        # 创建水平布局的框架
        self.horizontal_frame = ttk.Frame(self.main_frame)
        self.horizontal_frame.pack(fill=tk.X, expand=True)
        
        # 左侧：时间显示
        time_frame = ttk.Frame(self.horizontal_frame)
        time_frame.pack(side=tk.LEFT, padx=20)
        
        self.time_label = ttk.Label(
            time_frame,
            text="00:00",
            font=("Helvetica", 48, "bold"),
            bootstyle="primary"
        )
        self.time_label.pack()
        
        # 中间：快速选择按钮
        buttons_frame = ttk.LabelFrame(
            self.horizontal_frame,
            text="快速选择",
            padding=10
        )
        buttons_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)
        
        # 按钮布局
        btn_frame = ttk.Frame(buttons_frame)
        btn_frame.pack(fill=tk.BOTH, expand=True)
        
        self.btn_15 = ttk.Button(
            btn_frame,
            text="15秒",
            command=lambda: self.start_countdown(15),
            bootstyle="primary-outline",
            width=8
        )
        self.btn_15.pack(side=tk.LEFT, padx=5)
        
        self.btn_30 = ttk.Button(
            btn_frame,
            text="30秒",
            command=lambda: self.start_countdown(30),
            bootstyle="primary-outline",
            width=8
        )
        self.btn_30.pack(side=tk.LEFT, padx=5)
        
        # 右侧：自定义时间和控制
        control_frame = ttk.LabelFrame(
            self.horizontal_frame,
            text="自定义时间",
            padding=10
        )
        control_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)
        
        # 自定义时间输入
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill=tk.X)
        
        self.custom_entry = ttk.Entry(
            input_frame,
            font=("Helvetica", 12),
            width=6
        )
        self.custom_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(
            input_frame,
            text="秒",
            font=("Helvetica", 12)
        ).pack(side=tk.LEFT)
        
        # 控制按钮
        buttons_control_frame = ttk.Frame(control_frame)
        buttons_control_frame.pack(fill=tk.X, pady=5)
        
        self.btn_custom = ttk.Button(
            buttons_control_frame,
            text="开始",
            command=self.start_custom_countdown,
            bootstyle="success",
            width=8
        )
        self.btn_custom.pack(side=tk.LEFT, padx=2)
        
        self.btn_stop = ttk.Button(
            buttons_control_frame,
            text="停止",
            command=self.stop_countdown,
            bootstyle="danger",
            width=8
        )
        self.btn_stop.pack(side=tk.LEFT, padx=2)
        
        # 最右侧：透明度控制和退出
        settings_frame = ttk.LabelFrame(
            self.horizontal_frame,
            text="设置",
            padding=10
        )
        settings_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)
        
        # 透明度滑块
        ttk.Label(settings_frame, text="透明度").pack()
        self.opacity_scale = ttk.Scale(
            settings_frame,
            from_=0.3,
            to=1.0,
            value=0.9,
            command=self.change_opacity
        )
        self.opacity_scale.pack(fill=tk.X)
        
        # 退出按钮
        self.btn_exit = ttk.Button(
            settings_frame,
            text="退出",
            command=root.quit,
            bootstyle="danger-outline",
            width=8
        )
        self.btn_exit.pack(pady=5)
        
        # 进度条
        self.progress = ttk.Progressbar(
            self.main_frame,
            length=300,
            mode='determinate',
            bootstyle="primary"
        )
        self.progress.pack(fill=tk.X, pady=(10,0))
        
        # 初始化变量
        self.counting = False
        self.remaining_time = 0
        self.total_time = 0
    
    def start_drag(self, event):
        """开始拖动"""
        self.x = event.x
        self.y = event.y
    
    def on_drag(self, event):
        """拖动窗口"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def change_opacity(self, value):
        """改变窗口透明度"""
        self.root.attributes('-alpha', float(value))
    
    def start_countdown(self, seconds):
        """开始倒计时"""
        if not self.counting:
            self.counting = True
            self.remaining_time = seconds
            self.total_time = seconds
            self.progress['value'] = 100
            self.update_timer()
    
    def start_custom_countdown(self):
        """开始自定义时间倒计时"""
        try:
            seconds = int(self.custom_entry.get())
            if seconds > 0:
                self.start_countdown(seconds)
            else:
                messagebox.showerror("错误", "请输入大于0的数字")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def stop_countdown(self):
        """停止倒计时"""
        self.counting = False
        self.time_label.config(text="00:00")
        self.progress['value'] = 0
    
    def update_timer(self):
        """更新计时器显示"""
        if self.counting and self.remaining_time >= 0:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
            
            progress_value = (self.remaining_time / self.total_time) * 100
            self.progress['value'] = progress_value
            
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
            
            if self.remaining_time < 0:
                self.counting = False
                messagebox.showinfo("提示", "倒计时结束！")
                self.time_label.config(text="00:00")
                self.progress['value'] = 0

def main():
    root = ttk.Window(themename="cosmo")
    app = TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()