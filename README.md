# Installation

```

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