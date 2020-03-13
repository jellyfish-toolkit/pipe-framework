from pipe.core.base import Transformer
from pipe.core.data import Store


class TFromJiraToDict(Transformer):
    required_fields = {
        'issues': list,
        'user': object
    }

    def __cumulate_user_logs(self, user, issue):
        total_seconds = 0
        logs = issue.fields.worklog.worklogs
        for log in logs:

            if log.raw.get('author').get('accountId') == user.accountId:
                total_seconds += log.timeSpentSeconds

        return total_seconds

    def transform(self, store: Store):
        result = dict(**store.data)
        result['issues'] = {}

        for issue in store.get('issues'):
            if issue.fields.aggregatetimeoriginalestimate is not None:
                estimate = int(issue.fields.aggregatetimeoriginalestimate) / 3600.
            else:
                estimate = 0
            spent = self.__cumulate_user_logs(store.get('user'), issue) / 3600.
            result['issues'].update({
                issue.key: {
                    'key': issue.key,
                    'estimate': estimate,
                    'spent': spent,
                    'created': issue.fields.created,
                }})

        return Store(result)


class TCountPercents(Transformer):
    required_fields = {
        'issues': dict,
        'user': object
    }

    def __count_deviation(self, es, sp):

        if es is None:
            return 0

        if es != 0 and es != 0:
            return round((sp - es) / es * 100, 2)

        return 0

    def transform(self, store: Store):
        result = dict(**store.data)

        for key, issue in store.get('issues').items():
            result['issues'][key].update({
                'deviation': self.__count_deviation(
                    issue.get('estimate'), issue.get('spent')
                )
            })

        return Store(result)
