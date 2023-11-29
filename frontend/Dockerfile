FROM node:14-alpine

WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker cache
COPY package*.json ./

RUN npm install

COPY . .
