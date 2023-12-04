# Description

This Node.js application provides signup, login, and a user profile page, running on port 5000. It supports email and password validation, user profile creation (stored in the `users.json` file), stores hashed passwords, and displays user location, weather information, and location currency. It supports PWA part and can download the application.

## Installation steps

1. Install dependencies:

    ```bash
    cd ~/5130f2023/2023-11-27-lab/server/
    npm install
    ```

2. Run the application: Go inside the server directory and start the Node.js server

    ```bash
    cd ~/5130f2023/2023-11-27-lab/server/
    node server.js
    ```

3. Open the [http://localhost:5000](http://localhost:5000) in the browser

4. Download the PWA from the browser for this application and go through the signup, login and other info pages.

4. Screenshots for each feature from downloaded PWA app are under the `cd ~/5130f2023/2023-11-27-lab/screenshots` directory

## Usage

### Signup

- **Endpoint**: `POST /signup`
- **Description**: Register a new user.
- **Request Payload**:
    ```json
    {
        "firstName": "new",
        "lastName": "user",
        "email": "newuser@example.com",
        "password": "password123"
    }
    ```

### Login

- **Endpoint**: `POST /login`
- **Description**: Authenticate a user.
- **Request Payload**:
    ```json
    {
        "email": "newuser@example.com",
        "password": "password123"
    }
    ```

## File Structure

- `server/server.js`: Entry point for the Node.js server.
- `server/users.json`: Database file storing user details.
- `webpages/`: Contains frontend files (HTML, CSS, etc.) and manifest.json,service-worker.js

## Progressive Web App (PWA) Integration

This application has been enhanced to function as a Progressive Web App (PWA). Notable features include:

- **Manifest File**: The addition of a `manifest.json` file providing metadata about the app.
- **Service Worker**: A `service-worker.js` file to enable offline functionality and cache assets.

### Manifest File

The `manifest.json` file contains metadata about the app, enhancing the user experience, and allowing it to be added to the home screen.

### Service Worker

The `service-worker.js` file is responsible for caching assets, providing offline access, and improving overall performance.

## Other Facts
- After successful login, click the "Other Facts" button to view additional information such as the user's location, temperature, and currency details.
