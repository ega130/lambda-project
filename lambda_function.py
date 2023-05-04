def lambda_handler(event, context):
    message = "Hello from LocalStack Lambda!"
    print(message)
    return message
