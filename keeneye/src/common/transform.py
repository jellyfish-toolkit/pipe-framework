import string

from pipe.core.base import Transformer
from pipe.core.data import Store


class TSpreadsheetReady(Transformer):

    required_fields = {
        'issues': dict,
    }

    def __get_column_letter(self, index: int) -> str:
        return string.ascii_lowercase[index].upper()

    def __get_max_row_len(self, dict_values) -> int:
        return len(max(dict_values.values(), key=len))

    def __make_range(self, start: str, end: str, row: int) -> str:
        return start.format(row) + ":" + end.format(row)

    def transform(self, store: Store):
        current_row = 1
        result = dict(**store.data)

        issues = self.validated_data.get('issues', {})
        range_start = 'A{}'
        range_end = f'{self.__get_column_letter(self.__get_max_row_len(issues))}' + '{}'
        rows = {}

        range = self.__make_range(range_start, range_end, current_row)

        rows.update({
            range: list(list(issues.values()).pop().keys())
        })
        current_row += 1

        result.update({
            'spreadsheet': {
                'rows': None
            }
        })

        for issue in issues.values():
            row = self.__make_range(range_start, range_end, current_row)
            rows.update({row: list(issue.values())})
            current_row += 1

        result['spreadsheet']['rows'] = rows

        return Store(result)
