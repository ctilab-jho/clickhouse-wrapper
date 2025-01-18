# Installation

```
# 새로운 설치
pip install git+https://github.com/ctilab-jho/clickhouse-wrapper.git

# 기존 설치된 패키지 최신화
pip install --upgrade git+https://github.com/ctilab-jho/clickhouse-wrapper.git
```

# Features

### Connection

ClickHouseClient를 활용하여 자동으로 데이터베이스 연결을 구축합니다.

```py
from clickhouse_client import ClickHouseClient

clickhouse_client = ClickHouseClient(host="127.0.0.1", port=8123, database="MY_DB")
```

### Data Manipulation 

연결이 완료된 ClickHouseClient는 메서드 체이닝 기반의 쿼리 생성 및 실행 기능을 제공합니다.

```py
result = (clickhouse_client.select("id", "name")
                            .from_("user")
                            .order_by(age)
                            .limit(10)
                            .execute())

# 'SELECT id, name FROM user ORDER BY age LIMIT 10'의 실행 결과를 result에 할당.
```

### Buit-In Function

클릭하우스에서 제공되는 빌트인 함수를 파이선 함수의 형태로 사용하여 간편하게 쿼리를 생성할 수 있습니다. 단, Data Manipulation과 달리 실행 기능을 제공하지는 않습니다.

```py
from clickhose_function import *

query = array_string_concat('x', 'y', 'z')
query = decode_url_component(query)
query = lower(query)
query = replace(query, '/..', ' pathsearcher')
query = replace_regexp_all(query, 'host: [0-9].', ' hostcheck)
query = replace_regexp_all(query, '[\-%./!@#$?,;:&*)(+=0-9]', ' ')

# replaceRegexpAll(replaceRegexpAll(replace(lower(decodeURLComponent(arrayStringConcat([{x_cols}], ' '))), '/..', ' pathsearcher), 'host: [0-9].', ' hostcheck'), '[\-%./!@#$?,;:&*)(+=0-9]', ' ') 라는 문자열이 query에 할당됩니다.

# 위와 같이 생성된 query를 ClickHouseClient의 인자로 전달할 수 있습니다.

result = (clickhouse_client.select("id", query)
                            .from_("user")
                            .where("age=27")
                            .and_("name=abc")
                            .execute())
```



# FAQs

### 'latin-1' codec can't encode characters in position ...

client_connect 메서드는 연결 직전, 내부적으로 다음과 같은 문자열을 생성합니다.

```
211.115.206.7:8123
identity
28
clickhouse-connect/0.8.14 (lv:py/3.10.0; mode:sync; os:win32; os_user:user)
```

이 문자열에 한글이 포함되어 있으면 인코딩 에러가 발생합니다.

특히 os_user(운영체제의 계정 사용자 이름)이 한글이 아닌지 확인 바랍니다.