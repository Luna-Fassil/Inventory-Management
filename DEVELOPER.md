# Developer Documentation

This document is intended to guide future developers in understanding the structure, responsibilities, and modification or extension of the system. It includes explanations of core features, system components, and code organization.

## Project Overview

HyperLink is a role-based inventory management system designed to streamline item tracking, user access, and administrative control in an organizational setting. It aims to make inventory tasks intuitive, efficient, and accessible to users with varying levels of permissions.

## Technologies Used  
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python with Flask  
- **Testing:** PyTest & Flask’s test client  
- **Version Control:** Git & GitHub  
- **Video Tools:** ClipChamp (for final demo/tutorial)  

## Key Features  
- Role-based UI rendering (Admin, Manager, Employee access)  
- Add, edit, delete, and search inventory items  
- Filter items by category  
- Sort table columns dynamically  
- Export inventory as CSV  
- Input validation (e.g., no negative quantities)  
- Session and login system with secure access  
- Developer and user documentation included  
- Final demo video to showcase functionality  

## Project Structure

### Detailed Breakdown of Key Directories and Files:

- **`data/`**: Contains JSON files for storing data such as inventory items and users.
  - `inventory.json`: Stores the inventory data in JSON format.
  - `users.json`: Stores user data including credentials and roles.

- **`static/`**: Holds static files for the frontend of the application.
  - **`icons/`**: Contains SVG icon files used throughout the application.
  - **`scripts/`**: JavaScript files to handle dynamic behavior on the frontend.
    - `inventory.js`: JavaScript for managing inventory actions.
    - `login.js`: JavaScript for login page interactions.
    - `settings.js`: JavaScript for settings page actions.
    - `users.js`: JavaScript for managing users.

- **`templates/`**: Stores HTML templates used by Flask to render pages.
  - `inventory.html`: Template for displaying and managing inventory.
  - `login.html`: Template for the user login page.
  - `settings.html`: Template for user settings.
  - `users.html`: Template for managing users.

- **`venv/`**: Virtual environment that contains the Python dependencies for the project.

- **Main Files**:
  - `inventory.py`: The main backend file where the application's core logic resides, including routes and database handling.
  - `run.bat`: Batch file to run the Flask app.
  - `requirements.txt`: Lists the required Python packages for the project.
  - `build.bat`: Batch file to build the project.
  - `.envrc`: Contains environment variable configuration for the project.

- **Tests**:
  - `tests_integration.py`: Integration tests for testing interactions between different system components.
  - `tests_unit.py`: Unit tests for testing individual functions and modules.
  - `test_FlaskApp.py`: Tests for the Flask app functionality.
  - `test_inventory.py`: Tests for inventory-related features.
  - `test_searchTDD.py`: Tests for the search functionality in the system.
  - `test_users.py`: Tests for user management functionality.

---

### How to Set Up and Run the Project:

1. **Clone the Repository**:
   Clone the repository from GitHub:



## Target Users  
- Admins responsible for employee roles and system control  
- Managers and merchandisers needing efficient access to product data  
- Employees with limited, task-specific access  

## Problem Solved / Need Fulfilled  
HyperLink solves the problem of inefficient and unstructured inventory management systems by introducing a user-friendly, permission-based platform that’s easy to maintain and scale. It ensures that users can only access the features relevant to their roles, improving security, usability, and operational flow.