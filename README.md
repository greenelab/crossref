# Store and process the Crossref Database

This repository downloads Crossref metadata using the [Crossref API](https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md).
The items retrieved are stored in MongoDB to preserve their raw structure.
This design allows for flexible downstream analyses.

## MongoDB

MongoDB is run via [Docker](https://hub.docker.com/_/mongo/).
It's available on the host machine at http://localhost:27017/.

```sh
docker run \
  --name=mongo-crossref \
  --publish=27017:27017 \
  --volume=`pwd`/mongo.db:/data/db \
  --rm \
  mongo:3.4.2
```

## Execution

With mongo running, execute with the following commands:

```sh
# Download all works
# To start fresh, use `--cursor=*`
python download.py \
  --component=works \
  --batch-size=550 \
  --log=query-works.log \
  --cursor=*

# Export mongodb works collection to JSON
mongoexport \
  --db=crossref \
  --collection=works \
  | xz > data/mongo-export/crossref-works.json.xz
```

## Environment

This repository uses [conda](http://conda.pydata.org/docs/) to manage its environment as specified in [`environment.yml`](environment.yml).
Install the environment with:

```sh
conda env create --file=environment.yml
```

Then use `source activate crossref` and `source deactivate` to activate or deactivate the environment. On windows, use `activate crossref` and `deactivate` instead.

## Acknowledgements

This work is funded in part by the Gordon and Betty Moore Foundation's Data-Driven Discovery Initiative through Grant [GBMF4552](https://www.moore.org/grant-detail?grantId=GBMF4552) to [**@cgreene**](https://github.com/cgreene "Casey Greene on GitHub").
