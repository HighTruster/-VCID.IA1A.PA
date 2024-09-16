
# VM-Management Application

This repository contains the source code and documentation for the **VM-Management** application. The project is part of a practical assignment and aims to provide users with an easy-to-use platform for managing virtual machines (VMs). Below are the main features, technologies used, and instructions for deploying the application.

## Overview

The **VM-Management** application allows users to create, edit, and delete virtual machines, with resources like CPU, RAM, HDD, and network settings configurable via a user-friendly interface. The application is built using the Flask framework and MySQL as the database to store VM and user information.

## Features

- **VM Creation**: Users can create virtual machines by configuring settings such as CPU, RAM, storage, and network parameters.
- **VM Editing**: Users can modify existing virtual machines and update their configurations.
- **User Management**: The application supports user registration, login, and management of user accounts.
- **API Integration**: A RESTful API allows external applications to interact with the system, including retrieving VM data in JSON format.

## Technologies Used

- **Flask (Python)**: Web framework used to develop the application.
- **MySQL**: Relational database used to store user and VM data.
- **Docker**: Containerization platform used to deploy the application.
- **NGINX**: Used as a reverse proxy to handle HTTP/HTTPS traffic and provide SSL support.
- **SSL/TLS**: Ensures secure communication between users and the server.

## Deployment Instructions

The application is packaged using Docker, allowing for easy deployment across different environments.

### Prerequisites

- **Docker** and **Docker Compose** installed.
- **MySQL database** configured with the required credentials.

### Steps to Deploy

1. Clone this repository:
   ```bash
   git clone https://github.com/HighTruster/VCID.IA1A-MJK.git
   ```

2. Navigate to the project directory:
   ```bash
   cd VCID.IA1A-MJK
   ```

3. Update the environment variables and configuration files (`conf.env`).
   export MAIL_USERNAME='your mail'
   export MAIL_PASSWORD='your password'
   export MAIL_DEFAULT_SENDER='your mail'


4. Build and start the Docker containers:
   ```bash
   docker compose up --build
   ```

5. Access the application via your browser at `http://localhost` or your configured domain.

## API Endpoints

The following API endpoints are available for external integration:

- **GET /api/vms**: Retrieve a list of all virtual machines.
- **GET /api/users**: Retrieve a list of all registered users.

## Future Enhancements

Planned future features and improvements include:

- **Auto-scaling**: Integration of auto-scaling mechanisms to dynamically adjust resources based on load.
- **CI/CD Integration**: Automating testing and deployment using CI/CD pipelines.
- **Load Balancing**: Integration of load balancing for improved performance and availability.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Author

- Martin Jeremias Künzler
