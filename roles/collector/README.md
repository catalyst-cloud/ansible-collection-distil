# `catalystcloud.distil.collector`

An Ansible role for managing Distil Collector.

Distil Collector is the backend service that does the majority of the data processing.

A collection run is performed on startup.
Jobs are scheduled to perform subsequent collection runs at the same time the next hour, and so on.

First, Keystone is queried for a list of active projects.
After filtering domains and projects as defined in the configuration,
the following steps are performed for each defined rated service for each project:

1. Query the telemetry service (currently only Ceilometer API is supported) to discover usage within the next window to be collected for the project.
1. Transform (rate) the usage according to the meter mapping/transformer configuration.
1. Create the corresponding usage entries for Distil services within the rated window.

If a project is already up to date on its collection, it is skipped.

By default, a single service container named `distil-collector`,
that collects all projects and domains, will be created on the host.

Running multiple collectors at once from the same host is also supported,
with different domain/project filtering options defined for different collector types.
This is useful for separating collection concerns (e.g. customer projects and internal projects),
so that if one of the collectors fail or has performance issues, it does not affect others.

Distil Collector also exposes an optional Prometheus exporter called Distil Collector Exporter,
run as a separate thread within the Distil Collector process, with metrics tracked in-memory.
This allows for collection of reasonably accurate collection run metrics efficiently,
without performing expensive database queries. This collector serves HTTP to port 16799 by default.

To scrape this exporter, add a scrape config to your Prometheus instance like so:

```yaml
---

scrape_configs:
  - job_name: distil_collector
    metrics_path: /metrics
    scheme: http
    scrape_interval: 15s
    scrape_timeout: 10s
    static_configs:
      - targets:
          - 192.0.2.1:16799
          # Add additional configs for each additional configured collector.
```

The following metrics are exported:

* `distil_collector_build_info{...}` (`gauge`) - Distil Collector library versions and uptime status
* `distil_collector_last_run_start` (`gauge`) - Unix timestamp for the latest collection run's start time
* `distil_collector_last_run_end` (`gauge`) - Unix timestamp for the latest collection run's end time
* `distil_collector_last_run_duration_seconds` (`gauge`) - Latest collection run's duration, in seconds
* `distil_collector_usage_total{project_id(str), service(str), unit(str)}` (`counter`) - Total usage under each service for a given project

For more information, check the documentation for the `catalystcloud.distil` collection.
