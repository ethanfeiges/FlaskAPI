# FlaskAPI Setup Guide

This API manages point collection and spending for a singular user. 

## Endpoints

### 1. **Get Balance**
- **URL:** `/balance`
- **Method:** `GET`
- **Description:** Retrieves the current balance of the user.
- **Response:**
    ```json
    {
        "payer1": 100,
        "payer2": 200
    }
    ```

### 2. **Add Points**
- **URL:** `/add`
- **Method:** `POST`
- **Description:** Adds/Subtracts points to the user's account. Can only subtract points if the user's balance does not go negative.
- **Request Body:**
    ```json
    {
        "payer": "payer1",
        "points": 50,
        "timestamp": "2023-10-01T10:00:00Z"
    }
    ```
- **Response:**
    ```json
    {
        "message": "Points added!"
    }
    ```

### 3. **Spend Points**
- **URL:** `/spend`
- **Method:** `POST`
- **Description:** Deducts points from the user's account. Removes the oldest points first.
- **Request Body:**
    ```json
    {
        "points": 30
    }
    ```
- **Response:**
    ```json
    [
        {"payer1": -10},
        {"payer2": -20}
    ]
    ```

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/FlaskAPI.git
    ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install the dependencies:**
    ```bash
    pip install flask, 
    ```

## Running the Application

1. **Ensure the virtual environment is activated.**

2. **Run the Flask application:**
    ```bash
    flask run
    ```


