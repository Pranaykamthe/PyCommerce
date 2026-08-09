"""
Product-related user interface for PyCommerce.
"""

from typing import Optional

from models.product import Product
from services.product_service import ProductService
from services.cart_service import CartService

from utils.console import console
from utils.messages import success, error


# ============================================================
# Display Products
# ============================================================

def display_products(
    products: list[Product]
) -> None:
    """Display a list of products."""

    console.print(
        "\n[bold cyan]=== Products ===[/bold cyan]\n"
    )

    if not products:
        console.print(
            "[yellow]No products available.[/yellow]"
        )
        return

    console.print(
        "[bold]"
        "ID     Product                       Price       Stock"
        "[/bold]"
    )

    console.print("-" * 65)

    for product in products:
        console.print(
            f"{str(product.product_id):<6}"
            f"{product.name[:28]:<30}"
            f"₹{product.price:>9.2f}   "
            f"{product.stock:>5}"
        )


# ============================================================
# Browse Products
# ============================================================

def browse_products() -> None:
    """Display all available products."""

    try:
        products = ProductService.get_all_products()

        display_products(products)

    except Exception as exc:
        error(
            f"Unable to load products: {exc}"
        )


# ============================================================
# Product Details
# ============================================================

def show_product_details(
    product_id: int
) -> Optional[Product]:
    """Display details for a specific product."""

    try:
        product = ProductService.get_product(
            product_id
        )

        if product is None:
            error(
                "Product not found."
            )
            return None

        console.print(
            "\n[bold cyan]=== Product Details ===[/bold cyan]\n"
        )

        console.print(
            f"[bold]ID:[/bold] "
            f"{product.product_id}"
        )

        console.print(
            f"[bold]Name:[/bold] "
            f"{product.name}"
        )

        console.print(
            f"[bold]Description:[/bold] "
            f"{product.description or 'N/A'}"
        )

        console.print(
            f"[bold]Price:[/bold] "
            f"₹{product.price:.2f}"
        )

        console.print(
            f"[bold]Stock:[/bold] "
            f"{product.stock}"
        )

        console.print(
            f"[bold]Image:[/bold] "
            f"{product.image_url or 'N/A'}"
        )

        return product

    except ValueError as exc:
        error(str(exc))
        return None

    except Exception as exc:
        error(
            f"Unable to load product: {exc}"
        )
        return None


# ============================================================
# Search Product
# ============================================================

def search_products() -> None:
    """Search products by name."""

    console.print(
        "\n[bold cyan]=== Search Products ===[/bold cyan]\n"
    )

    search_term = input(
        "Enter product name: "
    ).strip()

    if not search_term:
        error(
            "Search term cannot be empty."
        )
        return

    try:
        products = ProductService.search_products(
            search_term
        )

        display_products(products)

    except Exception as exc:
        error(
            f"Search failed: {exc}"
        )


# ============================================================
# Add Product To Cart
# ============================================================

def add_product_to_cart(
    user_id: int
) -> bool:
    """Add a product to the customer's cart."""

    console.print(
        "\n[bold cyan]=== Add Product To Cart ===[/bold cyan]\n"
    )

    try:
        product_id = int(
            input(
                "Enter product ID: "
            ).strip()
        )

        product = ProductService.get_product(
            product_id
        )

        if product is None:
            error(
                "Product not found."
            )
            return False

        console.print(
            f"\n[bold]Product:[/bold] "
            f"{product.name}"
        )

        console.print(
            f"[bold]Price:[/bold] "
            f"₹{product.price:.2f}"
        )

        console.print(
            f"[bold]Available Stock:[/bold] "
            f"{product.stock}"
        )

        quantity = int(
            input(
                "Enter quantity: "
            ).strip()
        )

        result = CartService.add_to_cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )

        if result:
            success(
                "Product added to cart successfully."
            )
            return True

        error(
            "Product could not be added to cart."
        )

        return False

    except ValueError as exc:
        error(str(exc))
        return False

    except Exception as exc:
        error(
            f"Unable to add product to cart: {exc}"
        )
        return False


# ============================================================
# Product Menu
# ============================================================

def product_menu(
    user_id: Optional[int] = None
) -> None:
    """Display the customer product menu."""

    while True:

        console.print(
            "\n[bold cyan]=== Product Menu ===[/bold cyan]"
        )

        console.print(
            "1. Browse Products"
        )

        console.print(
            "2. Search Products"
        )

        console.print(
            "3. View Product Details"
        )

        console.print(
            "4. Add Product to Cart"
        )

        console.print(
            "5. Back"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            browse_products()

        elif choice == "2":

            search_products()

        elif choice == "3":

            product_id_text = input(
                "Enter product ID: "
            ).strip()

            try:
                product_id = int(
                    product_id_text
                )

                show_product_details(
                    product_id
                )

            except ValueError:
                error(
                    "Product ID must be a number."
                )

        elif choice == "4":

            if user_id is None:

                error(
                    "Customer information is required "
                    "to add products to cart."
                )

            else:

                add_product_to_cart(
                    user_id
                )

        elif choice == "5":

            break

        else:

            error(
                "Invalid choice."
            )


# ============================================================
# Admin Product Creation
# ============================================================

def create_product_ui() -> Optional[Product]:
    """Create a product through the console UI."""

    console.print(
        "\n[bold cyan]=== Add Product ===[/bold cyan]\n"
    )

    try:
        category_id = int(
            input(
                "Category ID: "
            ).strip()
        )

        name = input(
            "Product name: "
        ).strip()

        description = input(
            "Description: "
        ).strip()

        price = float(
            input(
                "Price: "
            ).strip()
        )

        stock = int(
            input(
                "Stock quantity: "
            ).strip()
        )

        image_url = input(
            "Image path: "
        ).strip()

        product = Product(
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            stock=stock,
            image_url=image_url
        )

        created_product = (
            ProductService.create_product(
                product
            )
        )

        if created_product is None:

            error(
                "Product could not be created."
            )

            return None

        success(
            "Product created successfully."
        )

        return created_product

    except ValueError as exc:

        error(str(exc))
        return None

    except Exception as exc:

        error(
            f"Unable to create product: {exc}"
        )

        return None


# ============================================================
# Admin Update Product
# ============================================================

def update_product_ui() -> bool:
    """Update an existing product."""

    console.print(
        "\n[bold cyan]=== Update Product ===[/bold cyan]\n"
    )

    try:
        product_id = int(
            input(
                "Product ID: "
            ).strip()
        )

        product = ProductService.get_product(
            product_id
        )

        if product is None:

            error(
                "Product not found."
            )

            return False

        console.print(
            f"Current name: {product.name}"
        )

        name = input(
            "New name "
            "(press Enter to keep current): "
        ).strip()

        console.print(
            f"Current price: ₹{product.price:.2f}"
        )

        price_text = input(
            "New price "
            "(press Enter to keep current): "
        ).strip()

        console.print(
            f"Current stock: {product.stock}"
        )

        stock_text = input(
            "New stock "
            "(press Enter to keep current): "
        ).strip()

        if name:
            product.name = name

        if price_text:
            product.price = float(
                price_text
            )

        if stock_text:
            product.stock = int(
                stock_text
            )

        result = ProductService.update_product(
            product
        )

        if result:

            success(
                "Product updated successfully."
            )

            return True

        error(
            "Product could not be updated."
        )

        return False

    except ValueError as exc:

        error(str(exc))
        return False

    except Exception as exc:

        error(
            f"Unable to update product: {exc}"
        )

        return False


# ============================================================
# Admin Delete Product
# ============================================================

def delete_product_ui() -> bool:
    """Delete a product."""

    console.print(
        "\n[bold cyan]=== Delete Product ===[/bold cyan]\n"
    )

    try:
        product_id = int(
            input(
                "Product ID: "
            ).strip()
        )

        product = ProductService.get_product(
            product_id
        )

        if product is None:

            error(
                "Product not found."
            )

            return False

        console.print(
            f"Product: {product.name}"
        )

        confirmation = input(
            "Delete this product? (y/n): "
        ).strip().lower()

        if confirmation != "y":

            console.print(
                "[yellow]Deletion cancelled.[/yellow]"
            )

            return False

        result = ProductService.delete_product(
            product_id
        )

        if result:

            success(
                "Product deleted successfully."
            )

            return True

        error(
            "Product could not be deleted."
        )

        return False

    except ValueError as exc:

        error(str(exc))
        return False

    except Exception as exc:

        error(
            f"Unable to delete product: {exc}"
        )

        return False


# ============================================================
# Admin Product Menu
# ============================================================

def product_admin_menu() -> None:
    """Display product management menu for admins."""

    while True:

        console.print(
            "\n[bold cyan]=== Product Management ===[/bold cyan]"
        )

        console.print(
            "1. View Products"
        )

        console.print(
            "2. Add Product"
        )

        console.print(
            "3. Update Product"
        )

        console.print(
            "4. Delete Product"
        )

        console.print(
            "0. Back"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            browse_products()

        elif choice == "2":

            create_product_ui()

        elif choice == "3":

            update_product_ui()

        elif choice == "4":

            delete_product_ui()

        elif choice == "0":

            break

        else:

            error(
                "Invalid choice."
            )