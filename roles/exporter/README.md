# `catalystcloud.distil.exporter`

An Ansible role for managing Distil Exporter.

Distil Exporter exposes a Prometheus exporter for tracking the collection status of projects.
This service is optional, but enabled by default.

By default, a service container named `distil-exporter` will be created on the host.

Distil Exporter is run as a WSGI app within [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest),
serving HTTP to port 16798 by default, with 2 workers and 1 concurrent thread per worker.

To scrape this exporter, add a scrape config to your Prometheus instance like so:

```yaml
---

scrape_configs:
  - job_name: distil
    metrics_path: /metrics
    scheme: http
    scrape_interval: 15s
    scrape_timeout: 10s
    static_configs:
      - targets:
          - 192.0.2.1:16798
```

The following metrics are exported:

* `distil_build_info{...}` (`gauge`) - Distil library versions and exporter uptime status
* `distil_last_collected{project_id(str)}` (`gauge`) - Unix timestamp for age of collection for each project

For more information, check the documentation for the `catalystcloud.distil` collection.
