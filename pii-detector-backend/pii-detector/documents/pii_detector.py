import re
from collections import defaultdict

class IDValidator:
    def __init__(self):
        self.patterns = {
            'aadhar': re.compile(r'\b[2-9][0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'),
            'pan': re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', re.IGNORECASE),
            'voter_id': re.compile(r'\b[A-Z]{2,3}[0-9]{6,8}\b', re.IGNORECASE)
        }

    def validate_aadhar(self, number):
        cleaned = re.sub(r'[\s-]', '', number)
        if not re.fullmatch(r'[2-9][0-9]{11}', cleaned):
            return False
        return self.verhoeff_checksum(cleaned)

    def validate_pan(self, number):
        return bool(re.fullmatch(r'[A-Z]{5}[0-9]{4}[A-Z]', number.upper()))

    def validate_voter_id(self, number):
        return bool(re.fullmatch(r'[A-Z]{2,3}[0-9]{6,8}', number.upper()))

    def verhoeff_checksum(self, number):
        d = [[0,1,2,3,4,5,6,7,8,9],
             [1,2,3,4,0,6,7,8,9,5],
             [2,3,4,0,1,7,8,9,5,6],
             [3,4,0,1,2,8,9,5,6,7],
             [4,0,1,2,3,9,5,6,7,8],
             [5,9,8,7,6,0,4,3,2,1],
             [6,5,9,8,7,1,0,4,3,2],
             [7,6,5,9,8,2,1,0,4,3],
             [8,7,6,5,9,3,2,1,0,4],
             [9,8,7,6,5,4,3,2,1,0]]
        
        p = [[0,1,2,3,4,5,6,7,8,9],
             [1,5,7,6,2,8,3,0,9,4],
             [5,8,0,3,7,9,6,1,4,2],
             [8,9,1,6,0,4,3,5,2,7],
             [9,4,5,3,1,2,6,8,7,0],
             [4,2,8,6,5,7,3,9,0,1],
             [2,7,9,3,8,0,6,4,1,5],
             [7,0,4,6,9,1,3,2,5,8]]
        
        inv = [0,4,3,2,1,5,6,7,8,9]

        c = 0
        digits = list(map(int, reversed(number)))

        for i, digit in enumerate(digits):
            c = d[c][p[i % 8][digit]]

        return c == 0

    def find_ids(self, text):
        """Find and validate all ID numbers in the input text"""
        results = defaultdict(list)
        for id_type, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                matched_text = match.group()
                validator = getattr(self, f'validate_{id_type}')
                
                if id_type == 'aadhar':
                    cleaned = re.sub(r'[\s-]', '', matched_text)
                    if validator(cleaned):
                        results[id_type].append(cleaned)
                else:
                    cleaned = matched_text.upper()
                    if validator(cleaned):
                        results[id_type].append(cleaned)
        
        return dict(results)


# ✅ Exposed function used in views.py
def detect_pii(text):
    validator = IDValidator()
    return validator.find_ids(text)
