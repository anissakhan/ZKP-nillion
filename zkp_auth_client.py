"""The Python implementation of the gRPC zkp authentication client."""

import grpc
import logging
import zkp_auth_pb2
import zkp_auth_pb2_grpc

# temporary global client vars
g_temp_global = 9
h_temp_global = 3
x_temp_global = 2

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = zkp_auth_pb2_grpc.AuthStub(channel)

        # calculate y1 and y2 using x here, before send in Registration?
        y1=g_temp_global**x_temp_global
        y2=h_temp_global**x_temp_global
        register_response = stub.Register(zkp_auth_pb2.RegisterRequest(user="anissa", y1=y1, y2=y2))
        print("Registration result: " + register_response.result)


if __name__ == "__main__":
    logging.basicConfig()
    run()

