import psycopg2
from psycopg2 import Error

# put in appropriate values for these variables (hard-coded)
from dbInfo import user, password, host, port, database_name

connection = None

# connects to PostgresSQL and checks to see if the database has already been created
# if it has been created, it calls createSchema() to deploy the schema using SQL commands
# if it has not been created, it first creates a database with that name and then calls createSchema()


def init_db(user, password, host, port, database_name):
    global connection
    try:
        # connect to the postgreSQL as specfified in the parameters
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port)
        print('Database connected')
    except Exception as e:
        print("Error while connecting to PostgreSQL " + str(e))

    if connection is not None:
        connection.autocommit = True

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database;")
        list_database = cursor.fetchall()

        # deploys the schema if the database has already been created
        if (database_name,) in list_database:
            createSchema(user, password, host, port, database_name)
        # if the database has not yet been created, create it and then deploy the schema
        else:
            print("'{}' does not exist yet as a database".format(database_name))
            cursor.execute("CREATE DATABASE" + "\"" + database_name + "\"; ")
            print("Database created")
            createSchema(user, password, host, port, database_name)

# connects to specific database that was checked/created in checkIfDatabaseCreated()
# checks whether the tables,indexing, foreign keys, etc. have been set up in the database
# if they have been set up, it closes the connection because no work is needed
# f they have not been set up, it runs SQL commands to fill up the database according to the architecture design


def createSchema(user, password, host, port, database_name):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database_name)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # SQL query to create a new table
        create_table_query = """

                            CREATE TABLE Outlaws (
                                outlawId bigserial NOT NULL,
                                name varchar(128000) NOT NULL PRIMARY KEY,
                                faceData BYTEA NOT NULL
                            );

                            CREATE TABLE Owners (
                                ownerId bigserial NOT NULL,
                                name varchar(128000) NOT NULL PRIMARY KEY,
                                faceData BYTEA NOT NULL
                            );

                            CREATE TABLE Guests (
                                guestId bigserial NOT NULL,
                                name varchar(128000) NOT NULL PRIMARY KEY,
                                faceData BYTEA NOT NULL
                            )
                            """

            # Execute a command: this creates a new table
        cursor.execute(create_table_query)
        connection.commit()
        print("Tables created successfully in PostgreSQL")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL " + str(error) )

    # close the cursor and connection at the end
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def run_init():
    init_db(user, password, host, port, database_name)


# run the function to test
if __name__ == "__main__":
    init_db(user, password, host, port, database_name)
