FASTAPI_PATH=main:app

run:
	uvicorn $(FASTAPI_PATH) --reload