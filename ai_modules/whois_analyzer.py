from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load fine-tuned WHOIS model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("./models/whois_bert")


def analyze_whois(domain):
    text = fetch_whois_text(domain)  # e.g. from Python-whois or custom parser
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    risk_score = torch.nn.functional.softmax(outputs.logits, dim=1)[0][1].item()
    return {"domain": domain, "risk_score": round(risk_score, 2)}
