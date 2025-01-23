# Student Information
**Name:** Sviderski Yaroslav Petrovich  
**Group:** IM-23

# How to Run the Project

1. **Install Docker**  
   Make sure Docker is installed on your system. 
   You can download it from [here](https://www.docker.com/products/docker-desktop) for your platform.

2. **Navigate to the Project Folder**  
   Open a terminal and move to the project directory:
   ```bash
   cd <project-folder>
3. **Set Environment Variables**
   Create a .env file in the root of your project folder and put something like:
   ```makefile
   POSTGRES_DB=defaultdb
   POSTGRES_USER=avnadmin
   POSTGRES_HOST=backend-4-db-labs-backend.e.aivencloud.com:21066
   PORT=8080
   JWT_SECRET_KEY=84389718518730203062025172669712122432
4. Run the Container
   Start the application by running:
   ```bash
   docker-compose up db