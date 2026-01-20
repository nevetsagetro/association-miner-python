import pandas as pd
import matplotlib.pyplot as plt
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

def get_baskets(df, id_col, item_col):
    """Cluster the products by ID of transaction in a list of Frozensets."""
    grouped = df.groupby(id_col)[item_col].apply(list)
    return [frozenset(items) for items in grouped]

def calculate_support(baskets, itemset):
    """ Calculate the relative frequency (support) of a set of items in the baskets."""
    if not baskets:
        return 0
    count = sum(1 for basket in baskets if itemset.issubset(basket))
    return count / len(baskets)
def generate_report(baskets):
    """Create a bart chart of the top 10 products and save as PNG."""
    all_items = [item for basket in baskets for item in basket]

    # Count frequency and take the TOP 10
    counts = pd.Series(all_items).value_counts().head(10).reset_index()
    counts.columns = ['product', 'frequency']

    # Configure the plot
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    plot = sns.barplot(x='frequency', y='product', hue='product', palette='viridis', legend=False , data=counts)

    plt.title('Top 10 Most Frequent Products(Market Basket Analysis)')
    plt.tight_layout()

    # Save the plot (CLI environment may not support direct display)
    output_name = "top_10_products.png"
    plt.savefig(output_name)
    print(f"Report generated and saved as '{output_name}'.")
    plt.close()
if __name__ == "__main__":
    main()