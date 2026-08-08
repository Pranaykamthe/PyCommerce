"""
test_review_model.py
--------------------
Tests for the Review model.
"""

from models.review import Review


def test_create_review():
    """Test creating a review."""

    review = Review(
        review_id=1,
        user_id=10,
        product_id=101,
        rating=5,
        comment="Excellent product!",
    )

    assert review.review_id == 1
    assert review.user_id == 10
    assert review.product_id == 101
    assert review.rating == 5
    assert review.comment == "Excellent product!"


def test_review_default_values():
    """Test review default values."""

    review = Review()

    assert review.review_id is None
    assert review.user_id is None
    assert review.product_id is None
    assert review.rating == 0
    assert review.comment == ""
    assert review.created_at is None
    assert review.updated_at is None


def test_review_string():
    """Test Review string representation."""

    review = Review(
        review_id=1,
        user_id=10,
        product_id=101,
        rating=5,
    )

    result = str(review)

    assert "1" in result
    assert "10" in result
    assert "101" in result
    assert "5" in result