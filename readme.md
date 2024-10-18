# Mock Vandar Payment Gateway

This project provides a mock implementation of the Vandar payment gateway using FastAPI. It is designed to help developers test their code by simulating the behavior of the actual Vandar payment gateway.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [Initiate Payment (`/send`)](#initiate-payment-send)
  - [Payment Page (`/payment/{token}`)](#payment-page-paymenttoken)
  - [Verify Payment (`/verify`)](#verify-payment-verify)
- [Usage Examples](#usage-examples)
- [Notes](#notes)
- [License](#license)

## Features

- Simulates the initiation of a payment transaction.
- Provides a mock payment page that redirects to a callback URL.
- Allows verification of payment status.
- Easy to set up and customize for testing purposes.

## Prerequisites

- Python 3.7 or higher
- pip package manager

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/mock-vandar-payment-gateway.git
   cd mock-vandar-payment-gateway
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install fastapi uvicorn
   ```

## Running the Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn mock_vandar:app --reload
```

The server will start running at `http://localhost:8000`.

## API Endpoints

### Initiate Payment (`/send`)

- **Method:** `POST`
- **Description:** Initiates a payment and returns a token.
- **Request Body:**

  ```json
  {
    "api_key": "your_valid_api_key",
    "amount": 10000,
    "callback_url": "http://your-callback-url.com/callback",
    "factorNumber": "12345",
    "mobile_number": "09123456789",
    "description": "Test Payment",
    "comment": "No Comment"
  }
  ```

- **Response:**

  ```json
  {
    "status": 1,
    "token": "token_1234"
  }
  ```

- **Errors:**

  - If `api_key` is invalid:

    ```json
    {
      "status": 0,
      "errors": "Invalid API Key"
    }
    ```

### Payment Page (`/payment/{token}`)

- **Method:** `GET`
- **Description:** Simulates the payment page. When accessed, it updates the payment status to "paid" and redirects to the callback URL provided during initiation.
- **URL Parameters:**
  - `token`: The token received from the `/send` endpoint.
- **Behavior:**
  - Updates the payment status to "paid".
  - Redirects to the `callback_url` with the token appended as a query parameter.
- **Example Redirect:**

  ```
  http://your-callback-url.com/callback?token=token_1234
  ```

### Verify Payment (`/verify`)

- **Method:** `POST`
- **Description:** Verifies the payment status.
- **Request Body:**

  ```json
  {
    "api_key": "your_valid_api_key",
    "token": "token_1234"
  }
  ```

- **Response:**

  - If payment is successful:

    ```json
    {
      "status": 1
    }
    ```

  - If payment has failed:

    ```json
    {
      "status": 2
    }
    ```

  - If token is invalid:

    ```json
    {
      "status": 0,
      "errors": "Invalid Token"
    }
    ```

## Usage Examples

### 1. Initiate Payment

Send a `POST` request to `/send` to initiate a payment.

**Request:**

```bash
curl -X POST "http://localhost:8000/send" -H "Content-Type: application/json" -d '{
  "api_key": "your_valid_api_key",
  "amount": 10000,
  "callback_url": "http://localhost:8000/your-callback",
  "factorNumber": "12345",
  "mobile_number": "09123456789",
  "description": "Test Payment",
  "comment": "No Comment"
}'
```

**Response:**

```json
{
  "status": 1,
  "token": "token_5678"
}
```

### 2. Redirect User to Payment Page

Redirect the user to the payment page using the token received.

**URL:**

```
http://localhost:8000/payment/token_5678
```

Upon accessing this URL, the server will simulate the payment process and redirect the user to the callback URL provided earlier, appending the token as a query parameter.

**Redirected URL Example:**

```
http://localhost:8000/your-callback?token=token_5678
```

### 3. Verify Payment

Send a `POST` request to `/verify` to check the payment status.

**Request:**

```bash
curl -X POST "http://localhost:8000/verify" -H "Content-Type: application/json" -d '{
  "api_key": "your_valid_api_key",
  "token": "token_5678"
}'
```

**Response:**

```json
{
  "status": 1
}
```

## Notes

- **API Key Validation:** Replace `"your_valid_api_key"` with the API key expected by your application or modify the validation logic as needed.
- **Data Persistence:** The mock server uses an in-memory dictionary to store payment data. This means all data will be lost when the server restarts. For persistent storage, consider integrating a database.
- **Payment Status Simulation:** The payment status is automatically set to `"paid"` when the `/payment/{token}` endpoint is accessed. You can modify this behavior to simulate different payment outcomes.
- **Callback URL:** Ensure the `callback_url` you provide is accessible and can handle the incoming request with the `token` query parameter.
- **Customization:** Feel free to modify the code to better fit the specific behaviors and responses of the actual Vandar payment gateway for more accurate testing.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

**Disclaimer:** This mock server is intended for testing purposes only and is not affiliated with or endorsed by Vandar. It does not process real payments.