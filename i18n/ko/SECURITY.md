# Security Policy

[简体中文](../../SECURITY.md) · [English](../en/SECURITY.md) · [繁體中文](../zh-TW/SECURITY.md) · [日本語](../ja/SECURITY.md) · [한국어](SECURITY.md)

## 지원 범위

현재 `main` 브랜치의 최신 릴리스 내용과 `dev` 브랜치에서 준비 중인 플러그인 변경 사항을 지원합니다.

## 보안 문제 보고

이 저장소와 관련된 보안 문제를 발견했다면 악용 가능한 세부 정보, token, API key, 비밀번호, 개인 키 또는 개인 민감 정보를 공개 issue 에 게시하지 마세요.

가능하면 GitHub 를 통해 관리자에게 비공개로 연락하세요. 공개 issue 를 열어야 한다면 민감한 내용 없이 비공개 논의가 필요하다는 점만 적어 주세요.

## 설치자를 위한 안전 안내

command hook 이 포함된 Antigravity 플러그인을 설치하기 전에 Antigravity 에서 다음을 실행하세요.

```text
/hooks
```

실제 명령을 검토한 뒤 trust 하세요. 알 수 없는 hook 을 무작정 신뢰하지 말고, API key, token, 머신 전용 경로를 플러그인 출력에 쓰지 마세요.
