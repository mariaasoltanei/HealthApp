from iotdb.Session import Session

class IoTDBConnection:
    """Encapsulates IoTDB connection and operations."""

    def __init__(self, host='127.0.0.1', port=6667, username='root', password='root'):
        """Initialize the connection settings."""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.session = None

    def connect(self):
        """Establish a connection to the IoTDB server."""
        if not self.session or not self.session.is_open():
            self.session = Session(self.host, self.port, self.username, self.password)
            self.session.open()
            print("Connected to IoTDB")

    def close(self):
        """Close the connection to the IoTDB server."""
        if self.session and self.session.is_open():
            self.session.close()
            print("Disconnected from IoTDB")

    def execute_non_query(self, statement):
        """
        Execute a non-query statement (e.g., CREATE, INSERT).
        
        Args:
            statement (str): The SQL statement to execute.
        """
        self.connect()
        try:
            self.session.execute_non_query_statement(statement)
        except Exception as e:
            print(f"Error executing non-query: {e}")

    def execute_query(self, query):
        """
        Execute a query statement and return the result.

        Args:
            query (str): The SQL query to execute.

        Returns:
            ResultSet: The query result.
        """
        self.connect()
        try:
            return self.session.execute_query_statement(query)
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def insert_record(self, device, timestamp, measurements, values):
        """
        Insert a single record into IoTDB.

        Args:
            device (str): The IoTDB device path.
            timestamp (int): The record timestamp in milliseconds.
            measurements (list): The list of measurement names.
            values (list): The corresponding list of measurement values.
        """
        self.connect()
        try:
            self.session.insert_record(device, timestamp, measurements, values)
        except Exception as e:
            print(f"Error inserting record: {e}")
