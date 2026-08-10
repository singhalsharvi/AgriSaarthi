# parser.py — Robust parser for plant disease Markdown profiles in the knowledge base.

import os
from typing import List, Dict

def parse_disease_markdown(filepath: str) -> Dict[str, List[str]]:
    """
    Parses a plant disease markdown file and returns clean, structured lists of:
    - symptoms
    - prevention
    - treatment_or_management
    """
    if not os.path.exists(filepath):
        return {
            "symptoms": [],
            "prevention": [],
            "treatment_or_management": []
        }
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    sections = {}
    current_section = None
    current_lines = []
    
    # Split content by lines and extract heading blocks
    for line in content.splitlines():
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = line[3:].strip().lower()
            current_lines = []
        elif current_section:
            current_lines.append(line)
            
    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()
        
    def to_list(text: str) -> List[str]:
        if not text:
            return []
        
        raw_items = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            # If line is bulleted, remove the bullet
            if stripped.startswith("-") or stripped.startswith("*"):
                item = stripped.lstrip("-* ").strip()
                if item:
                    raw_items.append(item)
            else:
                # Split by sentence periods
                sentences = [s.strip() for s in stripped.split(". ") if s.strip()]
                for s in sentences:
                    # Clean trailing period and spaces
                    s_clean = s.rstrip(".")
                    if s_clean:
                        raw_items.append(s_clean)
        return raw_items

    # Extract sections
    symptoms_text = sections.get("symptoms", "")
    if not symptoms_text:
        symptoms_text = sections.get("visual symptoms", "")
        
    prevention_text = sections.get("prevention", "")
    treatment_text = sections.get("management/treatment", "")
    
    return {
        "symptoms": to_list(symptoms_text),
        "prevention": to_list(prevention_text),
        "treatment_or_management": to_list(treatment_text)
    }
