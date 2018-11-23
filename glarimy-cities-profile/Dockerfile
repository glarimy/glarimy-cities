FROM openjdk:8-jdk-alpine
MAINTAINER Krishna Mohan Koyya <krishna@glarimy.com>
VOLUME /tmp
EXPOSE 8080
ARG JAR_FILE=target/glarimy-cities-profile.jar
ADD ${JAR_FILE} glarimy-cities-profile.jar
ENTRYPOINT ["java","-Dspring.data.mongodb.uri=mongodb://mongo:27017/glarimy-cities", "-Djava.security.egd=file:/dev/./urandom","-jar","/glarimy-cities-profile.jar"]