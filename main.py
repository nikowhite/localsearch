import argparse
from indexer import Indexer
from searcher import Searcher

def main():
    parser = argparse.ArgumentParser(description="Simple search engine for local text files.")
    parser.add_argument('query', nargs='*', help='Search query string')
    parser.add_argument('--reindex', action='store_true', help='Reindex the documents folder')
    parser.add_argument('--docs', default='data/docs', help='Folder with documents to index')
    parser.add_argument('--top', type=int, default=10, help='How many results to show')
    args = parser.parse_args()

    indexer = Indexer()

    if args.reindex:
        print(f'Indexing directory: {args.docs} ...')
        indexer.index_directory(args.docs)
        print('Indexing complete.')
    # No need to load or save, SQLite is used automatically

    if args.query:
        query = ' '.join(args.query)
        searcher = Searcher(indexer)
        results = searcher.search(query, top_k=args.top)
        if not results:
            print('No results found.')
        else:
            print('Search results:')
            for i, res in enumerate(results, 1):
                print(f"{i}. {res['path']} (score: {res['score']:.3f})")
    else:
        print('Enter search query. Example:')
        print('  python main.py "example query"')

if __name__ == '__main__':
    main()