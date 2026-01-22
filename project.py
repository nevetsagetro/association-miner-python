import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import pyfiglet
from itertools import combinations
import seaborn as sns
import sys
import os


def main():
    # Guardamos el nombre en una variable
    project_title = "Association Miner"
    print_banner(project_title)
    print("Welcome to the analysis tool.")

    # Load csv from my folder data
    # 1. request to my user only the anme of the file, should be in folder data/
    file_name = input("Please share the file name in the folder 'data': ").strip()

    if not file_name.endswith(".csv"):
        file_name += ".csv"

    file_path = os.path.join("data", file_name)

    try:
        # 2. load and clean csv
        # transaction id and product ocolumn requested
        df = load_data(file_path)
        print(f"Dataset loaded: {len(df)} rows found")
        # 3. transform to basket (cluster)

        # Individual analysis
        baskets = get_baskets(df, "transaction_id", "product")
        print(f"{len(baskets)} unique transactions processed")
        # 4. calculate for popular product
        top_product = df["product"].mode()[0]
        support_val = calculate_support(baskets, frozenset([top_product]))
        print(f"Support of '{top_product}': {support_val:.2%}")
        print("-" * 50)

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
            print(
                f"   The link between '{hidden_gem['item_A']}' and '{hidden_gem['item_B']}'"
            )
            print(
                f"   is your strongest relationship (Lift: {hidden_gem['lift']:.2f}).\n"
            )

            print(f"Found {len(rules)} strong relationships.")
            top_table = rules[["item_A", "item_B", "support", "confidence", "lift"]].head(5)
            # Mostramos la tabla con bordes de rejilla y formato de 3 decimales
            print(tabulate(top_table, headers='keys', tablefmt='grid', showindex=False, floatfmt=".3f"))

            # Guardamos las recomendaciones en CSV
            rules.to_csv("recommendations.csv", index=False)
            print("\nRecommendations saved to 'recommendations.csv'")
        else:
            print("No association rules found . Try a larger dataset. ")

        # --- AQUÍ GUARDAMOS EL ÚNICO CSV ---
        output_name = "association_rules.csv"
        rules.to_csv(output_name, index=False)
        print(f"\nAll rules saved to '{output_name}'")
        # Generate report visual relattionships
        create_visualizations(df, rules)

    except FileNotFoundError:
        sys.exit(f"Error: The file '{file_name}' does not exist in 'data/'.")
    except KeyError:
        sys.exit(f"Error: The CSV must have the columns 'transaction_id' and 'product'")
    except Exception as e:
        sys.exit(f"Error unexpected: {e}")

def print_banner(text):
    """
    Recibe un texto y lo imprime en formato ASCII art.
    """
    # Creamos el formato (puedes cambiar 'slant' por 'banner', 'block', etc.)
    ascii_art = pyfiglet.figlet_format(text, font="slant")
    print(ascii_art)
    print("-" * 55)

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
    if total_trans == 0:
        return pd.DataFrame()
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

            rules_list.append(
                {
                    "item_A": item_A,
                    "item_B": item_B,
                    "support": support_AB,
                    "confidence": conf_A_B,
                    "lift": lift,
                }
            )

    return pd.DataFrame(rules_list).sort_values(by="lift", ascending=False)


def calculate_support(baskets, itemset):
    """Calculate the relative frequency (support) of a set of items in the baskets."""
    if not baskets:
        return 0
    count = sum(1 for basket in baskets if itemset.issubset(basket))
    return count / len(baskets)


def print_strategic_insights(rules):
    """Imprime un resumen legible de las mejores reglas."""
    print("\n" + "=" * 50)
    print("🎯 STRATEGIC BUSINESS INSIGHTS")
    print("=" * 50)
    for i, row in rules.head(3).iterrows():
        conf = row["confidence"] * 100
        print(f"🔥 Recommendation {i+1}: '{row['item_A']}' ➔ '{row['item_B']}'")
        print(f"   - Behavior: {conf:.1f}% of buyers also picked this pair.")
        print(f"   - Value: This link is {row['lift']:.1f}x stronger than random.\n")


def create_visualizations(df, rules):
    """
    Genera un dashboard profesional de gran tamaño, priorizando el mapa estratégico.
    Layout: Scatter Plot arriba (grande), Bar Chart y Heatmap abajo (pequeños).
    """
    sns.set_theme(style="whitegrid")

    # Configuramos una figura GRANDE
    fig = plt.figure(figsize=(20, 16))

    # GridSpec con height_ratios para que la fila de arriba sea más alta (el héroe)
    # height_ratios=[1.5, 1] significa que la fila 0 es 1.5 veces más alta que la fila 1
    grid = plt.GridSpec(2, 2, wspace=0.2, hspace=0.25, height_ratios=[1.5, 1])

    # ZONA 1 (ARRIBA, ANCHO COMPLETO): EL MAPA ESTRATÉGICO (LA MAGIA)

    ax_main = fig.add_subplot(grid[0, :])  # Ocupa toda la fila 0

    if rules.empty:
        # Si no hay reglas, mostramos un mensaje en el área principal
        ax_main.text(
            0.5,
            0.5,
            "No significant associations found to plot.\nTry a larger dataset.",
            ha="center",
            va="center",
            fontsize=16,
            color="gray",
        )
    else:
        # Scatter plot principal
        sns.scatterplot(
            data=rules,
            x="support",
            y="confidence",
            size="lift",
            hue="lift",
            palette="YlOrRd",
            sizes=(80, 800),
            alpha=0.8,
            edgecolor="black",
            ax=ax_main,
        )

        # Líneas y Textos de Cuadrantes
        avg_support = rules["support"].mean()
        avg_confidence = rules["confidence"].mean()
        ax_main.axvline(x=avg_support, color="gray", linestyle="--", alpha=0.5)
        ax_main.axhline(y=avg_confidence, color="gray", linestyle="--", alpha=0.5)

        # Etiquetas estratégicas (ajustadas para el tamaño grande)
        ax_main.text(
            rules["support"].max(),
            rules["confidence"].max(),
            "GOLDEN RULES\n(High Value & Predictable)",
            fontsize=12,
            fontweight="bold",
            color="darkred",
            ha="right",
            va="top",
        )
        ax_main.text(
            rules["support"].min(),
            rules["confidence"].max(),
            "HIDDEN OPPORTUNITIES\n(Niche but Strong)",
            fontsize=12,
            fontweight="bold",
            color="darkblue",
            ha="left",
            va="top",
        )
        ax_main.text(
            rules["support"].max(),
            rules["confidence"].min(),
            "STAPLES\n(Frequent but Weak Link)",
            fontsize=12,
            fontweight="bold",
            color="darkgreen",
            ha="right",
            va="bottom",
        )

        # Anotar los Top 5 (con flechas para que se vea profesional)
        top_rules = rules.sort_values(by="lift", ascending=False).head(5)
        for i, row in top_rules.iterrows():
            ax_main.annotate(
                f"{row['item_A']} ➔ {row['item_B']}",
                xy=(row["support"], row["confidence"]),
                xytext=(0, 25),
                textcoords="offset points",
                ha="center",
                arrowprops=dict(
                    arrowstyle="->", connectionstyle="arc3,rad=0.2", color="black"
                ),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9),
                fontweight="bold",
            )

        ax_main.set_title(
            'STRATEGIC ASSOCIATION MAP (The "Magic" Quadrants)',
            fontsize=18,
            fontweight="bold",
            color="#333333",
        )
        ax_main.set_xlabel(
            "SUPPORT (How popular is the combo?)", fontsize=12, fontweight="bold"
        )
        ax_main.set_ylabel(
            "CONFIDENCE (How predictable is the link?)", fontsize=12, fontweight="bold"
        )
        ax_main.legend(
            title="Lift Strength",
            loc="upper right",
            fontsize=10,
            title_fontsize=11,
            fancybox=True,
        )

    # ZONA 2 (ABAJO IZQUIERDA): TOP PRODUCTOS (Contexto)

    ax_bottom_left = fig.add_subplot(grid[1, 0])
    top_10 = df["product"].value_counts().head(10).reset_index()
    top_10.columns = ["product", "count"]
    sns.barplot(
        data=top_10,
        x="count",
        y="product",
        hue="product",
        palette="viridis",
        legend=False,
        ax=ax_bottom_left,
    )
    ax_bottom_left.set_title("Context: Top 10 Most Frequent Products", fontsize=14)
    ax_bottom_left.set_xlabel("Total Transactions")
    ax_bottom_left.set_ylabel("")

    # ZONA 3 (ABAJO DERECHA): HEATMAP (Detalle de Intensidad)

    ax_bottom_right = fig.add_subplot(grid[1, 1])
    if rules.empty:
        ax_bottom_right.axis("off")
    else:
        try:
            # Usamos top 10 para que el heatmap no sea gigante
            top_rules_heatmap = rules.head(10).copy()
            pivot_table = top_rules_heatmap.pivot(
                index="item_A", columns="item_B", values="lift"
            )
            sns.heatmap(
                pivot_table,
                annot=True,
                fmt=".1f",
                cmap="YlGnBu",
                ax=ax_bottom_right,
                cbar_kws={"label": "Lift Score"},
            )
            ax_bottom_right.set_title(
                "Deep Dive: Relationship Intensity Heatmap", fontsize=14
            )
            ax_bottom_right.set_xlabel("Consequent Product")
            ax_bottom_right.set_ylabel("Antecedent Product")
        except Exception as e:
            ax_bottom_right.text(
                0.5,
                0.5,
                f"Heatmap unavailable for this dataset data.\n({e})",
                ha="center",
                va="center",
            )
            ax_bottom_right.axis("off")

    # Título Principal del Dashboard y Guardado
    plt.suptitle(
        "MARKET BASKET ANALYSIS: EXECUTIVE DASHBOARD",
        fontsize=24,
        fontweight="heavy",
        y=0.98,
    )

    # Guardar con alta resolución y bordes ajustados
    output_path = "executive_dashboard.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.5)
    plt.close()
    print(f"\nExecutive Dashboard generated successfully: '{output_path}'")
    print("(Open the image to see the strategic analysis)")
    print("Make with <3 by Nevets Agetro\n")


if __name__ == "__main__":
    main()
