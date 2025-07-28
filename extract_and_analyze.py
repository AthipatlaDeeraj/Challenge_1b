from pathlib import Path
import unicodedata
import re
from rapidfuzz import fuzz, process as fuzz_process
import fitz
import json
from datetime import datetime
from collections import Counter

#i have abstracted whole text inside pdf now and stored inside results
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    results = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if text.strip():
            results.append((i, text.strip()))
    return results

#making text extraction and better headings and all done using the below func
#also made convinient names to understand better broh
def clean_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("\u2022", " ")
    text = text.replace("\n", " ")
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    return ' '.join(text.split()).strip()
 
def extract_headings(text):
    lines = text.split("\n")
    headings = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if (re.match(r"^(\d+\.?\s*)?[A-Z][A-Za-z0-9\s\-&,]{3,50}:?$", line)
                and len(line.split()) <= 12
                and not any(ui in line.lower() for ui in ["note", "page", "blank page", "toolbar", ">"])):
            headings.append(line.strip(':').title())
    return headings
 
def get_keywords_from_task(task, persona=""):
    raw = task.lower().split()
    base_keywords = [word.strip(",.") for word in raw if len(word) > 3]
    related = {
        "trip": ["travel", "journey", "tour", "explore", "itinerary"],
        "group": ["friends", "companions", "team"],
        "college": ["student", "youth", "university"],
        "plan": ["schedule", "arrange", "prepare", "organize"]
    }
    if "hr" in persona.lower():
        related["form"] = ["onboarding", "compliance", "fillable", "signature", "submission"]
    enriched = []
    for word in base_keywords:
        enriched.append(word)
        if word in related:
            enriched.extend(related[word])
    return list(set(enriched))
 
def score_heading(heading, task_keywords, heading_freq_counter):
    heading_lower = heading.lower()
    score = heading_freq_counter[heading_lower]
    for kw in task_keywords:
        if kw in heading_lower:
            score += 2
        elif fuzz.token_sort_ratio(kw, heading_lower) > 80:
            score += 1
    if heading_lower in ["introduction", "overview", "summary"]:
        score -= 1
    return score 
def score_paragraph(para, task_keywords):
    para_lower = para.lower()
    score = 0
    for kw in task_keywords:
        score += para_lower.count(kw)
        score += fuzz.partial_ratio(kw, para_lower) // 50
    return score
 
def process_collection(collection_path):
    input_path = collection_path / "challenge1b_input.json"
    output_path = collection_path / "challenge1b_output.json"
    pdf_dir = collection_path / "PDFs"

    with open(input_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    metadata = {
        "input_documents": [doc["filename"] for doc in input_data["documents"]],
        "persona": input_data["persona"]["role"],
        "job_to_be_done": input_data["job_to_be_done"]["task"],
        "task_keywords": get_keywords_from_task(input_data["job_to_be_done"]["task"], input_data["persona"]["role"]),
        "processing_timestamp": datetime.utcnow().isoformat()
    }

    task_keywords = metadata["task_keywords"]
    heading_candidates = []
    subsection_by_doc = {}
    all_headings = []

#taking input data here and also if no file found also checking here broh
    for doc in input_data["documents"]:
        pdf_path = pdf_dir / doc["filename"]
        if not pdf_path.exists():
            print(f"Missing file: {doc['filename']}")
            continue

        pages = extract_text_from_pdf(pdf_path)
        best_score = 0
        best_snippet = ""
        best_page = 1

        for page_number, text in pages:
            headings = extract_headings(text)
            all_headings.extend([h.lower() for h in headings])
            for heading in headings:
                heading_candidates.append({
                    "document": doc["filename"],
                    "section_title": heading,
                    "page_number": page_number
                })

            for para in text.split("\n\n"):
                cleaned = clean_text(para)
                s = score_paragraph(cleaned, task_keywords)
                if s > best_score:
                    best_score = s
                    best_snippet = cleaned[:1500]
                    best_page = page_number

        subsection_by_doc[doc["filename"]] = {
            "document": doc["filename"],
            "refined_text": best_snippet,
            "page_number": best_page
        }

    heading_freq_counter = Counter(all_headings)

    for entry in heading_candidates:
        entry["score"] = score_heading(entry["section_title"], task_keywords, heading_freq_counter)

    heading_candidates.sort(key=lambda x: (-x["score"], x["page_number"]))

    extracted_sections = []
    seen = set()
    docs_included = set()
    rank = 1

    for entry in heading_candidates:
        key = (entry["document"], entry["section_title"])
        if key in seen or entry["document"] in docs_included:
            continue
        seen.add(key)
        docs_included.add(entry["document"])
        extracted_sections.append({
            "document": entry["document"],
            "section_title": entry["section_title"],
            "importance_rank": rank,
            "page_number": entry["page_number"]
        })
        rank += 1
        if rank > 5:
            break

    subsection_analysis = list(subsection_by_doc.values())[:5]

    output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"{output_path.name}")

#my starting point where the code starts running broh
def main():
    base = Path(".")
    for i in range(1, 4):
        collection = base / f"Collection {i}"
        if (collection / "challenge1b_input.json").exists():
            print(f"\n{collection.name}")
            process_collection(collection)

if __name__ == "__main__":
    main()
