## Language / 语言 / 言語 / 언어

Select the language used in this PR description. / 请选择本 PR 描述使用的语言。 / この PR 説明で使用する言語を選択してください。 / 이 PR 설명에 사용할 언어를 선택하세요。

- [ ] 简体中文
- [ ] English
- [ ] 繁體中文
- [ ] 日本語
- [ ] 한국어

## Summary / 变更内容 / 変更内容 / 변경 내용

-

## Scope / 影响范围 / 影響範囲 / 영향 범위

- [ ] Docs only / 只改文档 / 只改文件 / ドキュメントのみ / 문서만 변경
- [ ] Plugin manifest changed / 修改插件 manifest / 修改插件 manifest / プラグイン manifest 変更 / 플러그인 manifest 변경
- [ ] Hook configuration changed / 修改 hook 配置 / 修改 hook 設定 / hook 設定変更 / hook 설정 변경
- [ ] Hook / command implementation changed / 修改 hook / command 实现 / 修改 hook / command 實作 / hook / command 実装変更 / hook / command 구현 변경
- [ ] New plugin / 新增插件 / 新增插件 / 新規プラグイン / 새 플러그인
- [ ] Tests or CI changed / 修改测试或 CI / 修改測試或 CI / テストまたは CI 変更 / 테스트 또는 CI 변경

## Validation / 验证 / 驗證 / 検証 / 검증

List the validation commands you ran for each affected plugin. / 请按受影响插件列出已运行的验证命令。 / 請按受影響插件列出已執行的驗證命令。 / 影響を受けるプラグインごとに実行した検証コマンドを記載してください。 / 영향을 받는 플러그인별로 실행한 검증 명령을 적어 주세요。

```bash
# example:
# python -m py_compile <hook-script>
# python <hook-script>
# python -m unittest <test-module>
```

- [ ] Ran validation for affected plugins / 已运行受影响插件的对应验证 / 已執行受影響插件的對應驗證 / 影響を受けるプラグインの検証を実行済み / 영향을 받는 플러그인의 검증 실행 완료
- [ ] Checked documentation links and paths / 已检查文档链接和路径 / 已檢查文件連結和路徑 / ドキュメントのリンクとパスを確認済み / 문서 링크와 경로 확인 완료
- [ ] Explained skipped validation below / 如未运行某项验证，已在下方说明原因 / 如未執行某項驗證，已在下方說明原因 / 省略した検証がある場合は下に理由を記載済み / 생략한 검증이 있다면 아래에 이유 작성 완료

## Hook / Security impact / Hook / 安全影响 / Hook / 安全影響 / Hook / セキュリティ影響 / Hook / 보안 영향

- [ ] No command hook was added or changed / 未新增或修改 command hook / 未新增或修改 command hook / command hook の追加・変更なし / command hook 추가 또는 변경 없음
- [ ] If command hook changed, users are told to review / trust it with `/hooks` / 如新增或修改 command hook，已说明用户需要在 `/hooks` 中 review / trust / 如新增或修改 command hook，已說明使用者需要在 `/hooks` 中 review / trust / command hook を追加・変更した場合、ユーザーが `/hooks` で review / trust する必要を説明済み / command hook 을 추가 또는 변경했다면 사용자가 `/hooks` 에서 review / trust 해야 함을 설명 완료
- [ ] No API keys, tokens, passwords, private keys, or machine-specific paths were added / 未写入 API key、token、密码、私钥或机器专属路径 / 未寫入 API key、token、密碼、私鑰或機器專屬路徑 / API key、token、パスワード、秘密鍵、マシン固有パスを追加していない / API key, token, 비밀번호, 개인 키, 머신 전용 경로를 추가하지 않음
- [ ] Reviewed cross-platform command / commandWindows behavior / 已审查 command / commandWindows 的跨平台行为 / 已審查 command / commandWindows 的跨平台行為 / command / commandWindows のクロスプラットフォーム動作を確認済み / command / commandWindows 의 크로스 플랫폼 동작 검토 완료

## Notes / 备注 / 備註 / 備考 / 비고

