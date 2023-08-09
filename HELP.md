
Importing Required Libraries
============================

import os # Required to traverse through files and directories  
import importlib # Required for importing python files dynamically  
from concurrent.futures import ProcessPoolExecutor # Required for parallel processing

NUM\_PROCESSES = os.cpu\_count() # Getting the number of available CPU Cores in the system.

Function Definition starts here.
================================

def files\_in\_dir(directory):

```
# Iterating through given directory, including all subdirectories.
for dirpath, dirnames, filenames in os.walk(directory):
    
    # Looping through all file names in current directory
    for filename in filenames:
        # Returning full filepath for each file.
        yield os.path.join(dirpath, filename)
        
    # Looping through all subdirectory names in current directory
    for dirname in dirnames:
        # Recursively calling itself to get a list of files in the subdirectory
        yield from files_in_dir(os.path.join(dirpath, dirname))
```

Function to process each file with multiple scanners
====================================================

def process\_file(path, scanners):  
for scanner in scanners:  
scan\_data = scanner.scan\_file(path)  
if scan\_data\[0\]:  
\# Printing Virus Detected Scan Data  
print(f"\[Virus detected\] Path: {path}, Scanner: {scanner}, Data: {scan\_data\[1\]}")

Main Function Definition starts here.
=====================================

def main():

```
scanners = [] # Create an empty list to store imported scanners.

# Iterates through './modules' directory and imports any .py file other than 'scanner.py' dynamically.
for file in os.scandir('./modules'):
    if file.is_file() and file.name.endswith(".py") and file.name != "scanner.py":
        module_name = file.name.split('.')[0]
        module = importlib.import_module(f"modules.{module_name}")
        scanner_class = getattr(module, module_name)
        print('Module imported:', scanner_class().name)
        scanners.append(scanner_class())

# Requesting user for the input directory to be scanned.
directory = input("Enter directory to scan: ").strip()

inputs = list(files_in_dir(directory)) # Creating a list of file paths to be scanned.

with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
    for path in inputs:
        # Submitting path and scanners list to the process_file function using the executor object.
        executor.submit(process_file, path, scanners)

print("Scan finished.")
```

Checking if the current script is being executed directly.
==========================================================

if **name** == "**main**":  
main() # Running the program by calling the main() function.