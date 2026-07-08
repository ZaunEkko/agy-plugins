# Contributing

[简体中文](../../CONTRIBUTING.md) · [English](../en/CONTRIBUTING.md) · [繁體中文](../zh-TW/CONTRIBUTING.md) · [日本語](../ja/CONTRIBUTING.md) · [한국어](CONTRIBUTING.md)

`agy-plugins` 에 관심을 가져 주셔서 감사합니다. 이 저장소는 Antigravity 용 플러그인, hooks, skills, presets 및 관련 문서를 관리합니다.

## 브랜치와 기여 흐름

이 저장소는 Git Flow 를 사용합니다.

- `main`: 안정 릴리스 브랜치.
- `dev`: 일상 통합 브랜치.
- `feature/*`: 기능, 문서, 플러그인 변경. `dev` 에서 분기하고 Pull Request 로 `dev` 에 병합합니다.
- `release/*`: 릴리스 준비. `dev` 에서 분기하고 완료 후 `main` 과 `dev` 에 병합합니다.
- `hotfix/*`: 긴급 수정. `main` 에서 분기하고 완료 후 `main` 과 `dev` 에 병합합니다.

`main` 또는 `dev` 에 직접 push 하지 마세요. 두 브랜치는 보호되어 있으며, 변경은 Pull Request 와 필수 검사를 거쳐 병합해야 합니다.

## 저장소 구조

새 플러그인은 일반적으로 다음 구조를 따릅니다.

```text
plugins/<plugin-name>/
├── .agy-plugin/
│   └── plugin.json
└── ...

docs/<plugin-name>/
└── README.md
```

- `plugins/<plugin-name>/` 에는 설치 가능한 플러그인 파일을 둡니다.
- `docs/<plugin-name>/README.md` 에는 설치자와 사용자를 위한 플러그인 문서를 둡니다.
- 루트 `README.md` 는 저장소 개요와 플러그인 문서 라우팅만 담당합니다.
- 로컬 Claude Code 초기화 파일 `CLAUDE.md` 는 커밋하지 마세요. `.gitignore` 에서 무시됩니다.

## 플러그인 문서 요구사항

각 플러그인 문서에는 해결하는 문제, 설치 방법, 활성화 또는 trust 단계, 주요 파일 경로, 관리자 검증 방법을 포함해야 합니다. command hook 이 포함된 경우 `/hooks` 검토와 trust 절차를 설명하세요.

## 검증 요구사항

이번 변경의 영향을 받는 플러그인에 맞는 검증을 실행하세요. 모든 PR 에 하나의 고정 명령 세트만 사용하지 마세요.

일반 규칙:

- Python hook 변경: `python -m py_compile <hook-script>` 를 실행하고 hook 스크립트를 직접 실행해 유효한 JSON 을 출력하는지 확인합니다.
- hook 설정 변경: `hooks.json` 이 유효한 JSON 인지 확인하고 command / commandWindows 의 안전성, 가독성, 크로스 플랫폼 동작을 검토합니다.
- manifest 변경: `.agy-plugin/plugin.json` 이 유효한 JSON 이며 플러그인 이름, 버전, 설명, marketplace 항목과 일치하는지 확인합니다.
- 동작 변경: 해당 플러그인의 테스트를 실행합니다. 테스트가 없다면 초점을 맞춘 테스트를 추가하거나 PR 에 추가하지 않은 이유를 설명합니다.
- 문서 변경: 링크, 경로, 설치 명령이 정확한지 확인합니다.
- 새 플러그인: marketplace 가 플러그인을 발견할 수 있는지 확인하고 설치 및 trust 단계를 문서화합니다.

현재 `explanatory-output-style` 플러그인의 관리자 검증 예시:

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
```

이 명령은 해당 플러그인의 예시일 뿐입니다. 새 플러그인은 자체 문서나 테스트에서 검증 방법을 정의해야 합니다.

## Hook 및 보안 요구사항

- hook 출력, manifest, 테스트, 문서에 API key, token, 비밀번호, 개인 키 또는 머신 전용 경로를 쓰지 마세요.
- 검토하기 어려운 불투명한 명령 문자열을 추가하지 마세요.
- 필요한 크로스 플랫폼 지원을 유지하세요. Windows 와 Unix 명령이 다르면 각각 명확히 작성하세요.
- command hook 을 추가하거나 수정한 뒤에는 PR 에 보안 영향과 사용자가 review / trust 해야 할 내용을 설명하세요.

## Pull Request 요구사항

PR 설명에는 변경 요약, 실행한 검증 명령, hook / manifest / marketplace metadata 변경 여부, Hook / 보안 영향, 실행하지 않은 검증의 이유를 포함해야 합니다.
