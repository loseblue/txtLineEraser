import tkinter as tk
from tkinter import filedialog, messagebox
import os
from tkinterdnd2 import *

class TextFileDeleterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("txtLineEraser")
        self.root.geometry("600x400")

        # 启用拖放支持
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

        # 存储选择的文件路径
        self.file_paths = []

        # 创建打开文件按钮
        self.open_button = tk.Button(root, text="打开多个文件", command=self.open_files)
        self.open_button.pack(pady=10)

        # 创建可滚动的文本框，仅显示文件路径，最多显示2行
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.file_text = tk.Text(self.text_frame, width=80, height=2, wrap=tk.NONE)
        self.file_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 添加垂直滚动条（用于文件路径文本框）
        self.scrollbar = tk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.file_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_text.config(yscrollcommand=self.scrollbar.set)

        # 创建复选按钮区域，垂直排列
        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=5, fill=tk.X)

        # 复选按钮1：删除包含字段的行
        self.delete_field_frame = tk.Frame(self.options_frame)
        self.delete_field_frame.pack(anchor=tk.W)
        self.delete_field_var = tk.BooleanVar()
        self.delete_field_check = tk.Checkbutton(
            self.delete_field_frame, text="删除包含字段的行", variable=self.delete_field_var
        )
        self.delete_field_check.pack(side=tk.LEFT)
        self.delete_field_entry = tk.Entry(self.delete_field_frame, width=20)
        self.delete_field_entry.pack(side=tk.LEFT, padx=5)

        # 复选按钮2：删除空行
        self.delete_empty_frame = tk.Frame(self.options_frame)
        self.delete_empty_frame.pack(anchor=tk.W)
        self.delete_empty_var = tk.BooleanVar()
        self.delete_empty_check = tk.Checkbutton(
            self.delete_empty_frame, text="删除空行", variable=self.delete_empty_var
        )
        self.delete_empty_check.pack(side=tk.LEFT)

        # 创建确认处理按钮
        self.confirm_button = tk.Button(root, text="确认处理", command=self.process_files)
        self.confirm_button.pack(pady=5)

    def handle_drop(self, event):
        # 处理拖放事件，获取文件路径
        files = self.root.splitlist(event.data)
        self.process_selected_files(files)

    def open_files(self):
        # 打开文件对话框，仅允许选择所有文件
        files = filedialog.askopenfilenames(
            title="选择文件",
            filetypes=[("所有文件", "*.*")]
        )
        self.process_selected_files(files)

    def process_selected_files(self, files):
        # 清空之前的文件列表和文本框
        self.file_paths = []
        self.file_text.delete(1.0, tk.END)

        # 显示选择的文件路径
        for file in files:
            if os.path.isfile(file):
                self.file_paths.append(file)
                self.file_text.insert(tk.END, f"文件: {file}\n")

        # 如果没有选择文件，显示提示
        if not self.file_paths:
            messagebox.showinfo("提示", "未选择任何文件！")
        else:
            # 滚动到文件路径文本框最后一行
            self.file_text.see(tk.END)

    def process_files(self):
        # 如果没有选择文件，显示提示
        if not self.file_paths:
            messagebox.showinfo("提示", "请先选择文件！")
            return

        # 获取复选框状态和输入框内容
        delete_field = self.delete_field_var.get()
        field_text = self.delete_field_entry.get().strip()
        delete_empty = self.delete_empty_var.get()

        # 如果选择删除包含字段但未输入字段，显示提示
        if delete_field and not field_text:
            messagebox.showwarning("警告", "请输入要删除的字段！")
            return

        # 依次处理文件
        for file in self.file_paths:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    processed_lines = []

                    # 处理文件内容
                    for line in lines:
                        # 删除空行
                        if delete_empty and line.strip() == "":
                            continue
                        # 删除包含指定字段的行
                        if delete_field and field_text and field_text in line:
                            continue
                        processed_lines.append(line)

                    # 保存处理后的内容到新文件
                    base, ext = os.path.splitext(file)
                    new_file = f"{base}-fix{ext}"
                    try:
                        with open(new_file, 'w', encoding='utf-8') as f:
                            f.writelines(processed_lines)
                    except Exception as e:
                        messagebox.showerror("错误", f"无法保存文件 {new_file}: {str(e)}")
                        continue

            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件 {file}: {str(e)}")
                continue

        # 显示处理完成提示
        if self.file_paths:
            messagebox.showinfo("提示", f"已处理 {len(self.file_paths)} 个文件，新文件已保存")

# 创建主窗口
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = TextFileDeleterApp(root)
    root.mainloop()
