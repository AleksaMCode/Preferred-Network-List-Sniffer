FROM node:20.5.1

# Set the working direcory inside the container.
WORKDIR /app

# Install the React dependencies.
COPY package.json $WORKDIR
COPY package-lock.json $WORKDIR
RUN npm install

# Copy the solution code to the working directory.
COPY . $WORKDIR

# Run the web app.
CMD npm start
