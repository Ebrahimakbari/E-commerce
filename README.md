## E-commerce Project

This Django-based E-commerce project is designed to provide a robust and scalable online shopping platform. The project leverages various Django applications to manage user accounts, product listings, and order processing. It also utilizes Celery for asynchronous task management and integrates with AWS for storage solutions.

### Table of Contents

- [E-commerce Project](#e-commerce-project)
  - [Table of Contents](#table-of-contents)
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Applications](#applications)
  - [Accounts](#accounts)
  - [Home](#home)
  - [Orders](#orders)
  - [Core](#core)
- [Dependencies](#dependencies)
- [Dockerization](#dockerization)
- [How to Contribute](#how-to-contribute)

## Project Overview

This Django-based E-commerce project is designed to provide a robust and scalable online shopping platform. The project leverages various Django applications to manage user accounts, product listings, and order processing. It also utilizes Celery for asynchronous task management and integrates with AWS for storage solutions.

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone /home/ebrahim/Desktop/projects/django/E-commers
   ```
2. Navigate to the project directory:
   ```bash
   cd E-commers
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database and migrate:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the admin panel at `/admin` and log in with the superuser credentials to manage the site.
- Use the Django shell for testing and managing the application:
  ```bash
  python manage.py shell
  ```

## Applications

### Accounts

Manages user authentication, registration, and profile management. Key files include:
- `models.py`: Defines the `CustomUser` model and `OTP` model.
- `views.py`: Handles user registration, login, and profile views.
- `urls.py`: Routes for account-related pages.
- `management/commands/delete_expired_otps.py`: Custom management command to delete expired OTPs.

### Home

Handles the main website functionality, including product listings and category management. Key files include:
- `models.py`: Defines `Product`, `Category`, and related models.
- `views.py`: Manages product and category views.
- `urls.py`: Routes for the home and product pages.

### Orders

Manages shopping carts, orders, and coupon applications. Key files include:
- `cart.py`: Manages cart operations.
- `models.py`: Defines `Order`, `OrderItem`, `Coupon`, and related models.
- `views.py`: Handles order processing and coupon application.
- `urls.py`: Routes for order and cart pages.

### Core

Contains the main settings and configurations for the Django project. Key files include:
- `settings.py`: Django settings configuration.
- `urls.py`: Main URL routing for the project.
- `celery_conf.py`: Celery configuration for asynchronous tasks.

## Dependencies

The project requires several Python packages, listed in `requirements.txt`:
- Django: Web framework for building the project.
- Celery: Asynchronous task queue/job queue.
- Django-Celery-Beat: Periodic task scheduler for Celery.
- AWS SDKs: For integrating with AWS services like S3 for storage.
- Other various libraries for handling tasks like image processing, database interactions, etc.

## Dockerization

This project can be containerized using Docker. The `docker-compose.yml` file defines the services required to run the project:

- `web`: The Django application.
- `db`: The PostgreSQL database.
- `rabbitmq`: The message broker for Celery.
- `celery`: The Celery worker for asynchronous tasks.
- `redis`: The in-memory data store used by Celery.

To build and run the project using Docker Compose, follow these steps:

1. Ensure Docker is installed on your machine.
2. Build the Docker images and start the services:
   ```bash
   docker-compose up --build
   ```
3. Access the application at `http://localhost:8000`.

## How to Contribute

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m &#39;Add some AmazingFeature&#39;`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

Please note that this `README.md` is based on the provided project structure and files. You may need to adjust the content to accurately reflect the specific setup and structure of your project.