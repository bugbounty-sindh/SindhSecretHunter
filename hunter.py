print("=== Secret Hunter Started ===")
import re

text = input("Enter text to scan: ")

if "password" in text.lower() or "api_key" in text.lower() or "secret" in text.lower():
    print("\n[!] ALERT! Secret found in text!")
    print("[!] This is not safe.")
else:
    print("\n[OK] Safe - No secret found.")

print("\n=== Scan Complete ===")
