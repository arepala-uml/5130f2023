# Description

This is a nodejs application offers signup, login, and a user profile page and runs on 3000 port. It supports validation of email, validation of password constraints, create a user profile in database (writing into users.json file), stores the hashed passwords in users.json, displayng the users location & city, display the weather location and displaying location currency and its units.

## Installation steps

1. Install dependencies:

    ```bash
    cd ~/5130f2023/2023-11-13-lab/server/
    npm install
    ```

2. Run the application: Go inside the server directory and start node js server

    ```bash
    cd ~/5130f2023/2023-11-13-lab/server/
    node server.js
    ```

3. Open the (http://localhost:3000) in the browser

4. Screenshots for each feature under the cd ~/5130f2023/2023-11-13-lab/screenshots directory

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
- `webpages/`: Contains frontend files (HTML, CSS, etc.).

## Other Facts
- After successfull login, provided the user's location, location temperature, location currency information by clicking the other facts button on the page.