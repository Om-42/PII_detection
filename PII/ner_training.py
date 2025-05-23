# =========================
# Custom NER Training Code
# =========================
import spacy
from spacy.training.example import Example
import random

# Load spaCy's small English model
nlp = spacy.load("en_core_web_sm")
ner = nlp.get_pipe("ner")

# Define custom PII entity labels
LABELS = ["AADHAAR", "PAN", "VOTER_ID", "DRIVING_LICENSE", "BANK_ACCOUNT"]
for label in LABELS:
    ner.add_label(label)

# Create training examples with PII context

TRAIN_DATA = [
    # True PII examples (same as before)
    ("My Aadhaar number is 1234 5678 9123.", {"entities": [(21, 35, "aadhaar")]}),
    ("Please verify Aadhaar 2345-6789-0123 for the records.", {"entities": [(18, 32, "aadhaar")]}),
    ("User's UIDAI ID: 3456 7890 1234", {"entities": [(17, 31, "aadhaar")]}),
    ("The Aadhaar no. 4567 8901 2345 is confidential.", {"entities": [(16, 30, "aadhaar")]}),

    ("His PAN card number is ABCDE1234F.", {"entities": [(21, 31, "pan")]}),
    ("Please enter your Permanent Account Number: PQRST5678Z", {"entities": [(40, 50, "pan")]}),
    ("PAN: XYZAB1234L", {"entities": [(5, 15, "pan")]}),

    ("My Voter ID is XYZ1234567", {"entities": [(13, 23, "voter_id")]}),
    ("EPIC number is ABC9876543", {"entities": [(15, 25, "voter_id")]}),
    ("Voter card number: DEF7654321", {"entities": [(20, 30, "voter_id")]}),

    ("DL number is MH12 20110012345", {"entities": [(13, 28, "driving_license")]}),
    ("Driving License: KA05 20110067890", {"entities": [(17, 32, "driving_license")]}),
    ("License No. DL0420150123456", {"entities": [(12, 27, "driving_license")]}),

    ("Account number: 123456789012", {"entities": [(16, 28, "bank_account")]}),
    ("Bank A/C no. 987654321098765", {"entities": [(11, 26, "bank_account")]}),
    ("Transfer to account 234567890123456789", {"entities": [(16, 35, "bank_account")]}),
    ("PAN is ABCDE1234F", {"entities": [(7, 17, "PAN")]}),
    ("EPIC ID: XYZ1234567", {"entities": [(9, 19, "VOTER_ID")]}),
    ("Driving license MH12 20110012345 was renewed.", {"entities": [(17, 33, "DRIVING_LICENSE")]}),
    ("Bank account 1234567890123456 is active.", {"entities": [(13, 29, "BANK_ACCOUNT")]}),

    # Non-PII context (negative samples)
    ("The meeting was scheduled at 1234 Elm Street.", {"entities": []}),
    ("20110012345 is just an invoice number.", {"entities": []}),
    ("1234 5678 9123 is test data, not real Aadhaar.", {"entities": []}),
    ("ABCDE1234F is just a sample, not PAN.", {"entities": []}),
    ("XYZ1234567 is a dummy voter ID.", {"entities": []}),
    ("MH12 20110012345 was just a reference number.", {"entities": []}),
    ("1234567890123456 is used for examples only.", {"entities": []}),

    # False positives (should NOT be labeled as PII)
    ("Random number 1234 5678 9123 should not be detected as Aadhaar.", {"entities": []}),
    ("Placeholder ABCDE1234F not a real PAN.", {"entities": []}),
    ("Sample Voter ID XYZ1234567 is invalid.", {"entities": []}),
    ("Fake DL MH12 20110012345 mentioned here.", {"entities": []}),
    ("Demo bank account 1234567890123456 in this text.", {"entities": []}),
    ("The address 1234 Elm Street has nothing to do with Aadhaar.", {"entities": []}),
    ("Call me at 919876543210, this is not an Aadhaar number.", {"entities": []}),
    ("Invoice 20110012345 was processed.", {"entities": []}),
    ("This code ABCDE1234F is just an example, not PAN.", {"entities": []}),
    ("Random text 999999999999 that looks like a bank account.", {"entities": []}),
    ("The voter ID XYZ0000000 is a dummy value.", {"entities": []}),
    ("Phone number 1234567890 and Aadhaar 0000 0000 0000 are different.", {"entities": []}),
    ("Fake driving license number KA00 0000000000 entered.", {"entities": []}),

    # Mixed true + false positives in one sentence
    ("Aadhaar 1234 5678 9123 and sample PAN ABCDE1234F.", {"entities": [(8, 22, "aadhaar")]}),
    ("Voter ID XYZ1234567 and fake voter ID XYZ0000000.", {"entities": [(9, 19, "voter_id")]}),
    ("Bank account 1234567890123456 and demo account 000000000000.", {"entities": [(13, 29, "bank_account")]}),

    # Negative contexts with negation keywords to help model learn
    ("This is a fake Aadhaar number: 1234 5678 9123.", {"entities": []}),
    ("Demo PAN card number: ABCDE1234F.", {"entities": []}),
    ("Placeholder voter ID: XYZ1234567.", {"entities": []}),
    ("Sample driving license MH12 20110012345 used here.", {"entities": []}),
    ("Random bank account 1234567890123456 not real.", {"entities": []}),
]


# Disable other pipes for training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.resume_training()
    for itn in range(30):  # Increase epochs for better learning
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.3, losses=losses)
        print(f"Iteration {itn + 1} Losses: {losses}")

# Save the trained model
nlp.to_disk("custom_ner_model")
print("Model saved to 'custom_ner_model'")