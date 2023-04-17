FROM --platform=linux/amd64 node:latest
WORKDIR /app
RUN npm install express
COPY app.js .
CMD ["node", "app.js"]

# docker tag local-image:tagname new-repo:tagname
# docker push new-repo:tagname
