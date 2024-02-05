"""
File: zkp_auth_server.py
Author: Anissa Khan
Date: February 5, 2024
Description: The Python implementation of the gRPC zkp authentication server.
"""
"""The Python implementation of the gRPC zkp authentication server."""

from concurrent import futures
from typing import Optional
import grpc
import json
import logging
import random
import secrets
import zkp_auth_pb2
import zkp_auth_pb2_grpc

# global server variables; p, g, h assumed to be public information
p_global=179 # 100043
g_global=65 # 4453
h_global=29 # 3459
local_user_info=[]

# Helper methods
def read_write_user_db(
        mode: str,
        existing_entries: Optional[list[dict]]=[]
    )->list[dict]:
    """
    Open the json file containing user data to read or write content to the server's "database" of users.

    Args:
        mode (str): either "r" or "w" to indicate read or write mode, respectively
    Returns:
        list[dict]: If mode="r", returns list of dictionaries containing information about users.
            Example: [{'user': 'Anissa', 'y1': 22, 'y2': 12}]
            If mode="w", nothing to return
    """

    with open("server_user_db.json", mode) as server_user_db_file:
        if "r" in mode:
            # Load the existing entries
            existing_entries=json.load(server_user_db_file)
            return existing_entries
        else:
            # Write the updated entries to the file
            json.dump(existing_entries, server_user_db_file, indent=2)



class AuthServicer(zkp_auth_pb2_grpc.AuthServicer):
    """Provides methods that implement functionality of zkp auth server."""

    def Register(self, request, context):
        """
        Server receives a registration request from the client and responds.

        Args:
            request (RegisterRequest): RegisterRequest is received from the client and contains 'user', 'y1', 'y2'
        Returns:
            RegisterResponse: returned message contains 'result' which indicates either registration successful, or user already exists.
        """

        # Store y1 and y2 on the server's "db" (json file used to simulate a db)
        user_entry={
            "user": request.user,
            "y1": request.y1,
            "y2": request.y2
        }

        existing_entries=read_write_user_db(mode="r")

        # Check if the user already exists
        existing_users=[entry["user"] for entry in existing_entries]
        if user_entry["user"] in existing_users:
            return zkp_auth_pb2.RegisterResponse(result = f"User '{user_entry['user']}' already exists.")
        else:
            # Append the new entry to the existing entries
            existing_entries.append(user_entry)

            # Open the file in write mode and write the updated entries
            read_write_user_db(mode="w", existing_entries=existing_entries)

        # Server sends back message that the registration was successful
        return zkp_auth_pb2.RegisterResponse(result = f"registration successful")

    def CreateAuthenticationChallenge(self, request, context):
        """
        Server receives an authentication request from the client, and returns an authentication challenge.

        Args:
            request (AuthenticationChallengeRequest): AuthenticationChallengeRequest is received from the client and contains 'r1', 'r2'
        Returns:
            AuthenticationChallengeResponse: returned message contains 'auth_id' and 'c' as part of a challenge necessary for client to prove identity.
                If user does not exist, returns failure message.
        """

        user = request.user
        r1=request.r1
        r2=request.r2
        c=secrets.randbelow(99)

        # array to store auth_ids and other session specific user info to account for concurrent auth requests
        global local_user_info
        id=secrets.randbelow(90000)+10000
        local_user_info.append(
            {"user": user,
             "auth_id": f"{id}",
             "r1": r1,
             "r2": r2,
             "c": c}
             )

        existing_entries=read_write_user_db(mode="r")

        # Check if the user already exists
        existing_users=[entry["user"] for entry in existing_entries]
        if user in existing_users:
            return zkp_auth_pb2.AuthenticationChallengeResponse(auth_id=f"{id}", c=c)
        else:
            return zkp_auth_pb2.AuthenticationChallengeResponse(auth_id="user does not exist", c=-1)

    def VerifyAuthentication(self, request, context):
        """
        Server verifies client by checking r1 and r2 using 's'

        Server receives client's response to the authentication challenge and verifies identity for either successful or failed authentication.

        Args:
            request (AuthenticationAnswerRequest): AuthenticationAnswerRequest is received from client and contains 'auth_id' and 's',
                where 's' is the response to the authentication challenge
        Returns:
            AuthenticationAnswerResponse: returned message contains a session_id. If authentication succeeds, session_id is a numerical value
                stored in a string. Otherwise, "fail"

        """

        # initialize user specific vars stored locally on the server
        user=""
        y1=-1
        y2=-1
        c=-1
        r1_from_user=-1
        r2_from_user=-1

        auth_id=request.auth_id
        s=request.s

        # find the auth_id in the local_user_info array to find the username and other relevant info
        for user_info in local_user_info:
            if user_info["auth_id"]==auth_id:
                user=user_info["user"]
                c=user_info["c"]
                r1_from_user=user_info["r1"]
                r2_from_user=user_info["r2"]

        # then get y1 and y2 from the "db"
        existing_entries = read_write_user_db(mode="r")

        for entry in existing_entries:
            if entry["user"]==user:
                y1=entry["y1"]
                y2=entry["y2"]

        # server calculates r1 and r2; verify they match the original value passed by the client
        r1=(pow(g_global,s)*pow(y1, c))%p_global
        r2=(pow(h_global,s)*pow(y2,c))%p_global

        if r1==r1_from_user and r2==r2_from_user:
            return zkp_auth_pb2.AuthenticationAnswerResponse(session_id=f"{random.randint(10000, 99999)}")
        else:
            return zkp_auth_pb2.AuthenticationAnswerResponse(session_id="fail")

# Start the GRPC service via serve() method
def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    zkp_auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
