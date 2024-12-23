FROM python:3.10

COPY requirements.txt .
COPY app.py .
COPY config.py .
COPY funcs.py .
COPY classes.py .
COPY queries.py .
COPY templates ./templates
COPY static ./static

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
