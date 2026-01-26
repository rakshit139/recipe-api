from annotated_types import doc
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from bson import ObjectId
from app.core.auth import get_current_user
from app.database import get_db
from app.models.recipe import RecipeCreate
from app.core.limiter import limiter
from app.core.validators import validate_object_id
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException


router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.post("/")
def create_recipe(recipe: RecipeCreate, user=Depends(get_current_user)):
    """
    Create a new recipe for the logged-in user.
    """
    db = get_db()

    doc = recipe.model_dump()
    doc["owner_email"] = user["email"]
    
    existing = db.recipes.find_one({
    "title": recipe.title,
    "owner_email": user["email"]
})

    if existing:
        raise BadRequestException("Recipe with this title already exists")

    result = db.recipes.insert_one(doc)

    doc["id"] = str(result.inserted_id)
    del doc["_id"]

    return doc

@router.get("/")
@limiter.limit("100/minute")
def list_recipes(
    request: Request,
    search: str | None = None,
    category: str | None = None,
    ingredient: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    user=Depends(get_current_user)
):
    """
    Lists all recipes for the logged-in user with optional filters and pagination.
    """
    db = get_db()
    query = {"owner_email": user["email"]}

    if search:
        query["title"] = {"$regex": search, "$options": "i"}

    if category:
        query["category"] = category

    if ingredient:
        query["ingredients"] = {"$in": [ingredient]}

    skip = (page - 1) * limit
    recipes = []
    for r in db.recipes.find(query).skip(skip).limit(limit):
        r["id"] = str(r["_id"])
        del r["_id"]
        recipes.append(r)

    return recipes

@router.patch("/{recipe_id}")
def update_recipe(recipe: RecipeCreate, recipe_id: str = Depends(validate_object_id), user=Depends(get_current_user)):
    """
    Update an existing recipe for the logged-in user.
    """
    db = get_db()
    existing = db.recipes.find_one({"_id": ObjectId(recipe_id)})

    if not existing:
        raise NotFoundException("Recipe not found")

    if existing["owner_email"] != user["email"]:
        raise ForbiddenException("Not allowed")

    db.recipes.update_one(
        {"_id": ObjectId(recipe_id)},
        {"$set": recipe.model_dump()}
    )

    return {"message": "Updated"}

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: str = Depends(validate_object_id), user=Depends(get_current_user)):
    """
    Delete an existing recipe for the logged-in user.
    """
    db = get_db()
    existing = db.recipes.find_one({"_id": ObjectId(recipe_id)})

    if not existing:
        raise NotFoundException("Recipe not found")

    if existing["owner_email"] != user["email"]:
        raise ForbiddenException("Not allowed")

    db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    return {"message": "Deleted"}

@router.get("/{recipe_id}")
def get_recipe(recipe_id: str = Depends(validate_object_id), user=Depends(get_current_user)):
    """
    Get a specific recipe for the logged-in user.
    """
    db = get_db()

    recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})

    if not recipe:
        raise NotFoundException("Recipe not found")

    if recipe["owner_email"] != user["email"]:
        raise ForbiddenException("Not allowed")

    recipe["id"] = str(recipe["_id"])
    del recipe["_id"]

    return recipe

