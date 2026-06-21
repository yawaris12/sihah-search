import os

folders = [
    "data",
    "models"
]

files = {
    "build_index.py": "",
    "app.py": "",
    "data/.gitkeep": "",
    "models/.gitkeep": ""
}

print("📁 Creating project structure...\n")

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created folder: {folder}")

for file_path, content in files.items():
    # only create file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created file: {file_path}")
    else:
        print(f"Skipped existing file: {file_path}")

print("\n✅ Project structure ready!")