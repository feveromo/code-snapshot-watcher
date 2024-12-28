# Code Snapshot Watcher 📸

A lightweight, automated tool that creates intelligent diffs of your code changes in real-time. Perfect for:
- Sharing code context with AI assistants (like GitHub Copilot, ChatGPT)
- Documenting changes during development
- Creating focused, readable diffs of your work

## ✨ Features

- 🚀 **Auto-start**: Launches automatically when you open your project
- 🎯 **Smart Diffs**: Only shows actual changes, not entire files
- 🧹 **Clean Output**: Formatted diffs with + and - markers
- 🔄 **Real-time**: Updates on every file save
- 🎭 **Git-aware**: Respects your .gitignore rules
- ⚡ **Lightweight**: Minimal CPU and memory usage
- 🛡️ **Safe**: Read-only operations, no code modifications

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/feveromo/code-snapshot-watcher.git
```

2. Copy the required files to your project:
```bash
cd your-project
cp -r code-snapshot-watcher/{.vscode,utils,requirements.txt} .
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Open your project in VSCode/Cursor IDE - the watcher starts automatically!

## 📁 Project Structure

```
your-project/
├── .vscode/
│   ├── tasks.json     # Auto-start configuration
│   └── settings.json  # Python environment settings
└── utils/
    ├── file_watcher.py          # File system monitor
    └── create_code_snapshot.py  # Diff generator
```

## ⚙️ Configuration

### Python Path
Modify `.vscode/settings.json` to set your Python interpreter:
```json
{
    "python.defaultInterpreterPath": "path/to/your/python"
}
```

### Cooldown Period
Adjust the cooldown between snapshots in `utils/file_watcher.py`:
```python
def __init__(self, cooldown=2):  # Seconds between snapshots
```

### Output File
Change the snapshot file name in `utils/create_code_snapshot.py`:
```python
def create_code_snapshot(..., output_file='full_code_snapshot.txt')
```

## 📝 Example Output

```diff
================================================================================
File: src/main.py
================================================================================

Changes:

@@ -15,6 +15,7 @@
 def process_data(input):
-    # Old processing logic
+    # New improved processing
+    result = advanced_processing(input)
     return result
```

## 🔧 Requirements

- Python 3.11+
- VSCode or Cursor IDE
- Operating Systems:
  - Windows (default configuration)
  - Linux/MacOS (modify paths in settings.json)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- Built with [watchdog](https://github.com/gorakhargosh/watchdog) for file system events
- Uses Python's `difflib` for intelligent diff generation
- Inspired by the need for better AI-human code collaboration

## 🐛 Troubleshooting

### Watcher Not Starting
- Verify Python path in `.vscode/settings.json`
- Check if required packages are installed
- Look for error messages in the VSCode/Cursor terminal

### Missing Changes
- Ensure file isn't in .gitignore
- Check if file type is supported (non-binary)
- Verify cooldown period isn't too long 