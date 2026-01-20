import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
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

        #Individual analysis
        baskets=get_baskets(df, "transaction_id", "product")
        print(f"{len(baskets)} unique transactions processed")
        #4. calculate for popular product
        top_product= df["product"].mode()[0]
        support_val = calculate_support(baskets, frozenset([top_product]))
        print(f"Support of '{top_product}': {support_val:.2%}")
        print("-"*50)
        
        print(f"\nMining associations from '{file_name}'...")
        # define minimum support threshold
        rules = generate_rules(baskets, min_support=0.01)

        # Generate reports (Visual and CSV)
        if not rules.empty:
            print(f"Found {len(rules)} strong relationships.")
            print("\n--- TOP RECOMMENDATION RULES (by lift) ---")
            print(rules[['item_A', 'item_B', 'support', 'confidence', 'lift']].head(5))

            # Guardamos las recomendaciones en CSV
            rules.to_csv("recommendations.csv", index=False)
            print("\n Recommendations saved to 'recommendations.csv'")
        else:
            print("No association rules found . Try a larger dataset. ")

        #Generate report visual relattionships
        create_visualizations(df, rules)
        #Save recommendations
        rules.to_csv("association_rules.csv", index=False)
        print("Association rules saved to 'association_rules.csv'.")

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

def generate_rules(baskets, min_support=0.05):
    """Calcula las métricas de valor: Support, Confidence y Lift."""
    total_trans = len(baskets)
    item_counts = {}
    pair_counts = {}

    # Contar ocurrencias
    for basket in baskets:
        for item in basket:
            item_counts[item] = item_counts.get(item, 0) + 1
        for pair in combinations(sorted(basket), 2):
            pair_counts[pair] = pair_counts.get(pair, 0) + 1

    # Generar métricas
    rules_list = []
    for (item_A, item_B), count in pair_counts.items():
        support_AB = count / total_trans
        if support_AB >= min_support:
            support_A = item_counts[item_A] / total_trans
            support_B = item_counts[item_B] / total_trans
            conf_A_B = support_AB / support_A
            lift = conf_A_B / support_B
            
            rules_list.append({
                'item_A': item_A, 'item_B': item_B,
                'support': support_AB, 'confidence': conf_A_B, 'lift': lift
            })

    return pd.DataFrame(rules_list).sort_values(by='lift', ascending=False)

def calculate_support(baskets, itemset):
    """ Calculate the relative frequency (support) of a set of items in the baskets."""
    if not baskets:
        return 0
    count = sum(1 for basket in baskets if itemset.issubset(basket))
    return count / len(baskets)


def create_visualizations(df, rules):
    """Genera dos gráficos distintos para el reporte final."""
    sns.set_theme(style="whitegrid")
    
    # Gráfico 1: Los más vendidos (Tu visual original mejorado)
    plt.figure(figsize=(10, 5))
    top_10 = df['product'].value_counts().head(10).reset_index()
    top_10.columns = ['product', 'count']
    sns.barplot(data=top_10, x='count', y='product', hue='product', palette='viridis', legend=False)
    plt.title('Top 10 Most Frequent Products')
    plt.savefig("top_products_frequency.png")
    plt.close()

    # Gráfico 2: Análisis de Relaciones (Si existen reglas)
    if not rules.empty:
        plt.figure(figsize=(10, 5))
        scatter = sns.scatterplot(
            data=rules, x="support", y="confidence", 
            size="lift", hue="lift", palette="magma", sizes=(40, 400)
        )
        plt.title('Association Analysis: Support vs Confidence (Size = Lift)')
        plt.savefig("association_map.png")
        plt.close()
        print("Two charts generated: 'top_products_frequency.png' and 'association_map.png'")
if __name__ == "__main__":
    main()