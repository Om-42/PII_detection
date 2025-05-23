from cryptography.fernet import Fernet

def encrypt_pii(pii_results):
    encrypt_choice = input("\nWould you like to encrypt any detected PII? (yes/no): ").strip().lower()

    if encrypt_choice != 'yes':
        return

    pii_types = [item['type'] for item in pii_results]
    print(f"Detected PII types: {', '.join(pii_types)}")
    selected_types = input("Which types do you want to encrypt? (comma-separated, e.g., email,pan): ").strip().lower().split(',')

    selected_types = [ptype.strip() for ptype in selected_types if ptype.strip() in pii_types]

    if not selected_types:
        print("No valid PII types selected for encryption.")
        return

    key = Fernet.generate_key()
    fernet = Fernet(key)
    print(f"\nEncryption Key (save securely!): {key.decode()}")

    for item in pii_results:
        if item['type'] in selected_types:
            encrypted = [fernet.encrypt(match.encode()).decode() for match in item['matches']]
            print(f"\nEncrypted {item['type']}s:")
            for e in encrypted:
                print(f"  - {e}")