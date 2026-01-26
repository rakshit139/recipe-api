from pydantic import BaseModel, Field, field_validator

class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    ingredients: list[str] = Field(..., min_items=1)
    instructions: str = Field(..., min_length=10)
    category: str = Field(..., min_length=3, max_length=50)

    @field_validator("ingredients")
    @classmethod
    def no_empty_ingredients(cls, v):
        if any(len(i.strip()) == 0 for i in v):
            raise ValueError("Ingredients cannot be empty strings")
        return v



class RecipeOut(RecipeCreate):
    id: str
    owner_email: str
