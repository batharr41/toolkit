FILE_TYPE_MAP = {
    # 🖼️ VISUAL MEDIA
    "Images": [
        # Standard raster images
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        # High-quality/professional formats
        ".tiff",
        ".tif",
        ".psd",
        ".bmp",
        ".raw",
        ".cr2",
        ".nef",
        # Vector and icon formats
        ".svg",
        ".ico",
    ],
    # 🎬 VIDEO FILES
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"],
    # 🎧 AUDIO FILES
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a"],
    # 📄 DOCUMENTS (Text, Spreadsheets, Presentations)
    "Documents": [
        # Microsoft Office
        ".docx",
        ".doc",
        ".xlsx",
        ".xls",
        ".pptx",
        ".ppt",
        ".odt",
        ".ods",
        # PDF and Ebooks
        ".pdf",
        ".epub",
        ".mobi",
        # Plain text and rich text
        ".txt",
        ".rtf",
    ],
    # ⚙️ EXECUTABLES & APPLICATIONS
    "Applications": [
        # Windows
        ".exe",
        ".msi",
        # macOS
        ".dmg",
        ".app",
        # Linux / Scripts
        ".deb",
        ".rpm",
        ".sh",
        # Note: Be careful with scripts (.sh, .py) as they may be code files too
    ],
    # 📦 ARCHIVES & COMPRESSED FILES
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".bz2"],
    # 💻 CODE & SCRIPTS (Optional, for developers)
    "Code_Scripts": [
        ".py",
        ".html",
        ".css",
        ".js",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".json",
        ".xml",
        ".yaml",
    ],
    # 🌐 WEB FILES (Downloaded files that often land in Downloads)
    "Web_Files": [
        ".url",
        ".webloc",
        ".html",  # HTML can also be a document/code, depending on use
    ],
}


def getExtensionMap():
    map = {}
    for key, vals in FILE_TYPE_MAP.items():
        for val in vals:
            map[val] = key
    return map
