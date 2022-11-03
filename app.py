from graphqlclient import GraphQLClient
import json
from datetime import date
from datetime import timedelta
import logging
import requests
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

HYGRAPH_API_KEY = os.environ.get("HYGRAPH_API_KEY", "")
HYGRAPH_API_URL = os.environ.get("HYGRAPH_API_URL", "")
GATSBY_BUILD_HOOK = os.environ.get("GATSBY_BUILD_HOOK", "")

def handler(event, context):
    
    end_date_gte = date.today() - timedelta(days = 7)
    end_date_lt = date.today()
    
    query_string =f"""query {{
      waterwayEventNotices(where: {{endDate_gte: "{end_date_gte}", endDate_lt: "{end_date_lt}"}}) {{
        id
      }}
    }}"""
    
    try:
      client = GraphQLClient(HYGRAPH_API_URL)
      client.inject_token(f"Bearer {HYGRAPH_API_KEY}")
      query_result = json.loads(client.execute(query_string))

    except Exception as e:
      logger.error("Failed to read data from Hygraph")

    else:
      if len(query_result['data']['waterwayEventNotices']) > 0:
          logger.info("Update needed; triggering a build on Gatsby Cloud")
          requests.post(GATSBY_BUILD_HOOK)
      else:
          logger.info("No update needed")