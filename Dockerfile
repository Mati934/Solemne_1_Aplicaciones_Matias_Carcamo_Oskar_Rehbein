FROM python:3.13-alpine

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen

COPY hora/ ./hora/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "hora.main:app", "--host", "0.0.0.0", "--port", "8000"]



