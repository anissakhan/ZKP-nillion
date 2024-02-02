"""The Python implementation of the gRPC zkp authentication server."""

from concurrent import futures
import grpc
import json
import logging
import random
import zkp_auth_pb2
import zkp_auth_pb2_grpc

# temporary local server variables
# user_global="user0"
# y1_global=0
# y2_global=0
# r1_global=0
# r2_global=0
g_global=4
h_global=9
p_global=23

class AuthServicer(zkp_auth_pb2_grpc.AuthServicer):
    """Provides methods that implement functionality of zkp auth server."""



    def Register(self, request, context):
        """
        Param = RegisterRequest
        Returns RegisterResponse

        "request" param is RegisterRequest that comes from the client - y1, y2
        Return a string to the client that says "registered successfully"?

        TODO: add more info to docstrings
        """

        # Store y1 and y2 on the server's "db"
        user_entry={
            "user": request.user,
            "y1": request.y1,
            "y2": request.y2
        }

        # Open the file in read mode to get the existing content
        with open("server_user_db.json", "r") as server_user_db_file:
            # Load the existing entries
            existing_entries=json.load(server_user_db_file)

        # Check if the user already exists
        existing_users=[entry["user"] for entry in existing_entries]
        if user_entry["user"] in existing_users:
            print(f"User '{user_entry['user']}' already exists.")
        else:
            # Append the new entry to the existing entries
            existing_entries.append(user_entry)

            # Open the file in write mode and write the updated entries
            with open("server_user_db.json", "w") as server_user_db_file:
                # Write the updated entries to the file
                json.dump(existing_entries, server_user_db_file, indent=2)

        # Server sends back validation message that the registration was successful
        return zkp_auth_pb2.RegisterResponse(result = f"registration successful")

    def CreateAuthenticationChallenge(self, request, context):
        """
        "request" param is AuthenticationChallengeRequest that comes from client - r1 and r2
        Return AuthenticationChallengeResponse - c along with an authentication ID (part of the message in proto file)
        """

        user = request.user
        r1=request.r1
        r2=request.r2
        # c_global=random.randint(2, 5) # TODO: What should the random value be selected from...does it matter?
        c=4

        # array to store auth_ids
        global local_user_info
        # TODO: generate the user id using the secrets library; does it matter if a user is already in this list?
        local_user_info=[{"user": user, "auth_id": user+"temp", "r1": r1, "r2": r2, "c": c}]


        # Open the file in read mode to get the existing content
        with open("server_user_db.json", "r") as server_user_db_file:
            existing_entries=json.load(server_user_db_file)

        # Check if the user already exists
        existing_users=[entry["user"] for entry in existing_entries]
        if user in existing_users:
            return zkp_auth_pb2.AuthenticationChallengeResponse(auth_id=user+"temp", c=c) # TODO: what value should auth_id be?
        else:
            # TODO What do I return if the user does not exist in the database as a registered user? Unable to return None here
            return zkp_auth_pb2.AuthenticationChallengeResponse(auth_id="user does not exist", c=0)

    def VerifyAuthentication(self, request, context):
        """
        "request" param is AuthenticationAnswerRequest that comes from client - s calculated
        Return AuthenticationAnswerResponse - calculate r1 and r2 and verify it matches the original values and then respond with a session id if successful and nothing if not?
        """

        # Server verifies client by checking r1 and r2 using 's'

        # TODO: server needs to find the right
        # user to look up their y1 and y2 in the db
        # but they get the auth_id from the user,
        # not their username (username is stored in the db)

        # initialize user specific vars stored locally on the server
        user=""
        y1=-1
        y2=-1
        c=-1
        r1_from_user=-1
        r2_from_user=-1

        auth_id=request.auth_id
        s=request.s

        # find the auth_id in the local_user_info array to find the user
        for user_info in local_user_info:
            if user_info["auth_id"]==auth_id:
                user=user_info["user"]
                c=user_info["c"]
                r1_from_user=user_info["r1"]
                r2_from_user=user_info["r2"]

        # then get y1 and y2 from the db
        with open("server_user_db.json", "r") as server_user_db_file:
            existing_entries = json.load(server_user_db_file)

        for entry in existing_entries:
            if entry["user"]==user:
                y1=entry["y1"]
                y2=entry["y2"]

        r1=((g_global**s)*(y1**c))%p_global
        r2=(h_global**s)*(y2**c)%p_global

        if r1==r1_from_user and r2==r2_from_user:
            return zkp_auth_pb2.AuthenticationAnswerResponse(session_id="success") # TODO: make this more unique?
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
