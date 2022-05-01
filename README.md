# DevOps Tutorial

**Practical DevOps Book**

**Chapter 8:** Docker Container Concept  
**Chapter 9:** Using a Dockerfile, Docker-compose and Portainer docker  
**Chapter 10:** To setup LEMP Stack  
**Chapter 11:** To setup VPS and Let's Encrypt with Docker  
**Chapter 12:** Microservices Architecture Development with Docker Container  
**Chapter 13:** To setup API gateway and Monitoring system with KONG + Prometheus + Grafana  

&nbsp;&nbsp;&nbsp;&nbsp;***Remark: Konga has some bugs when first running with NODE_ENV=production***  
&nbsp;&nbsp;&nbsp;&nbsp;***Solution:***
1. $cd kong_dock
2. $docker-compose up -d
3. Navigate to Konga by browser. 
4. Register admin user and add Kong Admin URL, then close browser.
5. $docker-compose down
6. $mv docker-compose-production.yml docker-compose.yml
7. $docker-compose up -d
8. Konga can be used with less resources.

**Chapter 14:** OTP service and session server development with Redis and Flask  
**Chapter 15:** Web application development with nearly zero downtime  
**Chapter 16:** To setup a CI/CD pipeline for DevOps team  
