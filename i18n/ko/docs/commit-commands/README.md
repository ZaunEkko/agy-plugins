# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](../../../en/docs/commit-commands/README.md) · [繁體中文](../../../zh-TW/docs/commit-commands/README.md) · [日本語](../../../ja/docs/commit-commands/README.md) · [한국어](README.md)

`commit-commands` 는 [Anthropic 공식 원본](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) 의 세 slash command 를 Antigravity 네이티브 skill 로 적용합니다.

```text
$commit
$commit-push-pr
$clean-gone
```

워크플로 단계는 원본을 따릅니다. Antigravity 전용 차이는 네이티브 skill 구조, 명확한 의도에 따른 자동 선택, `$skill-name` 호출, Antigravity attribution 뿐입니다.

## 설치

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add commit-commands@zaunekko
```

설치 또는 업데이트 후 새 Antigravity thread 를 여세요.

## 자동 선택 예시

- "이 변경을 commit 해줘"는 `commit` 을 선택할 수 있습니다.
- "commit, push 하고 PR 을 만들어줘"는 `commit-push-pr` 을 선택할 수 있습니다.
- "gone 브랜치를 모두 정리해줘"는 `clean-gone` 을 선택할 수 있습니다.
- "구현이 끝났다"는 말만으로 Git 부작용을 실행하지 않습니다.

## `$commit`

`git status`, `git diff HEAD`, 현재 브랜치, 최근 commit 10개를 확인하고 현재 변경을 stage 한 뒤 하나의 commit 을 만듭니다.

```text
Co-authored-by: Antigravity <noreply@openai.com>
```

push 또는 PR 생성을 하지 않으며 변경이 없으면 빈 commit 도 만들지 않습니다.

## `$commit-push-pr`

현재 status, diff, branch 를 확인합니다. 현재 브랜치가 정확히 `main` 일 때만 새 브랜치를 만든 뒤 하나의 commit 을 만들고 `origin` 에 push 하며 `gh pr create` 로 PR 을 엽니다.

명시적인 PR 의도가 필요합니다. 원본과 마찬가지로 새 commit 없이 게시하는 경로나 `main` 이외의 브랜치 이름을 정책에 맞춰 자동 전환하는 동작은 없습니다.

GitHub CLI 설치와 로그인, 그리고 `origin` remote 가 필요합니다.

## `$clean-gone`

`git branch -v` 와 `git worktree list` 로 `[gone]` 브랜치를 찾습니다. 각 후보의 연결된 non-main worktree 를 `git worktree remove --force` 로 강제 제거하고 `git branch -D` 로 브랜치를 강제 삭제합니다.

이는 원본과 일치하는 파괴적 동작입니다. fetch, merge 검증, worktree clean 확인, ignored 파일 보호, 통합 브랜치 규칙을 추가하지 않습니다. 실행 전에 저장소 상태를 확인하세요.

## 로컬 검증

```bash
python -m unittest discover -s tests
agy plugin list
```
