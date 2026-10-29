FROM python:3.12-slim

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/

RUN useradd -r -u 10001 appuser
USER 10001

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.main:app"]
