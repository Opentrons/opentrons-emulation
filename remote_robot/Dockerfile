FROM --platform=linux/amd64 nginx:alpine
ARG ROBOT_URL
COPY nginx.conf /etc/nginx/templates/default.conf.template
RUN sed -i "s,ROBOT_URL,$ROBOT_URL,g" /etc/nginx/templates/default.conf.template
