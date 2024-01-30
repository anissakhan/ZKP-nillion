# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import zkp_auth_pb2 as zkp__auth__pb2


class AuthStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Register = channel.unary_unary(
                '/zkp_auth.Auth/Register',
                request_serializer=zkp__auth__pb2.RegisterRequest.SerializeToString,
                response_deserializer=zkp__auth__pb2.RegisterResponse.FromString,
                )
        self.CreateAuthenticationChallenge = channel.unary_unary(
                '/zkp_auth.Auth/CreateAuthenticationChallenge',
                request_serializer=zkp__auth__pb2.AuthenticationChallengeRequest.SerializeToString,
                response_deserializer=zkp__auth__pb2.AuthenticationChallengeResponse.FromString,
                )
        self.VerifyAuthentication = channel.unary_unary(
                '/zkp_auth.Auth/VerifyAuthentication',
                request_serializer=zkp__auth__pb2.AuthenticationAnswerRequest.SerializeToString,
                response_deserializer=zkp__auth__pb2.AuthenticationAnswerResponse.FromString,
                )


class AuthServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAuthenticationChallenge(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyAuthentication(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=zkp__auth__pb2.RegisterRequest.FromString,
                    response_serializer=zkp__auth__pb2.RegisterResponse.SerializeToString,
            ),
            'CreateAuthenticationChallenge': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAuthenticationChallenge,
                    request_deserializer=zkp__auth__pb2.AuthenticationChallengeRequest.FromString,
                    response_serializer=zkp__auth__pb2.AuthenticationChallengeResponse.SerializeToString,
            ),
            'VerifyAuthentication': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyAuthentication,
                    request_deserializer=zkp__auth__pb2.AuthenticationAnswerRequest.FromString,
                    response_serializer=zkp__auth__pb2.AuthenticationAnswerResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'zkp_auth.Auth', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Auth(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/zkp_auth.Auth/Register',
            zkp__auth__pb2.RegisterRequest.SerializeToString,
            zkp__auth__pb2.RegisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAuthenticationChallenge(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/zkp_auth.Auth/CreateAuthenticationChallenge',
            zkp__auth__pb2.AuthenticationChallengeRequest.SerializeToString,
            zkp__auth__pb2.AuthenticationChallengeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VerifyAuthentication(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/zkp_auth.Auth/VerifyAuthentication',
            zkp__auth__pb2.AuthenticationAnswerRequest.SerializeToString,
            zkp__auth__pb2.AuthenticationAnswerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
