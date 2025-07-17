# utils/llm_utils.py
from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

_model = None

def analyze_gestures(gestures):
    global _model
    if not gestures:
        return "No gestures detected for analysis"

    if _model is None:
        _model = pipeline(
            "text-generation", model="gpt2",
            device="cpu", framework="pt"
        )

    prompt = f"Analyze these body language gestures: {', '.join(gestures)}. Provide a short psychological interpretation (2 sentences max)."
    out = _model(prompt, max_new_tokens=60, num_return_sequences=1, truncation=True, pad_token_id=50256)[0]
    txt = out['generated_text'].replace(prompt, "").strip()
    return txt.split('\n')[0][:150]