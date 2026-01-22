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

def test_calculate_support():
    baskets = [
        frozenset(["milk", "bread"]),
        frozenset(["milk"]),
        frozenset(["bread", "apple"]),
    ]
    # "milk" aparece en 2 de 3
    assert calculate_support(baskets, frozenset(["milk"])) == pytest.approx(0.666, 0.01)
    # "milk" y "bread" juntos en 1 de 3
    assert calculate_support(baskets, frozenset(["milk", "bread"])) == pytest.approx(0.333, 0.01)
    # Algo que no existe
    assert calculate_support(baskets, frozenset(["beer"])) == 0

def test_generate_rules():
    # Caso simple donde A siempre va con B
    baskets = [
        frozenset(["coffee", "sugar"]),
        frozenset(["coffee", "sugar"]),
        frozenset(["coffee"]),
    ]
    rules = generate_rules(baskets, min_support=0.1)
    
    # Buscamos la regla coffee -> sugar
    # Support = 2/3 (0.66), Confidence = (2/3) / (3/3) = 0.66
    assert not rules.empty
    row = rules.iloc[0]
    assert row["item_A"] == "coffee"
    assert row["item_B"] == "sugar"
    assert row["support"] == pytest.approx(0.666, 0.01)