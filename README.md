# txtLineEraser

`txtLineEraser` 是一个基于 Python 和 Tkinter 的文本行删除工具，允许用户通过图形界面选择多个文件，删除包含指定字段（支持正则表达式）或空行的内容，并将处理后的内容保存到新文件。支持文件拖放和按钮选择，适合快速批量处理文本文件。

## 功能

- **文件选择**：
  - 通过“打开多个文件”按钮选择任意类型文件。
  - 支持将文件拖放到程序窗口，自动加载文件路径。
- **文件路径显示**：
  - 文件路径显示在 2 行文本框中，带垂直滚动条，不换行。
- **行删除功能**：
  - **删除包含字段的行**：支持输入正则表达式，删除匹配的行（忽略大小写）。
  - **删除空行**：删除文件中的空行（`strip() == ""`）。
- **保存处理结果**：
  - 处理后的内容保存到新文件，命名为 `<原文件名>-fix.<原扩展名>`。
- **用户界面**：
  - 窗口标题为 `txtLineEraser`，尺寸 600x400。
  - 复选按钮垂直排列，输入框延长至窗口右边。
  - 错误提示：未选择文件、输入框为空或无效正则表达式时显示警告。

## 安装要求

- **Python**：3.7 或以上。
- **依赖**：
  - `tkinter`：通常随 Python 安装。
  - `tkinterdnd2`：用于拖放功能，安装命令：
    ```bash
    pip install tkinterdnd2
    ```
- **操作系统**：测试于 Windows，理论上支持 macOS 和 Linux（需安装 `tkdnd` 依赖）。

## 安装步骤

1. **安装 Python**：
   - 下载并安装 Python 3.7+（[python.org](https://www.python.org/downloads/))。
   - 确保勾选“Add Python to PATH”和“tcl/tk and IDLE”选项。

2. **安装 `tkinterdnd2`**：
   - 打开命令提示符，运行：
     ```bash
     pip install tkinterdnd2
     ```
   - 验证安装：
     ```bash
     python -c "import tkinterdnd2; print(tkinterdnd2.__version__)"
     ```

3. **下载代码**：
   - 将 `main.py` 保存到项目目录（如 `D:\work\txtLineEraser\`）。

## 使用方法

1. **运行程序**：
   ```bash
   cd D:\work\txtLineEraser
   python main.py
   ```

2. **选择文件**：
   - **按钮选择**：点击“打开多个文件”，选择任意文件（支持多选）。
   - **拖放文件**：从文件资源管理器拖放文件到程序窗口。

3. **设置删除规则**：
   - 勾选“删除包含字段的行（支持正则）”，在输入框输入正则表达式（如 `error.*`）。
   - 勾选“删除空行”以移除空行。
   - 可同时勾选两个选项。

4. **处理文件**：
   - 点击“确认处理”按钮。
   - 程序将处理文件，删除匹配的行，并保存到 `<原文件名>-fix.<原扩展名>`。
   - 处理完成显示提示：“已处理 X 个文件，新文件已保存”。

5. **错误处理**：
   - 未选择文件：提示“请先选择文件！”。
   - 输入框为空（勾选“删除包含字段”）：提示“请输入要删除的字段（支持正则表达式）！”。
   - 无效正则表达式：提示“无效的正则表达式！”。
   - 读取或保存失败：显示错误信息。

## 示例

**输入文件**（`test.txt`）：
```
Line 1: This is a test
Line 2: Error occurred
Line 3: 
Line 4: Another error line
Line 5: Normal line
```

**操作**：
- 拖放 `test.txt` 到窗口，或通过“打开多个文件”选择。
- 勾选“删除包含字段的行（支持正则）”，输入正则表达式 `error.*`。
- 勾选“删除空行”。
- 点击“确认处理”。

**输出文件**（`test-fix.txt`）：
```
Line 1: This is a test
Line 5: Normal line
```

**说明**：
- 删除包含 `error` 的行（`Line 2` 和 `Line 4`）。
- 删除空行（`Line 3`）。

## 注意事项

- **文件编码**：程序使用 `utf-8` 编码读取和保存文件。非文本文件或不同编码可能导致错误。如需支持其他编码（如 `gbk`），需修改代码。
- **正则表达式**：
  - 支持标准 Python 正则表达式（`re` 模块），忽略大小写。
  - 示例：
    - `error.*`：匹配以 `error` 开头的行。
    - `\d+`：匹配包含数字的行。
    - `^test$`：精确匹配 `test` 的行。
  - 无效正则表达式会触发错误提示。
- **文件覆盖**：新文件若存在会被覆盖。如需避免覆盖（例如加时间戳），需修改代码。
- **性能**：处理大量或大文件可能较慢，可优化为分段处理。
- **依赖问题**：
  - 确保 `tkinterdnd2` 已安装。如果失败，尝试：
    ```bash
    python -m pip install tkinterdnd2 --user
    ```
  - 检查 Python 环境（`python --version`），确保与运行环境的 `pip` 一致。

## 故障排除

- **模块未找到**：
  - 运行 `pip install tkinterdnd2` 或以管理员身份运行。
  - 验证 Python 环境：`python -m pip list`。
- **拖放无效**：
  - 确保从文件资源管理器拖放，而不是 IDE 文件浏览器。
  - 检查 `tkinterdnd2` 是否正确安装。
- **打包为可执行文件**：
  - 使用 PyInstaller：
    ```bash
    pyinstaller -F -w main.py --additional-hooks-dir=.
    ```
  - 创建 `hook-tkinterdnd2.py` 包含：
    ```python
    from PyInstaller.utils.hooks import collect_data_files
    datas = collect_data_files("tkinterdnd2")
    ```

## 贡献

欢迎提交 issue 或 pull request，建议功能或改进代码。请确保代码兼容 Python 3.7+ 和 `tkinterdnd2`。

## 许可证

MIT License
