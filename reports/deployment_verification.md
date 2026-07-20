# Deployment verification

- task_id: 24f44a36
- checked_at_utc: 2026-07-20T00:37:59Z
- commit_pushed: db284cd665598581191e644344fd50a218baaa92
- public_url: https://aunomira-lab.github.io/knowledge-subscription/
- public_http_code: 200
- public_bytes: 20577
- public_contains_ai_radar_text: 6
- public_contains_new_marker_订阅意向表: 0
- raw_github_main_site_contains_new_marker_订阅意向表: 1
- raw_github_main_site_bytes: 22609
- result: PASS_PUBLIC_URL_REACHABLE_WITH_CONTENT_UPDATE_PENDING

## Commands actually run

- `bash deploy/deploy_github_pages.sh` -> exit_code 0; committed and pushed `db284cd` to `origin/main`; follow-up public URL check returned HTTP 200.
- `for i in 1 2 3 4 5; do curl ... https://aunomira-lab.github.io/knowledge-subscription/ ... grep -c '订阅意向表' ...; done` -> exit_code 5; public URL was reachable but still serving pre-push cached/previous page during the check window.
- `curl -L https://raw.githubusercontent.com/aunomira-lab/knowledge-subscription/main/site/index.html ... grep -c '订阅意向表'` -> exit_code 0; raw `main/site/index.html` contains the updated sales page.

## Interpretation

GitHub push authorization succeeded and the current public URL is reachable. The live GitHub Pages URL was still serving the previous page content immediately after push, likely because Pages rebuild/CDN propagation had not completed or Pages source is pinned to an older build. Do not start paid ads until `deploy/verify_public_url.sh` plus a marker check confirms the new page is live.

## Next verification command

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
curl -L --max-time 20 --connect-timeout 8 -s https://aunomira-lab.github.io/knowledge-subscription/ -o /tmp/ks_live.html
grep -c '订阅意向表' /tmp/ks_live.html
```

Expected value after propagation: `1` or more.
