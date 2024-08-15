# DevGrid Weather

The goal of this project is to create an API that interacts with an external weather API to collect data for a list of cities and provide the ability to monitor the progress of this data collection asynchronously.

### Requirements

- **POST**: Receives an ID used to monitor the progress of the request asynchronously. This request should trigger a series of asynchronous calls to the external API to store data from all the cities in the given cities ID list.
- **GET**: Receives the same ID from the previous request and returns the progress of all the requests triggered, showing the percentage of completion for the requested cities.

## Framework Choice

For API-based services, **FastAPI** has been chosen as it offers:

- **Speed**: FastAPI is one of the fastest frameworks for building APIs with Python due to its asynchronous nature and support for ASGI.
- **Modern Features**: It uses Python type hints, automatic generation of interactive API documentation, and supports async and await syntax for asynchronous programming.
- **Scalability**: FastAPI provides an excellent foundation for building scalable applications, handling both small and large applications effectively.

While Flask and Django are popular web frameworks, FastAPI's support for asynchronous operations and modern features make it a superior choice for this challenge, especially when dealing with potentially high volumes of API requests.

## Application Architecture

To manage the complexity of the application, the project is organized into several layers, each with a specific responsibility:

- **Config**: Configuration management for the application, such as environment variables and constants.
- **DB**: Database connection and setup, including session management.
- **Models**: ORM models representing the database schema.
- **Routes**: API endpoints and their respective handlers.
- **Schemas**: Pydantic models used for request validation and response serialization.
- **Services**: Business logic and interaction with external APIs.
- **Tests**: Unit and integration tests to ensure application reliability.
- **Utils**: Utility functions and constants, such as city IDs used throughout the application.

This layered architecture promotes separation of concerns, making the application modular and easier to maintain. Each layer communicates with others via clearly defined APIs or interfaces, ensuring encapsulation and reducing dependencies.

### Why Separate Layers?

- **Modularity**: Each layer can be developed, tested, and maintained independently.
- **Specialization**: Different team members can work on different layers according to their expertise.
- **Scalability**: Layers can be extended or replaced without affecting the entire system, allowing for easy scaling and adaptation to new requirements.
- **Maintainability**: A clean separation between layers helps in tracking down bugs and understanding the system architecture.

### Directory Structure

The project directory is structured to reflect this separation of concerns:

```plaintext
src/
  ├── config/
  ├── db/
  ├── models/
  ├── routes/
  ├── schemas/
  ├── services/
  ├── tests/
  └── utils/
```

Each directory contains an `__init__.py` file to treat the directory as a Python package. This layout allows for easy navigation and clear organization of the project's components, paving the way for future expansions.

## How to Run the Application

To set up and run the application locally, follow these steps:

### 1. Prerequisites

- **Docker** and **Docker Compose**: Used for containerization and to ensure consistent environment setup. Install Docker from the [official Docker website](https://www.docker.com/products/docker-desktop).

### 2. Clone the Repository

```bash
git clone https://github.com/vhsenna/devgrid-weather-challenge.git
```

### 3. Environment Configuration

To ensure the application functions correctly, you need to provide your Open Weather API key. Follow these steps to configure the environment:

1. **Create a `.env` File**: In the root directory of the project, create a file named `.env`.
2. **Add OpenWeather API Key and URL**: Insert the following variables into your `.env` file:

    ```plaintext
    OPEN_WEATHER_API_KEY=your_open_weather_api_key
    OPEN_WEATHER_API_URL=http://api.openweathermap.org/data/2.5/weather
    ```

    **Note**: The URL for the Open Weather API may change based on updates made by Open Weather. Make sure to refer to the [Open Weather API documentation](https://openweathermap.org/api) for the latest endpoint information and any additional configuration requirements.

### 4. Installation

1. **Build the Docker Image**:
   From the root directory of the project, run:

   ```bash
   docker build -t devgrid-weather-challenge .
   ```

2. **Run the Docker Container**:
   Execute the following command to run the application in a Docker container:

   ```bash
   docker run -p 8000:8000 --env-file .env devgrid-weather-challenge
   ```

   This command will start the application and make it accessible at `http://localhost:8000/docs`.

## Example Requests

### Start Data Collection

To initiate the weather data collection process, send a **POST** request to the `/weather/` endpoint with a JSON payload containing a `request_id` field:

```bash
curl -X POST http://localhost:8000/weather/ -H "Content-Type: application/json" -d '{"request_id": "unique_request_id"}'
```

### Check Collection Progress

To retrieve the progress of a data collection job, send a **GET** request to the `/weather/{request_id}` endpoint, replacing `{request_id}` with the ID of the initiated job:

```bash
curl http://localhost:8000/weather/unique_request_id
```

**Note**: Replace `unique_request_id` with a unique identifier for each data collection request.

## How to Test the Application

The project includes unit and integration tests to ensure the functionality and reliability of the application. Here's how you can run them:

### Running Tests

- **Run Tests**:
   Execute the test suite using `pytest`, which will automatically discover and run tests:

   ```bash
   docker compose run tests
   ```

   This command will run all the test cases and provide a detailed report of the results.

### Testing with Coverage

To ensure comprehensive test coverage, you can use the pytest-cov plugin, which integrates with pytest to measure code coverage during your test execution.

```bash
docker compose run --rm coverage
```

This command will display a report highlighting which parts of the codebase are covered by tests and which are not.

Alternatively, you can find an HTML report in the `htmlcov` directory:

- **Locate the Report**:
   ```bash
   ls htmlcov/index.html
   ```

- **Open the Report**: Use a web browser to view detailed insights into your code coverage:
   ```bash
   xdg-open htmlcov/index.html  # Linux
   open htmlcov/index.html      # macOS
   start htmlcov/index.html     # Windows
   ```

This HTML report provides a user-friendly way to navigate through your project's files and visually inspect which lines of code are covered by tests.

## Additional Information

- **Why Use Coverage?**
   Ensuring comprehensive test coverage is crucial for maintaining code quality and reliability. By identifying untested parts of your codebase, you can write additional tests to improve coverage and detect potential bugs early.

- **Customizing Coverage Reports**:
   You can customize the coverage reports by modifying the command in your Docker Compose setup.

- **Continuous Integration (CI)**:
   Integrating coverage checks into your CI pipeline can further enhance your development workflow by automatically enforcing code quality standards across all code changes.

## Troubleshooting

If you encounter issues, check the logs of your Docker container to diagnose the problem:

```bash
docker logs devgrid-weather-challenge
```

You can also view logs of specific services by running:

```bash
docker-compose logs web
docker-compose logs tests
docker-compose logs coverage
```

## API Documentation

FastAPI automatically generates interactive API documentation. You can access it by navigating to the following URL while the application is running:

- **Swagger UI**: `http://localhost:8000/docs`

This interactive documentation page allow you to explore the API endpoints, understand their input/output structures, and test them directly from the browser.
