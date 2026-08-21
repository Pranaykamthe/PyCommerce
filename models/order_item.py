"""
OrderItem model.

Represents a single product belonging to an order.
"""


class OrderItem:
    """Represents an item inside an order."""

    def __init__(
        self,
        order_item_id=None,
        order_id=None,
        product_id=None,
        quantity=1,
        price=0.0,
        subtotal=None
    ):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

        # Calculate automatically when subtotal is not supplied.
        if subtotal is None:
            self.subtotal = quantity * price
        else:
            self.subtotal = subtotal

    def __repr__(self):
        return (
            f"OrderItem("
            f"order_item_id={self.order_item_id}, "
            f"order_id={self.order_id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity}, "
            f"price={self.price}, "
            f"subtotal={self.subtotal}"
            f")"
        )