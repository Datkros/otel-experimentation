FROM python:3.10-slim

ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install fastapi httpx sqlalchemy[asyncio] uvicorn opentelemetry-sdk opentelemetry-exporter-otlp-proto-http aiosqlite

COPY /app /app
WORKDIR /app
RUN cd /app
RUN ls

CMD ["uvicorn", "main:app"]
