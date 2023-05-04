# 関数を選択するための関数
def choose_lambda_function(function_list):
    print("Select a Lambda function from the list:")
    for idx, func in enumerate(function_list):
        print(f"{idx + 1}. {func}")

    choice = int(input("Enter the number of the function you want to invoke: "))
    return function_list[choice - 1]
