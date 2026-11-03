package crossnode.gate

default allow = false

allow {
  input.signed == true
  input.manifest.records > 0
  input.metrics.false_success_rate <= input.thresholds.false_success_rate
  input.metrics.coverage >= input.thresholds.coverage
}

deny[msg] {
  not input.signed
  msg := "evidence is not signed (cosign bundle missing)"
}

deny[msg] {
  input.manifest.records <= 0
  msg := "evidence has no records"
}

deny[msg] {
  input.metrics.false_success_rate > input.thresholds.false_success_rate
  msg := sprintf(
    "false_success_rate %.6f exceeds threshold %.6f",
    [input.metrics.false_success_rate, input.thresholds.false_success_rate],
  )
}

deny[msg] {
  input.metrics.coverage < input.thresholds.coverage
  msg := sprintf(
    "coverage %.6f below threshold %.6f",
    [input.metrics.coverage, input.thresholds.coverage],
  )
}
