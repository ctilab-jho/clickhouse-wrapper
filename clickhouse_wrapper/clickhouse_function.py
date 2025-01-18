def array_string_concat(*columns, delimiter:str = ' ') -> str:
    """
    ClickHouse의 arrayStringConcat 함수를 생성하는 SQL 래퍼 함수입니다.
    delimiter를 구분자로 컬럼값을 하나의 문자열로 병합합니다.
    
    Args:
        *columns: 병합할 컬럼들의 이름. 가변 인자로 받습니다.
        delimiter: 컬럼값들을 병합할 때 사용할 구분자. 기본값은 공백(' ')입니다.
    
    Returns:
        str: arrayStringConcat SQL 함수 문자열
             예: "arrayStringConcat([col1, col2], ' ')"
    
    Examples:
        >>> array_string_concat('col1', 'col2')
        "arrayStringConcat([col1, col2], ' ')"
        >>> array_string_concat('col1', 'col2', delimiter=',')
        "arrayStringConcat([col1, col2], ',')"
    """
    if isinstance(columns, str):
        return f"arrayStringConcat([{columns}], '{delimiter}')"
    return f"arrayStringConcat([{', '.join(columns)}], '{delimiter}')"

def decode_url_component(expr: str) -> str:
    """
    ClickHouse의 decodeURLComponent 함수를 생성하는 SQL 래퍼 함수입니다.
    URL 인코딩된 문자열을 디코드하는 함수를 생성합니다.
    
    Args:
        expr: 디코드할 URL 인코딩된 문자열 또는 컬럼명
    
    Returns:
        str: decodeURLComponent SQL 함수 문자열
             예: "decodeURLComponent(column_name)"
    
    Examples:
        >>> decode_url_component('url_column')
        "decodeURLComponent(url_column)"
        >>> decode_url_component("arrayStringConcat([url1, url2], ' ')")
        "decodeURLComponent(arrayStringConcat([url1, url2], ' '))"
    """
    return f"decodeURLComponent({expr})"

def lower(expr: str) -> str:
   """
   ClickHouse의 lower 함수를 생성하는 SQL 래퍼 함수입니다.
   문자열을 소문자로 변환하는 함수를 생성합니다.
   
   Args:
       expr: 소문자로 변환할 문자열 또는 컬럼명
   
   Returns:
       str: lower SQL 함수 문자열
            예: "lower(column_name)"
   
   Examples:
       >>> lower('user_agent')
       "lower(user_agent)"
       >>> lower("arrayStringConcat([col1, col2], ' ')")
       "lower(arrayStringConcat([col1, col2], ' '))"
   """
   return f"lower({expr})"

def replace(expr: str, pattern: str, replacement: str) -> str:
   """
   ClickHouse의 replace 함수를 생성하는 SQL 래퍼 함수입니다.
   문자열에서 지정된 패턴을 새로운 문자열로 교체하는 함수를 생성합니다.
   
   Args:
       expr: 교체를 수행할 원본 문자열 또는 컬럼명
       pattern: 찾을 문자열 패턴
       replacement: 교체할 새로운 문자열
   
   Returns:
       str: replace SQL 함수 문자열
            예: "replace(column_name, 'pattern', 'new_text')"
   
   Examples:
       >>> replace('url', '/..', ' pathsearcherdetected ')
       "replace(url, '/..', ' pathsearcherdetected ')"
       >>> replace("lower(url)", 'http:', 'https:')
       "replace(lower(url), 'http:', 'https:')"
   """
   return f"replace({expr}, '{pattern}', '{replacement}')"

def replace_regexp_all(expr: str, pattern: str, replacement: str) -> str:
   """
   ClickHouse의 replaceRegexpAll 함수를 생성하는 SQL 래퍼 함수입니다.
   정규식 패턴과 일치하는 모든 부분을 새로운 문자열로 교체하는 함수를 생성합니다.
   
   Args:
       expr: 정규식 교체를 수행할 원본 문자열 또는 컬럼명
       pattern: 찾을 정규식 패턴
       replacement: 교체할 새로운 문자열
   
   Returns:
       str: replaceRegexpAll SQL 함수 문자열
            예: "replaceRegexpAll(column_name, 'pattern', 'new_text')"
   
   Examples:
       >>> replace_regexp_all('url', 'host: [0-9].', ' hostcheckdetected ')
       "replaceRegexpAll(url, 'host: [0-9].', ' hostcheckdetected ')"
       >>> replace_regexp_all('text', '[\-%./!@#$?,;:&*)(+=0-9]', ' ')
       "replaceRegexpAll(text, '[\-%./!@#$?,;:&*)(+=0-9]', ' ')"
       
   Notes:
       - 정규식 패턴에 포함된 작은따옴표(')는 자동으로 이스케이프 처리됩니다
       - pattern은 ClickHouse에서 지원하는 정규식 문법을 따릅니다
   """
   pattern = pattern.replace("'", "\\'")
   replacement = replacement.replace("'", "\\'")
   return f"replaceRegexpAll({expr}, '{pattern}', '{replacement}')"

if __name__ == "__main__":
    query = array_string_concat('request_header', 'request_body', 'response_header')
    query = decode_url_component(query)
    query = lower(query)
    query = replace(query, '/..', ' pathsearcherdetected ')
    query = replace_regexp_all(query, 'host: [0-9].', ' hostcheckdetected ')
    query = replace_regexp_all(query, '[\-%./!@#$?,;:&*)(+=0-9]', ' ')
    
    print(query)