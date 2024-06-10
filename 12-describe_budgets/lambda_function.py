import boto3
import json

accountId = "266549158321"


def lambda_handler(event, context):
    session = boto3.Session(profile_name="default")
    client = session.client("budgets")

    try:
        response = client.describe_budgets(AccountId=accountId)
        budgets = response.get("Budgets", [])

        alerts = []
        for budget in budgets:
            budget_name = budget["BudgetName"]
            print(budget_name)

            notification_response = client.describe_notifications_for_budget(
                AccountId=accountId, BudgetName=budget_name
            )
            print(notification_response)
        #     notifications = notification_response.get("Notifications", [])
        #     for notification in notifications:
        #         alerts.append(
        #             {
        #                 "Budget Name": budget_name,
        #                 "Notification": notification,
        #             }
        #         )
        # print(alerts)
        # return {
        #     "statusCode": 200,
        #     "body": json.dumps(alerts),
        # }

    except Exception as e:
        print(f"Error describing budgets: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps("Internal Server Error"),
        }


if __name__ == "__main__":
    lambda_handler({}, {})
