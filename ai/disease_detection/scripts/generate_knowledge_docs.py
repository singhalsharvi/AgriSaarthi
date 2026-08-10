import os
import sys

# Import the DISEASE_KNOWLEDGE from the sibling directory dynamically
desktop_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sibling_src = os.path.join(desktop_dir, "Farm AI Companion", "ai", "disease_detection", "src")
if sibling_src not in sys.path:
    sys.path.insert(0, sibling_src)

try:
    from disease_db import DISEASE_KNOWLEDGE
except ImportError as err:
    print(f"Could not import disease_db: {err}")
    sys.exit(1)

OUTPUT_DIR = os.path.join("ai", "disease_detection", "knowledge_base")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_markdown(key, info):
    crop = info.get("crop", "N/A")
    disease = info.get("disease_name", "N/A")
    symptoms = info.get("symptoms", "N/A")
    causes = info.get("causes", "N/A")
    affected_parts = info.get("affected_parts", "N/A")
    favorable_conditions = info.get("favorable_conditions", "N/A")
    severity = info.get("severity", "N/A")
    prevention = info.get("prevention", "N/A")
    treatment = info.get("treatment", "N/A")
    practices = info.get("practices", "N/A")
    reference = info.get("reference", "N/A")

    # Clean the class key to create the markdown file name
    # e.g. Pepper__bell___Bacterial_spot -> pepper_bell_bacterial_spot.md
    clean_key = key.lower().replace("___", "_").replace("__", "_")
    filename = f"{clean_key}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    content = f"""# {crop} - {disease}

## Crop
{crop}

## Disease
{disease}

## Description
A profile of {disease} affecting {crop} plants. This condition primarily impacts the {affected_parts.lower()} with a severity rating of {severity.lower()}.

## Symptoms
{symptoms}

## Visual symptoms
Affected plants display symptoms on {affected_parts.lower()}: {symptoms}

## Causes
{causes}

## Risk factors
Severity is rated {severity.lower()}. Key risk factors include planting in fields with a history of infection, poor sanitation, and not sanitizing farming tools.

## Environmental conditions
{favorable_conditions}

## Prevention
{prevention}
{practices}

## Management/treatment
{treatment}

## Sources
{reference}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated {filepath}")

def main():
    for key, info in DISEASE_KNOWLEDGE.items():
        generate_markdown(key, info)
    print("Successfully generated all 15 markdown files.")

if __name__ == "__main__":
    main()
