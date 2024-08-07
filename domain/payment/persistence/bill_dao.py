from pymysql import connect
from exceptions import query


class MySQLBillDao:
    def __init__(self, connection: connect):
        self.connection = connection

    def find_cost(self, group_id: int, user_id: int) -> int:
        sql = 'SELECT cost FROM bill_table WHERE group_id = %s AND user_id = %s'

        cursor = self.connection.cursor()
        cursor.execute(sql, (group_id, user_id))

        data = cursor.fetchone()
        if data is None:
            raise query.ResourceNotFound(msg='조회된 영수내역이 없습니다')
        cost = data[0]

        return cost
