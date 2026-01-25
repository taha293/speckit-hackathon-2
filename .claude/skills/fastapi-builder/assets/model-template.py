from typing import Annotated, List, Optional
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel


class {{MODEL_NAME}}Base(SQLModel):
    """Base model for {{MODEL_NAME}} with common fields."""
    {% for field in fields %}
    {{ field.name }}: {{ field.type }}{% if field.optional %} = Field(default=None{% if field.default %}, default={{ field.default }}{% endif %}{% else %} = Field({% if field.default %}default={{ field.default }}{% endif %}{% if field.index %}, index=True{% endif %}{% if field.unique %}, unique=True{% endif %}){% endif %}
    {% endfor %}


class {{MODEL_NAME}}({{MODEL_NAME}}Base, table=True):
    """Database model for {{MODEL_NAME}}."""
    id: Optional[int] = Field(default=None, primary_key=True)


class {{MODEL_NAME}}Public({{MODEL_NAME}}Base):
    """Public response model for {{MODEL_NAME}}."""
    id: int


class {{MODEL_NAME}}Create({{MODEL_NAME}}Base):
    """Model for creating new {{MODEL_NAME}}."""
    pass


class {{MODEL_NAME}}Update({{MODEL_NAME}}Base):
    """Model for updating existing {{MODEL_NAME}}."""
    {% for field in fields %}
    {{ field.name }}: {% if field.optional %}{{ field.type }}{% else %}Optional[{{ field.type }}]{% endif %} = None
    {% endfor %}


# Database setup
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    """Create database tables on startup."""
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    create_db_and_tables()
    yield


# Application instance
app = FastAPI(lifespan=lifespan)


# Database session dependency
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# CRUD Endpoints
@app.post("/{{MODEL_NAME.lower}}s/", response_model={{MODEL_NAME}}Public)
def create_{{MODEL_NAME.lower}}({{MODEL_NAME.lower}}: {{MODEL_NAME}}Create, session: SessionDep) -> {{MODEL_NAME}}Public:
    """Create a new {{MODEL_NAME}}."""
    db_{{MODEL_NAME.lower}} = {{MODEL_NAME}}.model_validate({{MODEL_NAME.lower}})
    session.add(db_{{MODEL_NAME.lower}})
    session.commit()
    session.refresh(db_{{MODEL_NAME.lower}})
    return db_{{MODEL_NAME.lower}}


@app.get("/{{MODEL_NAME.lower}}s/", response_model=List[{{MODEL_NAME}}Public])
def read_{{MODEL_NAME.lower}}s(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[{{MODEL_NAME}}Public]:
    """Get a list of {{MODEL_NAME.lower}}s."""
    {{MODEL_NAME.lower}}s = session.exec(select({{MODEL_NAME}}).offset(offset).limit(limit)).all()
    return {{MODEL_NAME.lower}}s


@app.get("/{{MODEL_NAME.lower}}s/{id}", response_model={{MODEL_NAME}}Public)
def read_{{MODEL_NAME.lower}}(id: int, session: SessionDep) -> {{MODEL_NAME}}Public:
    """Get a specific {{MODEL_NAME}} by ID."""
    {{MODEL_NAME.lower}} = session.get({{MODEL_NAME}}, id)
    if not {{MODEL_NAME.lower}}:
        raise HTTPException(status_code=404, detail="{{MODEL_NAME}} not found")
    return {{MODEL_NAME.lower}}


@app.patch("/{{MODEL_NAME.lower}}s/{id}", response_model={{MODEL_NAME}}Public)
def update_{{MODEL_NAME.lower}}(
    id: int,
    {{MODEL_NAME.lower}}: {{MODEL_NAME}}Update,
    session: SessionDep
) -> {{MODEL_NAME}}Public:
    """Update a specific {{MODEL_NAME}} by ID."""
    {{MODEL_NAME.lower}}_db = session.get({{MODEL_NAME}}, id)
    if not {{MODEL_NAME.lower}}_db:
        raise HTTPException(status_code=404, detail="{{MODEL_NAME}} not found")

    {{MODEL_NAME.lower}}_data = {{MODEL_NAME.lower}}.model_dump(exclude_unset=True)
    {{MODEL_NAME.lower}}_db.sqlmodel_update({{MODEL_NAME.lower}}_data)
    session.add({{MODEL_NAME.lower}}_db)
    session.commit()
    session.refresh({{MODEL_NAME.lower}}_db)
    return {{MODEL_NAME.lower}}_db


@app.delete("/{{MODEL_NAME.lower}}s/{id}")
def delete_{{MODEL_NAME.lower}}(id: int, session: SessionDep) -> dict:
    """Delete a specific {{MODEL_NAME}} by ID."""
    {{MODEL_NAME.lower}} = session.get({{MODEL_NAME}}, id)
    if not {{MODEL_NAME.lower}}:
        raise HTTPException(status_code=404, detail="{{MODEL_NAME}} not found")
    session.delete({{MODEL_NAME.lower}})
    session.commit()
    return {"ok": True}