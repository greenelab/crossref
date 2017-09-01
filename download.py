import argparse
import logging

import pymongo

from utilities import query_all


def get_mongo_collection(db, component):
    """
    Return the collection for the specified component.
    """
    collection = db[args.component]
    if component == 'works':
        collection.create_index('DOI', unique=True)
    elif component == 'types':
        collection.create_index('id', unique=True)
    else:
        msg = f'{component} component not supported by get_mongo_collection'
        raise SystemExit(msg)
    return collection


def generator_to_mongo(generator, collection):
    """
    Insert items from a generator into MongoDB
    """
    component = collection.name
    msg = f'Initiating queries with {collection.count():,} {component} in db.'
    logging.info(msg)
    print(msg)

    # Add works
    if component == 'works':
        for work in generator:
            filter_ = {'DOI': work['DOI']}
            collection.replace_one(filter_, work, upsert=True)

    # Add types
    elif component == 'types':
        for type_ in generator:
            filter_ = {'id': type_['id']}
            collection.replace_one(filter_, type_, upsert=True)

    # Component not supported
    else:
        msg = f'{component} component not supported by generator_to_mongo'
        raise SystemExit(msg)

    msg = f'Finished queries with {collection.count():,} {component} in db.'
    logging.info(msg)
    print(msg)


if __name__ == '__main__':
    # Parse arguments
    desc = ('Download all items of the specified type from '
            'the Crossref API and store them in MongoDB.')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--component', required=True,
                        help='Which Crossref API endpoint to retrieve. '
                        'See https://git.io/vyp7S.')
    parser.add_argument('--batch-size', type=int, default=450,
                        help='Specify a query batch size.')
    parser.add_argument('--cursor', default=None,
                        help='Specify a cursor. Useful when starting up '
                        'querying from a previous position.')
    parser.add_argument('--log', help='Path to write log to.')
    parser.add_argument('--mongo', default='localhost:27017',
                        help='MongoDB host URI.')
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s\n%(message)s',
        filename=args.log,
        level=logging.INFO,
    )

    # Only works are supported for now
    if args.component not in {'works', 'types'}:
        raise SystemExit(f'{args.component} component is not supported.')

    # Connect to mongo
    client = pymongo.MongoClient(args.mongo)
    db = client.crossref
    collection = get_mongo_collection(db, args.component)

    # Perform queries
    generator = query_all(
        component=args.component,
        batch_size=args.batch_size,
        cursor=args.cursor,
    )
    generator_to_mongo(generator, collection)

    # Shutdown
    client.close()
