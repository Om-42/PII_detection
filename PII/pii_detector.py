import re
import spacy

nlp = spacy.load("custom_ner_model")

def verhoeff_checksum(number: str) -> bool:
    d_table = [
        [0,1,2,3,4,5,6,7,8,9],
        [1,2,3,4,0,6,7,8,9,5],
        [2,3,4,0,1,7,8,9,5,6],
        [3,4,0,1,2,8,9,5,6,7],
        [4,0,1,2,3,9,5,6,7,8],
        [5,9,8,7,6,0,4,3,2,1],
        [6,5,9,8,7,1,0,4,3,2],
        [7,6,5,9,8,2,1,0,4,3],
        [8,7,6,5,9,3,2,1,0,4],
        [9,8,7,6,5,4,3,2,1,0]
    ]

    p_table = [
        [0,1,2,3,4,5,6,7,8,9],
        [1,5,7,6,2,8,3,0,9,4],
        [5,8,0,3,7,9,6,1,4,2],
        [8,9,1,6,0,4,3,5,2,7],
        [9,4,5,3,1,2,6,8,7,0],
        [4,2,8,6,5,7,3,9,0,1],
        [2,7,9,3,8,0,6,4,1,5],
        [7,0,4,6,9,1,3,2,5,8]
    ]

    c = 0
    reversed_digits = list(map(int, reversed(number)))

    for i, digit in enumerate(reversed_digits):
        c = d_table[c][p_table[i % 8][digit]]

    return c == 0

def detect_pii(text: str):
    results = []

    # Strict Aadhaar regex: exactly 4 digits - 4 digits - 4 digits, only hyphens as separators
    patterns = {
        "aadhaar": r"(?<!\d)(\d{12}|\d{4} \d{4} \d{4}|\d{4}-\d{4}-\d{4})(?!\d)",
        "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "voter_id": r"\b[A-Z]{3}[0-9]{7}\b",
        "passport": r"\b[A-Z][0-9]{7}\b",
        "driving_license": r"\b(?:[A-Z]{2}\d{2}\s?\d{11}|\d{13})\b",
        "bank_account": r"\b\d{9,18}\b"
    }

    context_keywords = {
        "aadhaar": {"adhaar", "aadhaar", "uidai", "aadhar"},
        "pan": {"pan", "permanent account number"},
        "voter_id": {"voter", "epic", "election", "voter id", "voter_id"},
        "passport": {"passport", "travel document"},
        "driving_license": {"driving license", "dl", "rto", "license number"},
        "bank_account": {"account number", "a/c", "bank account", "ac no"}
    }

    negation_keywords = {"not", "fake", "placeholder", "demo", "sample", "random"}

    doc = nlp(text)
    pii_found = {}

    for pii_type, pattern in patterns.items():
        matches = re.finditer(pattern, text)
        filtered_matches = []

        for match in matches:
            start, end = match.start(), match.end()

            # Find sentence containing the match
            sent = None
            for s in doc.sents:
                if s.start_char <= start < s.end_char:
                    sent = s
                    break

            context_text = sent.text.lower() if sent else text[max(0,start-20):min(len(text),end+20)].lower()

            # Skip matches if negation keywords present in context
            if any(neg in context_text for neg in negation_keywords):
                continue

            # Proceed only if context keywords present
            if any(kw in context_text for kw in context_keywords[pii_type]):
                if pii_type == "aadhaar":
                    digits_only = match.group().replace("-", "")
                    # Must be exactly 12 digits after removing hyphens
                    if len(digits_only) != 12:
                        continue
                    # Verhoeff checksum validation
                    if not verhoeff_checksum(digits_only):
                        continue

                filtered_matches.append(match.group())

        if filtered_matches:
            pii_found[pii_type] = list(set(filtered_matches))

    # Add spaCy NER detected entities if label matches
    for ent in doc.ents:
        label = ent.label_.lower()
        if label in patterns.keys():
            pii_found.setdefault(label, [])
            if ent.text not in pii_found[label]:
                pii_found[label].append(ent.text)

    for pii_type, matches in pii_found.items():
        results.append({
            "type": pii_type,
            "method": "regex + spacy context + ner",
            "matches": matches
        })

    if not results:
        results.append({"type": None, "method": None, "matches": []})

    return results
