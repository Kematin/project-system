FROM python:3.10
WORKDIR /project_api
COPY requirements.txt /project_api
RUN pip install --upgrade pip && pip install -r /project_api/requirements.txt
EXPOSE 9999
ADD ./src /project_api
CMD ["python", "main.py"]

