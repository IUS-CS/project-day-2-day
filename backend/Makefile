install:
	pip install -r requirements.txt

run:
	PYTHONPATH=./src uvicorn src.calendar_app.__main__:app --reload

test:
	PYTHONPATH=./src pytest -q
