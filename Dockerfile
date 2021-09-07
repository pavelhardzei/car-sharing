FROM python:3
ENV PYTHONBUFFERED=1
WORKDIR /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["gunicorn", "car_sharing_project.wsgi:application", "--bind", "0.0.0.0:8000"]
