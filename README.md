PLEASE PROVIDE YOUR OWN INPUT BY MODIFYING FILES (PDFs && challenge1b_input.json) AND CHECK WITH THE OUTPUT OUR MODEL WILL DO ITS PART 😉 BROH!

# Our Folder Structure

Challenge_1b/
├── Collection 1/                    # Travel Planning
│   ├── PDFs/                       # South of France guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 2/                    # Adobe Acrobat Learning
│   ├── PDFs/                       # Acrobat tutorials
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/                       # Cooking guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
└── README.md

<img width="347" height="498" alt="image" src="https://github.com/user-attachments/assets/720011cc-a5ec-44c4-b9f2-cdd7d0fbee0e" />


## DEMO INPUT OUTPUT GENERATED CHECKOUT BROH
<img width="1910" height="1018" alt="image" src="https://github.com/user-attachments/assets/1a4308e6-cc7c-41ae-a432-439964777ff0" />

## Input Format

<img width="1280" height="725" alt="image" src="https://github.com/user-attachments/assets/52427862-97f6-4bb1-85b5-8e82d443388a" />

- Each **Collection** contains:
  - `challenge1b_input.json`: Describes the persona, task, and list of PDFs.
  - A `PDFs/` folder with the mentioned documents.

### Sample challenge1b_input.json

```json
{
  "persona": { "role": "HR Executive" },
  "job_to_be_done": { "task": "Find policies related to onboarding and compliance." },
  "documents": [
    { "filename": "EmployeeHandbook.pdf" },
    { "filename": "PolicyGuide.pdf" }
  ]
}

Output Format
The script produces a challenge1b_output.json in each collection folder:
{
  "metadata": {
    "input_documents": [...],
    "persona": "...",
    "job_to_be_done": "...",
    "task_keywords": [...],
    "processing_timestamp": "..."
  },
  "extracted_sections": [
    {
      "document": "PolicyGuide.pdf",
      "section_title": "Compliance Rules",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "EmployeeHandbook.pdf",
      "refined_text": "Onboarding procedures include filling forms and submitting documents...",
      "page_number": 2
    }
  ]
}
```

### SAMPLE OUTPUT YOU CAN CHECK

<img width="1910" height="1017" alt="image" src="https://github.com/user-attachments/assets/f6710765-1a7c-4910-a080-6bce51368cd5" />


## Key Features

-Extracts section headings using regex and layout cues.
-Enhances keyword matching using fuzzy string matching (RapidFuzz).
-Ranks sections and paragraphs by relevance to the persona’s task.
-Cross-references multiple PDFs to boost commonly recurring headings.
-Fully offline-capable and deterministic.

## Run with Docker
Build the Image

docker build -t pdf-analyzer .

Run the Tool On Windows (PowerShell) powershell

docker run --rm `
  -v ${PWD}\Collection 1:/app/Collection 1 `
  -v ${PWD}\Collection 2:/app/Collection 2 `
  -v ${PWD}\Collection 3:/app/Collection 3 `
  --network none `
  pdf-analyzer

## Dependencies
List of required packages in requirements.txt:

PyMuPDF==1.23.7
rapidfuzz

### Notes
No internet access is required during execution.
Script automatically processes all collections named Collection 1, Collection 2, etc.
JSON output is deterministic and formatted for easy programmatic evaluation.

