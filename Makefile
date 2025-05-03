.PHONY: run flask uvicorn all

FLASK_CMD=flask run --port=5000
UVICORN_CMD=uvicorn endpoints:app --reload
UVICORN_DOCS=open http://127.0.0.1:8000/docs

all: run

run:
	@echo "Starting Flask and Uvicorn..."
	@$(FLASK_CMD) & echo $$! > flask.pid & \
	$(UVICORN_CMD) & echo $$! > uvicorn.pid & \
	sleep 3 && $(UVICORN_DOCS) & \
	wait

flask:
	@echo "Running Flask app..."
	@$(FLASK_CMD)

uvicorn:
	@echo "Running Uvicorn app..."
	@$(UVICORN_CMD)

stop:
	-@kill -9 `cat flask.pid` 2>/dev/null || true
	-@kill -9 `cat uvicorn.pid` 2>/dev/null || true
	@rm -f flask.pid uvicorn.pid
