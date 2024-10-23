from iotdb.Session import Session

class IoTDBConnection:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.session = None

    def connect(self):
        """Establish connection to IoTDB."""
        self.session = Session(self.host, self.port, self.username, self.password)
        self.session.open(False)  # Set False for non-encryption
        print(f"Connected to IoTDB at {self.host}:{self.port}")

    def close(self):
        """Close the connection to IoTDB."""
        if self.session:
            self.session.close()
            print("IoTDB session closed.")

    def execute_query(self, query: str):
        """Execute a query on IoTDB and return the result."""
        if not self.session:
            raise ConnectionError("Not connected to IoTDB.")
        result = self.session.execute_query_statement(query)
        return result
