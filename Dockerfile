FROM flask

COPY app /app
WORKDIR /app

EXPOSE 8080

WORKDIR /app/
CMD ["flask", "run", "--host=0.0.0.0"]
