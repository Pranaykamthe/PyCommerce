from models.wishlist import Wishlist


def test_create_wishlist():
    wishlist = Wishlist(
        wishlist_id=1,
        user_id=10,
        product_id=20
    )

    assert wishlist.wishlist_id == 1
    assert wishlist.user_id == 10
    assert wishlist.product_id == 20


def test_wishlist_default_values():
    wishlist = Wishlist()

    assert wishlist.wishlist_id is None
    assert wishlist.user_id is None
    assert wishlist.product_id is None
    assert wishlist.added_at is None


def test_wishlist_string():
    wishlist = Wishlist(
        wishlist_id=1,
        user_id=10,
        product_id=20
    )

    result = str(wishlist)

    assert "Wishlist" in result
    assert "id=1" in result
    assert "user_id=10" in result
    assert "product_id=20" in result