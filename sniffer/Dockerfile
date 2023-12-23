FROM python:3.11.4

# Set the working direcory inside the container.
WORKDIR /pnls

# Copy the requirements file to the working directory.
COPY ./requirements.txt $WORKDIR

# Install the Python dependencies.
RUN pip3 install -r requirements.txt

# Copy the solution code to the working directory.
COPY . $WORKDIR

# Expose the port on which the server will run.
EXPOSE 3001

# Run the uvicorn server.
CMD python3 pnls.py
