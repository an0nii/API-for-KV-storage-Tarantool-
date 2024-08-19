FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV ADMIN_LOGIN=admin
ENV ADMIN_PASSWORD=presale
ENV SECRET_KEY=secret_key

RUN python init.py

CMD ["python", "app.py"]