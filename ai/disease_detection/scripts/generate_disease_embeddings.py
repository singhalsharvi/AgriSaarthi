import os
import logging
from pathlib import Path
from typing import Dict, List, Optional

import chromadb
from sentence_transformers import SentenceTransformer

LOG = logging.getLogger("generate_disease_embeddings")

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "disease_knowledge"

def build_disease_embeddings(
    data_dir: Path,
    persist_dir: Path,
    collection_name: str = COLLECTION_NAME,
    model_name: str = MODEL_NAME,
):
    """Read disease Markdown files, chunk them by section, generate embeddings, and store in ChromaDB."""
    data_dir = Path(data_dir)
    persist_dir = Path(persist_dir)

    files = sorted([p for p in data_dir.glob("*.md") if p.is_file()])
    if not files:
        LOG.warning("No disease markdown files found in %s", data_dir)
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
    metadatas: List[Dict[str, str]] = []
    ids: List[str] = []

    for p in files:
        doc_text = p.read_text(encoding="utf-8")
        doc_id = p.stem.lower()

        # Split by header sections
        # The markdown files are structured with "## SectionName" headings
        sections = doc_text.split("\n## ")
        
        # Parse crop and disease names first
        crop_name = ""
        disease_name = ""
        
        # We search sections for "Crop" and "Disease" values to attach to metadata
        for sec in sections[1:]:
            sec_lines = sec.strip().splitlines()
            if not sec_lines:
                continue
            header = sec_lines[0].strip().lower()
            content = "\n".join(sec_lines[1:]).strip()
            if header == "crop":
                crop_name = content
            elif header == "disease":
                disease_name = content

        if not crop_name:
            crop_name = doc_id.split("_")[0].replace("-", " ").title()
        if not disease_name:
            disease_name = doc_id.split("_")[-1].replace("-", " ").title()

        # Generate chunks for each section
        # The first section is the title # Crop - Disease, we skip it or save it as an overview
        overview_text = sections[0].strip()
        overview_id = f"{doc_id}_overview"
        docs.append(overview_text)
        metadatas.append({
            "crop": crop_name,
            "disease": disease_name,
            "source": str(p.relative_to(data_dir.parent.parent)),
            "document": p.name,
            "section": "Overview"
        })
        ids.append(overview_id)

        for sec in sections[1:]:
            sec_lines = sec.strip().splitlines()
            if not sec_lines:
                continue
            section_name = sec_lines[0].strip()
            section_content = "\n".join(sec_lines[1:]).strip()
            
            if not section_content:
                continue
            
            # Formulate grounded content containing crop, disease, section name and content
            chunk_text = f"Crop: {crop_name}. Disease: {disease_name}. Section: {section_name}.\nContent: {section_content}"
            chunk_id = f"{doc_id}_{section_name.lower().replace('/', '_').replace(' ', '_')}"
            
            docs.append(chunk_text)
            metadatas.append({
                "crop": crop_name,
                "disease": disease_name,
                "source": str(p.relative_to(data_dir.parent.parent)),
                "document": p.name,
                "section": section_name
            })
            ids.append(chunk_id)

    LOG.info("Encoding %d disease knowledge chunks...", len(docs))
    embeddings = model.encode(docs, normalize_embeddings=True)
    embs_list = [e.tolist() if hasattr(e, "tolist") else list(e) for e in embeddings]

    LOG.info("Adding %d items to ChromaDB collection '%s' at %s", len(ids), collection_name, persist_dir)
    collection.add(ids=ids, documents=docs, metadatas=metadatas, embeddings=embs_list)
    LOG.info("Disease knowledge embedding generation complete. Total records stored: %d", collection.count())


def main():
    logging.basicConfig(level=logging.INFO)
    base = Path(__file__).resolve().parents[1]
    data_dir = base / "knowledge_base"
    persist_dir = base / "chroma_db"
    build_disease_embeddings(data_dir=data_dir, persist_dir=persist_dir)


if __name__ == "__main__":
    main()
