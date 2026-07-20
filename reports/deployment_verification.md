# Deployment verification

- task_id: 24f44a36
- checked_at_utc: 2026-07-20T00:37:04Z
- public_url: https://aunomira-lab.github.io/knowledge-subscription/
- http_code: 200
- bytes: 20577
- contains_ai_radar_text: 6
- result: PASS_PUBLIC_URL_REACHABLE

## Commands actually run

- curl -L --max-time 20 --connect-timeout 8 -s -o /tmp/ks_public_verify_24f44a36.html -w '%{http_code}' https://aunomira-lab.github.io/knowledge-subscription/
- grep -c 'AI商机雷达' /tmp/ks_public_verify_24f44a36.html

## Important note

This verifies the current public URL is reachable. If local files changed after the last successful push, rerun: bash deploy/deploy_github_pages.sh after GitHub/Cloudflare authorization, then rerun this verifier.
