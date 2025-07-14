import os
import shutil
import tempfile
import pytest

from indexer import Indexer
from searcher import Searcher

@pytest.fixture
def temp_docs():
    temp_dir = tempfile.mkdtemp()
    doc1 = os.path.join(temp_dir, "doc1.txt")
    doc2 = os.path.join(temp_dir, "doc2.txt")
    with open(doc1, "w", encoding="utf-8") as f:
        f.write("hello world hello")
    with open(doc2, "w", encoding="utf-8") as f:
        f.write("world of search engines")
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_indexer_and_searcher(temp_docs):
    indexer = Indexer()
    indexer.index_directory(temp_docs)
    assert len(indexer.documents) == 2
    assert "hello" in indexer.inverted_index
    assert "world" in indexer.inverted_index

    # Testing doc_freq
    assert indexer.doc_freq["hello"] == 1
    assert indexer.doc_freq["world"] == 2

    # Testing search functionality
    searcher = Searcher(indexer)
    results = searcher.search("hello")
    assert len(results) == 1
    assert "hello" in indexer.inverted_index
    assert results[0]['score'] > 0

    results = searcher.search("world")
    assert len(results) == 2
    assert all(r['score'] > 0 for r in results)