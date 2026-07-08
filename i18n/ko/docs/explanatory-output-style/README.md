# explanatory-output-style

[简体中文](../../../../docs/explanatory-output-style/README.md) · [English](../../../en/docs/explanatory-output-style/README.md) · [繁體中文](../../../zh-TW/docs/explanatory-output-style/README.md) · [日本語](../../../ja/docs/explanatory-output-style/README.md) · [한국어](README.md)

`explanatory-output-style` 은 Antigravity 세션에서 설명형 출력 스타일을 활성화하는 Antigravity 플러그인입니다.

Claude Code 공식 [`explanatory-output-style`](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style) 플러그인의 경험을 참고했습니다. `SessionStart` hook 으로 세션 시작 시 추가 지침을 주입하여, 모델이 코드를 작성하거나 수정할 때 현재 코드베이스에 맞는 짧은 Insight 설명을 덧붙이도록 합니다.

## 언제 사용하면 좋은가

- Antigravity 가 최종 변경만 제공하는 것이 아니라 왜 그렇게 구현했는지도 설명하길 원할 때.
- 팀이 같은 "작업하면서 설명하는" 협업 스타일을 공유하길 원할 때.
- 출력 스타일을 각 프로젝트에 프롬프트로 복사하지 않고 설치 가능한 플러그인으로 배포하고 싶을 때.

## Claude Code 공식 플러그인과의 관계

Claude Code 공식 플러그인은 `SessionStart` hook 을 사용해 세션 시작 시 설명형 출력 지침을 추가합니다. 이 저장소의 구현은 해당 동작을 Antigravity 플러그인 시스템에 맞게 다시 적용한 것입니다.

- Antigravity 플러그인 manifest: `plugins/explanatory-output-style/.agy-plugin/plugin.json`
- Antigravity hook 설정: `plugins/explanatory-output-style/hooks/hooks.json`
- Antigravity 가 요구하는 JSON payload 를 출력하는 Python hook: `hookSpecificOutput.additionalContext`
- 크로스 플랫폼 설치를 위해 Windows / Unix hook command 를 모두 유지

## 주입 후 협업 방식

주입된 컨텍스트는 Antigravity 에 다음을 요청합니다.

1. 코드를 작성하거나 수정하기 전후에 짧은 Insight 를 제공합니다.
2. 현재 코드베이스의 구현 선택, 프로젝트 규칙, 트레이드오프에 집중합니다.
3. 일반적인 프로그래밍 개념을 장문의 튜토리얼처럼 설명하지 않습니다.
4. 좁은 터미널에서도 깨지지 않는 출력 블록 형식을 사용해 줄바꿈과 오른쪽 테두리 어긋남을 줄입니다.

현재 Insight 블록 예시:

```text
`+-------------------- ★ Insight --------------------+`
| 현재 구현 선택을 설명하는 짧은 요점 2-3개
`+---------------------------------------------------+`
```

bullet 줄에는 왼쪽 `|` 만 유지하고 오른쪽 테두리는 추가하지 않습니다. 이렇게 하면 터미널 자동 줄바꿈 후에도 테두리 어긋남을 줄일 수 있습니다.

## 설치 및 활성화

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add explanatory-output-style@zaunekko
```

command hook 이 포함된 플러그인은 처음 실행하기 전에 Antigravity 에서 검토하고 trust 해야 합니다.

```text
/hooks
```

검토할 내용:

- `hooks/hooks.json` 에서 실제 실행되는 command.
- `hooks/session_start.py` 가 예상한 JSON 만 출력하는지.
- hook 출력에 API key, token, 머신 전용 경로 또는 기타 민감한 정보가 포함되지 않는지.

## 로컬 검증

저장소 루트에서 실행하세요.

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
agy plugin list
```

처음 세 명령은 Python 문법, hook JSON payload, 플러그인 출력 형식을 검증합니다. `agy plugin list` 는 Antigravity 가 marketplace 플러그인을 발견할 수 있는지 확인하는 데 사용합니다.
