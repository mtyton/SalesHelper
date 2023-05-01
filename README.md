# `SalesHelper`
This tool main purpose is to simplify the process of matching candidate with job offer.
To simplify this process we've decided to use machine learning, currently only the process of extracting data from resume is based on machine learning.

## Architecture
We've decided to split our application to three separate subsystems, which are being called services.
Each of this service is self-dependent, and uses API/client layer to contact with other applications.
We've provided Dockerfile and docker-compose for each service, this allows to easily launch all of them.

### `data_service`
This service is responsible for collecting and managing learning data.
To collect data we've created `harvesters` module it is scrapy based application, which scrapes data from job offer boards.
After scraping web page, it simply yields:
``` json
{
    "title": "title",
    "skills": "skills", 
    "url": "htpps://jobnboard.com/12/",
    "description": "description",
    "platform": 1,
    "uuid": "random-uuid",
    "category": 1,
    "lang": "EN"
}
```
We currently download only those offers which support ENG/PL languages, this may be easily changed by modifying: `detect_description_language` in `data_services/tools.py`, this utility function allows detecting language of passed text, it uses `Spacy` library to achieve this.

After scraping and parsing data we save it to database, we've decided to use `MongoDB` here, because we don't need relations here, and storing data as documents will be easier and faster.
Main disadvantage of this decision was lack of enforced data structure, we've handled this by providing additional abstraction layer, which ensures same structure for all documents on code side.
To provide this we use two files:
 * `data_service/database/models.py`
 * `data_service/database/schemas.py`

Schemas file contains definitions of database entities, which are definitions of required structure, it also provides some basic methods for data parsing during read/write operations:
``` py
class DatabaseSchemaBase:

    def get_database_dict(self):
        ...

    @classmethod
    def from_db_instance(cls, **kwargs):
        ...


class UUIDHandleMixin:
    def get_database_dict(self):
        ...

    @classmethod
    def from_db_instance(cls, **kwargs):
        ...
```

Model file is providing simple interface which should be inherited for each schema separately, it allows executing read/write methods, using just an abstraction layer provided by this interface. Beneath you may observe hot find methods is being abstracted:
``` py
    def find(
        self, query: Dict[str, Any], find_one: bool = False,
        skip: int = None, limit: int = None
    ) -> Union[List[mongo_dataclass], mongo_dataclass]:
        if find_one:
            data = self.collection.find_one(query)
        else:
            data = self.collection.find(query)
        if skip is not None and not find_one:
            data = data.skip(skip)
        if limit is not None and not find_one:
            data = data.limit(limit)  
        # if nothing has been found, return None
        if data is None:
            return
        
        if isinstance(data, Iterable) and not isinstance(data, dict):
            return [self.mongo_dataclass.from_db_instance(**d) for d in data]
        return self.mongo_dataclass.from_db_instance(**data)
```

### `ml_service`

This service as it names clearly says takes care of machine learning part.
Here you may find the NER algorithm which is written in `Spacy`.
This model is being wrapped in additional abstract layer: `class NER`. This provides methods for learning/prediction/saving model/evaluating it. During initialization, we simply load best/latest model saved during learning process, or load pre-trained `Spacy` model.

``` py
class NER:
    
    def _load_spacy_model(self, use_latest: bool=False):
        # By default we use best model not the latest model.
        if use_latest and os.path.isdir(MODEL_PATHS["LATEST_MODEL"]):
            return spacy.load(MODEL_PATHS["LATEST_MODEL"])

        if os.path.isdir(MODEL_PATHS["BEST_MODEL"]):
            return spacy.load(MODEL_PATHS["BEST_MODEL"])
        else:
            return spacy.load("en_core_web_sm")

    def __init__(self, use_latest: bool=False) -> None:
        # first load the proper model
        self.nlp = self._load_spacy_model(use_latest)
        data = dt_client.get_training_data()
        self._train_dataset, self._test_dataset = split_data(data)
        self.other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
        self.ner_pipe = self.nlp.get_pipe("ner")
        self.initial_score = self.evaluate_model(save_score=False)
        self.current_score = None
```

To evaluate model we've decided to use `f_score` metric, because this will give us the most balanced output. We simply ignore other metrics produced by `Spacy`.
To contact with other services this one also uses API/client layer.

### `client_api`

This service is responsible to wrap it all up and provide API to communicate with all services by frontend client.
Here we use `FastAPI` to easily provide API interface for out application. This service is not quite finished yet, it lacks test, and solid user/group management. The work on it is still in progress.

### Future development:
 * Provide tests for `client_api` service
 * Modify matching algorithm, allow it to be ML also
 * Create test pipeline to ensure tests are running correctly
 * Add linters
 * Create solid frontend application for this
