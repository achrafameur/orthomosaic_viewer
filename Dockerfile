FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/data
COPY data/export_result.tif /app/data/export_result.tif

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
