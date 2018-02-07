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

### works

With mongo running, execute with the following commands:

```sh
# Download all works
# To start fresh, use `--cursor=*`
# If querying fails midway, you can extract the cursor of the
# last successful query from the tail of query-works.log.
# Then rerun download.py, passing the intermediate cursor
# to --cursor instead of *.
python download.py \
  --component=works \
  --batch-size=550 \
  --log=logs/query-works.log \
  --cursor=*

# Export mongodb works collection to JSON
mongoexport \
  --db=crossref \
  --collection=works \
  | xz > data/mongo-export/crossref-works.json.xz
```

See [`data/mongo-export`](data/mongo-export) for more information on `crossref-works.json.xz`.
Note that creating this file from the Crossref API takes several weeks.
Users are encouraged to use the cached version available on [figshare](https://doi.org/10.6084/m9.figshare.4816720) (see also [Other resources](#other-resources) below).

[`1.works-to-dataframe.ipynb`](1.works-to-dataframe.ipynb) is a Jupyter notebook that extracts tabular datasets of works (TSVs), which are tracked using Git LFS:

+ [`doi.tsv.xz`](data/doi.tsv.xz): a table where each row is a work, with columns for the DOI, type, and issued date.
+ [`doi-to-issn.tsv.xz`](data/doi-to-issn.tsv.xz): a table where each row is a work (DOI) to journal (ISSN) mapping.

### types

With mongo running, execute with the following command:

```sh
python download.py \
  --component=types \
  --log=logs/query-types.log
```

## Environment

This repository uses [conda](http://conda.pydata.org/docs/) to manage its environment as specified in [`environment.yml`](environment.yml).
Install the environment with:

```sh
conda env create --file=environment.yml
```

Then use `source activate crossref` and `source deactivate` to activate or deactivate the environment. On windows, use `activate crossref` and `deactivate` instead.

## Other resources

Ideally, Crossref would provide a complete database dump, rather than requiring users to go through the inefficient process of API querying all works: see [CrossRef/rest-api-doc#271](https://github.com/CrossRef/rest-api-doc/issues/271).
Until then, users should checkout the Crossref data currently hosted by this repository, whose query date is 2017-03-21, and its corresponding [figshare](https://doi.org/10.6084/m9.figshare.4816720.v1).
For users who need more recent data, Bryan Newbold [used this codebase](https://github.com/greenelab/crossref/issues/5) to create a MongoDB dump dated January 2018 (query date of approximately 2018-01-10), which he uploaded to the [Internet Archive](https://archive.org/download/crossref_doi_dump_201801).
His output file `crossref-works.2018-01-21.json.xz` contains 93,585,242 DOIs and consumes 28.9 GB compared to 87,542,370 DOIs and 7.0 GB for the `crossref-works.json.xz` dated 2017-03-21.
This increased size is presumably due to the addition of [I4OC](https://i4oc.org/ "Initiative for Open Citations") references to Crossref work records.
This repository is currently seeking contributions to update the convenient TSV outputs based on the January 2018 database dump.

Daniel Ecer also downloaded the Crossref work metadata in January 2018, using the codebase at [elifesciences/datacapsule-crossref](https://github.com/elifesciences/datacapsule-crossref).
His database dump is available on [figshare](https://doi.org/10.6084/m9.figshare.5845554.v2 "Crossref Works Dump - January 2018").
While the multi-part format of this dump is likely less convenient than the dumps produced by this repository, Daniel Ecer's analysis also exports a DOI-to-DOI table of citations/references [available here](https://doi.org/10.6084/m9.figshare.5849916.v1 "Crossref Citation Links - January 2018").
This citation catalog contains 314,785,303 citations ([summarized here](https://elifesci.org/crossref-data-notebook)) and is thus more comprehensive than the catalog available from [greenelab/opencitations](https://github.com/greenelab/opencitations).

## Acknowledgements

This work is funded in part by the Gordon and Betty Moore Foundation's Data-Driven Discovery Initiative through Grant [GBMF4552](https://www.moore.org/grant-detail?grantId=GBMF4552) to [**@cgreene**](https://github.com/cgreene "Casey Greene on GitHub").
