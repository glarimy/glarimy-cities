1. Build the package (from the directory where pom.xml is present)
mvn clean package

2. Dockerize (from the directory where Dockerfile is present)
docker build -t glarimy-cities-profile .

3. Tag the image (optional)
docker tag glarimy-cities-profile:latest <username>/glarimy-cities-profile:latest

4. Push the image to DockerHub (optional)
docker login (if not logged in already)
docker push <username>/glarimy-cities-profile:latest

5. Deploy and run the containers (from the directory where docker-compose.yml is present)
docker-compose up