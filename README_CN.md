<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="许可证">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="平台">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_CN.md">简体中文</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🔥 HotkeyForge</h1>

<p align="center">
  <strong>强大的跨平台热键管理CLI工具，专为开发者打造</strong>
</p>

<p align="center">
  <em>用可自定义的系统级热键锻造您的生产力</em>
</p>

---

## 🎉 项目介绍

**HotkeyForge** 是一款强大的命令行工具，旨在帮助开发者和高级用户高效管理系统级热键。它提供了统一的界面来创建、配置和监控 Windows、Linux 和 macOS 上的键盘快捷键。

### 为什么选择 HotkeyForge？

- 🎯 **统一管理**：在一个地方管理所有热键
- ⚡ **跨平台**：在 Windows、Linux 和 macOS 上无缝运行
- 🔧 **高度可配置**：支持命令、脚本、URL 和自定义操作
- 📊 **使用统计**：追踪每个热键的使用频率
- 🛡️ **冲突检测**：自动检测并警告冲突的快捷键
- 📦 **模板系统**：预置常用场景的热键模板

---

## ✨ 核心特性

### 🔑 热键管理
- 使用简单的 CLI 命令**添加/删除/更新**热键
- 支持**复杂组合键**（Ctrl+Alt+Shift+Key）
- **启用/禁用**热键而无需删除
- 基于**配置文件**组织不同工作流

### 🚀 操作类型
| 操作类型 | 描述 |
|---------|------|
| `command` | 执行 Shell 命令 |
| `script` | 运行脚本文件 |
| `url` | 在浏览器中打开 URL |
| `custom` | 自定义 Python 处理函数 |

### 📊 统计与监控
- 追踪每个热键的**触发次数**
- 查看**最后触发**时间戳
- 导出统计数据进行分析

### 🛡️ 智能功能
- **冲突检测**：当多个热键使用相同按键时自动警告
- **模板库**：预配置的常用热键集合
- **导入/导出**：备份和恢复您的配置

---

## 🚀 快速开始

### 环境要求
- Python 3.8 或更高版本
- pip 包管理器

### 安装方式

```bash
# 从 PyPI 安装
pip install hotkeyforge

# 或从源码安装
git clone https://github.com/gitstq/HotkeyForge.git
cd HotkeyForge
pip install -e .
```

### 基本使用

```bash
# 显示帮助
hotkeyforge --help

# 添加新热键
hotkeyforge add -n "open_terminal" -k "ctrl+alt+t" -d "打开终端" -a command -c "gnome-terminal"

# 列出所有热键
hotkeyforge list

# 启动热键监听器
hotkeyforge start

# 显示统计信息
hotkeyforge stats

# 检测冲突
hotkeyforge conflicts
```

---

## 📖 详细使用指南

### 添加热键

```bash
# 添加命令热键
hotkeyforge add -n "screenshot" -k "print_screen" -d "截图" -a command -c "gnome-screenshot"

# 添加 URL 热键
hotkeyforge add -n "google" -k "ctrl+alt+g" -d "打开 Google" -a url -u "https://google.com"

# 添加带标签的热键
hotkeyforge add -n "vscode" -k "ctrl+alt+v" -d "打开 VS Code" -a command -c "code" -t "dev,editor"
```

### 管理热键

```bash
# 列出所有热键
hotkeyforge list

# 按配置文件列出热键
hotkeyforge list --profile work

# 仅列出启用的热键
hotkeyforge list --enabled

# 更新热键
hotkeyforge update "open_terminal" --keys "ctrl+shift+t"

# 禁用热键
hotkeyforge update "screenshot" --disabled

# 删除热键
hotkeyforge remove "google"
```

### 使用模板

```bash
# 列出可用模板
hotkeyforge templates

# 应用模板
hotkeyforge apply clipboard
hotkeyforge apply developer
hotkeyforge apply media
```

### 配置管理

```bash
# 查看当前设置
hotkeyforge config --show

# 启用自动启动
hotkeyforge config --auto-start

# 禁用通知
hotkeyforge config --no-notifications

# 导出配置
hotkeyforge export ~/hotkeyforge_backup.yaml

# 导入配置
hotkeyforge import-config ~/hotkeyforge_backup.yaml
```

---

## 💡 设计理念

### 为什么开发 HotkeyForge

作为开发者，我们经常在应用程序之间切换、运行命令、执行重复性任务。虽然大多数操作系统提供基本的热键功能，但在不同应用程序和工作流中管理热键往往是分散且不一致的。

**HotkeyForge** 的诞生正是为了解决这个问题：

1. **统一界面**：一个工具管理所有热键
2. **开发者优先**：为习惯终端的开发者打造
3. **可扩展性**：轻松扩展自定义操作和处理函数
4. **可移植性**：配置文件可在不同机器间通用

### 架构设计

```
HotkeyForge
├── CLI 层 (基于 Click 的命令)
├── 核心层 (热键管理逻辑)
│   ├── HotkeyConfig (YAML 配置管理)
│   └── HotkeyManager (监听器和执行器)
└── 平台层 (pynput 跨平台支持)
```

---

## 📦 构建与部署

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/HotkeyForge.git
cd HotkeyForge

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 构建包
pip install build
python -m build
```

### 创建发布版本

```bash
# 安装构建工具
pip install build twine

# 构建分发包
python -m build

# 上传到 PyPI
twine upload dist/*
```

---

## 🤝 贡献指南

欢迎参与贡献！以下是参与方式：

1. **Fork** 本仓库
2. **创建** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 更改 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **提交** Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 为新功能编写测试
- 更新 API 变更的文档
- 使用规范的提交信息

---

## 📄 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [pynput](https://github.com/moses-palmer/pynput) - 跨平台键盘监听
- [Click](https://github.com/pallets/click) - CLI 框架
- [Rich](https://github.com/Textualize/rich) - 美观的终端输出

---

<p align="center">
  HotkeyForge 团队用 ❤️ 打造
</p>
