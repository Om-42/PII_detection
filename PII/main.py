from pii_detector import detect_pii
if __name__ == "__main__":
    user_input = input("Enter text to scan for PII:\n")
    res = detect_pii(user_input)
    if not res:
        print("No PII detected.")
    else:
        for item in res:
            print(f"\nPII Type: {item['type']}")
            print("Matches:")
            for m in item['matches']:
                print(f"  - {m}")