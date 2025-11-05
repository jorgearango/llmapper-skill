#!/usr/bin/env python3
"""
Generic article text extractor for any website.
Works with Wikipedia, news sites, blogs, and other article-based content.
"""

from html.parser import HTMLParser
import re
import sys

class GenericArticleExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_blocks = []
        self.current_text = []
        self.in_script = False
        self.in_style = False
        self.in_nav = False
        self.in_header = False
        self.in_footer = False
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'iframe', 'noscript'}

    def handle_starttag(self, tag, attrs):
        # Skip unwanted tags
        if tag in self.skip_tags:
            if tag == 'script':
                self.in_script = True
            elif tag == 'style':
                self.in_style = True
            elif tag == 'nav':
                self.in_nav = True
            elif tag == 'header':
                self.in_header = True
            elif tag == 'footer':
                self.in_footer = True

        # Check for navigation/skip areas via class names
        if tag in ['div', 'section', 'aside']:
            for attr, value in attrs:
                if attr == 'class' or attr == 'id':
                    lower_value = value.lower()
                    # Skip common navigation/UI element class names
                    if any(skip in lower_value for skip in [
                        'nav', 'menu', 'sidebar', 'header', 'footer',
                        'advertisement', 'ad-', 'banner', 'popup',
                        'social', 'share', 'comment', 'related'
                    ]):
                        self.in_nav = True
                        break

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
        elif tag == 'nav':
            self.in_nav = False
        elif tag == 'header':
            self.in_header = False
        elif tag == 'footer':
            self.in_footer = False

        # Treat block-level tags as paragraph breaks
        if tag in ['p', 'div', 'section', 'article', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
            if self.current_text:
                text = ' '.join(self.current_text).strip()
                if len(text) > 30:  # Only keep substantial text blocks
                    self.text_blocks.append(text)
                self.current_text = []

    def handle_data(self, data):
        # Skip if in unwanted sections
        if any([self.in_script, self.in_style, self.in_nav, self.in_header, self.in_footer]):
            return

        text = data.strip()
        if text and len(text) > 1:
            self.current_text.append(text)

    def get_article_text(self):
        """Return extracted article text, cleaned and concatenated."""
        # Join all blocks
        full_text = ' '.join(self.text_blocks)

        # Clean up whitespace
        full_text = re.sub(r'\s+', ' ', full_text).strip()

        return full_text

def extract_article_from_html(html_content, max_length=15000):
    """
    Extract main article content from HTML.

    Args:
        html_content: Raw HTML string
        max_length: Maximum character length to return

    Returns:
        Extracted article text
    """
    parser = GenericArticleExtractor()
    parser.feed(html_content)
    article_text = parser.get_article_text()

    # Limit length for LLM processing
    if len(article_text) > max_length:
        article_text = article_text[:max_length]

    return article_text

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: extract-article.py <html_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        html = f.read()

    text = extract_article_from_html(html)
    print(text)
