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
   Create a .env file in the root of the project folder and specify the following variables:
   ```makefile
   POSTGRES_DB=<your_database_name>
   POSTGRES_USER=<your_database_user>
   POSTGRES_PASSWORD=<your_database_password>
   POSTGRES_HOST=<your_host_name>
4. Run the Container
   Start the application by running:
   ```bash
   docker-compose up db

## Notes
**Deployed site:**
https://backend-lab3-7rjr.onrender.com
