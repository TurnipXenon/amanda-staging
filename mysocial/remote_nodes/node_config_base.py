import json
import urllib.parse

import requests
from django.http import HttpResponseNotFound
from rest_framework.response import Response

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from mysocial.settings import base


class NodeConfigBase:
    """
    Serves as sample and base configuration for remote server/node specific implementations

    Remember to call super whenever possible; use good judgment to determine when to call super in the method body.
    """

    """
    Call domain with self.__class__.domain so you can override it in classes that inherit this.
    Inheriting classes may not need it unless when needed
    """
    domain = 'domain.herokuapp.com'
    author_serializer = AuthorSerializer

    def __init__(self):
        if base.CURRENT_DOMAIN not in base.REMOTE_NODE_CREDENTIALS:
            print(f'{self.__class__.domain} is not in ConfigVars REMOTE_CONFIG_CREDENTIALS')
            self.username = '127.0.0.1:8000'
            self.password = '127.0.0.1:8000'
            return

        credentials = base.REMOTE_NODE_CREDENTIALS[base.CURRENT_DOMAIN]
        self.username = credentials['username']
        self.password = credentials['password']
        # todo(turnip): check entry in Author, check if inactive?

    @classmethod
    def create_dictionary_entry(cls):
        return {cls.domain: cls()}

    # endpoints
    def get_all_authors_request(self, params: dict):
        url = f'http://{self.__class__.domain}/authors/'
        if len(params) > 0:
            query_param = urllib.parse.urlencode(params)
            url += '?' + query_param
        response = requests.get(url)
        if response.status_code == 200:
            # todo(turnip): map to our author?
            return Response(json.loads(response.content))
        return HttpResponseNotFound()

    def from_author_id_to_url(self, author_id: str) -> dict:
        url = f'http://{self.__class__.domain}/authors/{author_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            # todo(turnip): map to our author?
            json_dict = json.loads(response.content)
            return json_dict['url']
        return None

    def get_author_request(self, author_id: str):
        response = requests.get(f'http://{self.__class__.domain}/authors/{author_id}/')
        if response.status_code == 200:
            # todo(turnip): map to our author?
            return Response(json.loads(response.content))
        return HttpResponseNotFound()

    def get_author_via_url(self, author_url: str) -> Author:
        response = requests.get(author_url)

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data # <- GOOD RESULT HERE!!!

            print('GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None

    def get_all_followers_request(self, params: dict, author_id: str):
        url = f'http://{self.__class__.domain}/authors/{author_id}/followers/'
        if len(params) > 0:
            query_param = urllib.parse.urlencode(params)
            url += '?' + query_param
        response = requests.get(url)
        if response.status_code == 200:
            # todo(turnip): map to our author?
            return Response(json.loads(response.content))
        return HttpResponseNotFound()

    def post_local_follow_remote(self, actor_url: str, target_id: str) -> dict:
        """Make call to remote node to follow"""
        target_author_url = self.from_author_id_to_url(target_id)
        if target_author_url is None:
            return 404
        url = f'{target_author_url}/followers/'
        response = requests.post(url,
                                 auth=(self.username, self.password),
                                 data={'actor': actor_url})
        if 200 <= response.status_code < 300:
            try:
                return json.loads(response.content.decode('utf-8'))
            except Exception as e:
                print(f"Failed to deserialize response: {response.content}")
        else:
            print(f"post_local_follow_remote: remote server response: {response.status_code}")
        return response.status_code
