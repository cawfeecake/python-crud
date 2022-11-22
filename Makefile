.RECIPEPREFIX = >

# TODO make port (8080) a variable to use across Makefile
PORT=8080
LOCAL_URL=http://127.0.0.1:$(PORT)
SEVER_URL?=$(LOCAL_URL)

add_items:
> for i in $$(seq 0 $$(jq '.| length - 1' $(JSON))); do \
>   name=$$(jq --raw-output ".[$$i].name" $(JSON)); \
>   desc=$$(jq --raw-output ".[$$i].desc" $(JSON)); \
>   children=$$(jq --raw-output ".[$$i].children" $(JSON)); \
>   curl -s -L -H 'Accept: application/json' \
>     -H 'Content-Type: application/json' \
>     $(SEVER_URL)/items \
>     -d "{\"name\":\"$$name\",\"desc\":\"$$desc\",\"children\":\"$$children\"}" \
>     > /dev/null; \
> done
> curl -s -L -H 'Accept: application/json' \
>   $(SEVER_URL)/items;
.PHONY: add_items

run:
> flask --debug run --port=$(PORT)

clean_run: clean run
.PHONY: run clean_run

clear_cache:
> find . -type d -name __pycache__ -exec rm -rf {} \; -print -prune

rm_backend:
> rm -f backend.db instance/backend.db

clean: clear_cache rm_backend
.PHONY: clear_cache rm_backend clean
