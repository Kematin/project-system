FROM python:3.10
WORKDIR /bot
COPY requirements.txt /bot/requirements.txt
RUN pip install --upgrade pip && pip install -r /bot/requirements.txt
ADD ./src /bot
CMD ["python", "bot.py"]
