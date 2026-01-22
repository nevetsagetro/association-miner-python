import pytest
import pandas as pd
from project import get_baskets, calculate_support, generate_rules

def test_get_baskets():
    # Creamos un DataFrame de prueba
    data = {
        "transaction_id": [1, 1, 2, 3, 3],
        "product": ["milk", "bread", "milk", "apple", "bread"]
    }
    df = pd.DataFrame(data)
    baskets = get_baskets(df, "transaction_id", "product")
    
    assert len(baskets) == 3
    assert frozenset(["milk", "bread"]) in baskets
    assert frozenset(["apple", "bread"]) in baskets
