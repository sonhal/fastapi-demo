FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install aiofiles

COPY ./fastapi_demo /app/app
COPY ./fastapi_demo/static /app/static
