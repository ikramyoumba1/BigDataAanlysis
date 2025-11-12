FROM nginx:stable-alpine
WORKDIR /usr/share/nginx/html
COPY tp3_BigData.pbix .
RUN echo "<h1>TP3 Power BI - Big Data Dashboard</h1><p>Le fichier TP3_BigData.pbix est disponible dans le conteneur.</p>" > index.html
EXPOSE 80
