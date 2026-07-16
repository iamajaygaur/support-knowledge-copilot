.PHONY: install ingest ask api ui eval eval-dense eval-retrieval test

install:
	python3.12 -m venv .venv
	. .venv/bin/activate && pip install -U pip && pip install -e ".[dev]"

ingest:
	. .venv/bin/activate && python ingest.py --source docs/ --rebuild

ask:
	. .venv/bin/activate && python ask.py "$(Q)"

api:
	. .venv/bin/activate && uvicorn knowledge_copilot.api.main:app --reload --app-dir src

ui:
	. .venv/bin/activate && streamlit run streamlit_app.py

eval:
	. .venv/bin/activate && python eval.py --strategy hybrid --no-rerank --limit 12

eval-dense:
	. .venv/bin/activate && python eval.py --strategy dense --no-rerank --retrieval-only

eval-retrieval:
	. .venv/bin/activate && python eval.py --strategy dense --no-rerank --retrieval-only
	. .venv/bin/activate && python eval.py --strategy hybrid --no-rerank --retrieval-only
	. .venv/bin/activate && python eval.py --strategy sparse --no-rerank --retrieval-only

test:
	. .venv/bin/activate && pytest -q
