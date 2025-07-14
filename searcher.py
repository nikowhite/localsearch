import math
from utils import tokenize, normalize

class Searcher:
    def __init__(self, indexer):
        self.indexer = indexer # Indexer instance
        
    def bm25(self, term, doc_id, k1=1.5, b=0.75):
        postings = dict(self.indexer.inverted_index.get(term, []))
        tf = postings.get(doc_id, 0)
        if tf == 0:
            return 0.0
        df = self.indexer.doc_freq.get(term, 1)
        N = len(self.indexer.documents)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        dl = self.indexer.doc_lengths.get(doc_id, 1)
        avgdl = sum(self.indexer.doc_lengths.values()) / max(len(self.indexer.doc_lengths), 1)
        score = idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))
        return score

    def tf_idf(self, term, doc_id):
        postings = dict(self.indexer.inverted_index.get(term, []))
        tf = postings.get(doc_id, 0)
        if tf == 0:
            return 0.0
        df = self.indexer.doc_freq.get(term, 1)
        N = len(self.indexer.documents)
        idf = math.log((N + 1) / (df + 1)) + 1
        return tf * idf

    def parse_query(self, query):
        """
        Parses the query string into tokens, handling AND, OR, NOT operators.
        Converts terms to their normalized form.
        """
        tokens = []
        for token in query.strip().split():
            t = token.upper()
            if t in {"AND", "OR", "NOT"}:
                tokens.append(t)
            else:
                tokens.append(normalize(token))
        return tokens

    def eval_query(self, tokens):
        """
        Evaluates the query tokens and returns a set of document IDs that match the query.
        Supports AND, OR, NOT operations.
        """
        result = set()
        op = None
        not_mode = False

        def docs_for_term(term):
            return set(doc_id for doc_id, _ in self.indexer.inverted_index.get(term, []))

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == "NOT":
                not_mode = True
                i += 1
                continue
            elif token in {"AND", "OR"}:
                op = token
                i += 1
                continue
            else:
                docs = docs_for_term(token)
                if not_mode:
                    docs = set(self.indexer.documents.keys()) - docs
                    not_mode = False
                if not result:
                    result = docs
                else:
                    if op == "AND":
                        result = result & docs
                    elif op == "OR":
                        result = result | docs
                    else:
                        result = docs  # если нет оператора, просто заменяем
                op = None
            i += 1
        return result

    def search(self, query, top_k=10, use_bm25=True):
        """
        Searches for documents matching the query.
        If use_bm25 is True, uses BM25 scoring; otherwise uses TF-IDF
        """
        tokens = self.parse_query(query)
        doc_ids = self.eval_query(tokens)
        scores = {}
        for doc_id in doc_ids:
            score = 0.0
            for token in tokens:
                if token in {"AND", "OR", "NOT"}:
                    continue
                if use_bm25:
                    score += self.bm25(token, doc_id)
                else:
                    score += self.tf_idf(token, doc_id)
            if score > 0:
                scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:top_k]:
            results.append({
                'doc_id': doc_id,
                'path': self.indexer.documents[doc_id],
                'score': score
            })
        return results

    def tf_idf(self, term, doc_id):
        """
        Оставлено для обратной совместимости и тестов.
        """
        postings = dict(self.indexer.inverted_index.get(term, []))
        tf = postings.get(doc_id, 0)
        if tf == 0:
            return 0.0
        df = self.indexer.doc_freq.get(term, 1)
        N = len(self.indexer.documents)
        idf = math.log((N + 1) / (df + 1)) + 1
        return tf * idf

# Example usage:
# from indexer import Indexer
# indexer = Indexer()
# indexer.load('data/index.json')
# searcher = Searcher(indexer)
# results = searcher.search("example query", use_bm25=True)
# for r in results:
#     print(f"Document: {r['path']}, Score: {r['score']}")