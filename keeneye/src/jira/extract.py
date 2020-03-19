import typing as t

import jira
from pipe.core.base import Extractor
from pipe.core.data import Store
from schema import And
from validators import url, email


class EJiraIssues(Extractor):
    ISSUE_STATUS = 'Done'
    save_validated: bool = True
    client: t.Optional[jira.JIRA] = None

    required_fields = {
        'api_key': str,
        'base_url': And(str, url),
        'email': And(str, email),
        'profile_email': str
    }

    def __init_client(self, email: str, api_key: str, base_url: str):
        self.client = jira.JIRA(base_url, basic_auth=(email, api_key), max_retries=0)

    def extract(self, store: Store):
        result = dict(**store.data)

        self.__init_client(
            store.get('email'),
            store.get('api_key'),
            store.get('base_url')
        )

        users = self.client.search_users(
            store.get('profile_email')
        )

        user = users.pop()

        search_prompt = 'assignee = "{}" and status = {}'.format(
            user, self.ISSUE_STATUS)

        issues = self.client.search_issues(search_prompt, maxResults=200,
                                           fields='worklog, created, aggregatetimeoriginalestimate')

        result.update({
            'issues': issues,
            'user': user
        })

        return Store(data=result)
