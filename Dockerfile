FROM python:3.10

COPY requirements.txt .
COPY app.py .
COPY run.py .


RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000"]
