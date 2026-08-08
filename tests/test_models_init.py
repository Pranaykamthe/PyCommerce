"""
test_models_init.py
-------------------
Tests the models package exports.
"""

from models import (
    User,
    Category,
    Product,
    Cart,
    Order,
    OrderItem,
    Payment,
    Review,
)


def test_models_package_imports():
    """Test that all models can be imported from the package."""

    assert User is not None
    assert Category is not None
    assert Product is not None
    assert Cart is not None
    assert Order is not None
    assert OrderItem is not None
    assert Payment is not None
    assert Review is not None