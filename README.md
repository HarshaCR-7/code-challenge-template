# Weather Data API Project

This project provides a Flask-based API to manage and analyze weather data records. The data is sourced from weather stations across several states, including Nebraska, Iowa, Illinois, Indiana, and Ohio, covering the period from January 1, 1985 to December 31, 2014. The project includes endpoints for ingesting weather data, calculating statistics, and serving data through a REST API.


### Directories:
- **`wx_data`**: Contains weather data records in text files (1985-2014) for various weather stations.
- **`yld_data`**: (To be defined, as per your additional files or use).
- **`src`**: Contains the main application code including configuration, routes, models, and logic for the API.

### Key Files:
- **`run.py`**: Entry point for starting the Flask application.
- **`Dockerfile`**: For building a Docker image to run the Flask application.
- **`docker-compose.yml`**: Defines services, networks, and volumes for the project.
- **`config.py`**: Configuration settings for the Flask application.
- **`pyproject.toml`**: Project dependency management with Poetry.

---

## Weather Data Description

The **`wx_data`** directory contains files with weather data from 1985 to 2014. Each file corresponds to a specific weather station in Nebraska, Iowa, Illinois, Indiana, or Ohio. Each line in the data files contains four records separated by tabs:

1. **Date**: In the format `YYYYMMDD`.
2. **Maximum Temperature**: The maximum temperature for that day (in tenths of a degree Celsius).
3. **Minimum Temperature**: The minimum temperature for that day (in tenths of a degree Celsius).
4. **Precipitation**: The amount of precipitation for that day (in tenths of a millimeter).

Missing data is represented by **-9999**.

---

## Instructions for Setting Up the Flask Application

### 1. Install Docker

If you do not have Docker installed on your local machine, follow the instructions below to install it:

#### For macOS:
1. Download the Docker Desktop installer from the [official Docker website](https://www.docker.com/products/docker-desktop).
2. Open the downloaded `.dmg` file and drag Docker to your Applications folder.
3. Launch Docker from the Applications folder and follow the on-screen instructions to complete the setup.

#### For Windows:
1. Download the Docker Desktop installer from the [official Docker website](https://www.docker.com/products/docker-desktop).
2. Run the installer and follow the on-screen instructions.
3. After installation, launch Docker Desktop and complete the initial setup.

#### For Linux:
1. Follow the installation steps for your specific distribution as outlined in the official Docker documentation: [Install Docker on Linux](https://docs.docker.com/engine/install/).
2. After installation, ensure Docker is running by executing the following command:

```bash
sudo systemctl start docker
```
### 2. Build the Docker Image

Once Docker is installed and running, navigate to the `src` folder in your terminal and use the following command to build the Docker image for the Flask application:

```bash
docker-compose build
```
This will create a Docker image based on the configuration defined in the Dockerfile and docker-compose.yml files.

### 3. Running the Flask Application with Docker

After building the image, start the Flask app by running the following command:

```bash
docker-compose up
```
This will start the application inside a Docker container. The Flask app will now be accessible at: http://127.0.0.1:5000


### 4. Accessing the Application

Once the container is up and running, you can access the application via the following link:

```bash
http://127.0.0.1:5000
```
This will start the application inside a Docker container. The Flask app will now be accessible at:

### 5. Stopping the Application

To stop the running application and the Docker containers, use the following command:

```bash
docker-compose down
```

### 6. API Documentation with Swagger
This application includes Swagger UI for easy exploration and testing of API endpoints.

#### Accessing Swagger UI
Once the Flask app is running, you can access the API documentation at:

```bash
http://127.0.0.1:5000/swagger/
```
Swagger provides an interactive interface where you can:

View all available endpoints.
See request and response formats.
Test API calls directly from the browser.

### If we need to deploy Flask App to AWS EC2
#### Step 1: Spin Up the EC2 Instance
Launch an EC2 instance with Docker pre-installed (or install Docker manually if needed).
Choose an appropriate instance type, such as t2.micro for free-tier usage.
Set up SSH access to securely connect to the instance.
#### Step 2: Transfer the Flask App to EC2
You can either manually upload the project files to the EC2 instance using SCP or
If the Docker image is already pushed to Docker Hub, you can pull it directly onto the EC2 instance.
#### Step 3: Build the Docker Image (If Using Files)
SSH into the EC2 instance and navigate to the project directory.
If the project files were uploaded manually, build the Docker image from the Dockerfile.
#### Step 4: Run the Docker Container
Start the Flask app inside a Docker container in detached mode so it runs in the background.
Verify that the container is running properly.
#### Step 5: Configure EC2 Security Group
In the AWS EC2 Security Groups settings, add an Inbound Rule to allow external access on port 80 or the port your app is running on.
Once configured, you should be able to access the Flask API using the EC2 public IP.
#### Step 6: Enable Auto-Restart (Optional)
To ensure the application automatically restarts if the EC2 instance reboots, configure the container to restart always.
#### Step 7: Set Up Nginx as a Reverse Proxy (Optional)
For production deployments, install and configure Nginx as a reverse proxy to forward requests to the Flask app.
This improves performance, handles requests efficiently, and secures the application.
#### Step 8: Monitor & Troubleshoot
Check the container logs to debug any issues.
Verify running containers and application status to ensure smooth operation.