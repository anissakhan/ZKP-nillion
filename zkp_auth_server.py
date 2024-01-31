"""The Python implementation of the gRPC zkp authentication server."""

from concurrent import futures
import grpc
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
c_global=0

class AuthServicer(zkp_auth_pb2_grpc.AuthServicer):
    """Provides methods that implement functionality of zkp auth server."""



    def Register(self, request, context):
        """
        Param = RegisterRequest
        Returns RegisterResponse

        "request" param is RegisterRequest that comes from the client - y1, y2
        Return a string to the client that says "registered successfully"?

        question: where to store y1 and y2
        """

        # temporary globals
        global user_global
        global y1_global
        global y2_global

        # Store y1 and y2 on the server
        user_global=request.user
        y1_global=request.y1
        y2_global=request.y2

        # debug print values
        # return zkp_auth_pb2.RegisterResponse(result = f"registration successful {y1_temp_global=} {y2_temp_global=} {user_temp_global=}")

        # Server sends back validation message that the registration was successful
        return zkp_auth_pb2.RegisterResponse(result = f"registration successful")

    def CreateAuthenticationChallenge(self, request, context):
        """
        "request" param is AuthenticationChallengeRequest that comes from client - r1 and r2
        Return AuthenticationChallengeResponse - c along with an authentication ID (part of the message in proto file)
        """

        # temporary global variables
        global r1_global
        global r2_global

        user = request.user
        r1_global=request.r1
        r2_global=request.r2
        c_global=random.randint(2, 5) # TODO: What should the random value be selected from...does it matter?

        # TODO when add database, use user value to look up in the table for that user instead of comparing user==user_temp_global. If user doesn't exist in the database, return None
        if user==user_global:
            return zkp_auth_pb2.AuthenticationChallengeResponse(auth_id="anissa", c=c_global) # TODO: what value should auth_id be?
        else:
            # TODO What do I return if the user does not exist in the database as a registered user? Unable to return None here
            return zkp_auth_pb2.AuthenticationChallengeResponse(auth_id="user does not exist", c=0)

    def VerifyAuthentication(self, request, context):
        """
        "request" param is AuthenticationAnswerRequest that comes from client - s calculated
        Return AuthenticationAnswerResponse - calculate r1 and r2 and verify it matches the original values and then respond with a session id if successful and nothing if not?
        """
        pass

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
