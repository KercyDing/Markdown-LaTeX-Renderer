import re
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QTextEdit, QVBoxLayout,
                             QHBoxLayout, QPushButton, QScrollArea, QSplitter)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon
import markdown2
import os


class MarkdownRenderer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Markdown & LaTeX Renderer')
        self.setGeometry(200, 100, 1280, 800)  # 调整窗口位置和大小，使其更大且居中显示
        self.setWindowIcon(QIcon(app_icon_path))  # 添加窗口图标

    def init_ui(self):
        # 设置整体窗口样式
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(245,244,239);
                font-family: "Helvetica Neue", Arial;
            }
        """)
        
        # 创建主布局为水平布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)  # 设置边距
        
        # 创建QSplitter实现可调节的左右布局
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(2)  # 设置分隔条宽度
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #c0c7d0;
                border-radius: 1px;
            }
            QSplitter::handle:hover {
                background-color: #4CAF50;
            }
        """)
        
        # 输入区域
        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("输入内容...")
        self.input_edit.setAcceptRichText(False)
        self.input_edit.setMinimumWidth(250)  # 设置输入区域最小宽度
        self.input_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #c0c7d0;
                border-radius: 8px;
                padding: 8px;
                background-color: white;
                font-size: 14px;
                line-height: 1.5;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.2);
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.3);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        # 连接文本变化信号到延迟渲染函数
        self.input_edit.textChanged.connect(self.delayed_render)
        
        # 显示区域
        self.web_view = QWebEngineView()
        self.web_view.setMinimumWidth(250)  # 设置显示区域最小宽度
        
        # 创建滚动区域并设置样式
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #c0c7d0;
                border-radius: 8px;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 0, 0, 0.05);
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.2);
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.3);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        scroll.setWidget(self.web_view)
        
        # 将输入区域和显示区域添加到QSplitter
        self.splitter.addWidget(self.input_edit)
        self.splitter.addWidget(scroll)
        
        # 设置初始大小比例（1:1）
        self.splitter.setSizes([640, 640])  # 调整分割区域的初始大小，与新窗口宽度匹配
        
        # 将QSplitter添加到主布局
        main_layout.addWidget(self.splitter)
        
        # 创建定时器，用于延迟渲染
        self.render_timer = QTimer()
        self.render_timer.setSingleShot(True)  # 设置为单次触发
        self.render_timer.timeout.connect(self.render_content)

    def render_content(self):
        raw_text = self.input_edit.toPlainText()

        # 处理LaTeX公式
        processed_text = self.process_latex(raw_text)

        # 转换Markdown
        html_content = markdown2.markdown(processed_text, extras=['fenced-code-blocks', 'tables'])

        # 生成完整HTML
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script>
            window.MathJax = {{
              tex: {{
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']],
                processEscapes: false,
                tags: 'ams'
              }},
              svg: {{
                fontCache: 'global'
              }}
            }};
            </script>
            <script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js' async></script>
            <style>
                /* 自定义滚动条样式 */
                ::-webkit-scrollbar {{
                    width: 10px;
                    background: rgba(0, 0, 0, 0.05);
                }}
                ::-webkit-scrollbar-thumb {{
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 5px;
                }}
                ::-webkit-scrollbar-thumb:hover {{
                    background: rgba(0, 0, 0, 0.3);
                }}
                body {{ 
                    font-family: "Helvetica Neue", Arial; 
                    margin: 25px; 
                    line-height: 1.8;
                    color: #333;
                    background-color: #fcfcfa;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    margin-top: 1.5em;
                    margin-bottom: 0.8em;
                    font-weight: 600;
                }}
                h1 {{ font-size: 2em; }}
                h2 {{ font-size: 1.7em; }}
                h3 {{ font-size: 1.4em; }}
                h4 {{ font-size: 1.2em; }}
                pre {{ 
                    background: #f8f8f8; 
                    padding: 15px; 
                    border-radius: 8px; 
                    overflow-x: auto; 
                    border: 1px solid #e0e0e0;
                    margin: 1.2em 0;
                }}
                code {{ 
                    font-family: Consolas, Monaco, "Andale Mono", monospace;
                    font-size: 0.9em;
                    background-color: #f0f0f0;
                    padding: 2px 4px;
                    border-radius: 3px;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                    border-radius: 0;
                }}
                .math {{ 
                    color: #2e7d32; 
                    padding: 5px 0;
                }}
                p {{ 
                    margin: 0.8em 0;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
                ul, ol {{
                    padding-left: 2em;
                    margin: 0.8em 0;
                }}
                li {{
                    margin: 0.4em 0;
                }}
                blockquote {{
                    border-left: 4px solid #4CAF50;
                    padding-left: 1em;
                    margin: 1em 0;
                    color: #555;
                    background-color: #f9f9f9;
                    padding: 10px 15px;
                    border-radius: 0 5px 5px 0;
                }}
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 1em 0;
                    overflow-x: auto;
                    display: block;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 1em auto;
                    border-radius: 5px;
                }}
                hr {{
                    border: 0;
                    height: 1px;
                    background-color: #ddd;
                    margin: 1.5em 0;
                }}
            </style>
        </head>
        <body>
            {html_content}
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    if (window.MathJax) {{
                        // 使用正确的MathJax API
                        window.MathJax.typeset && window.MathJax.typeset();
                    }}
                }});
            </script>
        </body>
        </html>
        """
        self.web_view.setHtml(full_html)

    def process_latex(self, text):
        """
        处理 LaTeX 公式，确保 MathJax 可以正确解析：
        1. \\[...\\] 转换为 $$...$$  (块级公式)
        2. \\(...\\) 转换为 $...$  (行内公式)
        3. 保护 `_` 和 `{}`，避免 Markdown 误解析
        4. 处理 $...$ 和 $$...$$ 环境中的特殊字符
        5. 处理 \\begin{equation}...\\end{equation} 转换为 $$...$$
        6. 处理 align 环境，确保特殊字符正确显示
        7. 保护Markdown表格语法
        """
        
        # 保护Markdown表格语法
        # 临时替换表格中的竖线和冒号，避免被LaTeX处理
        table_pattern = r'(\|[^\n]*\|\s*\n\|[-:\s|]*\|\s*\n(\|[^\n]*\|\s*\n)+)'
        tables = re.findall(table_pattern, text, re.DOTALL)
        table_placeholders = {}
        
        for i, table_match in enumerate(tables):
            placeholder = f"TABLE_PLACEHOLDER_{i}"
            table_placeholders[placeholder] = table_match[0]
            text = text.replace(table_match[0], placeholder)

        # 1. 替换块级公式 \[...\] 为 $$...$$
        text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)

        # 2. 替换行内公式 \(...\) 为 $...$
        text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text)

        # 3. 保护 `_` 和 `{}`，确保 LaTeX 语法不被破坏
        def escape_latex(match):
            """保护 LaTeX 公式，避免 `_` 和 `{}` 被 Markdown 解析"""
            content = match.group(1)
            # 处理反斜杠，确保LaTeX命令正确显示
            escaped_content = content
            # 处理反斜杠，先替换为临时标记
            escaped_content = escaped_content.replace('\\', '\\BACKSLASH')
            # 处理下划线和花括号
            escaped_content = escaped_content.replace('_', '\\_').replace('{', '\\{').replace('}', '\\}')
            # 恢复反斜杠
            escaped_content = escaped_content.replace('\\BACKSLASH', '\\\\')
            return f"${escaped_content}$"

        def escape_latex_block(match):
            """保护块级公式 `$$...$$`，确保 LaTeX 语法正确"""
            content = match.group(1)
            # 处理反斜杠，确保LaTeX命令正确显示
            escaped_content = content
            # 处理反斜杠，先替换为临时标记
            escaped_content = escaped_content.replace('\\', '\\BACKSLASH')
            # 处理下划线和花括号
            escaped_content = escaped_content.replace('_', '\\_').replace('{', '\\{').replace('}', '\\}')
            # 恢复反斜杠
            escaped_content = escaped_content.replace('\\BACKSLASH', '\\\\')
            return f"$$ {escaped_content} $$"

        # 4. 处理 $...$ 和 $$...$$ 环境中的特殊字符
        text = re.sub(r'\$(.*?)\$', escape_latex, text)  # 行内公式
        text = re.sub(r'\$\$(.*?)\$\$', escape_latex_block, text, flags=re.DOTALL)  # 块级公式

        # 5. 处理 \begin{equation}...\end{equation} 转换为 $$...$$
        text = re.sub(r'\\begin{equation}(.*?)\\end{equation}', escape_latex_block, text, flags=re.DOTALL)

        # 6. 处理 align 环境，确保特殊字符正确显示
        def fix_align(match):
            """处理 align 环境中的特殊字符，确保它们能被 MathJax 正确解析"""
            content = match.group(1)
            # 先处理反斜杠，避免后续替换时出现问题
            # 注意：在 align 环境中，每行结束需要 \\ 表示换行，这里需要特殊处理
            fixed_content = content
            # 处理换行符 \\ (在LaTeX中表示换行)
            fixed_content = re.sub(r'\\\\', r'\\newline', fixed_content)
            # 处理其他反斜杠开头的命令
            fixed_content = fixed_content.replace('\\', '\\\\')  
            # 恢复换行符
            fixed_content = fixed_content.replace('\\newline', '\\\\\\\\')
            # 处理下划线和花括号
            fixed_content = fixed_content.replace('_', '\\_').replace('{', '\\{').replace('}', '\\}')
            # 使用 $$...$$ 包裹 align 环境，让 MathJax 正确识别
            return f"$$ \\begin{{align}}{fixed_content}\\end{{align}} $$"

        text = re.sub(r'\\begin{align}(.*?)\\end{align}', fix_align, text, flags=re.DOTALL)
        
        # 恢复表格占位符
        for placeholder, table in table_placeholders.items():
            text = text.replace(placeholder, table)

        return text


    def delayed_render(self):
        """当文本内容变化时，延迟0.5秒后自动渲染"""
        # 重置定时器，确保在用户停止输入0.5秒后才渲染
        self.render_timer.stop()
        self.render_timer.start(500)  # 500毫秒

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    app_icon_path = os.path.join(base_path, 'icon', 'app.ico')
    app.setWindowIcon(QIcon(app_icon_path))  # 设置任务栏图标
    window = MarkdownRenderer()
    window.show()
    sys.exit(app.exec())