import pytest
import pandas as pd
import os
from project import load_data, get_baskets, calculate_support, generate_rules

# Helper to create a temporary CSV for testing
@pytest.fixture
def temp_csv(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    file = d / "test.csv"
    df = pd.DataFrame({
        "transaction_id": [1, 1, 2, 2, 3],
        "product": ["Milk", "Bread", "Milk", "Coke", "Milk"]
    })
    df.to_csv(file, index=False)
    return str(file)

def test_load_data(temp_csv):
    # Test if data loads correctly
    df = load_data(temp_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert list(df.columns) == ["transaction_id", "product"]
    
    # Test FileNotFoundError
    with pytest.raises(FileNotFoundError):
        load_data("non_existent_file.csv")

def test_get_baskets():
    df = pd.DataFrame({
        "transaction_id": [1, 1, 2],
        "product": ["A", "B", "A"]
    })
    baskets = get_baskets(df, "transaction_id", "product")
    assert len(baskets) == 2
    assert frozenset(["A", "B"]) in baskets
    assert frozenset(["A"]) in baskets

def test_calculate_support():
    baskets = [
        frozenset(["Milk", "Bread"]),
        frozenset(["Milk"]),
        frozenset(["Bread", "Coke"])
    ]
    # Support of Milk = 2/3
    assert calculate_support(baskets, frozenset(["Milk"])) == pytest.approx(0.666, abs=1e-3)
    # Support of Coke = 1/3
    assert calculate_support(baskets, frozenset(["Coke"])) == pytest.approx(0.333, abs=1e-3)
    # Support of non-existent item = 0
    assert calculate_support(baskets, frozenset(["Diamond"])) == 0

def test_generate_rules():
    # Simple dataset where A and B are always together
    baskets = [
        frozenset(["A", "B"]),
        frozenset(["A", "B"]),
        frozenset(["C"])
    ]
    rules = generate_rules(baskets, min_support=0.1)
    assert not rules.empty
    # Check if 'lift' is calculated (it should be 1.5 in this case)
    # P(A&B) = 2/3, P(A)=2/3, P(B)=2/3 -> Lift = (2/3) / (2/3 * 2/3) = 1.5
    assert rules.iloc[0]["lift"] == 1.5
    assert rules.iloc[0]["item_A"] == "A"
    assert rules.iloc[0]["item_B"] == "B"