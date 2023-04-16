from aws_cdk import (
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as apigw_integrations,
    aws_cognito as cognito,
    aws_lambda as lambda_,
    core,
)


class CognitoStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a user pool with a client and domain
        user_pool = cognito.UserPool(
            self, "UserPool",
            self_signup_enabled=True,
            user_pool_name="my-user-pool",
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_digits=True,
                require_symbols=True,
                require_uppercase=True,
            )
        )
        
        user_pool_client = user_pool.add_client(
            "UserPoolClient",
            auth_flows=cognito.AuthFlow(
                admin_user_password=True,
                user_srp=True,
            )
        )
        
        domain = user_pool.add_domain(
            "UserPoolDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix="my-user-pool"
            )
        )

        # Define two Lambda functions for sign up and sign in
        signup_function = lambda_.Function(
            self, "SignUpFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="signup.handler",
            code=lambda_.Code.from_asset("lambdas/code/"),
            environment={
                "USER_POOL_ID": user_pool.user_pool_id,
                "USER_POOL_CLIENT_ID": user_pool_client.user_pool_client_id,
            }
        )

        signin_function = lambda_.Function(
            self, "SignInFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="signin.handler",
            code=lambda_.Code.from_asset("lambdas/code/"),
            environment={
                "USER_POOL_ID": user_pool.user_pool_id,
                "USER_POOL_CLIENT_ID": user_pool_client.user_pool_client_id,
            }
        )

        # Create an HTTP API and add two routes for sign up and sign in
        api = apigw.HttpApi(
            self, "HttpApi",
            default_integration=apigw_integrations.LambdaProxyIntegration(
                handler=signin_function
            )
        )

        api.add_routes(
            path="/signup",
            methods=[apigw.HttpMethod.POST],
            integration=apigw_integrations.LambdaProxyIntegration(
                handler=signup_function
            )
        )

        api.add_routes(
            path="/signin",
            methods=[apigw.HttpMethod.POST],
            integration=apigw_integrations.LambdaProxyIntegration(
                handler=signin_function
            )
        )

        """ # Output the URL of the HTTP API
        core.CfnOutput(
            self, "ApiUrl",
            value=api.url!,
            export_name="ApiUrl"
        ) """
    
    
    