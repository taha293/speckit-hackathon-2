# FastAPI Models and Schemas

## SQLModel Best Practices

### Model Definition Patterns

**Base Model Pattern:**
```python
from sqlmodel import Field, SQLModel
from typing import Optional

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: Optional[int] = Field(default=None, index=True)
    secret_name: str
```

**Complete Model with Table:**
```python
class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Additional fields specific to database storage
```

**Input Models:**
```python
class HeroCreate(HeroBase):
    # Additional validation for creation if needed
    pass

class HeroUpdate(HeroBase):
    name: Optional[str] = None
    age: Optional[int] = None
    secret_name: Optional[str] = None
```

**Output Models:**
```python
class HeroPublic(HeroBase):
    id: int
    # Exclude sensitive fields from public responses
```

## Pydantic Validation

### Field Validation
```python
from sqlmodel import Field
from pydantic import EmailStr, validator

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    age: int = Field(ge=0, le=120)  # Greater/equal 0, Less/equal 120
    rating: float = Field(gt=0, lt=5.0)  # Greater than 0, Less than 5.0
    name: str = Field(min_length=1, max_length=100)
```

### Custom Validators
```python
from pydantic import validator

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    price: float
    discount_price: Optional[float] = None

    @validator('discount_price')
    def validate_discount(cls, v, values):
        if v is not None and 'price' in values:
            if v >= values['price']:
                raise ValueError('Discount price must be less than regular price')
        return v
```

## Relationship Patterns

### One-to-Many Relationships
```python
class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")
```

### Many-to-Many Relationships
```python
class HeroTeamLink(SQLModel, table=True):
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id", primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    teams: List["Team"] = Relationship(
        back_populates="heroes",
        link_model=HeroTeamLink
    )

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    heroes: List["Hero"] = Relationship(
        back_populates="teams",
        link_model=HeroTeamLink
    )
```

## Model Validation and Serialization

### Custom Serialization
```python
from pydantic import BaseModel, Field

class HeroPublic(HeroBase):
    id: int
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### Excluding Sensitive Fields
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str = Field(exclude=True)
    is_active: bool = True

    class Config:
        # Exclude sensitive fields from serialization
        fields = {
            'hashed_password': {'exclude': True}
        }
```

## Schema Patterns

### Request/Response Schema Separation
```python
# Input schema - what the client sends
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Update schema - what the client can update
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

# Response schema - what the server sends
class Item(ItemCreate):
    id: int
    owner_id: int
```

### Generic Response Wrapper
```python
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ApiResponse(Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None
```

## Migration Considerations

### Schema Evolution
```python
class UserV1(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str

class UserV2(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    phone: Optional[str] = Field(default=None, unique=True)  # New field
    is_verified: bool = False  # New field with default
```

### Backward Compatibility
```python
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    # Always maintain backward compatibility for public APIs
    # Add new fields as optional with defaults

    class Config:
        # Allow extra fields for forward compatibility
        extra = 'allow'
```