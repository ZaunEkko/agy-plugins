<div align="center">

# 🧩 Antigravity Plugins

### Antigravity 워크플로를 위한 개인 마켓플레이스

*자주 쓰는 plugins, skills, hooks, 출력 스타일을 다른 사람도 설치할 수 있게 패키징합니다.*

[简体中文](../../README.md) · [English](../en/README.md) · [繁體中文](../zh-TW/README.md) · [日本語](../ja/README.md) · [한국어](README.md)

</div>

---

## ✨ 이 저장소는 무엇인가요?

이 저장소는 Antigravity용 개인 워크플로 마켓플레이스입니다. 재사용 가능한 Antigravity 플러그인, skills, hooks, 시작 컨텍스트, 출력 스타일, 개발 보조 흐름을 모읍니다.

## 📦 현재 플러그인

| 플러그인 | 유형 | 설명 | 문서 |
|----------|------|------|------|
| explanatory-output-style | Plugin + SessionStart Hook | Claude Code 공식 explanatory-output-style 경험을 Antigravity에 맞게 적용합니다. | [플러그인 문서](docs/explanatory-output-style/README.md) |
| commit-commands | Plugin + Skills | Anthropic 원본의 commit, commit-push-pr, gone 브랜치 force 정리 흐름을 제공합니다. | [플러그인 문서](docs/commit-commands/README.md) |

## 🚀 빠른 시작

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add explanatory-output-style@zaunekko
agy plugin add commit-commands@zaunekko
```

command hook 이 포함된 플러그인은 처음 사용하기 전에 Antigravity에서 검토하고 trust 해야 합니다.

```text
/hooks
```

## 📚 플러그인 문서

- [explanatory-output-style](docs/explanatory-output-style/README.md): 기능, 설치, hook trust, 로컬 검증 안내.
- [commit-commands](docs/commit-commands/README.md): 커밋, PR 게시, 브랜치 정리, 안전 제한, 로컬 검증 안내.

## ⚠️ Trust & Safety

- 설치 전에 플러그인 설명을 확인하세요.
- `/hooks` 에서 command hook 을 검토하세요.
- hook 을 변경했다면 다시 trust 하세요.
- 커밋, push 또는 브랜치 삭제를 수행하는 skill 실행 전 저장소 상태를 확인하세요.
- API key, token, 비밀번호, 머신 전용 경로를 hook 출력에 넣지 마세요.

## 📄 라이선스

이 프로젝트는 [MIT License](../../LICENSE) 로 공개됩니다.

## 🤝 커뮤니티

- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
