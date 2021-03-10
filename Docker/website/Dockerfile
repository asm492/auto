FROM node:10
WORKDIR /app
COPY package.json .
RUN npm install
EXPOSE 8080
COPY . /app
CMD [ "node", "app.js" ]