from modules.scanner import Scanner
import subprocess

class YaraScanner(Scanner):
    name='Yara rules Scanner'
    desc='Scan files with fast Yare rules'

    rules = 'ALL'

    def scan_file(self, file_path):
            print("[YARA] - ",end="")
            print(subprocess.call(f'yara.exe -C "./modules/yara_rules/{self.rules}" {file_path}'))
            return [False]