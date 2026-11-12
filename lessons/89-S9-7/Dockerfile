FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir qdrant-client sentence-transformers fastapi uvicorn
COPY search.py app.py index.html shop_vocab.json wix_vocab.json ./
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
