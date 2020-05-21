from django.test import Client, TestCase

from . import factories


class TestReviewModel(TestCase):
    def test_review_capitalization(self):
        self.review = factories.ReviewFactory(text="  lorem   IPSUM   DoLoR sit amet,,,,,,   CONSECTEUR adipiscing elit!!!!")
        self.assertEquals(
            self.review.formatted_text,
            "Lorem ipsum dolor sit amet, consecteur adipiscing elit!",
        )

    def test_punctuation_formatting(self):
        self.review = factories.ReviewFactory(text="раз , два")
        self.assertEquals(
            self.review.format_text(), "раз, два",
        )

    def test_punctuation_repeats(self):
        self.review = factories.ReviewFactory(text="раз ,,,,, два!!!!")
        self.assertEquals(
            self.review.format_text(), "раз, два!",
        )

    def test_punctuation_leading(self):
        self.review = factories.ReviewFactory(text=",раз , два")
        self.assertEquals(
            self.review.format_text(), ",раз, два",
        )

    def test_punctuation_one_dot(self):
        self.review = factories.ReviewFactory(text=".")
        self.assertEquals(
            self.review.format_text(), ".",
        )

    def test_punctuation_multiple_spaces(self):
        self.review = factories.ReviewFactory(text="раз    , два")
        self.assertEquals(
            self.review.format_text(), "раз, два",
        )
