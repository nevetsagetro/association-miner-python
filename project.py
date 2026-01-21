import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from fpdf import FPDF
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
            # 5. Reporte de Insights Estratégicos en CLI
            print_strategic_insights(rules)
            
            # 6. Identificación del 'Hidden Gem'
            hidden_gem = rules.sort_values(by="lift", ascending=False).iloc[0]
            print(f"💎 HIDDEN GEM IDENTIFIED:")
            print(f"   The link between '{hidden_gem['item_A']}' and '{hidden_gem['item_B']}'")
            print(f"   is your strongest relationship (Lift: {hidden_gem['lift']:.2f}).\n")

            # 7. Generar Visualizaciones Avanzadas
            create_visualizations(df, rules)


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

def print_strategic_insights(rules):
    """Imprime un resumen legible de las mejores reglas."""
    print("\n" + "="*50)
    print("🎯 STRATEGIC BUSINESS INSIGHTS")
    print("="*50)
    for i, row in rules.head(3).iterrows():
        conf = row['confidence'] * 100
        print(f"🔥 Recommendation {i+1}: '{row['item_A']}' ➔ '{row['item_B']}'")
        print(f"   - Behavior: {conf:.1f}% of buyers also picked this pair.")
        print(f"   - Value: This link is {row['lift']:.1f}x stronger than random.\n")

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
        plt.figure(figsize=(12, 8))
        # Usamos un scatter plot donde el color y el tamaño dependen del LIFT
        scatter = sns.scatterplot(
            data=rules, 
            x="support", 
            y="confidence", 
            size="lift", 
            hue="lift", 
            palette="YlOrRd", # Colores de "calor": amarillo a rojo
            sizes=(100, 1000),
            alpha=0.7,
            edgecolor="black"
        )
        
        # 1. LÍNEAS DE CUADRANTES (Basadas en el promedio)
        avg_support = rules['support'].mean()
        avg_confidence = rules['confidence'].mean()
        
        plt.axvline(x=avg_support, color='gray', linestyle='--', alpha=0.5)
        plt.axhline(y=avg_confidence, color='gray', linestyle='--', alpha=0.5)
        
        # 2. ETIQUETAS DE TEXTO PARA LOS CUADRANTES
        plt.text(rules['support'].max()*0.85, 0.98, 'GOLDEN RULES (High Value)', fontsize=10, fontweight='bold', color='darkred')
        plt.text(rules['support'].min(), 0.98, 'OPPORTUNITIES (Growth)', fontsize=10, fontweight='bold', color='darkblue')
        plt.text(rules['support'].max()*0.85, rules['confidence'].min(), 'STAPLES (Regulars)', fontsize=10, fontweight='bold', color='darkgreen')

        # 3. ANOTAR LOS TOP 5 PUNTOS (Los de mayor Lift)
        top_rules = rules.sort_values(by="lift", ascending=False).head(5)
        for i, row in top_rules.iterrows():
            plt.annotate(
                f"{row['item_A']}➔{row['item_B']}", 
                (row['support'], row['confidence']),
                textcoords="offset points", 
                xytext=(0,12), 
                ha='center', 
                fontsize=8,
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
            )

        # Personalización de títulos y ejes
        plt.title('Strategic Association Map\n(How products relate to each other)', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('SUPPORT (How popular is the combo?)', fontsize=11)
        plt.ylabel('CONFIDENCE (How predictable is the link?)', fontsize=11)
        
        # Mejorar la leyenda
        plt.legend(title="Lift (Relationship Strength)", loc="upper right", bbox_to_anchor=(1.25, 1))
        
        plt.tight_layout()
        plt.savefig("association_map.png", dpi=300) 
        plt.close()


if __name__ == "__main__":
    main()