from typing import Literal
import clickhouse_connect
import pandas as pd
import sys
import traceback

class ClickHouseClient():

    def __init__(self, 
                host:str=None,
                port:int=8123,
                database:str=None
    ):
        self.client = None
        self.query = list()
        try:
            self.client = clickhouse_connect.get_client(
                host=host,
                port=port,
                database=database
            )
        except Exception as e:
            print(f"클릭하우스 데이터베이스 연결에 실패했습니다: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    def __str__(self):
        return ' '.join(self.query)

    def select(self, *columns) -> "ClickHouseClient":
        if type(columns) is str:
            self.query.append(f"SELECT {columns}")
        else:
            self.query.append(f"SELECT {', '.join(columns)}")
        return self
    
    def from_(self, table) -> "ClickHouseClient":  # 'from'은 파이선의 예약어이므로 'from_table'로 명명합니다.
        self.query.append(f"FROM {table}")
        return self
    
    def where(self, condition) -> "ClickHouseClient":
        self.query.append(f"WHERE {condition}")
        return self
    
    def and_(self, condition) -> "ClickHouseClient":
        self.query.append(f"AND {condition}")
        return self
    
    def or_(self, condition) -> "ClickHouseClient":
        self.query.append(f"OR {condition}")
        return self
    
    def union(self) -> "ClickHouseClient":
        self.query.append(f"UNION")
        return self
    
    def intersect(self) -> "ClickHouseClient":
        self.query.append(f"INTERSECT")
        return self

    def group_by(self, columns:list) -> "ClickHouseClient":
        if type(columns) is str:
            self.query.append(f"GROUP BY {columns}")
        else:
            self.query.append(f"GROUP BY {', '.join(columns)}")
        return self
    
    def order_by(self, columns:list, asc=True) -> "ClickHouseClient":
        if type(columns) is str:
            self.query.append(f"ORDER BY {columns} {'ASC' if asc else 'DESC'}")
        else:
            self.query.append(f"ORDER BY {', '.join(columns)} {'ASC' if asc else 'DESC'}")
        return self

    def limit(self, limit) -> "ClickHouseClient":
        self.query.append(f"LIMIT {limit}")
        return self
    
    def execute(self, return_type:Literal["row", "column", "dictionary", "dataframe"]="dataframe", verbose=False) -> pd.DataFrame:
        """
        생성된 쿼리를 실행하고 결과를 반환합니다.
        """
        query = ' '.join(self.query)
        if verbose:
            print(f"Query built: {query}")
        result = self.client.query(query)
        self.query.clear()
        if return_type == "row":
            return result.result_rows
        elif return_type == "column":
            return result.result_columns
        elif return_type == "dictionary":
            return list(result.named_results())
        elif return_type == "dataframe":
            return pd.DataFrame(list(result.named_results()))
        print(f"Unknown return type: {return_type}", file=sys.stderr)
        return None
    
if __name__ == "__main__":
    clickhouse_client = ClickHouseClient(host="127.0.0.1", port=8123, database="DTIAI")

    result = (clickhouse_client.select("id", "response_header")
                                .from_("http_packet")
                                .limit(10)
                                .execute(return_type="dataframe", verbose=True))
    
    print(result)