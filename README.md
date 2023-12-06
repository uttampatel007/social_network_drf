# Social Network Django Rest Application

## Installation Steps

### Prerequisites
- [Python3.9](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)


### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/uttampatel007/social_network_drf.git
    cd social_network_drf
    ```

1. **Run Migrations and Create Superuser**

    ```bash
    python3 manage.py migrate
    python3 manage.py createsuperuser
    ```

2. **Build and Run the Docker Containers**

    ```bash
    docker-compose up --build
    ```

3. **Access the Application**

    Once the containers are up and running, access your Django application in a web browser using [http://localhost:8000](http://localhost:8000).

4. **Additional Notes**

    1- API Collection: https://api.postman.com/collections/11118851-92451450-84e1-4d8c-86eb-7bc68eacdb2b?access_key=PMAT-01HGYZJQ3FR2M2MFYHA64TB3XY

    2- In collection update the token in Authorization to access other apis except login and sign up.

    3- To generate the token use login api.
