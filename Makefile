.PHONY: run

run:
	uvicorn main:app --reload --log-level=debug
