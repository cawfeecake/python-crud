.RECIPEPREFIX = >

# TODO make port (8080) a variable to use across Makefile
LOCAL_URL=http://127.0.0.1:8080
SEVER_URL?=$(LOCAL_URL)

add_items:
> for i in $$(seq 0 $$(jq '.| length - 1' data/items_init.json)); do \
>   name=$$(jq --raw-output ".[$$i].name" data/items_init.json); \
>   desc=$$(jq --raw-output ".[$$i].desc" data/items_init.json); \
>   children=$$(jq --raw-output ".[$$i].children" data/items_init.json); \
>   curl -L -H 'Accept: application/json' \
>     -H 'Content-Type: application/json' \
>     $(SEVER_URL)/items -d "{\"name\":\"$$name\",\"desc\":\"$$desc\",\"children\":\"$$children\"}"; \
> done
.PHONY: add_items

run:
> flask --debug run --port=8080

clean_run: clean run
.PHONY: run clean_run

clear_cache:
> find . -type d -name __pycache__ -exec rm -rf {} \; -print -prune

rm_backend:
> rm -f backend.db instance/backend.db

clean: clear_cache rm_backend
.PHONY: clear_cache rm_backend clean
