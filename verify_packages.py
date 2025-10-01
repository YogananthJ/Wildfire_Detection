import importlib

# List of required packages
required = [
    "flask",
    "numpy",
    "cv2",
    "PIL",
    "ultralytics",
    "tensorflow"
]

for pkg in required:
    try:
        module = importlib.import_module(pkg if pkg != "cv2" else "cv2")
        version = getattr(module, "__version__", "built-in")
        print(f"✅ {pkg} is installed (version: {version})")
    except ImportError:
        print(f"❌ {pkg} is NOT installed")
