FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# نصب ابزارهای مورد نیاز
RUN apt-get update && apt-get install -y \
    supervisor \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

RUN mkdir -p /var/log && chmod -R 777 /var/log




COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . /app



COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]






