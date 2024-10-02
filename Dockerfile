# FROM baseImage
# WORKDIR /the/workdir/path
# COPY source dest
# RUN command
# CMD [ "executable" ]
# ENTRYPOINT [ "executable" ]
# EXPOSE port

# Use a Python image to build the FastAPI app
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]