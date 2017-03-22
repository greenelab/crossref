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
  --detach \
  --rm \
  mongo:3.4.2
```

## Environment

This repository uses [conda](http://conda.pydata.org/docs/) to manage its environment as specified in [`environment.yml`](environment.yml).
Install the environment with:

```sh
conda env create --file=environment.yml
```

Then use `source activate crossref` and `source deactivate` to activate or deactivate the environment. On windows, use `activate crossref` and `deactivate` instead.
