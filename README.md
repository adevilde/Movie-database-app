## Movie Database Application 

### Description:
This Python application allows users to interact with a movie database. 
Users can search for movies, actors, and more. 
The application provides various search functionalities and displays detailed information about movies and actors.

![Demo of the App](gif_streamlit_imdb_app.gif)

### Prerequisites:
- Python 3.8/3.9/3.10/3.11/3.12

- PostgreSQL database (named `imdb`)

- Required Python libraries: `streamlit`, `pandas`, `psycopg2`

- streamlit can be installed through terminal by using the following command: pip install streamlit

- User can populate the database 'imdb' with data from 'imdb-small.sql' by using the following command : 
  psql -d imdb -f imdb_small.sql


### Structure of the folder
- The folder contains one folder named 'queries' which contains all the queries.
- It also contains the file imdb-app.py file which contains the code executing the queries and the code for streamlit.
- The file named functions.py contains the psycopg2 used to connect to postgres and to execute the queries.

### Execution:
1. Clone the repository and navigate to the project folder:
  ```bash
  git clone https://github.com/adevilde/Movie-database-app.git
  
  cd twitter-climate-change-sentiment
  ```

2. In the terminal write the following command : 
  ```bash
  streamlit run imdb-app.py
  ```

3. Above step should open an application in the user's browser. Otherwise, click on the localhost url given in the terminal.

4. The web app will ask for postgres username and password. User should enter its own username and password to run the application.
   User should keep in mind that each time user will try to reload the application, he/she will have to enter the postgres username and password again.

6. Once the application is running, interact with it through the Streamlit UI.

7. From the dropdown menu, user can select what he wants and/or user can enter IDs or names of what he/she wants to search depending on the previously chosen option. 

