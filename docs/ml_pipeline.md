# ML Pipeline

Normal development happens locally on a Mac M1 using VS Code. Google Colab is used only for optional model training. VS Code does not need to connect to Colab.

## Local Food Concept Embeddings

`models/food_concepts.json` defines a small curated vocabulary. `training/generate_food_concept_embeddings.py` reads those concepts, uses `sentence-transformers/all-MiniLM-L6-v2`, and exports:

```text
models/food_concept_embeddings.npz
```

The artifact contains:

- `terms`: food concept terms.
- `embeddings`: normalized vectors.

## FastAPI Loading

`ArtifactLoader` loads `food_concepts.json` and `food_concept_embeddings.npz`. `SemanticRanker` averages matching query concept vectors and matching candidate concept vectors, computes cosine similarity, and adds a small score contribution.

If artifacts are missing or invalid, semantic ranking returns a neutral path and the app falls back to deterministic ranking.

## Optional Colab Ranker

`training/colab_train_ranker.ipynb` trains a tiny optional ranker and exports:

```text
ranker.pkl
ranker_metadata.json
```

The user manually downloads or copies those files from Colab into `models/`. The backend only loads them when `ENABLE_TRAINED_RANKER=true`.

## Production

The deployed backend performs inference only. It never trains models. If ML artifacts are unavailable, the app falls back to deterministic ranking.

Production needs no GPU and the backend requirements intentionally exclude `sentence-transformers`.
