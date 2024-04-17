from typing import Any, Dict, Iterator, Union

from langchain_core.document_loaders import Blob
from langchain_core.documents import Document

from ..settings import Settings
from langchain.document_loaders.base import BaseBlobParser


class HTMLParser(BaseBlobParser):
    def __init__(
            self,
            settings: Settings,
            *,
            features: str = "lxml",
            get_text_separator: str = "",
            **kwargs: Any
    ) -> None:
        """Initialize a bs4 based HTML parser."""
        try:
            import bs4  # noqa:F401
        except ImportError:
            raise ImportError(
                "beautifulsoup4 package not found, please install it with "
                "`pip install beautifulsoup4`"
            )

        self.settings = settings
        self.bs_kwargs = {"features": features, **kwargs}
        self.get_text_separator = get_text_separator

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """Load HTML document into document objects."""
        from bs4 import BeautifulSoup

        with blob.as_bytes_io() as f:
            soup = BeautifulSoup(f, **self.bs_kwargs)

        skip_selectors = self.settings["skip_selectors"].split(" ")

        # find by css selector and remove
        for tag in skip_selectors:
            for el in soup.select(tag):
                el.decompose()

        filtered_doc = ""
        relevant_selectors = self.settings["relevant_selectors"].split(" ")
        for tag in relevant_selectors:
            tags = soup.select(tag)
            for el in tags:
                filtered_doc += el.text + "\n"

        if filtered_doc:
            text = filtered_doc
        else:
            text = soup.get_text(self.get_text_separator)

        if soup.title:
            title = str(soup.title.string)
        else:
            title = ""

        metadata: Dict[str, Union[str, None]] = {
            "source": blob.source,
            "title": title,
        }

        yield Document(page_content=text, metadata=metadata)
