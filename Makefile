.RECIPEPREFIX = >

.PHONY: clean rm_backend

clean:
> find . -type d -name __pycache__ -exec rm -rf {} \; -print -prune

rm_backend:
> rm -f backend.db
