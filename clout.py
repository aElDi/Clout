# The os module provides interaction with the operating system
import os
# The importlib module enables dynamic module importing
import importlib

def files_in_dir(directory):
    # Generator function that recursively yields all files in a directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(dirpath, filename)
        for dirname in dirnames:
            yield from files_in_dir(os.path.join(dirpath, dirname))

def process_file(path, scanners):
    # Process a file by calling the scan_file method of each scanner module and print any detected viruses
    for scanner in scanners:
        scan_data = scanner.scan_file(path)
        if scan_data[0]:
            print(f"[Virus detected] Path: {path}, Scanner: {scanner.name}, Data: {scan_data[1]}")

def main():
    scanners = []
    # Import scanner modules dynamically from the modules directory
    for file in os.scandir('./modules'):
        if file.is_file() and file.name.endswith(".py") and file.name != "scanner.py":
            module_name = file.name.split('.')[0]
            module = importlib.import_module(f"modules.{module_name}")
            scanner_class = getattr(module, module_name)
            print(f'[Info] Module imported: {scanner_class().name}')
            scanners.append(scanner_class())

    # Prompt for a directory to scan
    directory = input("[Input] Enter directory to scan: ").strip()
    inputs = list(files_in_dir(directory))
    for path in inputs:
        process_file(path, scanners)

    print("[Success] Scan finished.")

if __name__ == "__main__":
    main()
