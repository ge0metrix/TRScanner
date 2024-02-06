import sqlalchemy.orm as _orm
import database_models as _models, schemas as _schemas, database as _database

def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_pydantic(obj: object):
    """ Checks whether an object is pydantic. """
    return type(obj).__class__.__name__ == "ModelMetaclass"

def parse_pydantic_schema(schema):
    """
        Iterates through pydantic schema and parses nested schemas
        to a dictionary containing SQLAlchemy models.
        Only works if nested schemas have specified the Meta.orm_model.
    """
    parsed_schema = dict(schema)
    for key, value in parsed_schema.items():
        try:
            if isinstance(value, list) and len(value):
                if is_pydantic(value[0]):
                    parsed_schema[key] = [schema.Meta.orm_model(**schema.dict()) for schema in value]
            else:
                if is_pydantic(value):
                    parsed_schema[key] = value.Meta.orm_model(**value.dict()) # type: ignore
        except AttributeError:
            raise AttributeError("Found nested Pydantic model but Meta.orm_model was not specified.")
    return parsed_schema

def get_calls(db: _orm.Session, skip:int=0, limit:int=10) -> _orm.Query[_models.Call]:
    return db.query(_models.Call).offset(skip).limit(limit)

def get_call(db:_orm.Session, call_id:int) -> _models.Call | None:
    return db.query(_models.Call).filter(_models.Call.id == call_id).first()

def post_call_to_db(db: _orm.Session, call:_schemas.CallIn):
    parsed = parse_pydantic_schema(call)
    post_call = _models.Call(**parsed)
    print(post_call.srcList)
    db.add(post_call)
    db.commit()
    db.refresh(post_call)
    return post_call