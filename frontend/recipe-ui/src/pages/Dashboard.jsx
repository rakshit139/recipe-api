import { useEffect, useState } from "react";
import api from "../api/client";

export default function Dashboard() {
  const [recipes, setRecipes] = useState([]);

  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("");
  const [ingredients, setIngredients] = useState("");
  const [instructions, setInstructions] = useState("");

  const [editTitle, setEditTitle] = useState("");
  const [editCategory, setEditCategory] = useState("");

  const [search, setSearch] = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const [filterIngredient, setFilterIngredient] = useState("");

  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState(null);
  const [expandedId, setExpandedId] = useState(null);

  const loadRecipes = () => {
    setLoading(true);
    api
      .get("/recipes/", {
        params: {
          search,
          category: filterCategory,
          ingredient: filterIngredient,
        },
      })
      .then((res) => {
        setRecipes(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    loadRecipes();
  }, [search, filterCategory, filterIngredient]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/recipes/", {
        title,
        category,
        ingredients: ingredients.split(",").map((i) => i.trim()),
        instructions,
      });

      setTitle("");
      setCategory("");
      setIngredients("");
      setInstructions("");

      loadRecipes();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/recipes/${id}`);
      loadRecipes();
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpdate = async (id) => {
    try {
      await api.patch(`/recipes/${id}`, {
        title: editTitle,
        category: editCategory,
      });
      setEditingId(null);
      setEditTitle("");
      setEditCategory("");
      loadRecipes();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto min-h-screen">
      <div className="flex justify-end mb-4">
        <button
          onClick={() => {
            localStorage.removeItem("token");
            window.location.href = "/login";
          }}
          className="bg-red-100 text-red-600 px-3 py-1 rounded hover:bg-red-200"
        >
          Logout
        </button>
      </div>

      <h1 className="text-2xl font-bold mb-4">Your Recipes</h1>

      {/* Create Recipe */}
      <form onSubmit={handleSubmit} className="space-y-3 mb-6">
        <input
          className="border p-2 w-full"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          className="border p-2 w-full"
          placeholder="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />

        <input
          className="border p-2 w-full"
          placeholder="Ingredients (comma separated)"
          value={ingredients}
          onChange={(e) => setIngredients(e.target.value)}
        />

        <textarea
          className="border p-2 w-full"
          placeholder="Instructions"
          value={instructions}
          onChange={(e) => setInstructions(e.target.value)}
        />

        <button className="bg-green-500 text-white w-full p-2 rounded">
          Add Recipe
        </button>
      </form>

      {/* Filters */}
      <div className="mb-4 space-y-2">
        <input
          className="border p-2 w-full"
          placeholder="Search by title"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <input
          className="border p-2 w-full"
          placeholder="Filter by category"
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
        />

        <input
          className="border p-2 w-full"
          placeholder="Filter by ingredient"
          value={filterIngredient}
          onChange={(e) => setFilterIngredient(e.target.value)}
        />
      </div>

      {/* List */}
      {loading && <p className="text-gray-500">Loading...</p>}
      {!loading && recipes.length === 0 && (
        <p className="text-gray-500">No recipes found.</p>
      )}

      <ul className="space-y-2">
        {recipes.map((r) => (
          <li key={r.id} className="border p-3 rounded">
            {/* Header */}
            <div
              className="flex justify-between items-center cursor-pointer"
              onClick={() =>
                setExpandedId(expandedId === r.id ? null : r.id)
              }
            >
              <h2 className="text-lg font-semibold">{r.title}</h2>
              <span className="text-gray-500">
                {expandedId === r.id ? "▲" : "▼"}
              </span>
            </div>

            {/* Details */}
            {expandedId === r.id && (
              <div className="mt-2 text-sm space-y-1">
                <p><strong>Category:</strong> {r.category}</p>
                <p>
                  <strong>Ingredients:</strong>{" "}
                  {Array.isArray(r.ingredients)
                    ? r.ingredients.join(", ")
                    : r.ingredients}
                </p>
                <p><strong>Instructions:</strong> {r.instructions}</p>
              </div>
            )}

            {/* Actions */}
            <div className="mt-2 flex justify-end space-x-3 text-sm">
              <button
                className="text-blue-500"
                onClick={() => {
                  setEditingId(r.id);
                  setEditTitle(r.title);
                  setEditCategory(r.category);
                }}
              >
                Edit
              </button>
              <button
                className="text-red-500"
                onClick={() => handleDelete(r.id)}
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
