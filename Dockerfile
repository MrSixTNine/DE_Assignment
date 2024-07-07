# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Set the working directory to /app/Python Script
WORKDIR /app/Python Script

# Copy the wait-for-postgres.sh script into the container
COPY wait-for-postgres.sh /usr/local/bin/wait-for-postgres.sh

# Make the wait-for-postgres.sh script executable
RUN chmod +x /usr/local/bin/wait-for-postgres.sh

# CMD to wait for PostgreSQL and then run pipeline.py
CMD ["wait-for-postgres.sh", "postgresql:5432", "--", "python", "pipeline.py"]
