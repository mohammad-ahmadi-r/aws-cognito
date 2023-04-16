import aws_cdk as core
import aws_cdk.assertions as assertions

from 05_cognito.05_cognito_stack import 05CognitoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in 05_cognito/05_cognito_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = 05CognitoStack(app, "05-cognito")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
