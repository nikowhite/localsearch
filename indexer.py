import os
import sqlite3
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from utils import tokenize, normalize

class Indexer:
    def __init__(self, db_path='data/index.sqlite'):
        self.db_path = db_path
        self.conn = None
        self._ensure_db()

    def _ensure_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS inverted_index (term TEXT, doc_id INTEGER, freq INTEGER)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS doc_freq (term TEXT PRIMARY KEY, df INTEGER)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS doc_lengths (doc_id INTEGER PRIMARY KEY, length INTEGER)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS documents (doc_id INTEGER PRIMARY KEY, path TEXT)''')
        self.conn.commit()

    def _process_file(self, args):
        doc_id, path = args
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        tokens = [normalize(token) for token in tokenize(text)]
        term_counts = Counter(tokens)
        return doc_id, path, len(tokens), term_counts

    def index_directory(self, directory):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM inverted_index')
        cur.execute('DELETE FROM doc_freq')
        cur.execute('DELETE FROM doc_lengths')
        cur.execute('DELETE FROM documents')
        doc_paths = []
        doc_id = 0
        for root, _, files in os.walk(directory):
            for fname in files:
                if fname.lower().endswith('.txt'):
                    path = os.path.join(root, fname)
                    doc_paths.append((doc_id, path))
                    doc_id += 1

        doc_freq = defaultdict(int)
        results = []
        with ThreadPoolExecutor() as executor:
            for result in executor.map(self._process_file, doc_paths):
                results.append(result)

        for doc_id, path, length, term_counts in results:
            cur.execute('INSERT INTO documents (doc_id, path) VALUES (?, ?)', (doc_id, path))
            cur.execute('INSERT INTO doc_lengths (doc_id, length) VALUES (?, ?)', (doc_id, length))
            for term, freq in term_counts.items():
                cur.execute('INSERT INTO inverted_index (term, doc_id, freq) VALUES (?, ?, ?)', (term, doc_id, freq))
                doc_freq[term] += 1

        for term, df in doc_freq.items():
            cur.execute('INSERT INTO doc_freq (term, df) VALUES (?, ?)', (term, df))
        self.conn.commit()

    def get_inverted_index(self, term):
        cur = self.conn.cursor()
        cur.execute('SELECT doc_id, freq FROM inverted_index WHERE term=?', (term,))
        return cur.fetchall()

    def get_doc_freq(self, term):
        cur = self.conn.cursor()
        cur.execute('SELECT df FROM doc_freq WHERE term=?', (term,))
        row = cur.fetchone()
        return row[0] if row else 0

    def get_doc_length(self, doc_id):
        cur = self.conn.cursor()
        cur.execute('SELECT length FROM doc_lengths WHERE doc_id=?', (doc_id,))
        row = cur.fetchone()
        return row[0] if row else 0

    def get_documents(self):
        cur = self.conn.cursor()
        cur.execute('SELECT doc_id, path FROM documents')
        return dict(cur.fetchall())

    def get_num_docs(self):
        cur = self.conn.cursor()
        cur.execute('SELECT COUNT(*) FROM documents')
        return cur.fetchone()[0]

# Example usage:
# indexer = Indexer()
# indexer.index_directory('data/docs')
# print(indexer.get_inverted_index('example'))