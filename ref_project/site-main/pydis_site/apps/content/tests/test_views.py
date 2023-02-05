import textwrap
from pathlib import Path
from unittest import TestCase

import django.test
import markdown
from django.http import Http404
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.urls import reverse

from pydis_site.apps.content.models import Commit, Tag
from pydis_site.apps.content.tests.helpers import (
    BASE_PATH, MockPagesTestCase, PARSED_CATEGORY_INFO, PARSED_HTML, PARSED_METADATA
)
from pydis_site.apps.content.tests.test_utils import TEST_COMMIT_KWARGS
from pydis_site.apps.content.views import PageOrCategoryView


def patch_dispatch_attributes(view: PageOrCategoryView, location: str) -> None:
    """
    Set the attributes set in the `dispatch` method manually.

    This is necessary because it is never automatically called during tests.
    """
    view.location = Path(BASE_PATH, location)

    # URL location on the filesystem
    view.full_location = view.location

    # Possible places to find page content information
    view.category_path = view.full_location
    view.page_path = view.full_location.with_suffix(".md")


@override_settings(CONTENT_PAGES_PATH=BASE_PATH)
class PageOrCategoryViewTests(MockPagesTestCase, SimpleTestCase, TestCase):
    """Tests for the PageOrCategoryView class."""

    def setUp(self):
        """Set test helpers, then set up fake filesystem."""
        self.factory = RequestFactory()
        self.view = PageOrCategoryView.as_view()
        self.ViewClass = PageOrCategoryView()
        super().setUp()

    # Integration tests
    def test_valid_page_or_category_returns_200(self):
        cases = [
            ("Page at root", "root"),
            ("Category page", "category"),
            ("Page in category", "category/with_metadata"),
            ("Subcategory page", "category/subcategory"),
            ("Page in subcategory", "category/subcategory/with_metadata"),
        ]
        for msg, path in cases:
            with self.subTest(msg=msg, path=path):
                request = self.factory.get(f"/{path}")
                response = self.view(request, location=path)
                self.assertEqual(response.status_code, 200)

    def test_nonexistent_page_returns_404(self):
        with self.assertRaises(Http404):
            request = self.factory.get("/invalid")
            self.view(request, location="invalid")

    # Unit tests
    def test_get_template_names_returns_correct_templates(self):
        category_template = "content/listing.html"
        page_template = "content/page.html"
        cases = [
            ("root", page_template),
            ("root_without_metadata", page_template),
            ("category/with_metadata", page_template),
            ("category/subcategory/with_metadata", page_template),
            ("category", category_template),
            ("category/subcategory", category_template),
        ]

        for path, expected_template in cases:
            with self.subTest(path=path, expected_template=expected_template):
                patch_dispatch_attributes(self.ViewClass, path)
                self.assertEqual(self.ViewClass.get_template_names(), [expected_template])

    def test_get_template_names_with_nonexistent_paths_returns_404(self):
        for path in ("invalid", "another_invalid", "nonexistent"):
            with self.subTest(path=path):
                patch_dispatch_attributes(self.ViewClass, path)
                with self.assertRaises(Http404):
                    self.ViewClass.get_template_names()

    def test_get_template_names_returns_page_template_for_category_with_page(self):
        """Make sure the proper page is returned for category locations with pages."""
        patch_dispatch_attributes(self.ViewClass, "tmp")
        self.assertEqual(self.ViewClass.get_template_names(), ["content/page.html"])

    def test_get_context_data_with_valid_page(self):
        """The method should return required fields in the template context."""
        request = self.factory.get("/root")
        self.ViewClass.setup(request)
        self.ViewClass.dispatch(request, location="root")

        cases = [
            ("Context includes HTML page content", "page", PARSED_HTML),
            ("Context includes page title", "page_title", PARSED_METADATA["title"]),
            (
                "Context includes page description",
                "page_description",
                PARSED_METADATA["description"]
            ),
            (
                "Context includes relevant link names and URLs",
                "relevant_links",
                PARSED_METADATA["relevant_links"]
            ),
        ]
        context = self.ViewClass.get_context_data()
        for msg, key, expected_value in cases:
            with self.subTest(msg=msg):
                self.assertEqual(context[key], expected_value)

    def test_get_context_data_with_valid_category(self):
        """The method should return required fields in the template context."""
        request = self.factory.get("/category")
        self.ViewClass.setup(request)
        self.ViewClass.dispatch(request, location="category")

        cases = [
            (
                "Context includes subcategory names and their information",
                "categories",
                {"subcategory": PARSED_CATEGORY_INFO}
            ),
            (
                "Context includes page names and their metadata",
                "pages",
                {"with_metadata": PARSED_METADATA}
            ),
            (
                "Context includes page description",
                "page_description",
                PARSED_CATEGORY_INFO["description"]
            ),
            ("Context includes page title", "page_title", PARSED_CATEGORY_INFO["title"]),
        ]

        context = self.ViewClass.get_context_data()
        for msg, key, expected_value in cases:
            with self.subTest(msg=msg):
                self.assertEqual(context[key], expected_value)

    def test_get_context_data_for_category_with_page(self):
        """Make sure the proper page is returned for category locations with pages."""
        request = self.factory.get("/category")
        self.ViewClass.setup(request)
        self.ViewClass.dispatch(request, location="tmp")

        context = self.ViewClass.get_context_data()
        expected_page_context = {
            "page": PARSED_HTML,
            "page_title": PARSED_METADATA["title"],
            "page_description": PARSED_METADATA["description"],
            "relevant_links": PARSED_METADATA["relevant_links"],
            "subarticles": [{"path": "category", "name": "Category Name"}]
        }
        for key, expected_value in expected_page_context.items():
            with self.subTest():
                self.assertEqual(context[key], expected_value)

    def test_get_context_data_breadcrumbs(self):
        """The method should return correct breadcrumbs."""
        request = self.factory.get("/category/subcategory/with_metadata")
        self.ViewClass.setup(request)
        self.ViewClass.dispatch(request, location="category/subcategory/with_metadata")

        context = self.ViewClass.get_context_data()

        # Convert to paths to avoid dealing with non-standard path separators
        for item in context["breadcrumb_items"]:
            item["path"] = Path(item["path"])

        self.assertEqual(
            context["breadcrumb_items"],
            [
                {"name": PARSED_CATEGORY_INFO["title"], "path": Path(".")},
                {"name": PARSED_CATEGORY_INFO["title"], "path": Path("category")},
                {"name": PARSED_CATEGORY_INFO["title"], "path": Path("category/subcategory")},
            ]
        )


class TagViewTests(django.test.TestCase):
    """Tests for the TagView class."""

    def setUp(self):
        """Set test helpers, then set up fake filesystem."""
        super().setUp()
        self.commit = Commit.objects.create(**TEST_COMMIT_KWARGS)

    def test_routing(self):
        """Test that the correct template is returned for each route."""
        Tag.objects.create(name="example", last_commit=self.commit)
        Tag.objects.create(name="grouped-tag", group="group-name", last_commit=self.commit)

        cases = [
            ("/pages/tags/example/", "content/tag.html"),
            ("/pages/tags/group-name/", "content/listing.html"),
            ("/pages/tags/group-name/grouped-tag/", "content/tag.html"),
        ]

        for url, template in cases:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(200, response.status_code)
                self.assertTemplateUsed(response, template)

    def test_valid_tag_returns_200(self):
        """Test that a page is returned for a valid tag."""
        Tag.objects.create(name="example", body="This is the tag body.", last_commit=self.commit)
        response = self.client.get("/pages/tags/example/")
        self.assertEqual(200, response.status_code)
        self.assertIn("This is the tag body", response.content.decode("utf-8"))
        self.assertTemplateUsed(response, "content/tag.html")

    def test_invalid_tag_404(self):
        """Test that a tag which doesn't exist raises a 404."""
        response = self.client.get("/pages/tags/non-existent/")
        self.assertEqual(404, response.status_code)

    def test_context_tag(self):
        """Test that the context contains the required data for a tag."""
        body = textwrap.dedent("""
        ---
        unused: frontmatter
        ----
        Tag content here.
        """)

        tag = Tag.objects.create(name="example", body=body, last_commit=self.commit)
        response = self.client.get("/pages/tags/example/")
        expected = {
            "page_title": "example",
            "page": markdown.markdown("Tag content here."),
            "tag": tag,
            "breadcrumb_items": [
                {"name": "Pages", "path": "."},
                {"name": "Tags", "path": "tags"},
            ]
        }
        for key in expected:
            self.assertEqual(
                expected[key], response.context.get(key), f"context.{key} did not match"
            )

    def test_context_grouped_tag(self):
        """
        Test the context for a tag in a group.

        The only difference between this and a regular tag are the breadcrumbs,
        so only those are checked.
        """
        Tag.objects.create(
            name="example", body="Body text", group="group-name", last_commit=self.commit
        )
        response = self.client.get("/pages/tags/group-name/example/")
        self.assertListEqual([
            {"name": "Pages", "path": "."},
            {"name": "Tags", "path": "tags"},
            {"name": "group-name", "path": "tags/group-name"},
        ], response.context.get("breadcrumb_items"))

    def test_group_page(self):
        """Test rendering of a group's root page."""
        Tag.objects.create(name="tag-1", body="Body 1", group="group-name", last_commit=self.commit)
        Tag.objects.create(name="tag-2", body="Body 2", group="group-name", last_commit=self.commit)
        Tag.objects.create(name="not-included", last_commit=self.commit)

        response = self.client.get("/pages/tags/group-name/")
        content = response.content.decode("utf-8")

        self.assertInHTML("<div class='level-left'>group-name</div>", content)
        self.assertInHTML(
            f"<a class='level-item fab fa-github' href='{Tag.URL_BASE}/group-name'>",
            content
        )
        self.assertIn(">tag-1</span>", content)
        self.assertIn(">tag-2</span>", content)
        self.assertNotIn(
            ">not-included</span>",
            content,
            "Tags not in this group shouldn't be rendered."
        )

        self.assertInHTML("<p>Body 1</p>", content)

    def test_markdown(self):
        """Test that markdown content is rendered properly."""
        body = textwrap.dedent("""
        ```py
        Hello world!
        ```

        **This text is in bold**
        """)

        Tag.objects.create(name="example", body=body, last_commit=self.commit)
        response = self.client.get("/pages/tags/example/")
        content = response.content.decode("utf-8")

        self.assertInHTML('<code class="language-py">Hello world!</code>', content)
        self.assertInHTML("<strong>This text is in bold</strong>", content)

    def test_embed(self):
        """Test that an embed from the frontmatter is treated correctly."""
        body = textwrap.dedent("""
        ---
        embed:
            title: Embed title
            image:
                url: https://google.com
        ---
        Tag body.
        """)

        Tag.objects.create(name="example", body=body, last_commit=self.commit)
        response = self.client.get("/pages/tags/example/")
        content = response.content.decode("utf-8")

        self.assertInHTML('<img alt="Embed title" src="https://google.com"/>', content)
        self.assertInHTML("<p>Tag body.</p>", content)

    def test_embed_title(self):
        """Test that the page title gets set to the embed title."""
        body = textwrap.dedent("""
        ---
        embed:
            title: Embed title
        ---
        """)

        Tag.objects.create(name="example", body=body, last_commit=self.commit)
        response = self.client.get("/pages/tags/example/")
        self.assertEqual(
            "Embed title",
            response.context.get("page_title"),
            "The page title must match the embed title."
        )

    def test_hyperlinked_item(self):
        """Test hyperlinking of tags works as intended."""
        filler_before, filler_after = "empty filler text\n\n", "more\nfiller"
        body = filler_before + "`!tags return`" + filler_after
        Tag.objects.create(name="example", body=body, last_commit=self.commit)

        other_url = reverse("content:tag", kwargs={"location": "return"})
        response = self.client.get("/pages/tags/example/")
        self.assertEqual(
            markdown.markdown(filler_before + f"[`!tags return`]({other_url})" + filler_after),
            response.context.get("page")
        )

    def test_hyperlinked_group(self):
        """Test hyperlinking with a group works as intended."""
        Tag.objects.create(
            name="example", body="!tags group-name grouped-tag", last_commit=self.commit
        )
        Tag.objects.create(name="grouped-tag", group="group-name")

        other_url = reverse("content:tag", kwargs={"location": "group-name/grouped-tag"})
        response = self.client.get("/pages/tags/example/")
        self.assertEqual(
            markdown.markdown(f"[!tags group-name grouped-tag]({other_url})"),
            response.context.get("page")
        )

    def test_hyperlinked_extra_text(self):
        """Test hyperlinking when a tag is followed by extra, unrelated text."""
        Tag.objects.create(
            name="example", body="!tags other unrelated text", last_commit=self.commit
        )
        Tag.objects.create(name="other")

        other_url = reverse("content:tag", kwargs={"location": "other"})
        response = self.client.get("/pages/tags/example/")
        self.assertEqual(
            markdown.markdown(f"[!tags other]({other_url}) unrelated text"),
            response.context.get("page")
        )

    def test_tag_root_page(self):
        """Test the root tag page which lists all tags."""
        Tag.objects.create(name="tag-1", last_commit=self.commit)
        Tag.objects.create(name="tag-2", last_commit=self.commit)
        Tag.objects.create(name="tag-3", last_commit=self.commit)

        response = self.client.get("/pages/tags/")
        content = response.content.decode("utf-8")

        self.assertTemplateUsed(response, "content/listing.html")
        self.assertInHTML('<div class="level-left">Tags</div>', content)

        for tag_number in range(1, 4):
            self.assertIn(f"tag-{tag_number}</span>", content)
