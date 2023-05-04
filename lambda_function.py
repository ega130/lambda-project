def lambda_handler(event, context):
    first_name = event.get('first_name', 'John')
    last_name = event.get('last_name', 'Doe')
    message = f"Hello {first_name} {last_name} from LocalStack Lambda!"
    print(message)

    # contextオブジェクトからリクエストIDと実行時間を取得し、ログに記録
    request_id = context.aws_request_id
    remaining_time = context.get_remaining_time_in_millis()
    print(f"Request ID: {request_id}, Remaining Time: {remaining_time}ms")

    return message
