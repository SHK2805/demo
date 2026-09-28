# Title: iOS MDM Enrolment Interception and Pinning Failures
# Description: Detects dropped or reset TLS handshakes targeting Apple MDM infrastructure.

tag=network tag=communicate
| search dest_host IN ("://apple.com", "://apple.com", "://apple.com", "://microsoft.com")
| where (action="blocked" OR action="reset" OR action="failure" OR status="reset" OR ssl_error="*")
| eval possible_reason=case(
    match(ssl_error, "(?i)unknown_ca|cert_not_trusted|pinning"), "Rogue CA / Decryption Interception",
    action="reset", "Device Aborted TLS Handshake",
    1=1, "Network Block / Drop")
| table _time, src_ip, dest_host, dest_ip, action, transport, ssl_error, possible_reason
| sort - _time
