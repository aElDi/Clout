import os
import math
from modules.scanner import Scanner


class HeuristicScanner(Scanner):
    name = "Heuristic Scanner"
    desc = "Scan file by heuristic rules(filename, entropy)"

    def entropy(self, file_path):
        # Computes the entropy value of a given file
        with open(file_path, 'rb') as f:
            byte_freq = [0] * 256
            byte_count = 0
            while True:
                byte = f.read(1)
                if not byte:
                    break
                byte_freq[ord(byte)] += 1
                byte_count += 1
            entropy = 0.0
            for freq in byte_freq:
                if freq > 0:
                    p = freq / byte_count
                    entropy -= p * math.log2(p)
            return entropy

        # Define a list of heuristic rules to check for potential viruses
    heuristic_rules = [
        # Check for executable files with a high entropy value
        {
            'name': 'High Entropy Executable',
            'description': 'Detects an executable file with high entropy value',
            'rule': lambda self, f: os.path.splitext(f)[1].lower() == '.exe' and self.entropy(f) > 7.0
        },
        # Check for suspicious files with a long name and non-alphanumeric characters
        {
            'name': 'Suspicious Filename',
            'description': 'Detects a suspicious file with long name and non-alphanumeric characters',
            'rule': lambda f: len(os.path.basename(f)) > 20 and not os.path.basename(f).isalnum()
        },
        # Check for scripts or batch files that are obfuscated
        {
            'name': 'Obfuscated Script/Batch File',
            'description': 'Detects a script or batch file with obfuscated code',
            'rule': lambda self, f: os.path.splitext(f)[1].lower() in ('.vbs', '.ps1', '.bat', '.cmd') and 'powershell' in self._get_file_content(f) or 'exec' in self._get_file_content(f)
        },

        # Check for encrypted file formats
        {
            'name': 'Encrypted File',
            'description': 'Detects an encrypted file format',
            'rule': lambda self, f: os.path.splitext(f)[1].lower() in ('.zip', '.rar', '.7z') and self.entropy(f) < 4.0
        },

        # Check for suspicious files that are using a double file extension
        {
            'name': 'Double Extension Suspicion',
            'description': 'Detects a file with a suspicious double file extension',
            'rule': lambda f: '..' in os.path.basename(f)
        }
        # Add more heuristic rules as needed
    ]

    def scan_file(self, file_path):
        # Scans a file
        try:
            for rule in self.heuristic_rules:
                if rule['rule'](file_path):
                    print(
                        f"[Suspicious file]: {rule['name']}\n:{rule['description']}\n:{file_path}")
                    return [False]
            return [False]
        except:
            return [False]
