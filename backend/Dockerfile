# Official Python image from the Docker Hub
FROM python:3.12-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Copy project
COPY . /app/

# Expose the port
EXPOSE 5050

# Run supervisord
CMD ["flask", "run"]