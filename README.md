
# Clout

 
> This is my first significant Python project and was developed from December 2022 to April 2023. This project was submitted as my school project for my final exam.



## Usage

1. Open a terminal or command prompt and navigate to the project directory.
2. Run the following command to execute the program:

   ```shell
   python scanner.py
   ```

3. Follow the prompts to enter the directory you want to scan.

## Dependencies

This program requires the following dependencies:

- Python 3.x
- `os` module
- `importlib` module

## Scanners

The program dynamically imports scanner modules from the `modules` directory. Each scanner module should be a Python file with a class that implements a `scan_file` method. The `scan_file` method should return a tuple with two elements: a boolean indicating whether a virus was detected, and a string with additional data about the scan.

To add new scanners, create a new Python file in the `modules` directory following the naming convention `scanner_name.py`. The file should contain a class with the same name as the file (excluding the extension). The class should implement the `scan_file` method.

Example scanner module (`example_scanner.py`):

```python
class ExampleScanner:
    def __init__(self):
        self.name = "Example Scanner"

    def scan_file(self, path):
        # Implement your scanning logic here
        # Return a tuple with a boolean and additional data
        return False, "No virus detected"
```

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.