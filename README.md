# 🧹 Project Cleaner Pro

**Project Cleaner Pro** is a cross-platform GUI tool for cleaning up unnecessary build artifacts, dependency folders, cache files, and lockfiles from JavaScript, Python, and Node.js projects.

## ✨ Features

- 📁 Template-based cleanup for:
  - Next.js
  - React
  - Vite
  - Python
  - Node.js
  - Custom mode for advanced users
- 🔍 Scans and lists detected junk by category
- 🗑️ Lets you preview and delete selected items safely
- 📦 Build into standalone `.exe` for Windows

---

## 📸 Screenshot

![Project Cleaner Pro UI](https://github.com/darkwaves-ofc/NodeModulesCleaner/blob/f6057322ee292b10618cd4d68f330933f650a365/screenshots/image.png)

---

## 🚀 Download

> Visit the [Releases](https://github.com/your-username/project-cleaner-pro/releases) page to download the latest `.exe` for Windows.

---

## 🛠️ Build Locally

### 📦 Requirements

- Python 3.11 or higher
- `pyinstaller`

### 🔧 Install dependencies

```bash
pip install -r requirements.txt
```

### 🏗️ Build

```bash
pyinstaller --name ProjectCleanerPro --onefile --windowed main.py
```

Executable will be in the `dist/` folder.

---

## 📂 Templates & What They Clean

| Template   | Folders Removed                                | Files Removed                         |
|------------|-----------------------------------------------|----------------------------------------|
| **Next.js** | `.next`, `node_modules`, `dist`, `build`      | `package-lock.json`, `yarn.lock`, `.env.local` |
| **React**   | `build`, `node_modules`, `dist`               | `package-lock.json`, `yarn.lock`, `.env.local` |
| **Vite**    | `dist`, `node_modules`, `.vite`               | `package-lock.json`, `yarn.lock`, `.env.local` |
| **Python**  | `__pycache__`, `.venv`, `dist`, `build`       | `poetry.lock`, `.coverage`, etc.       |
| **Node.js** | `node_modules`, `.cache`, `build`, `dist`     | `package-lock.json`, `yarn.lock`, etc. |

---

## 🧠 License

MIT License — use it freely in personal and commercial projects.

---

## ❤️ Contributing

Pull requests welcome! If you find bugs or want new features, feel free to open an issue.
