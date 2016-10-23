FROM python:3.5.2
RUN mkdir /app
ADD . ./app
WORKDIR /app
RUN pip install -r /app/requirements/base.txt


EXPOSE 5000
CMD ["python", "manage.py"]