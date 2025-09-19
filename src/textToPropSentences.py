import re
import sys

# ---------- Filler / disfluency removal ----------
FILLERS = [
    r"\babsolutely\b", r"\bdefinitely\b", r"\bactually\b", r"\bmaybe\b",
    r"\bwell\b", r"\bjust\b", r"\bbasically\b", r"\bkind of\b", r"\bsort of\b",
    r"\bum\b", r"\buh\b", r"\blike\b", r"\byou know\b", r"\bsorry\b",
    r"\bi mean\b", r"\bthat came out awkward\b", r"\boh god\b",
    r"\bha!?[\s]*", r"\bgood morning\b", r"\blet'?s be clear\b",
    r"\bin reality\b", r"\bseriously\b", r"\bthey know\b"
]

def clean_text(text: str) -> str:
    text = text.lower()
    for f in FILLERS:
        text = re.sub(f, "", text, flags=re.I)
    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------- Mapping templates ----------
TEMPLATES = [
    # Experience
    (r"(\d+)\s+years?", lambda m: f"I have {m.group(1)} years of experience."),
    (r"(\d+)\s+months?", lambda m: f"I have {m.group(1)} months of experience."),
    (r"over a decade", lambda m: "I have over 10 years of experience."),
    (r"for the past (\d+)\s+year", lambda m: f"I have {m.group(1)} years of recent experience."),
    (r"since (\d{4})", lambda m: f"I have experience since {m.group(1)}."),

    # Skills
    (r"devops engineer.*kubernetes", lambda m: "I am a DevOps engineer specializing in Kubernetes."),
    (r"c\+\+ developer", lambda m: "I am a C++ developer."),
    (r"ruby on rails developer", lambda m: "I am a Ruby on Rails developer."),
    (r"distributed systems", lambda m: "I specialize in distributed systems."),
    (r"machine learning", lambda m: "I have experience in machine learning."),
    (r"data", lambda m: "I work with data."),

    # Responsibilities
    (r"responsible for (.+)", lambda m: f"I am responsible for {m.group(1)}."),
    (r"wrote .*policies", lambda m: "I wrote network policies."),
    (r"deploy.*yaml", lambda m: "I deploy yaml files."),
    (r"ran some scripts", lambda m: "I ran scripts."),
    (r"check the logs", lambda m: "I check logs."),
    (r"restart the pod", lambda m: "I restart pods."),

    # Leadership
    (r"\btech lead\b", lambda m: "I was a tech lead."),
    (r"\bmanager of (\d+)", lambda m: f"I managed {m.group(1)} engineers."),
    (r"\bmanaged\b", lambda m: "I managed a team."),
    (r"\bled\b|\blead\b", lambda m: "I led a team."),
    (r"\bcoordinated\b", lambda m: "I coordinated work."),
    (r"\bmentored\b", lambda m: "I mentored engineers."),
    (r"worked alone|not comfortable with people", lambda m: "I mostly work alone."),

    # Negations / corrections
    (r"not an? (.+)", lambda m: f"I am not a {m.group(1)}."),
    (r"just an? (.+)", lambda m: f"I am a {m.group(1)}."),
    (r"fraud|impostor", lambda m: "I admitted to being a fraud."),
]

def map_to_propositions(text: str):
    # split into rough sentences
    sentences = re.split(r"[.?!]", text)
    results = []
    for s in sentences:
        s = s.strip()
        if not s: 
            continue
        mapped = None
        for pat, func in TEMPLATES:
            m = re.search(pat, s)
            if m:
                mapped = func(m)
                results.append(mapped)
                break
        if not mapped:
            results.append(s)  # fallback
    return results

# ---------- Pipeline ----------
def transcript_to_props(input_file: str, output_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned = clean_text(raw_text)
    props = map_to_propositions(cleaned)

    with open(output_file, "w", encoding="utf-8") as f:
        for p in props:
            f.write(p.strip() + "\n")

    print(f"Processed {len(props)} propositions written to {output_file}")

# ---------- Run as script ----------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transcript_to_props.py input.txt output.txt")
        sys.exit(1)
    transcript_to_props(sys.argv[1], sys.argv[2])
