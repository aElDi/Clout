# Méthylene 

Methylene is a tool for reading and writing binary data using the NumPy library. It provides two classes: `Methylene_ReWriter` and `Methylene_Reader`.

## Features

- Reading binary data from a file and storing it as a NumPy array.
- Writing NumPy array data to a file.
- Support for reading and writing binary data in a compact format.

## Usage

To use Methylene, follow these steps:

1. Ensure that you have NumPy installed. You can install it using the following command:

   ```shell
   pip install numpy
   ```

2. Import the necessary classes from the `methylene.py` script into your Python code:

   ```python
   from methylene import Methylene_ReWriter, Methylene_Reader
   ```

3. Create an instance of the `Methylene_ReWriter` class to write binary data to a file:

   ```python
   rewriter = Methylene_ReWriter()
   rewriter.read('input.txt')  # Read binary data from the input file
   rewriter.write('output.bin')  # Write the data to the output file
   ```

4. Create an instance of the `Methylene_Reader` class to read binary data from a file:

   ```python
   reader = Methylene_Reader()
   reader.read('input.bin')  # Read binary data from the input file
   ```
