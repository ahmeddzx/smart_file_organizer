# Smart File Organizer 📂

Automatically organizes your messy downloads folder into neatly categorized directories  
(documents, images, videos, music, archives, etc.).

## 🚀 Features
- Detects file type/extension automatically.
- Moves files into categorized folders (`Images/`, `Docs/`, `Videos/`, etc.).
- Supports custom rules (e.g., move `.pdf` files to `Work/`).
- Optional background mode to watch a folder in real-time.

## 📦 Installation
```bash
git clone https://github.com/YOUR_USERNAME/smart_file_organizer.git
cd smart_file_organizer
pip install -r requirements.txt
▶️ Usage
Organize a folder:

bash
Copy code
python main.py --path "C:/Users/Tim/Downloads"
Run in real-time watch mode:

bash
Copy code
python main.py --watch "C:/Users/Tim/Downloads"
📂 Folder Structure

cpp
Copy code
smart_file_organizer/
│── main.py
│── requirements.txt
│── README.md
└── organized_files/ (auto-generated)
