# 🔍 LocalSearch — Lightweight Full-Text Search Engine in Python

**LocalSearch** is a modular, high-performance full-text search engine built with Python and SQLite. It supports advanced ranking (TF-IDF and BM25), boolean query operators, multithreaded indexing, and optional HTML/PDF parsing.

This project is designed to be easy to integrate into other applications or use standalone via CLI.

---

## 🚀 Features

- 📂 **Recursive indexing** of `.txt` files in any directory
- ⚙️ **TF-IDF** and **BM25** scoring models for document ranking
- 🔎 Boolean queries: `AND`, `OR`, `NOT`
- 💾 **SQLite-backed index** for persistent storage
- 🧵 Multithreaded indexing for speed
- 📄 Optional **PDF and HTML** support
- 🧪 Built-in unit tests using `pytest`
- 💻 Command-line interface for reindexing and searching

---

## 📦 Installation

```bash
git clone https://github.com/your-username/localsearch
cd localsearch
pip install -r requirements.txt
```

### Optional dependencies

- For PDF support: `PyPDF2`
- For HTML support: `beautifulsoup4`
- For stemming: `nltk` (with SnowballStemmer)

---

## 🏗️ Project Structure

```
search_engine/
├── main.py            # CLI interface
├── indexer.py         # Document reading and indexing (SQLite-based)
├── searcher.py        # Search algorithms (TF-IDF, BM25, Boolean logic)
├── utils.py           # Parsers, normalization, tokenization, stemming
├── tests/
│   └── test_index.py  # Unit tests
├── data/
│   └── docs/          # Example documents
│   └── index.sqlite   # SQLite index (auto-created)
├── requirements.txt   # Dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Index your documents

```bash
python main.py --reindex --docs data/docs
```

### 2. Search for documents

```bash
python main.py "your search query"
```

### 3. Boolean queries

```bash
python main.py "python AND search NOT java"
python main.py "deep OR learning"
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🛠️ Configuration

- By default, the index is stored in `data/index.sqlite`.
- You can change the documents folder or index path via CLI arguments.

---

## 📝 Example Usage

```bash
python main.py --reindex --docs data/docs
python main.py "machine learning"
python main.py "python AND search"
```

---

## 📄 Requirements

See `requirements.txt` for all dependencies.

---

## 📚 License

MIT License

---

## 🤝 Contributing

Pull requests and issues are welcome!

---

## ✨ Credits

- [NLTK](https://www.nltk.org/) for stemming
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF parsing
