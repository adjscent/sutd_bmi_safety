scancode \
  --license \
  --copyright \
  --package \
  --summary \
  --classify \
  --license-policy gpl-policy.yml \
  --json-pp scancode-with-policy.json \
  .

jq '
  .files[]
  | select(.licenses)
  | select(any(.licenses[]; (.spdx_license_key == null) or (.key == "unknown-license-reference") ))
  | {path, licenses}
' scancode-with-policy.json