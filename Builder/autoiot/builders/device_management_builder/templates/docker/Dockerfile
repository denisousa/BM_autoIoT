FROM python:3.6
LABEL maintainer "AutoIoT <autoiot.de>"
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["main.py"]