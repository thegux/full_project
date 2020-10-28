# Full Stack Capstone

## Getting Started

### Pre-requisites

In order to run this project properly, make sure you have the following installed:
  * Python 3
  * Flask
  * SQL Alchemy
  * Jose - python-jose

## In case of offline use: Initial Setup (Windows Based)
  1. Install the dependencies:
      ```
      pip install -r requirements.txt
      ```
  2. Run the app
      ```
      flask run
      ```
      
  
## API Reference (Windows Based)
 * This project was intended to run virtually, thus the backend is hosted at the default ```https://https://full-project-udacity.herokuapp.com/```.
 * Authentication: This application uses Auth0 authentication and permission will be granted as users sign-in.

### Error Handling
The errors in this application are returned as JSON objects in the following format:
```
        {
          "success": False,
          "error": 404,
          "message": "Not found"
        }
```

This API handles the following errors:
* 400 - Bad Request
* 404 - Not Found
* 422 - Unprocessable Entity
* 500 - Internal Server Error



### Endpoints
There are 10 endpoints in this Application:
  1. GET/COMPANIES
  2. GET/JOBS
  3. POST/COMPANY
  4. POST/JOB
  5. PATCH/COMPANY/COMPANY_ID
  6. PATCH/JOB/JOB_ID
  7. DELETE/COMPANY/COMPANY_ID
  8. DELETE/JOB/JOB_ID
  9. GET/CANDIDATES/JOB_ID
  10. POST/CANDIDATE/APPLY
    
You can test them and check the documentation specific for each endpoint by using the postman collection located at the src folder.
In case you run into errors while testing, make sure you're using valid company and job ids. 
