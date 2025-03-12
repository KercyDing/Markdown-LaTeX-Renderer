# Markdown & LaTeX Renderer

一个简洁、强大的 Markdown 和 LaTeX 实时渲染工具，支持即时预览和数学公式渲染。
![example](https://github.com/user-attachments/assets/987e48c5-abf2-43ae-975c-59d061135076)

## 主要特性

- 实时预览：输入即可看到渲染效果，无需手动刷新
- LaTeX 公式支持：完整支持数学公式的编写和渲染
- 美观的界面：现代化的 UI 设计，提供舒适的编辑体验
- 可调节布局：编辑区和预览区大小可自由调节
- 多种格式支持：
  - 完整的 Markdown 语法支持
  - 行内公式：
  ```LaTeX
  质能方程：$E=mc^2$
  ```
  - 块级公式：
  ```LaTeX
  高斯求和公式为：
  $$\sum_{i=1}^n i = \frac{n(n+1)}{2}$$
  ```
  - 表格
  - 代码块
  - 引用
  - 列表

## 快速开始

### 方式一：直接运行（推荐）

1. 下载并解压软件包
2. 双击运行 `renderer.exe`
3. 开始编写

### 方式二：从源码运行

1. 确保已安装 Python 3.8 或更高版本
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行程序：
   ```bash
   python main.py
   ```

## 注意事项

- 首次加载 LaTeX 公式可能需要几秒钟时间
- 需要保持网络连接（用于加载MathJax在线资源）
- 安装依赖失败时可尝试更换pip镜像源
- 复杂公式渲染可能需要额外加载时间

## 技术栈

- PyQt6：用于构建桌面应用界面
- markdown2：提供 Markdown 解析功能
- MathJax：提供 LaTeX 公式渲染支持

## 反馈与建议

- 如果您在使用过程中遇到任何问题，或有任何改进建议，欢迎提出。
- 联系邮箱：<u>dkx215417@gmail.com</u>
