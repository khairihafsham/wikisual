#Wikisual

##Requirement:

1. docker >= 1.10
2. docker-compose >= 1.6
3. npm >= 3.5 (for builds only)
4. node >= 5.5 (for builds only)


##Usage:

1. make setup-geodb 
2. cd wikiweb/jsapp && npm install
3. cd wikiweb/jsapp && tsc
4. docker-compose build
5. docker-compose up -d
6. access localhost:8080
