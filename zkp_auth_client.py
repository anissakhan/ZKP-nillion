"""The Python implementation of the gRPC zkp authentication client."""

import grpc
import logging
import random
import zkp_auth_pb2
import zkp_auth_pb2_grpc

# temporary global client vars; these values don't change so can declare them here
g_global = 4
h_global = 9
x_global = 6
p_global = 23

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = zkp_auth_pb2_grpc.AuthStub(channel)

        # Client registration
        # Client calculates y1 and y2 and sends to server for registration
        y1=(g_global**x_global)%p_global
        y2=(h_global**x_global)%p_global
        register_response = stub.Register(zkp_auth_pb2.RegisterRequest(user="anissa", y1=y1, y2=y2))
        print("Registration result: " + register_response.result)

        # Client authentication request
        # Client generates random 'k', calculates r1, r2 and sends to server to request authentication
        # TODO: try using the secrets library instead to generate x and k? https://docs.python.org/3/library/secrets.html#module-secrets
        # k=random.randint(2,5)
        k=7
        r1=(g_global**k)%p_global
        r2=(h_global**k)%p_global
        print(f"{r1=}, {r2=}")
        auth_req_response=stub.CreateAuthenticationChallenge(zkp_auth_pb2.AuthenticationChallengeRequest(user="anissa", r1=r1, r2=r2))

        if "user does not exist" in auth_req_response.auth_id:
            print("Authentication Request failed. User does not exist.")
        else:
            print(f"Authentication Request accepted. User auth_id is '{auth_req_response.auth_id}'")
            c = auth_req_response.c

            # Client proves identity to complete authentication
            # Client computes 's' using 'c' and sends to server to verify identity
            q=11 #TODO WHAT IS Q
            s=k-c*x_global % q
            auth_verify_response = stub.VerifyAuthentication(zkp_auth_pb2.AuthenticationAnswerRequest(auth_id=auth_req_response.auth_id, s=s))
            if "success" in auth_verify_response.session_id:
                print("Authentication successful.")
            else:
                print("Authentication failed.")



if __name__ == "__main__":
    logging.basicConfig()
    run()

