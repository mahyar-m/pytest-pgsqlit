import re


class ImportParser:
    @staticmethod
    def is_import(sql_command):
        return re.match('import ', sql_command, re.I)

    @staticmethod
    def parse(sql_command):
        match = re.match('import (.*)$', sql_command, re.I)
        if not match:
            raise ValueError('bad import')

        return match.group(1)
