"""
@Author : xiaoce2025
@File   : config.py
@Date   : 2025-05-10
""" 
import tkinter as tk
from tkinter import ttk, messagebox
from configparser import ConfigParser


class ConfigEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("编辑选课配置")
        self.master.geometry("1000x700")
        self.setup_style()

        self.config = ConfigParser()
        self.config.read('./_internal/config.ini', encoding='utf-8')

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        self.create_user_tab()
        self.create_client_tab()
        self.create_monitor_tab()
        self.create_notification_tab()
        self.create_courses_tab()
        self.create_mutex_tab()
        self.create_delay_tab()

        ttk.Button(master, text="保存配置", command=self.save_config).pack(pady=10)

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配色方案
        bg_color = "#f0f0f0"
        accent_color = "#4a90d9"
        style.configure('.', background=bg_color, font=('Segoe UI', 10))
        style.configure('TNotebook.Tab', padding=(12,4), font=('Segoe UI', 9, 'bold'))
        style.configure('Accent.TButton', foreground='white', background=accent_color)
        style.map('Accent.TButton', 
                 background=[('active', '#3b7ec2'), ('pressed', '#306699')])
        
        style.configure('Header.TFrame', background='#e0e0e0')
        style.configure('Help.TLabelframe', background=bg_color, bordercolor='#a0a0a0')
        style.configure('Help.TLabelframe.Label', foreground='#606060', font=('Segoe UI', 9))
        style.configure('Help.TLabel', foreground='#404040', background=bg_color)
        
        # 输入控件样式
        style.configure('TEntry', fieldbackground='white', bordercolor='#c0c0c0', lightcolor='#c0c0c0')
        style.map('TEntry', 
                 bordercolor=[('focus', accent_color), ('hover', '#a0a0a0')],
                 lightcolor=[('focus', accent_color)])
        
        style.configure('TCheckbutton', background=bg_color)
        style.configure('TRadiobutton', background=bg_color)
        
        # 滚动条样式
        style.configure('TScrollbar', troughcolor=bg_color, bordercolor=bg_color)
        style.map('TScrollbar',
                 background=[('active', '#c0c0c0'), ('pressed', '#a0a0a0')])


    # 创建用户信息标签页
    def create_user_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="用户信息")

        entries = [
            ("student_id", "学号", "entry"),
            ("password", "密码", "entry"),
            ("dual_degree", "双学位", "combobox", ["true", "false"]),
            ("identity", "身份", "combobox", ["bzx", "bfx"])
        ]

        for i, (key, label, widget_type, *options) in enumerate(entries):
            ttk.Label(tab, text=label).grid(
                row=i, column=0, padx=5, pady=5, sticky='e')
            var = tk.StringVar(value=self.config.get('user', key, fallback=''))
            if widget_type == "entry":
                ttk.Entry(tab, textvariable=var, show="" if key !=
                          "pa" else "*").grid(row=i, column=1, padx=5, pady=5, sticky='w')
            elif widget_type == "combobox":
                ttk.Combobox(tab, textvariable=var, values=options[0]).grid(
                    row=i, column=1, padx=5, pady=5, sticky='w')
            setattr(self, f"user_{key}", var)

        # 添加说明文字
        help_frame = ttk.LabelFrame(tab, text="配置说明")
        help_frame.grid(row=len(entries)+1, column=0,
                        columnspan=2, padx=10, pady=10, sticky="w")

        help_text = """• 学号：IAAA统一认证学号
• 密码：IAAA统一认证密码
• 双学位：是否为双学位账号（true/false）
        （注：如果登录时需要选择主修/辅双身份，务必设为 true）
• 身份：双学位登录身份（bzx=主修，bfx=辅双）"""

        help_label = ttk.Label(help_frame, text=help_text,
                               wraplength=600, justify="left")
        help_label.pack(padx=5, pady=5, fill="x")

        tab.columnconfigure(1, weight=1)

    # 创建客户端设置标签页
    def create_client_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="客户端设置")

        keys = [
            ('supply_cancel_page', '补退选页码', "entry"),
            ('refresh_interval', '刷新间隔(s)', "entry"),
            ('random_deviation', '随机偏移', "entry"),
            ('iaaa_client_timeout', 'IAAA超时', "entry"),
            ('elective_client_timeout', '选课超时', "entry"),
            ('elective_client_pool_size', '连接池大小', "entry"),
            ('elective_client_max_life', '会话存活时间', "entry"),
            ('login_loop_interval', '登录间隔', "entry"),
            ('print_mutex_rules', '打印互斥规则', "combobox", ["true", "false"]),
            ('debug_print_request', '调试请求', "combobox", ["true", "false"]),
            ('debug_dump_request', '记录请求日志', "combobox", ["true", "false"])
        ]

        self.client_vars = {}
        for i, (key, label, widget_type, *options) in enumerate(keys):
            ttk.Label(tab, text=label).grid(
                row=i//2, column=(i % 2)*2, padx=5, pady=5, sticky='e')
            var = tk.StringVar(value=self.config.get(
                'client', key, fallback=''))
            if widget_type == "entry":
                ttk.Entry(tab, textvariable=var).grid(
                    row=i//2, column=(i % 2)*2+1, padx=5, pady=5)
            elif widget_type == "combobox":
                ttk.Combobox(tab, textvariable=var, values=options[0]).grid(
                    row=i//2, column=(i % 2)*2+1, padx=5, pady=5)
            self.client_vars[key] = var

        # 添加说明文字
        help_frame = ttk.LabelFrame(tab, text="配置说明")
        help_frame.grid(row=10, column=0, columnspan=4,
                        padx=10, pady=10, sticky="ew")

        help_text = """刷新间隔配置示例：
- refresh_interval = 8
- random_deviation = 0.2
实际间隔时间：8 * (1.0 ± 0.2) 秒

参数说明：
1. 补退选页码：待抢课程在选课计划的第几页（请将要刷的课程放至同一页）
2. 刷新间隔：每次循环后的暂停时间（秒）
3. 随机偏移：偏移量分数，如果设置为 <= 0 的值，则视为 0
4. IAAA超时：IAAA 客户端最长请求超时
5. 选课超时：elective 客户端最长请求超时
6. 连接池大小：最多同时保持几个 elective 的有效会话（同一 IP 下最多为 5）
7. 会话存活时间：elvetive 客户端的存活时间，单位 s（设置为 -1 则存活时间为无限长）
8. 登录间隔：IAAA 登录线程每回合结束后的等待时间
9. 打印互斥规则：是否在每次循环时打印完整的互斥规则列表
10. 调试请求：是否打印请求细节
11. 记录请求日志：是否将重要接口的请求以日志的形式记录到本地（包括补退选页、提交选课等接口）"""

        help_label = ttk.Label(help_frame, text=help_text,
                               wraplength=800, justify="left")
        help_label.pack(padx=5, pady=5, fill="x")

    # 创建课程设置标签页
    def create_courses_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="课程设置")

        # 添加说明
        help_frame = ttk.LabelFrame(tab, text="配置说明")
        help_text = """此页面配置要刷取的课程
※ 课程优先级按从上到下的顺序排列
1. 课程ID：后续互斥规则等识别用，必须唯一，不要包含逗号或冒号
2. 课程名称：选课网中课程全名
3. 班号：选课网中课程号，阿拉伯数字
4. 开课单位：选课网中开课单位全名"""

        ttk.Label(help_frame, text=help_text, wraplength=600,
                  justify="left").pack(padx=5, pady=5)
        help_frame.pack(fill="x", padx=10, pady=5)

        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        self.courses_container = ttk.Frame(canvas)

        self.courses_container.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window(
            (0, 0), window=self.courses_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(tab, text="添加课程", command=self.add_course).pack(pady=5)

        # 加载现有课程
        for section in self.config.sections():
            if section.startswith('course:'):
                self.add_course(
                    section.split(':', 1)[1].strip(),
                    self.config.get(section, 'name'),
                    self.config.get(section, 'class'),
                    self.config.get(section, 'school')
                )

    def add_course(self, cid="", name="", class_="", school=""):
        frame = ttk.Frame(self.courses_container)
        frame.pack(fill='x', padx=5, pady=2)

        entries = []
        for i, (label, value) in enumerate([
            ("课程ID", cid),
            ("课程名称", name),
            ("班级号", class_),
            ("开课单位", school)
        ]):
            ttk.Label(frame, text=label).grid(row=0, column=i*2, padx=2)
            var = tk.StringVar(value=value)
            ttk.Entry(frame, textvariable=var, width=20).grid(
                row=0, column=i*2+1, padx=2)
            entries.append(var)

        ttk.Button(frame, text="×", width=3,
                   command=lambda f=frame: f.destroy()).grid(row=0, column=8, padx=5)
        frame.vars = entries

    # 创建互斥规则标签页
    def create_mutex_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="互斥规则")

        # 添加说明
        help_frame = ttk.LabelFrame(tab, text="配置说明")
        help_text = """1. 规则ID：唯一，不得重复，不要包含逗号或冒号
2. 互斥课程：填写课程ID，用英文逗号分隔，如：math_1,math_2,math_3

互斥规则作用：同一个规则ID下的课程只能选择其中一门
如当math_1已选上时，自动忽略math_2和math_3"""

        ttk.Label(help_frame, text=help_text, wraplength=600,
                  justify="left").pack(padx=5, pady=5)
        help_frame.pack(fill="x", padx=10, pady=5)

        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        self.mutex_container = ttk.Frame(canvas)

        self.mutex_container.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.mutex_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(tab, text="添加规则", command=self.add_mutex).pack(pady=5)

        # 加载现有规则
        for section in self.config.sections():
            if section.startswith('mutex:'):
                self.add_mutex(
                    section.split(':', 1)[1].strip(),
                    self.config.get(section, 'courses')
                )

    def add_mutex(self, mid="", courses=""):
        frame = ttk.Frame(self.mutex_container)
        frame.pack(fill='x', padx=5, pady=2)

        ttk.Label(frame, text="规则ID:").grid(row=0, column=0)
        id_var = tk.StringVar(value=mid)
        ttk.Entry(frame, textvariable=id_var, width=15).grid(row=0, column=1)

        ttk.Label(frame, text="互斥课程（逗号分隔）:").grid(row=0, column=2)
        courses_var = tk.StringVar(value=courses)
        ttk.Entry(frame, textvariable=courses_var,
                  width=40).grid(row=0, column=3)

        ttk.Button(frame, text="×", width=3,
                   command=lambda f=frame: f.destroy()).grid(row=0, column=4)
        frame.vars = (id_var, courses_var)

    # 创建延迟规则标签页
    def create_delay_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="延迟规则")

        # 添加说明
        help_frame = ttk.LabelFrame(tab, text="配置说明")
        help_text = """1. 规则ID：唯一，不得重复，不要包含逗号或冒号
2. 课程ID：填写课程ID，如math_1
3. 阈值：触发选课的剩余名额的阈值，剩余名额小于等于该值的时候才会触发选课"""

        ttk.Label(help_frame, text=help_text, wraplength=600,
                  justify="left").pack(padx=5, pady=5)
        help_frame.pack(fill="x", padx=10, pady=5)

        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        self.delay_container = ttk.Frame(canvas)

        self.delay_container.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.delay_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(tab, text="添加规则", command=self.add_delay).pack(pady=5)

        # 加载现有规则
        for section in self.config.sections():
            if section.startswith('delay:'):
                self.add_delay(
                    section.split(':', 1)[1].strip(),
                    self.config.get(section, 'course'),
                    self.config.get(section, 'threshold')
                )

    def add_delay(self, did="", course="", threshold=""):
        frame = ttk.Frame(self.delay_container)
        frame.pack(fill='x', padx=5, pady=2)

        ttk.Label(frame, text="规则ID:").grid(row=0, column=0)
        id_var = tk.StringVar(value=did)
        ttk.Entry(frame, textvariable=id_var, width=15).grid(row=0, column=1)

        ttk.Label(frame, text="课程ID:").grid(row=0, column=2)
        course_var = tk.StringVar(value=course)
        ttk.Entry(frame, textvariable=course_var,
                  width=20).grid(row=0, column=3)

        ttk.Label(frame, text="阈值:").grid(row=0, column=4)
        threshold_var = tk.StringVar(value=threshold)
        ttk.Entry(frame, textvariable=threshold_var,
                  width=10).grid(row=0, column=5)

        ttk.Button(frame, text="×", width=3,
                   command=lambda f=frame: f.destroy()).grid(row=0, column=6)
        frame.vars = (id_var, course_var, threshold_var)

    # 创建监控设置标签页

    def create_monitor_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="监控设置")

        ttk.Label(tab, text="Host:").grid(
            row=0, column=0, padx=5, pady=5, sticky='e')
        self.monitor_host = tk.StringVar(
            value=self.config.get('monitor', 'host', fallback=''))
        ttk.Entry(tab, textvariable=self.monitor_host).grid(
            row=0, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Port:").grid(
            row=1, column=0, padx=5, pady=5, sticky='e')
        self.monitor_port = tk.StringVar(
            value=self.config.get('monitor', 'port', fallback=''))
        ttk.Entry(tab, textvariable=self.monitor_port).grid(
            row=1, column=1, padx=5, pady=5)

        # 添加说明
        help_frame = ttk.LabelFrame(tab, text="配置说明")
        help_text = """此配置如不具备专业能力请不要修改
1. Host：本地监控服务地址（通常为127.0.0.1）    
2. Port：监控服务端口号（需与监控程序配置一致，一般为7074）"""

        ttk.Label(help_frame, text=help_text, wraplength=600,
                  justify="left").pack(padx=5, pady=5)
        help_frame.grid(row=2, column=0, columnspan=2,
                        padx=10, pady=10, sticky="ew")

    # 创建通知设置标签页
    def create_notification_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="通知设置")

        entries = [
            ("disable_push", "禁用推送", "combobox", ["1", "0"]),
            ("token", "推送Token", "entry"),
            ("verbosity", "详细级别", "combobox", ["1", "2"]),
            ("minimum_interval", "最小间隔（秒）", "entry")
        ]

        for i, (key, label, widget_type, *options) in enumerate(entries):
            ttk.Label(tab, text=label).grid(
                row=i, column=0, padx=5, pady=5, sticky='e')
            var = tk.StringVar(value=self.config.get(
                'notification', key, fallback=''))
            if widget_type == "entry":
                ttk.Entry(tab, textvariable=var).grid(
                    row=i, column=1, padx=5, pady=5)
            elif widget_type == "combobox":
                ttk.Combobox(tab, textvariable=var, values=options[0]).grid(
                    row=i, column=1, padx=5, pady=5)
            setattr(self, f"notification_{key}", var)

        help_frame = ttk.LabelFrame(tab, text="配置说明")
        help_text = """此页面可配置微信公众号推送
1. 禁用推送：1=关闭推送，0=开启推送提醒
2. 推送token：从公众号获取的接入令牌
3. 详细级别：
   - 1=推送选课成功、失败
   - 2=在此基础上推送所有ERROR类型消息
4. 最小间隔：数字，若消息产生时，距离上次成功发送不足这一时间，则取消发送。-1为不限制"""

        ttk.Label(help_frame, text=help_text, wraplength=600,
                  justify="left").pack(padx=5, pady=5)
        help_frame.grid(row=4, column=0, columnspan=2,
                        padx=10, pady=10, sticky="e")

    # 保存配置
    def save_config(self):
        new_config = ConfigParser()

        # 保存用户信息
        new_config.add_section('user')
        for key in ['student_id', 'password', 'dual_degree', 'identity']:
            new_config.set('user', key, getattr(self, f"user_{key}").get())

        # 保存客户端设置
        new_config.add_section('client')
        for key, var in self.client_vars.items():
            new_config.set('client', key, var.get())

        # 保存监控设置
        new_config.add_section('monitor')
        new_config.set('monitor', 'host', self.monitor_host.get())
        new_config.set('monitor', 'port', self.monitor_port.get())

        # 保存通知设置
        new_config.add_section('notification')
        for key in ['disable_push', 'token', 'verbosity', 'minimum_interval']:
            new_config.set('notification', key, getattr(
                self, f"notification_{key}").get())

        # 保存课程信息
        for frame in self.courses_container.winfo_children():
            if hasattr(frame, 'vars'):
                cid, name, class_, school = [
                    var.get().strip() for var in frame.vars]
                if cid:
                    section = f'course:{cid}'
                    new_config.add_section(section)
                    new_config.set(section, 'name', name)
                    new_config.set(section, 'class', class_)
                    new_config.set(section, 'school', school)

        # 保存互斥规则
        for frame in self.mutex_container.winfo_children():
            if hasattr(frame, 'vars'):
                mid, courses = [var.get().strip() for var in frame.vars]
                if mid:
                    section = f'mutex:{mid}'
                    new_config.add_section(section)
                    new_config.set(section, 'courses', courses)

        # 保存延迟规则
        for frame in self.delay_container.winfo_children():
            if hasattr(frame, 'vars'):
                did, course, threshold = [var.get().strip()
                                          for var in frame.vars]
                if did:
                    section = f'delay:{did}'
                    new_config.add_section(section)
                    new_config.set(section, 'course', course)
                    new_config.set(section, 'threshold', threshold)

        # 写入文件
        with open('./_internal/config.ini', 'w', encoding='utf-8') as f:
            new_config.write(f)

        messagebox.showinfo("保存成功", "配置文件已成功保存！")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigEditor(root)
    root.mainloop()
