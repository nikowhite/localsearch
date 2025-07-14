import argparse
from indexer import Indexer
from searcher import Searcher

def main():
    parser = argparse.ArgumentParser(description="Простой поисковый движок по локальным текстовым файлам.")
    parser.add_argument('query', nargs='*', help='Строка поискового запроса')
    parser.add_argument('--index', default='data/index.json', help='Путь к файлу индекса')
    parser.add_argument('--reindex', action='store_true', help='Переиндексировать папку документов')
    parser.add_argument('--docs', default='data/docs', help='Папка с документами для индексации')
    parser.add_argument('--top', type=int, default=10, help='Сколько результатов выводить')
    args = parser.parse_args()

    indexer = Indexer()

    if args.reindex:
        print(f'Indexing directory: {args.docs} ...')
        indexer.index_directory(args.docs)
        indexer.save(args.index)
        print(f'Index saved to {args.index}')
    else:
        indexer.load(args.index)

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