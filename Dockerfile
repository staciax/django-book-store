FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get upgrade -y \ 
    && apt-get install -y netcat-traditional \
    && apt-get clean

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -U pip && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

COPY . .

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]