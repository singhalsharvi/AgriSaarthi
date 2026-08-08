import sys
from pathlib import Path
import chromadb

base = Path(r"c:/Users/lenovo/Crop-recommendation/ai/government_schemes")
persist_dir = base / "chroma_db"
markdown_files = sorted((base / "data").glob("*.md"))

print(f"persist_dir={persist_dir}")
print(f"markdown_files={len(markdown_files)}")

try:
    client = chromadb.PersistentClient(path=str(persist_dir))
    collections = client.list_collections()
    collection_names = [c.name for c in collections]
    if "government_schemes" not in collection_names:
        print("collection_count=0")
        sys.exit(0)

    collection = client.get_collection(name="government_schemes")
    result = collection.get(include=["documents"])
    count = len(result.get("ids", []) or [])
    print(f"collection_count={count}")
except Exception as exc:
    print(f"verification_error={exc}", file=sys.stderr)
    print("collection_count=0")

sys.exit(0)
