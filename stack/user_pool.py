from aws_cdk import (
    aws_cognito as cognito
)
import aws_cdk as cdk
from constructs import Construct

class CognitoStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a user pool with a client and domain
        user_pool = cognito.UserPool(
            self, "UserPool",
            self_sign_up_enabled=True,
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
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    implicit_code_grant=True
                ),
            callback_urls=["https://google.com"],
            #prevent_user_existence_errors=True,
            #auth_session_validity=Duration.minutes(15),
            #generate_secret=True
            #logout_urls=["https://my-app-domain.com/signin"]
            #auth_flows=cognito.AuthFlow(
            #    admin_user_password=True,
            #    user_srp=True,
            )
        )

        
        domain = user_pool.add_domain(
            "UserPoolDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix="myfastpic"
            )
        )
        sign_in_url = domain.sign_in_url(user_pool_client,
            redirect_uri="https://google.com"
        )
        """ # Output the URL of the HTTP API
        core.CfnOutput(
            self, "ApiUrl",
            value=api.url!,
            export_name="ApiUrl"
        ) """
    
    
    
