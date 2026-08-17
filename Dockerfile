#Step 1: Start with an official, ultra-lightweight Linux Python base image
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
# Forces stdout/stderr streams to flush instantly (gives real-time terminal logs)
ENV PYTHONUNBUFFERED=1
# Force the container's internal operating system clock to run on absolute UTC
ENV TZ=UTC

# Step 3: Define the working directory inside the container's virtual filesystem
WORKDIR /app

#  Step 4: Install low-level system binary requirements needed for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#  Step 5: Copy over your dependencies list and install them inside the sandbox
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of your local application files into the container space
COPY . /app/

#  Step 7: Document that this container will listen for network web traffic on Port 8000
EXPOSE 8000

#  Step 8: The default command to run when the container springs to life
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
