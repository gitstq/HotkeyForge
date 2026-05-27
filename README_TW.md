<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="授權條款">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="平台">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_CN.md">简体中文</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🔥 HotkeyForge</h1>

<p align="center">
  <strong>強大的跨平台熱鍵管理 CLI 工具，專為開發者打造</strong>
</p>

<p align="center">
  <em>用可自訂的系統級熱鍵鍛造您的生產力</em>
</p>

---

## 🎉 專案介紹

**HotkeyForge** 是一款強大的命令列工具，旨在幫助開發者和進階使用者高效管理系統級熱鍵。它提供了統一的介面來建立、設定和監控 Windows、Linux 和 macOS 上的鍵盤快速鍵。

### 為什麼選擇 HotkeyForge？

- 🎯 **統一管理**：在一個地方管理所有熱鍵
- ⚡ **跨平台**：在 Windows、Linux 和 macOS 上無縫運行
- 🔧 **高度可設定**：支援命令、腳本、URL 和自訂操作
- 📊 **使用統計**：追蹤每個熱鍵的使用頻率
- 🛡️ **衝突偵測**：自動偵測並警告衝突的快速鍵
- 📦 **模板系統**：預設常用情境的熱鍵模板

---

## ✨ 核心特性

### 🔑 熱鍵管理
- 使用簡單的 CLI 命令**新增/刪除/更新**熱鍵
- 支援**複雜組合鍵**（Ctrl+Alt+Shift+Key）
- **啟用/停用**熱鍵而無需刪除
- 基於**設定檔**組織不同工作流程

### 🚀 操作類型
| 操作類型 | 描述 |
|---------|------|
| `command` | 執行 Shell 命令 |
| `script` | 執行腳本檔案 |
| `url` | 在瀏覽器中開啟 URL |
| `custom` | 自訂 Python 處理函數 |

### 📊 統計與監控
- 追蹤每個熱鍵的**觸發次數**
- 查看**最後觸發**時間戳
- 匯出統計資料進行分析

### 🛡️ 智慧功能
- **衝突偵測**：當多個熱鍵使用相同按鍵時自動警告
- **模板庫**：預設的常用熱鍵集合
- **匯入/匯出**：備份和還原您的設定

---

## 🚀 快速開始

### 環境需求
- Python 3.8 或更高版本
- pip 套件管理器

### 安裝方式

```bash
# 從 PyPI 安裝
pip install hotkeyforge

# 或從原始碼安裝
git clone https://github.com/gitstq/HotkeyForge.git
cd HotkeyForge
pip install -e .
```

### 基本使用

```bash
# 顯示說明
hotkeyforge --help

# 新增熱鍵
hotkeyforge add -n "open_terminal" -k "ctrl+alt+t" -d "開啟終端機" -a command -c "gnome-terminal"

# 列出所有熱鍵
hotkeyforge list

# 啟動熱鍵監聽器
hotkeyforge start

# 顯示統計資訊
hotkeyforge stats

# 偵測衝突
hotkeyforge conflicts
```

---

## 📖 詳細使用指南

### 新增熱鍵

```bash
# 新增命令熱鍵
hotkeyforge add -n "screenshot" -k "print_screen" -d "截圖" -a command -c "gnome-screenshot"

# 新增 URL 熱鍵
hotkeyforge add -n "google" -k "ctrl+alt+g" -d "開啟 Google" -a url -u "https://google.com"

# 新增帶標籤的熱鍵
hotkeyforge add -n "vscode" -k "ctrl+alt+v" -d "開啟 VS Code" -a command -c "code" -t "dev,editor"
```

### 管理熱鍵

```bash
# 列出所有熱鍵
hotkeyforge list

# 按設定檔列出熱鍵
hotkeyforge list --profile work

# 僅列出已啟用的熱鍵
hotkeyforge list --enabled

# 更新熱鍵
hotkeyforge update "open_terminal" --keys "ctrl+shift+t"

# 停用熱鍵
hotkeyforge update "screenshot" --disabled

# 刪除熱鍵
hotkeyforge remove "google"
```

### 使用模板

```bash
# 列出可用模板
hotkeyforge templates

# 套用模板
hotkeyforge apply clipboard
hotkeyforge apply developer
hotkeyforge apply media
```

### 設定管理

```bash
# 查看目前設定
hotkeyforge config --show

# 啟用自動啟動
hotkeyforge config --auto-start

# 停用通知
hotkeyforge config --no-notifications

# 匯出設定
hotkeyforge export ~/hotkeyforge_backup.yaml

# 匯入設定
hotkeyforge import-config ~/hotkeyforge_backup.yaml
```

---

## 💡 設計理念

### 為什麼開發 HotkeyForge

作為開發者，我們經常在應用程式之間切換、執行命令、執行重複性工作。雖然大多數作業系統提供基本的熱鍵功能，但在不同應用程式和工作流程中管理熱鍵往往是分散且不一致的。

**HotkeyForge** 的誕生正是為了解決這個問題：

1. **統一介面**：一個工具管理所有熱鍵
2. **開發者優先**：為習慣終端機的開發者打造
3. **可擴充性**：輕鬆擴充自訂操作和處理函數
4. **可攜性**：設定檔可在不同機器間通用

### 架構設計

```
HotkeyForge
├── CLI 層 (基於 Click 的命令)
├── 核心層 (熱鍵管理邏輯)
│   ├── HotkeyConfig (YAML 設定管理)
│   └── HotkeyManager (監聽器和執行器)
└── 平台層 (pynput 跨平台支援)
```

---

## 📦 建置與部署

### 從原始碼建置

```bash
# 複製儲存庫
git clone https://github.com/gitstq/HotkeyForge.git
cd HotkeyForge

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows

# 安裝開發相依套件
pip install -e ".[dev]"

# 執行測試
pytest

# 建置套件
pip install build
python -m build
```

### 建立發布版本

```bash
# 安裝建置工具
pip install build twine

# 建置分發套件
python -m build

# 上傳到 PyPI
twine upload dist/*
```

---

## 🤝 貢獻指南

歡迎參與貢獻！以下是參與方式：

1. **Fork** 本儲存庫
2. **建立** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 變更 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **提交** Pull Request

### 開發規範

- 遵循 PEP 8 程式碼風格
- 為新功能撰寫測試
- 更新 API 變更的文件
- 使用規範的提交訊息

---

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳情請查看 [LICENSE](LICENSE) 檔案。

---

## 🙏 致謝

- [pynput](https://github.com/moses-palmer/pynput) - 跨平台鍵盤監聽
- [Click](https://github.com/pallets/click) - CLI 框架
- [Rich](https://github.com/Textualize/rich) - 美觀的終端機輸出

---

<p align="center">
  HotkeyForge 團隊用 ❤️ 打造
</p>
