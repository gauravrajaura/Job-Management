# Job Management Project

Welcome to the **Job Management Project**! This a walk through for setting up, running, and testing the project. Please Follow these steps to get started.

---

## Project Setup Instructions

### Step 1: Clone the Repository
Clone the project repository to your local machine using the following command:
```bash
git clone https://github.com/gauravrajaura/Job-Management.git
```

### Step 2: Navigate to the Project Directory
Move into the project's root directory where all files are located:
```bash
cd Job-Management
```

### Step 3: Create a Python Virtual Environment
To manage dependencies and avoid conflicts, create a Python virtual environment:
##### For Linux/Mac:
```bash
python3 -m venv myenv
source myenv/bin/activate
```
### Step 4: Install Required Packages
Install all necessary dependencies for the project using the ```requirements.txt``` file:
```bash
pip install -r requirements.txt
```

### Step 5: Run the Django Development Server
Start the Django development server to run the application locally:
```bash
python manage.py runserver
```

---

## API Testing Instructions
### To test the APIs:

Import the provided Postman collection ```/Job management.postman_collection.json``` into your Postman application or follow the postman collection link
Follow the documentation within Postman to test all available endpoints.

[Postman Collection Link](https://assessment-9358.postman.co/workspace/ff4c42e9-f6df-4278-8fa9-c8db354c536c/collection/36416783-d660139c-26c8-45d5-a7e8-e2fa1e25dd92?action=share&source=copy-link&creator=36416783&active-environment=b7be4858-406d-4966-8045-4afc72c78189) <br><br>
[Link to accept an invite for Postman Collection access](https://app.getpostman.com/join-team?invite_code=220c41e8fa5c464de890e90b6335ce88511ea74f3247c978bbdd75cd160f55e5)

--- 

## Running Tests and Viewing Coverage Reports
### Option 1: View Pre-Generated Coverage Report
If a coverage report has already been generated, you can view it directly by running:
```bash
xdg-open htmlcov/index.html
```

### Option 2: Generate a New Coverage Report
If you need to generate a new coverage report, follow these steps:

1. Run the Test Cases
Execute all test cases in the project using:
```bash
coverage run manage.py test
```
2. View Coverage Summary
View the test coverage summary directly in the terminal:
```bash
coverage report
```

3. Generate an HTML Coverage Report
Create a detailed HTML report:
```bash
coverage html
```

4. Open the HTML Report
View the HTML report in your browser:
```bash
xdg-open htmlcov/index.html
```
---

## **Important Notes for Evaluators**

Please consider the following points while evaluating the project:

1. **Environment File**  
   - The project does not include a separate `.env` file for managing sensitive keys and environment variables. All configuration settings are directly included in the project files.

2. **Debug Mode**  
   - The project is currently running in **Debug Mode**. This is not recommended for production environments and is enabled solely for evaluation and development purposes.

3. **Pre-Populated SQLite Database**  
   - The project comes with a pre-populated SQLite database to make evaluation easier. You can directly access the existing data without additional setup.
   - Super Admin's creds are
     ```bash
     username : admin@gmail.com
     password : admin@123
     ```
     
4. **Coverage Files Included**  
   - The project contains pre-generated coverage files to simplify the review process. You can view the test coverage by opening the provided HTML report (`htmlcov/index.html`).

> These points highlight the current state of the project for convenience during evaluation. They can be addressed in future to adhere to production-ready best practices.
