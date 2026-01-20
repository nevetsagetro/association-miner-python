import pandas as pd
import matplotlib as plt
import seaborn as sns
import sys 
import os


def main():
    print("_"*30)
    print("--- 🛒 Association Miner | CS50 Final Project ---")

    # Load csv from my folder data
    #request to my user only the anme of the file, should be in folder data/
    file_name = input("Please share the file name in the folder 'data': ").strip()
    
    if not file_name.endswith(".csv"):
        file_name += ".csv"

    file_path = os.path.join("data", file_name)

    
    try:

    except FileNotFoundError:
        sys.exit(f"Error: The file '{file_name}' does not exist in 'data/'.")


if __name__ == "__main__":
    main()