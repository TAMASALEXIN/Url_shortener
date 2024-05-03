This is a simple URL shortener application built with Flask and SQLAlchemy.

## Features

- Shorten URL: You can shorten your URL by sending a POST request to the `/shorten` endpoint with the URL in the request body. You can optionally provide a shortcode, if not, one will be generated for you.
- Redirect: You can use the shortened URL to redirect to the original URL by sending a GET request to the `/<shortcode>` endpoint.
- Stats: You can get the stats of a shortcode by sending a GET request to the `/<shortcode>/stats` endpoint. It will return the creation time, last redirect time, and the redirect count.

## Usage

1. **Environment Setup**: First, you need to set up a Python virtual environment. This can be done using the following commands:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

2. **Install Dependencies**: Next, install the necessary Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Environment Variables**: You need to set the `DATABASE_URI` environment variable to the URI of your database. If you're using SQLite, this could be a file path. For example:

    ```bash
    export DATABASE_URI=sqlite:///database.db  # On Windows, use `set DATABASE_URI=sqlite:///database.db`
    ```

4. **Initialize the Database**: Run the application once to initialize the database:

    ```bash
    python app.py
    ```

    Note: When you run the server with `python app.py`, it will be running on port 8000.

5. **Run the Server**: Finally, start the Flask development server:

    ```bash
    flask run
    ```

    Note: When you run the server with `flask run`, it will be running on port 5000.

Now, your application should be running at `http://localhost:5000` or `http://localhost:8000` depending on how you started it. You can interact with it using the `/shorten`, `/<shortcode>`, and `/<shortcode>/stats` endpoints.

Remember to replace the commands with the appropriate ones for your operating system if you're not using a Unix-like system.

## API Documentation

This API uses Swagger UI for documentation and testing purposes. Once the application is running, you can view the Swagger UI and interact with the API by navigating to the `/apidocs` endpoint in your web browser.

Each endpoint is documented in the Swagger UI, including the expected inputs and responses.

The API includes an error handler for server errors (HTTP 500). If a server error occurs, the API will return a JSON response with the error message and a `500` status code. Note that error handlers are not directly invoked by the user, but are triggered by the application in response to an error.

## API

### Shorten URL

**Endpoint:** `/shorten`

**Method:** `POST`

**Data Params:** 

```json
{
    "url": "[valid url]",
    "shortcode": "[optional shortcode]"
}
```

**Success Response:**

- **Code:** 201
- **Content:** `{ "shortcode" : "your_shortcode" }`

### Redirect

**Endpoint:** `/<shortcode>`

**Method:** `GET`

**Success Response:**

- **Code:** 302
- **Content:** Redirects to the original URL.

### Get Stats

**Endpoint:** `/<shortcode>/stats`

**Method:** `GET`

**Success Response:**

- **Code:** 200
- **Content:** 

```json
{
    "created": "creation_time",
    "lastRedirect": "last_redirect_time",
    "redirectCount": "redirect_count"
}
```

## Dependencies

- Flask
- Flask-SQLAlchemy
- Python's built-in datetime, string, random, and os modules.

## Application Structure

- `app.py`: This is the main file that runs the Flask application. It sets up the routes for the `/shorten`, `/<shortcode>`, and `/<shortcode>/stats` endpoints.

## Testing

- `test_app.py`: This file contains the unit tests for the application. To run the tests, use the following command:

    ```bash
    python -m unittest test_app.py
    ```

The tests cover the following scenarios:

- Shortening a URL without providing a shortcode
- Shortening a URL with a provided shortcode
- Redirecting using a shortcode
- Getting the stats of a shortcode