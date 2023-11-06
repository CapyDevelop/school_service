import school_service.school_service_pb2 as school_pb2
import school_service.school_service_pb2_grpc as school_pb2_grpc

from .auth import get_auth_info
from .gql import get_user_info, get_coalition


class SchoolService(school_pb2_grpc.SchoolServiceServicer):
    def get_school_info(self, request, context):
        auth_info = get_auth_info(request.username, request.password)
        if not auth_info:
            return school_pb2.GetSchoolResponse(description="Логин или пароль не подходит")
        user_info = get_user_info(auth_info.json()["access_token"])
        print(user_info)
        if not user_info:
            return school_pb2.GetSchoolResponse()
        return school_pb2.GetSchoolResponse(
            access_token=auth_info.json()["access_token"],
            school_user_id=user_info["data"]["user"]["getCurrentUser"]["id"],
            refresh_token=auth_info.json()["refresh_token"],
            session_state=auth_info.json()["session_state"],
            expires_in=auth_info.json()["expires_in"],
            coalition=get_coalition(auth_info.json()["access_token"], user_info["data"]["user"]["getCurrentUser"]["id"])
        )
