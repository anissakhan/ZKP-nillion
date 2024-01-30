"""The Python implementation of the gRPC zkp authentication server."""

import grpc
import zkp_auth_pb2
import zkp_auth_pb2_grpc

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
        pass

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

