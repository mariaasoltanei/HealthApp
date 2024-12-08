from iotdb.Session import Session

# Connect to IoTDB
session = Session("127.0.0.1", 6667, "root", "root")
session.open()

# Query all users
query = "SHOW TIMESERIES root.users.profile;"
result = session.execute_query_statement(query)
# print(result)

print("Users in Database:")
while result.has_next():
    row = result.next()
    timestamp = row.get_timestamp()
    fields = row.get_fields()
    print(fields)
    profile = fields[0].get_string_value()  # Assuming only one field, "profile"
    print(f"Time: {timestamp}, Profile: {profile}")

result.close_operation_handle()
session.close()
