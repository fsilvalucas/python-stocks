FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD 123
ENV MYSQL_DATABASE production
ENV MYSQL_USER fsilva
ENV MYSQL_PASSWORD
EXPOSE 3306