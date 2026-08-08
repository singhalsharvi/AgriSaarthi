import logging
from pathlib import Path
from typing import Dict, List, Optional

import chromadb
from sentence_transformers import SentenceTransformer

LOG = logging.getLogger("generate_crop_embeddings")

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "crop_knowledge"


def build_crop_embeddings(
    data_dir: Path,
    persist_dir: Path,
    collection_name: str = COLLECTION_NAME,
    model_name: str = MODEL_NAME,
):
    """Read crop Markdown files, generate embeddings, and store them in a Crop ChromaDB collection."""
    data_dir = Path(data_dir)
    persist_dir = Path(persist_dir)

    files = sorted([p for p in data_dir.glob("*.md") if p.is_file()])
    if not files:
        LOG.warning("No crop markdown files found in %s", data_dir)
        return

    LOG.info("Loading embedding model '%s'...", model_name)
    model = SentenceTransformer(model_name)

    client = chromadb.PersistentClient(path=str(persist_dir))

    # Remove existing collection if present to ensure idempotent run
    try:
        client.delete_collection(name=collection_name)
        LOG.info("Existing collection '%s' deleted.", collection_name)
    except Exception:
        pass

    collection = client.create_collection(name=collection_name)

    docs: List[str] = []
    metadatas: List[Dict[str, Optional[str]]] = []
    ids: List[str] = []

    for p in files:
        doc_text = p.read_text(encoding="utf-8")
        crop_id = p.stem.lower()

        # Extract title from first line
        title = doc_text.splitlines()[0].lstrip("# ").strip() if doc_text else p.stem

        docs.append(doc_text)
        metadatas.append(
            {
                "crop_name": crop_id,
                "title": title,
                "source_file": str(p.relative_to(data_dir.parent)),
            }
        )
        ids.append(crop_id)

    LOG.info("Encoding %d crop knowledge documents...", len(docs))
    embeddings = model.encode(docs, normalize_embeddings=True)
    embs_list = [e.tolist() if hasattr(e, "tolist") else list(e) for e in embeddings]

    LOG.info("Adding %d items to ChromaDB collection '%s' at %s", len(ids), collection_name, persist_dir)
    collection.add(ids=ids, documents=docs, metadatas=metadatas, embeddings=embs_list)
    LOG.info("Crop knowledge embedding generation complete.")


def main():
    logging.basicConfig(level=logging.INFO)
    base = Path(__file__).resolve().parents[1]
    data_dir = base / "knowledge_base"
    persist_dir = base / "chroma_db"
    build_crop_embeddings(data_dir=data_dir, persist_dir=persist_dir)


if __name__ == "__main__":
    main()
