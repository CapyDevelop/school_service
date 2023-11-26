import logging

import school_service.school_service_pb2 as school_pb2
import school_service.school_service_pb2_grpc as school_pb2_grpc

from .auth import get_auth_info
from .gql import get_coalition, get_coins_and_rp, get_user_info, \
    get_users_from_coalition

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - '
                           '%(levelname)s - %(message)s')

class SchoolService(school_pb2_grpc.SchoolServiceServicer):
    def get_school_info(self, request, context):
        logging.info("[ GET SCHOOL INFO ] - Get school info request. ----- START -----")
        auth_info = get_auth_info(request.username, request.password)
        if not auth_info:
            logging.info("[ GET SCHOOL INFO ] - Not such user. ----- END -----")
            return school_pb2.GetSchoolResponse(description="Логин или пароль не подходит")
        logging.info("[ GET SCHOOL INFO ] - Success response from s21. Get coalition. ----- END -----")
        user_info = get_user_info(auth_info.json()["access_token"])
        if not user_info:
            logging.info("[ GET SCHOOL INFO ] - Not such info. ----- END -----")
            return school_pb2.GetSchoolResponse()
        logging.info("[ GET SCHOOL INFO ] - Success get coalition from s21. ----- END -----")
        return school_pb2.GetSchoolResponse(
            access_token=auth_info.json()["access_token"],
            school_user_id=user_info["data"]["user"]["getCurrentUser"]["id"],
            refresh_token=auth_info.json()["refresh_token"],
            session_state=auth_info.json()["session_state"],
            expires_in=auth_info.json()["expires_in"],
            coalition=get_coalition(auth_info.json()["access_token"], user_info["data"]["user"]["getCurrentUser"]["id"])
        )

    def get_rp_info(self, request, context):
        logging.info("[ GET RP INFO ] - Get rp info request. ----- START -----")
        user_info = get_coins_and_rp(request.access_token)
        if not user_info:
            logging.info("[ GET RP INFO ] - Not such info. ----- END -----")
            return school_pb2.GetRpResponse()
        logging.info("[ GET RP INFO ] - Success get rp info from s21. ----- END -----")
        return school_pb2.GetRpResponse(
            coins=user_info["data"]["student"]["getExperience"]["coinsCount"],
            prp=user_info["data"]["student"]["getExperience"]["cookiesCount"],
            crp=user_info["data"]["student"]["getExperience"]["codeReviewPoints"],
            level=user_info["data"]["student"]["getExperience"]["level"]["range"]["levelCode"],
            first_name=user_info["data"]["user"]["getCurrentUser"]["firstName"],
            last_name=user_info["data"]["user"]["getCurrentUser"]["lastName"],
            login=user_info["data"]["user"]["getCurrentUser"]["login"]
        )

    def get_all_members_from_platform(self, request, context):
        logging.info("[ GET ALL MEMBERS FROM PLATFORM ] - Get all members from platform request. ----- START -----")
        tmp_counter = 0
        result = []
        all_users = get_users_from_coalition(request.access_token, request.offset, request.limit)
        if not all_users:
            logging.info("[ GET ALL MEMBERS FROM PLATFORM ] - Not such info. ----- END -----")
            return school_pb2.GetAllMembersFromPlatformResponse(status=1, description="Failure request to platform")

        tmp_counter += len(all_users)
        for user in all_users:
            # logging.info("[ GET ALL MEMBERS FROM PLATFORM ] - Success get user from platform. ----- END -----")
            result.append(school_pb2.Member(login=user["user"]["login"], school_user_id=user["user"]["id"]))
        print("COUNT: ", tmp_counter)
        logging.info("[ GET ALL MEMBERS FROM PLATFORM ] - Success get coalition from s21. ----- END -----")
        return school_pb2.GetAllMembersFromPlatformResponse(members=result, status=0, description="Success")
