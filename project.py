import pandas as pd
import matplotlib as plt
import seaborn as sns
import sys 
import os


def main():
    print("-"*50)
    print("--- 🛒 Association Miner | CS50 Final Project ---")
    print("-"*50)

    # Load csv from my folder data
    #1. request to my user only the anme of the file, should be in folder data/
    file_name = input("Please share the file name in the folder 'data': ").strip()
    
    if not file_name.endswith(".csv"):
        file_name += ".csv"

    file_path = os.path.join("data", file_name)

    
    try:
    #2. load and clean csv
        #transaction id and product ocolumn requested
        df = load_data(file_path)
        print(f"Dataset loaded: {len(df)} rows found")
        #3. transform to basket (cluster)
        baskets=get_baskets(df, "transaction_id", "product")
        print(f"{len(baskets)} unique transactions processed")
        #4. calculate for popular product
        top_product= df["product"].mode()[0]
        support_val = calculate_support(baskets, frozenset([top_product]))
        print(f"Support of '{top_product}': {support_val:.2%}")
        #5. Generate the visual
        generate_report(baskets)
    except FileNotFoundError:
        sys.exit(f"Error: The file '{file_name}' does not exist in 'data/'.")
    except KeyError:
        sys.exit(f"Error: The CSV must have the columns 'transaction_id' and 'product'")
    except Exception as e:
        sys.exit(f"Error unexpected: {e}")

def load_data(file_path):
    """Load the CSV, drop the nulls and verified columns."""
    if not os.path.exists(file_path):
        raise FileNotFoundError
    df = pd.read_csv(file_path)
    return df.dropna()

def calculate_support(baskets, itemset):

def generate_report(baskets):

if __name__ == "__main__":
    main()