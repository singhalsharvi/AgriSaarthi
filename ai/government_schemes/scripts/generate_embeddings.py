import os
import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional

try:
    from sentence_transformers import SentenceTransformer
except Exception as e:
    raise ImportError(
        "Missing dependency 'sentence-transformers'. Install with: pip install sentence-transformers"
    )

try:
    import chromadb
except Exception:
    raise ImportError("Missing dependency 'chromadb'. Install with: pip install chromadb")


LOG = logging.getLogger("generate_embeddings")


def _load_metadata_csv(csv_path: Path) -> Dict[str, Dict[str, Optional[str]]]:
    """Load metadata.csv and return mapping from document filename -> metadata dict.

    Expected columns: Scheme Name,Official Website,...,Document Name
    """
    mapping: Dict[str, Dict[str, Optional[str]]] = {}
    if not csv_path.exists():
        LOG.warning("metadata.csv not found at %s", csv_path)
        return mapping
    with csv_path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            doc = (row.get("Document Name") or row.get("Document") or "").strip()
            if not doc:
                continue
            mapping[doc] = {
                "scheme_name": (row.get("Scheme Name") or row.get("Scheme") or "").strip() or None,
                "official_website": (row.get("Official Website") or row.get("Website") or "").strip() or None,
            }
    return mapping


def _read_markdown(md_path: Path) -> str:
    return md_path.read_text(encoding="utf-8")


def _extract_title_from_markdown(text: str) -> Optional[str]:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("# ")
    return None


def build_embeddings(
    data_dir: Path,
    metadata_csv: Path,
    persist_dir: Path,
    collection_name: str = "government_schemes",
    model_name: str = "all-MiniLM-L6-v2",
):
    """Read markdown files, generate embeddings, and store them in a ChromaDB collection.

    - Each markdown file is treated as one document.
    - Stores metadata: scheme_name, source_file, official_website.
    """
    data_dir = Path(data_dir)
    persist_dir = Path(persist_dir)
    # load metadata mapping
    meta_map = _load_metadata_csv(metadata_csv)

    # list markdown files
    files = sorted([p for p in data_dir.glob("*.md") if p.is_file()])
    if not files:
        LOG.info("No markdown files found in %s", data_dir)
        return

    LOG.info("Loading embedding model '%s'...", model_name)
    model = SentenceTransformer(model_name)

    # prepare chroma client
    client = chromadb.PersistentClient(path=str(persist_dir))

    # remove existing collection if present to ensure idempotent run
    try:
        existing = client.get_collection(name=collection_name)
        LOG.info("Collection '%s' exists, deleting and recreating.", collection_name)
        client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = client.create_collection(name=collection_name)

    docs: List[str] = []
    metadatas: List[Dict[str, Optional[str]]] = []
    ids: List[str] = []
    embeddings: List[List[float]] = []

    for p in files:
        doc_text = _read_markdown(p)
        doc_name = p.name
        md = meta_map.get(doc_name, {})
        scheme_name = md.get("scheme_name")
        official_website = md.get("official_website")
        if not scheme_name:
            scheme_name = _extract_title_from_markdown(doc_text) or p.stem

        docs.append(doc_text)
        metadatas.append({
            "scheme_name": scheme_name or "",
            "source_file": str(p.relative_to(data_dir.parent)),
            "official_website": official_website or "",
        })
        ids.append(p.name)

    LOG.info("Encoding %d documents...", len(docs))
    embs = model.encode(docs, show_progress_bar=True)

    # ensure embeddings are lists
    embs_list = [e.tolist() if hasattr(e, "tolist") else list(e) for e in embs]

    LOG.info("Adding to ChromaDB collection '%s' (persist dir: %s)", collection_name, persist_dir)
    collection.add(ids=ids, documents=docs, metadatas=metadatas, embeddings=embs_list)
    LOG.info("Embedding generation and persistence complete. Stored %d items.", len(ids))


def main():
    logging.basicConfig(level=logging.INFO)
    base = Path(__file__).resolve().parents[1]
    data_dir = base / "data"
    metadata_csv = data_dir / "metadata.csv"
    persist_dir = base / "chroma_db"
    build_embeddings(data_dir=data_dir, metadata_csv=metadata_csv, persist_dir=persist_dir)


if __name__ == "__main__":
    main()
