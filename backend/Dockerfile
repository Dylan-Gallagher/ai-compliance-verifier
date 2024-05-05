# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD ./server.py /app
ADD ./server-requirements.txt /app
ADD ./documentation_input/pdf_parser.py /app/documentation_input/
ADD ./rules_mining/rules_mining.py /app/rules_mining/
ADD ./compliance_checklist.json /app

# Install any needed packages specified in requirements.txt
RUN pip install -r server-requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "server.py"]
