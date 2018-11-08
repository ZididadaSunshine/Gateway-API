FROM python:3
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt
COPY app /app
COPY manage.py /
CMD ["python", "manage.py", "run"]
