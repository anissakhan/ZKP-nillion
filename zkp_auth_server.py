"""The Python implementation of the gRPC zkp authentication server."""

from concurrent import futures
import grpc
import logging
import zkp_auth_pb2
import zkp_auth_pb2_grpc

# temporary local server variables
user_temp_global = "user0"
y1_temp_global = 0
y2_temp_global = 0

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
        user_temp_global=request.user
        y1_temp_global=request.y1
        y2_temp_global=request.y2

        # debug print values
        # return zkp_auth_pb2.RegisterResponse(result = f"registration successful {y1_temp_global=} {y2_temp_global=} {user_temp_global=}")
        return zkp_auth_pb2.RegisterResponse(result = f"registration successful")

    def CreateAuthenticationChallenge(self, request, context):
        """
        "request" param is AuthenticationChallengeRequest that comes from client - r1 and r2
        Return AuthenticationChallengeResponse - c along with an authentication ID (part of the message in proto file)
        """
        pass

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
