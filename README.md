<h1 align="center"> Currency converter </h1>

<p align="center">
  <a href="https://github.com/Yu-Leo/currency-converter/blob/main/LICENSE" target="_blank"> <img alt="license" src="https://img.shields.io/github/license/Yu-Leo/currency-converter?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/currency-converter/releases/latest" target="_blank"> <img alt="last release" src="https://img.shields.io/github/v/release/Yu-Leo/currency-converter?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/currency-converter/commits/main" target="_blank"> <img alt="last commit" src="https://img.shields.io/github/last-commit/Yu-Leo/currency-converter?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/currency-converter/graphs/contributors" target="_blank"> <img alt="commit activity" src="https://img.shields.io/github/commit-activity/m/Yu-Leo/currency-converter?style=for-the-badge&labelColor=090909"></a>
</p>

<hr>

## Navigation

* [Project description](#chapter-0)
* [Interface](#chapter-1)
* [Getting started](#chapter-2)
* [Source code](#chapter-3)
* [License](#chapter-5)

<a id="chapter-0"></a>

## :page_facing_up: Project description

Simple currency converter website.

Using [exchangerate-api.com](https://www.exchangerate-api.com/)

<a id="chapter-1"></a>

## :camera: Interface

![main_page](./docs/img/main_page.jpg)

<a id="chapter-2"></a>

## :hammer: Getting started

1. Download this repository
    * Option 1
        1. Install [git](https://git-scm.com/download)
        2. Clone this repository
        ```bash
        git clone https://github.com/Yu-Leo/currency-converter.git
        cd currency-converter
        ```
    * Option 2
        - [Download ZIP](https://github.com/Yu-Leo/currency-converter/archive/refs/heads/main.zip)
2. Config [required environment variables](#envvars)
    - Create `.env` file with values for **production** mode
    - Create `.env.dev` file with values for **development** mode

Now you can:

- Run in **production** mode using docker-compose
- Run in **development** mode using docker-compose
- Configure for development on local machine

### Run in **production** mode using docker-compose:

```bash
docker-compose up --build
```

### Run in **development** mode using docker-compose:

```bash
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build
```

### Configure for development in local machine:

1. Create a virtual environment in the project repository
    ```bash
    python3 -m venv venv
    ```
2. Activate the virtual environment
    ```bash
    source venv/bin/activate
    ```
3. Install project dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Run the server on a local machine
    ```bash
    cd converter
    python manage.py runserver
    ```

<a id="chapter-3"></a>

## :computer: Source code

### [Technical documentation](./docs/README.md)

### :wrench: Technologies

#### BackEnd:

- Programming language: **Python (3.10.4)**
- Frameworks and libraries:
    - **Django (4.0.5)**
    - **Requests (2.28.1)**

#### FrontEnd:

- Language: **html**, **css**
- Frameworks and libraries:
    - **Bootstrap 5**

#### Tools:

- Docker and Docker Compose

### :wrench: Settings

#### Required environment variables:

- `DJANGO_DEBUG` - Run in DEBUG mode or not (set 1 or 0). Default 0.
- `DJANGO_SECRET_KEY` - SECRET_KEY for the Django config

#### config/settings.py

- `EXCHANGE_RATE_API_URL` - link to the exchange rate API

### :coffee: Tests

Run all tests (run in the outer `converter` folder):

```bash
./manage.py test converter.tests
```

Using `coverage`:

```bash
coverage run ./manage.py test converter.tests
```

With report page generation:

```bash
coverage run ./manage.py test converter.tests && coverage html
```

<a id="chapter-5"></a>

## :open_hands: License

If you use my code, put a star ⭐️ on the repository

Author: [Yu-Leo](https://github.com/Yu-Leo)

GNU General Public License v3.0

Full text in [LICENSE](LICENSE)
