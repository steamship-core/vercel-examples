"""Script to upload books to a vector index."""
import json
import re
from pathlib import Path
from typing import Optional, Set

import click
from langchain.document_loaders import PagedPDFSplitter
from steamship import Steamship
from steamship_langchain.vectorstores import SteamshipVectorStore

# Step 1: Give your index a name
INDEX_NAME = "test-123"

# Step 2: List the books or folders of books you want to add to your index
BOOKS_OR_BOOK_FOLDERS = [
    "uploads",
]


def index_book(
    book: Path, doc_index: SteamshipVectorStore, loaded_books: Optional[Set[str]] = None
):
    loaded_books = loaded_books or set()

    if book.name in loaded_books:
        if click.confirm(
            f'The book "{book.name}" is already indexed, do you want me to skip it?',
            default=True,
        ):
            return

    loader = PagedPDFSplitter(str(book.resolve()))
    pages = loader.load_and_split()

    doc_index.add_texts(
        texts=[re.sub("\u0000", "", page.page_content) for page in pages],
        metadatas=[{**page.metadata, "source": book.name} for page in pages],
    )


if __name__ == "__main__":
    client = Steamship(workspace=INDEX_NAME)

    doc_index = SteamshipVectorStore(
        client=client, index_name=INDEX_NAME, embedding="text-embedding-ada-002"
    )

    books = set(
        json.loads(item.metadata)["source"]
        for item in doc_index.index.index.list_items().items
    )

    if len(books) > 0:
        print(
            "The index already contains the following books: \n* " + "\n* ".join(books)
        )
        if click.confirm("Do you want to reset your index?", default=True):
            print("Resetting your index, this will take a while ⏳")
            doc_index.index.reset()

    for book in BOOKS_OR_BOOK_FOLDERS:
        book_path = Path(book)

        if book_path.is_dir():
            for folder in book_path.iterdir():
                index_book(book_path, doc_index, books)
        else:
            index_book(book_path, doc_index, books)
