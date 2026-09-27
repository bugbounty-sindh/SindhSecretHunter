#!/usr/bin/env python3
import re, os, argparse
from pathlib import Path
PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Token": r"ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82}",
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "Slack Token": r"xox[bpras]-[0-9a-zA-Z]{10,48}",
    "Private Key": r"-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----"
}
def scan_file(file_path):
    findings = []
    try:
        text = Path(file_path).read_text(errors='ignore')
        for name, pattern in PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                findings.append((name, matches[0][:50], file_path))
    except: pass
    return findings
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default=".", help="Local path")
    args = parser.parse_args()
    print(f"[+] Scanning: {args.path}\n")
    all_findings = []
    for root, dirs, files in os.walk(args.path):
        if '.git' in dirs: dirs.remove('.git')
        for f in files:
            if f.endswith(('.py','.js','.env','.json','.yaml','.yml','.txt','.sh')):
                fp = os.path.join(root, f)
                all_findings.extend(scan_file(fp))
    if not all_findings:
        print("[-] No secrets found!")
    else:
        print(f"[!!!] Found {len(all_findings)} secrets:\n")
        for name, match, path in all_findings:
            print(f" -> {name} : {match}... | File: {path}")
if __name__ == "__main__":
    main()
