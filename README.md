# 🛒 Association Miner | CS50 Final Project
#### Video Demo:  [Watch the Video Demo here](https://youtu.be/wu4TrLy68-o)
#### Description:

**Association Miner** is a specialized data science tool developed as my final project for CS50. It is designed to uncover hidden patterns and consumer behavior trends within retail transaction data. Based on the data mining principles of **Market Basket Analysis**, this project allows business owners and analysts to identify which products are frequently purchased together. 

By calculating essential metrics like **Support, Confidence, and Lift**, the program transforms raw CSV data into actionable strategic insights. These insights help businesses make informed decisions regarding product placement (grouping related items), cross-selling strategies, and the creation of promotional bundles to increase revenue.

The project was inspired by the real-world application of the Apriori principle. I wanted to build a tool that wasn't just a spreadsheet processor, but a descriptive engine that tells a story about consumer behavior through automated visualizations and a "Hidden Gem" detection system that highlights the most non-obvious but strong relationships in the data.

---

### 📂 File Descriptions

* **`project.py`**: This is the main script of the application. It contains the logic for loading data via Pandas, cleaning null values, generating item combinations, calculating statistical metrics, and triggering the visualization engine.
* **`data/`**: A dedicated directory for input CSV files. The program is designed to look here for datasets that include at least a `transaction_id` and a `product` column.
* **`association_rules.csv`**: The primary output file. It saves all calculated association rules and metrics, allowing for deeper exploration in Excel or other BI tools.
* **`executive_dashboard.png`**: A high-resolution, professional dashboard. It combines the Strategic Association Map, the Product Popularity analysis, and the Relationship Heatmap into a single image.
* **`requirements.txt`**: A file listing the external dependencies (`pandas`, `seaborn`, `tabulate`, `matplotlib`) required to run the project.

---

## 🛠️ How it Works

The application follows a rigorous data processing pipeline to ensure statistical accuracy:

1.  **Ingestion & Cleaning**: The program loads the CSV via Pandas and drops null values to ensure the integrity of the calculations.
2.  **Basket Transformation**: Individual rows of products are grouped by their `transaction_id` into Python **frozensets**. This allows for highly efficient subset checking during the mining phase.
3.  **Mining Engine**: Using `itertools.combinations`, the program calculates the frequency of item pairs and applies the following formulas:
    * **Support**: The relative popularity of a product combination.
        $$Support(A \rightarrow B) = \frac{\text{freq}(A, B)}{N}$$
    * **Confidence**: The predictability that buying Product A will lead to buying Product B.
        $$Confidence(A \rightarrow B) = \frac{\text{freq}(A, B)}{\text{freq}(A)}$$
    * **Lift**: The strength of the association, adjusted for the individual popularity of the items. A Lift > 1 indicates a relationship that is stronger than random chance.
        $$Lift(A \rightarrow B) = \frac{Confidence(A, B)}{Support(B)}$$
4.  **Reporting**: Results are rendered in the CLI using the `tabulate` library and exported as a visual dashboard.

---

## 🧠 Design Choices

Throughout the development of this project, I made several critical design decisions to balance technical performance with a professional user experience:

* **Frozensets for Performance**: I chose to use `frozenset` instead of standard lists for transaction "baskets." Because frozensets are hashable and unordered, the subset checking required for support calculations is significantly faster. This ensures the program remains performant even when processing large datasets with over 50,000 rows.
* **Strategic Dashboard Prioritization**: I utilized `matplotlib.GridSpec` to create an asymmetrical dashboard layout. I decided that the **Strategic Association Map** should occupy 60% of the visual space because that is where the "magic" happens—identifying **Golden Rules** and **Hidden Opportunities** via a coordinate system.
* **Custom Engine vs. Libraries**: While libraries like `mlxtend` exist for this purpose, I chose to program the rule calculation engine from scratch. This was done to demonstrate a deep understanding of the underlying mathematics of data mining.



---

## 🚀 Installation & Usage

1.  **Install dependencies**:
    ```bash
    pip install pandas seaborn tabulate matplotlib
    ```
2.  **Prepare data**: Place your transaction CSV file inside the `data/` folder.
3.  **Run the program**:
    ```bash
    python project.py
    ```
4.  **Analyze**: Enter your filename when prompted, and find your results in `association_rules.csv` and `executive_dashboard.png`.

---