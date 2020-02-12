FROM python:latest

WORKDIR /app
COPY ./app /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
