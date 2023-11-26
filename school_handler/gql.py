import requests


def get_user_info(access_token):
    session = requests.Session()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "schoolid": "6bfe3c56-0211-4fe1-9e59-51616caac4dd",
        "Content-Type": "application/json",
        "cookie": f"tokenid={access_token}"
    }

    data = {
        "operationName": "userRoleLoaderGetRoles",

        "query": """query userRoleLoaderGetRoles {
  user {
    getCurrentUser {
      functionalRoles {
        code
        __typename
      }
      id
      studentRoles {
        id
        school {
          id
          shortName
          organizationType
          __typename
        }
        status
        __typename
      }
      userSchoolPermissions {
        schoolId
        permissions
        __typename
      }
      systemAdminRole {
        id
        __typename
      }
      businessAdminRolesV2 {
        id
        school {
          id
          organizationType
          __typename
        }
        orgUnitId
        __typename
      }
      __typename
    }
    getCurrentUserSchoolRoles {
      schoolId
      __typename
    }
    __typename
  }
}
""",
        "variables": {}
    }
    response = session.post("https://edu.21-school.ru/services/graphql", headers=headers, json=data)
    return response.json()


def get_coins_and_rp(access_token):
    session = requests.Session()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "schoolid": "6bfe3c56-0211-4fe1-9e59-51616caac4dd",
        "Content-Type": "application/json",
        "cookie": f"tokenid={access_token}"
    }
    data = {
        "operationName": "getCurrentUser",
        "query": """query getCurrentUser {
  user {
    getCurrentUser {
      ...CurrentUser
      __typename
    }
    __typename
  }
  student {
    getExperience {
      ...CurrentUserExperience
      __typename
    }
    __typename
  }
}

fragment CurrentUser on User {
  id
  avatarUrl
  login
  firstName
  middleName
  lastName
  currentSchoolStudentId
  __typename
}

fragment CurrentUserExperience on UserExperience {
  id
  cookiesCount
  codeReviewPoints
  coinsCount
  level {
    id
    range {
      id
      levelCode
      __typename
    }
    __typename
  }
  __typename
}
""",
        "variables": {}
    }
    response = session.post("https://edu.21-school.ru/services/graphql", headers=headers, json=data)
    return response.json()


def get_coalition(access_token, school_user_id):
    session = requests.Session()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "schoolid": "6bfe3c56-0211-4fe1-9e59-51616caac4dd",
        "Content-Type": "application/json",
        "cookie": f"tokenid={access_token}"
    }
    data = {
        "operationName": "publicProfileGetCoalition",
        "query": """query publicProfileGetCoalition($userId: UUID!) {
  student {
    getUserTournamentWidget(userId: $userId) {
      coalitionMember {
        coalition {
          avatarUrl
          color
          name
          memberCount
          __typename
        }
        currentTournamentPowerRank {
          rank
          power {
            id
            points
            __typename
          }
          __typename
        }
        __typename
      }
      lastTournamentResult {
        userRank
        power
        __typename
      }
      __typename
    }
    __typename
  }
}
""",
        "variables": {
            "userId": school_user_id
        }
    }
    response = session.post("https://edu.21-school.ru/services/graphql", headers=headers, json=data)
    return response.json()["data"]["student"]["getUserTournamentWidget"]["coalitionMember"]["coalition"]["name"]


def get_users_from_coalition(access_token, offset, limit):
    session = requests.Session()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "schoolid": "6bfe3c56-0211-4fe1-9e59-51616caac4dd",
        "Content-Type": "application/json",
        "cookie": f"tokenid={access_token}"
    }
    data = {
        "operationName": "competitionCoalitionGetMyCoalitionMembers",
        "query": """query competitionCoalitionGetMyCoalitionMembers($page: PagingInput) {
  student {
    getUserTournamentWidget {
      getMyCoalitionMembers(page: $page) {
        user {
          id
          login
          avatarUrl
          userExperience {
            level {
              id
              levelCode
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
""",
        "variables": {
            "page": {
                "limit": limit,
                "offset": offset,
            }
        }
    }
    response = session.post("https://edu.21-school.ru/services/graphql", headers=headers, json=data)
    print(response)
    return response.json()["data"]["student"]["getUserTournamentWidget"]["getMyCoalitionMembers"]
