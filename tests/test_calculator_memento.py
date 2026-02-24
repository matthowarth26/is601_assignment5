import datetime
from unittest.mock import Mock, patch
from app.calculator_memento import CalculatorMemento


@patch("app.calculator_memento.Calculation")
def test_memento_to_dict_uses_calc_to_dict(mock_calculation):
    """
    'history': [calc.to_dict() for calc in self.history]
    """
    calc_instance = Mock()
    calc_instance.to_dict.return_value = {"operation": "Addition"}
    
    ts = datetime.datetime(2026, 1, 1, 12, 0, 0)
    memento = CalculatorMemento(history=[calc_instance], timestamp=ts)

    result = memento.to_dict()

    assert result["history"] == [{"operation": "Addition"}]
    assert result["timestamp"] == ts.isoformat()
    calc_instance.to_dict.assert_called_once()


@patch("app.calculator_memento.Calculation.from_dict")
def test_memento_from_dict_uses_calculation_from_dict(mock_from_dict):
    """
    history=[Calculation.from_dict(calc) for calc in data['history']]
    """
    ts = datetime.datetime(2026, 1, 1, 12, 0, 0)
    payload = {
        "history": [{"operation": "Addition"}],
        "timestamp": ts.isoformat()
    }

    calc_obj = Mock()
    mock_from_dict.return_value = calc_obj

    memento = CalculatorMemento.from_dict(payload)

    assert memento.history == [calc_obj]
    assert memento.timestamp == ts
    mock_from_dict.assert_called_once_with({"operation": "Addition"})