.RECIPEPREFIX = >

.PHONY: clean rm_backend run

clean:
> find . -type d -name __pycache__ -exec rm -rf {} \; -print -prune

rm_backend:
> rm -f backend.db instance/backend.db

run:
> flask --debug run --port=8080
