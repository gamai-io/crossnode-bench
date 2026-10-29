# Security

CrossNode-Bench runs commands on the nodes you configure. Treat it as a test harness, not a sandbox.

- Run it only against machines you own or are authorized to test.
- The `probe` tasks intentionally invoke missing programs; they do not modify the system.
- `LocalNode` executes shell commands on the host that runs the benchmark. Use containers or a disposable VM for untrusted nodes.
- Never commit node tokens. Use `token_env` and environment variables.
