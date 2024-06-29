FROM node:18.18-alpine
WORKDIR /admin_panel
EXPOSE 8080
ADD ./ /admin_panel/
RUN npm i
CMD ["npm", "run", "dev"]