FROM node:20.16

WORKDIR /backend

COPY package*.json ./

RUN npm install --production

COPY . .

EXPOSE 3000

CMD ["npm run dev"]
