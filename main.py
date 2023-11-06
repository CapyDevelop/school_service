import grpc
import os
from concurrent import futures
from dotenv import load_dotenv
import school_service.school_service_pb2_grpc as school_pb2_grpc

from school_handler import SchoolService


load_dotenv()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    school_pb2_grpc.add_SchoolServiceServicer_to_server(SchoolService(), server)
    server.add_insecure_port(f'[::]:{os.getenv("SCHOOL_GRPC_PORT")}')
    print("start on", os.getenv("SCHOOL_GRPC_PORT"))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()