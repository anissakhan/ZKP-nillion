"""
File: zkp_auth_client.py
Author: Anissa Khan
Date: February 5, 2024
Description: The Python implementation of the gRPC zkp authentication client.
"""

import grpc
import logging
import secrets
import sys
import zkp_auth_pb2
import zkp_auth_pb2_grpc

# global client vars; p, g, h assumed to be public information
p_global = 179 # 100043
g_global = 65 # 4453
h_global = 29 # 3459
x=-1

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = zkp_auth_pb2_grpc.AuthStub(channel)

        # Get command line args
        n = len(sys.argv)
        if n<2:
                print("Usage: python zkp_auth_client.py <action>")
                print("  - action: 'register'/'reg' or 'authenticate'/'auth'")
                sys.exit(1)

        action=sys.argv[1]
        valid_actions = ["register", "reg", "authenticate", "auth"]
        if action in valid_actions:
            user=input("Input username: ")
        else:
            print("Action invalid")
            print("Usage: python script_name.py <action>")
            print("  - action: 'register' or 'authenticate'")
            sys.exit(1)

        # Client registration
        if action == "register" or action=="reg":
            # Client calculates y1 and y2 and sends to server for registration
            x=input("Input numerical password (number between 1 and 9999999): ")
            x=int(x)
            y1=pow(g_global, x, p_global)
            y2=pow(h_global, x, p_global)
            register_response = stub.Register(zkp_auth_pb2.RegisterRequest(user=user, y1=y1, y2=y2))
            print("Registration result: " + register_response.result)
        # Client authentication request
        elif action == "authenticate" or action=="auth":
            # Client generates random 'k', calculates r1, r2 and sends to server to request authentication
            x=input("Input numerical password used during registration (number between 1 and 9999999): ")
            x=int(x)
            k=secrets.randbelow(99)
            r1=pow(g_global, k, p_global)
            r2=pow(h_global, k, p_global)
            auth_req_response=stub.CreateAuthenticationChallenge(zkp_auth_pb2.AuthenticationChallengeRequest(user=user, r1=r1, r2=r2))

            if "user does not exist" in auth_req_response.auth_id:
                print("Authentication Request failed. User does not exist. You must register first.")
            else:
                print(f"Authentication Request accepted.")
                c = auth_req_response.c

                # Client proves identity to complete authentication
                # Client computes 's' using 'c' and sends to server to verify identity
                q=89 # 50021
                s=(k-c*x) % q
                auth_verify_response = stub.VerifyAuthentication(zkp_auth_pb2.AuthenticationAnswerRequest(auth_id=auth_req_response.auth_id, s=s))
                if "fail" not in auth_verify_response.session_id:
                    print("Authentication successful.")
                else:
                    print("Authentication failed.")
        else:
            print("Action failed.")
            sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig()
    run()

