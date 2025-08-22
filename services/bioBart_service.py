from pathlib import Path

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# model_name = "microsoft/biobart-v1.1"
model_name = "GanjinZero/biobart-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

summarizer = pipeline(
    "summarization",
    model=model,
    tokenizer=tokenizer,
    device_map="auto"
)

def bio_bart_summarize(files: list):
    summary = []
    for source_filename in files:
        text = Path(source_filename).read_text(encoding="utf-8")

        text = """"
Hypertension is a major risk factor for cardiovascular diseases, including heart failure,
stroke, and myocardial infarction. Despite multiple pharmacological treatments available,
optimal blood pressure control remains challenging. Recent studies indicate that lifestyle
interventions, such as dietary modification, increased physical activity, and weight loss,
can significantly reduce blood pressure in hypertensive patients. This review summarizes
the current evidence supporting lifestyle interventions for hypertension management
and highlights potential mechanisms, clinical outcomes, and implementation strategies.
"""
        res = summarizer(
            text,
            max_new_tokens=200,
            truncation=True
        )

        summary.append({
            "name": source_filename,
            "summary": res[0]["summary_text"]
        })

    return summary