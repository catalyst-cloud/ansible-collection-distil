# Ansible collection for OpenStack Distil

[![GitHub License](https://img.shields.io/github/license/catalyst-cloud/ansible-collection-distil)](https://github.com/catalyst-cloud/ansible-collection-distil/blob/main/LICENSE) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/catalyst-cloud/ansible-collection-distil/test.yml?label=tests)](https://github.com/catalyst-cloud/ansible-collection-distil/actions/workflows/test.yml)

This is an example Ansible collection for deploying the Distil rating service
to an OpenStack control plane.

The various Distil services are run inside Docker containers,
managed by Docker Compose V2.

## Installation

To install this collection in your Ansible environment, you can create a `requirements.yml`
file with the following contents, or add the contents to an existing `requirements.yml` file.
Make sure to substitute `<git ref>` for the latest tagged version,
or the desired development branch name.

```yaml
collections:
  - name: https://github.com/catalyst-cloud/ansible-collection-distil.git
    version: "<git ref>"
    type: git
```

The collection will then be installed when `ansible-galaxy install -r requirements.yml` is run.

## Usage

### Inventory

To use this collection, inventory variables need to be defined for the managed host groups.

When using the built-in Ansible playbooks (optional), the following host groups are used:

* `distil` - Host group for installing **all** available Distil services
* `distil_api` - Host froup for installing Distil API only
* `distil_manage` - Host froup for installing Distil Manage only
* `distil_exporter` - Host froup for installing Distil Exporter only
* `distil_collector` - Host froup for installing Distil Collector only

If you are making use of the Ansible playbooks bundled within this playbook to manage Distil,
make sure the target hosts have at least one of the above groups assigned to it.

#### Distil common configuration

* `distil_base_dir` - The base directory under which Distil service files will be installed. Default is `/opt/distil`.
* `distil_config_dir` - The host directory to install Distil configuration files to. Default is `{{ distil_base_dir }}/etc`.
* `distil_lib_dir` - The host directory to use for Distil runtime files. Default is `{{ distil_base_dir }}/lib`.
* `distil_docker_group` - The group to assign to directories that need to be accessible by users who can use Docker. Default is `root`.
* `distil_log_dir` - The target directory for Distil service log files on the host. Default is `/var/log/distil`.
* `distil_log_group` - The group to assign to the logging directory. Default is to assign the Distil service group.
* `distil_log_dir_mode` - The permissions for the logging directory. Default is `"0750"`.
* `distil_ssl_cert` - Service SSL certificate filepath on the host.
* `distil_ssl_key` - Service SSL private key filepath on the host.
* `distil_ssl_cacert` - Service CA certificate bundle filepath on the host.
* `distil_openstack_region` - The name of the OpenStack region being deployed to. Distil must be deployed individually to all regions.
* `distil_user_name` - Distil service user name. Default is `distil`.
* `distil_user_group` - Distil service group name. Default is `distil`.
* `distil_user_uid` - UID for the created service user. **Must be unique**. Default is `305`.
* `distil_user_gid` - GID for the created service group. **Must be unique**. Default is `305`.
* `distil_user_groups` - A list of additional groups to assign to the service user (if required). Default is to assign no additional groups.
* `distil_timezone` - The operating timezone for the Distil services. As billing itself is always processed in UTC, this mainly effects logging. Default is `Etc/UTC`.
* `distil_erp_driver` - The ERP driver to use for invoice and quotation handling in Distil API.
    * Supported values are:
        * `jsonfile` (default)
        * `odoo`
    * Make sure to configure the selected ERP driver using the appropriate variables below.

#### Distil Keystone configuration

* `distil_keystone_enable` - Enable installation and configuration of service resources in Keystone. Default is `true`.
* `distil_keystone_auth_url` - Auth URL for the Keystone service in the OpenStack region.
    * This is used as the endpoint for Keystone authentication in Distil.
    * Define as the base URL without the version endpoint, e.g. `https://keystone.example.com:5000`.
* `distil_keystone_auth_version` - Keystone API endpoint version to use for authentication. Default is `v3`.
* `distil_keystone_user_name` - Service username in Keystone. Default is `distil`.
* `distil_keystone_user_password` - Password for the service user in Keystone. Should be defined in Ansible Vault.
* `distil_keystone_user_email` - Email address for the service user in Keystone. Default is `distil@localhost`.
* `distil_keystone_user_project` - The name of the default project for the service user in Keystone (and the service project to use in the service configuration). Default is `services`.
* `distil_keystone_user_domain` - The name of the default domain for the service user in Keystone. Default is `Default`.
* `distil_keystone_ansible_auth_cloud` - Optional variable for explicitly provided credentials to authenticate with Keystone in the target region, so Ansible can create service resources. Useful in CI environments. Default is to auto-fetch session environment variables defined in the Ansible controller's environment.

#### Distil API configuration

* `distil_api_hostname` - Hostname for Distil API that clients should use.
    * This is used to configure the service endpoints in Keystone.
* `distil_api_port` - Bind port for Distil API. Default is `9999`.
* `distil_api_ignore_products_in_quotations` - List of products (services) to remove from quotations. Useful for hiding services that are being collected by Distil, but not yet charged. Default is to not remove any products.

#### Distil Exporter configuration

* `distil_exporter_port` - Bind port for Distil Exporter. Default is `16798`.

#### Distil Collector configuration

* `distil_collectors` - Configuration for what collectors to create and run. For more information on how to define this, refer to the `catalystcloud.distil.collector` role inventory defaults file. Default is to create a single collector (the default collector) that collects **all** existing domains and projects.
* `distil_collector_periodic_interval` - The interval at which Distil Collector carries out usage collection jobs, in seconds. Default is `3600` (collect once every hour).
* `distil_collector_collect_window` - The amount of usage Distil should collect at a time (per window), in hours. Default is `1` (collect in 1 hour windows).
* `distil_collector_max_windows_per_cycle` - The maximum amount of windows Distil should collect for a project per collection run. Default is `12` (collect up to 12 windows).
* `distil_collector_max_collection_start_age` - The maximum time period for determining the start time for usage collection on a new project, in hours. Default is `864` hours (36 days).
    * Whenever a new project is collected by Distil, it uses the latest (newest) of three possible values:
        * The Keystone project `created_on` field, if it is available. This field is set by Adjutant when it creates new projects on sign-ups. This is usually the newest, and thus the most likely to be used.
        * The oldest found `last_collected` value for the existing projects being serviced by this collector instance. If Keystone is used to create the project directly (and not via Adjutant), this is the one that will likely be used.
        * The maximum `last_collected` value for the current time, which is calculated from `distil_collector_max_collection_start_age`. The default value is 36 days, to allow for at least one month's worth of billing to be caught up if required. This serves as the fallback for when no better alternative is found, as it means the collector will spend some time catching up the project to the present.
* `distil_collector_exporter_enable` - Enable Distil Collector Exporter, the Prometheus exporter within the Distil Collector service. Default is `true`.
* `distil_collector_exporter_port` - The default port for Distil Collector Exporter. When using multiple collectors on the same host, define unique ports for each individual collector. Default is `16799`.

#### Distil database configuration

* `distil_database_flavor` - The type of database storage backend to use. Default is `mysql`.
* `distil_database_library` - The library to use to interface with the database. Default is `pymysql`.
* `distil_database_hosts` - A list of database servers (in `<hostname-or-IP>:<port>` format) to connect to.
* `distil_database_username` - Service username in the database.
* `distil_database_password` - Password for the service user in the database. Should be defined in Ansible Vault.
* `distil_database_name` - Name of the service database. Default is `distil`.

#### Distil JSON file configuration

Ensure these options are configured when using the `jsonfile` ERP driver.

* `distil_jsonfile_tax_rate` - The tax rate to use when calculating, as a decimal percentage. Default is `0` (no tax).

#### Distil Odoo configuration

Ensure these options are configured when using the `odoo` ERP driver.

* `distil_odoo_version` - Version of the Odoo server. Set to `null` to auto-detect the server version. Default is `null`.
* `distil_odoo_hostname` - Hostname of the Odoo server.
* `distil_odoo_port` - Listening port of the Odoo driver. Default is `8069`.
* `distil_odoo_protocol` - Odoo protocol to use. Use `jsonrpc+ssl` for HTTPS. Default is `jsonrpc` (for HTTP).
* `distil_odoo_database` - Odoo database to load.
* `distil_odoo_username` - Username of the Odoo user to authenticate as.
* `distil_odoo_password` - Password for the Odoo user.
    * Should be defined either in Hiera eyaml or Ansible Vault.
* `distil_odoo_licensed_os_distros` - List of OS distros in Nova to treat as "licensed" for billing purposes. Default is empty.
* `distil_odoo_extra_product_categories` - List of product categories listed in Odoo (that Distil does not check by default). Default is set to the following:
  ```yaml
  distil_odoo_extra_product_categories:
    - "Database"
    - "COE"
  ```
* `distil_odoo_invisible_products` - List of product IDs that should be hidden from invoices when user query the Distil API. Default is empty.

## Playbooks

Once the collection has been installed, the playbooks documented below can be run
from the command line using the `ansible-playbook` command.

```bash
ansible-playbook -i <path-to-inventory> catalystcloud.distil.deploy
```

You can also optionally use `--limit` to run playbooks on specific hosts.

To run a Distil collection playbook from inside another playbook, import it into your playbook using
[`ansible.builtin.import_playbook`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_playbook_module.html).

```yaml
---

- name: Deploy Distil
  ansible.builtin.import_playbook: catalystcloud.distil.deploy
```

### `catalystcloud.distil.deploy`

Deploy all Distil services to all nodes.

This is the standard playbook to be used for releases.
It also can be used to install Distil on a new node in a region where Distil is already running.

This playbook deploys Distil one-by-one on each host, ensuring there is little to no downtime
of the service for API access and billing.
Deploys are idempotent, and services are only restarted on a host if the service was updated.

**Do not use this playbook when a database migration of Distil is required.**
**Database migrations are NOT performed by this playbook.**
**Use the [`catalystcloud.distil.upgrade`](#catalystclouddistilupgrade) playbook**
**for version upgrades of Distil.**

Related playbooks:

* `catalystcloud.distil.deploy_distil` - Deploy Distil (to nodes with all services installed, not service-specific nodes)
* `catalystcloud.distil.deploy_api` - Deploy Distil API (to dedicated nodes only)
* `catalystcloud.distil.deploy_manage` - Deploy Distil Manage (to dedicated nodes only)
* `catalystcloud.distil.deploy_exporter` - Deploy Distil Exporter (to dedicated nodes only)
* `catalystcloud.distil.deploy_collector` - Deploy Distil Collector (to dedicated nodes only)
* `catalystcloud.distil.deploy_openstack` - Deploy Distil OpenStack resources (e.g. Keystone)

### `catalystcloud.distil.upgrade`

Upgrade all Distil services on all nodes.

This playbook serves two main purposes:

* Upgrading Distil in an existing region when a database migration is required (e.g. version upgrade).
* Bootstrap a new installation of Distil in a new region.

The following process is undertaken when upgrading:

1. Stop and disable all Distil services on all nodes, to ensure the database is not being used during migration.
1. Upgrade the Distil service resources on OpenStack (e.g. Keystone).
1. Upgrade Distil API, Distil Exporter and Distil Collector on all nodes.
1. Migrate the Distil database.
    * The database migration is only performed once, on the first node to be upgraded.
1. Restart Distil API, Distil Exporter and Distil Collector on all nodes.

**Take care when using this playbook, as Distil is completely shutdown while upgrading.**
**This results in a short Distil API outage (affecting the billing dashboard customers use).**
**Distil Collector may also fall behind on collection if the outage is for an extended period.**

If Distil is not changed in the release, or the upgrade is limited to changes
that do not require a database migration, use the
[`catalystcloud.distil.deploy`](#catalystclouddistildeploy) playbook.

### `catalystcloud.distil.enable`

Start all Distil services on all nodes, and ensure they are configured to start automatically when the node restarts.

* `catalystcloud.distil.enable_api` - Enable only Distil API
* `catalystcloud.distil.enable_exporter` - Enable only Distil Exporter
* `catalystcloud.distil.enable_collector` - Enable only Distil Collector

### `catalystcloud.distil.stop`

Temporarily stop all Distil services on all nodes, without disabling startup on next boot.

* `catalystcloud.distil.stop_api` - Stop only Distil API
* `catalystcloud.distil.stop_exporter` - Stop only Distil Exporter
* `catalystcloud.distil.stop_collector` - Stop only Distil Collector

### `catalystcloud.distil.disable`

Stop all Distil services on all nodes, and ensure they do not restart if the node restarts.

* `catalystcloud.distil.disable_api` - Disable only Distil API
* `catalystcloud.distil.disable_exporter` - Disable only Distil Exporter
* `catalystcloud.distil.disable_collector` - Disable only Distil Collector

### `catalystcloud.distil.decommission`

Completely uninstall all Distil services from all nodes, and remove service files.

Related playbooks (note that these will not remove the base service files, only service-specific files):

* `catalystcloud.distil.decommission_api` - Decommission only Distil API
* `catalystcloud.distil.decommission_manage` - Decommission only Distil Manage
* `catalystcloud.distil.decommission_exporter` - Decommission only Distil Exporter
* `catalystcloud.distil.decommission_collector` - Decommission only Distil Collector
* `catalystcloud.distil.decommission_openstack` - Decommission only Distil OpenStack resources (e.g. Keystone)

### Other playbooks

The following additional playbooks are also available, but are generally not intended to be used for regular releases.

These playbooks are used internally by other playbooks.

#### `catalystcloud.distil.install`

Install all Distil service files to all nodes.

Differs from `deploy` and `upgrade` by simply installing/updating the service files, without managing running services.

Related playbooks:

* `catalystcloud.distil.install_base` - Install only Distil base service files
* `catalystcloud.distil.install_api` - Install only Distil API
* `catalystcloud.distil.install_manage` - Install only Distil Manage
* `catalystcloud.distil.install_exporter` - Install only Distil Exporter
* `catalystcloud.distil.install_collector` - Install only Distil Collector
* `catalystcloud.distil.install_openstack` - Install only Distil OpenStack resources (e.g. Keystone)

#### `catalystcloud.distil.uninstall`

Remove all Distil service files from all nodes.

Used as the service uninstallation step in the [`catalystcloud.distil.decommission`](#catalystclouddistildecommission) playbooks.

Related playbooks:

* `catalystcloud.distil.uninstall_base` - Uninstall only Distil base services files
* `catalystcloud.distil.uninstall_api` - Uninstall only Distil API
* `catalystcloud.distil.uninstall_manage` - Uninstall only Distil Manage
* `catalystcloud.distil.uninstall_exporter` - Uninstall only Distil Exporter
* `catalystcloud.distil.uninstall_collector` - Uninstall only Distil Collector
* `catalystcloud.distil.uninstall_openstack` - Uninstall only Distil OpenStack resources (e.g. Keystone)

#### `catalystcloud.distil.predeploy`

Run pre-deploy tasks on all nodes.

Usually used for shutting down old versions of services.

Run as part of the the [`catalystcloud.distil.deploy`](#catalystclouddistildeploy) and [`catalystcloud.distil.upgrade`](#catalystclouddistilupgrade) playbooks.

Related playbooks:

* `catalystcloud.distil.predeploy_base` - Run pre-deploy tasks only for Distil base services files
* `catalystcloud.distil.predeploy_api` - Run pre-deploy tasks only for Distil API
* `catalystcloud.distil.predeploy_manage` - Run pre-deploy tasks only for Distil Manage
* `catalystcloud.distil.predeploy_exporter` - Run pre-deploy tasks only for Distil Exporter
* `catalystcloud.distil.predeploy_collector` - Run pre-deploy tasks only for Distil Collector
* `catalystcloud.distil.predeploy_openstack` - Run pre-deploy tasks only for Distil OpenStack resources (e.g. Keystone)

#### `catalystcloud.distil.postdeploy`

Run post-deploy tasks on all nodes.

Usually used for cleaning up old service files.

Run as part of the the [`catalystcloud.distil.deploy`](#catalystclouddistildeploy) and [`catalystcloud.distil.upgrade`](#catalystclouddistilupgrade) playbooks.

Related playbooks:

* `catalystcloud.distil.postdeploy_base` - Run post-deploy tasks only for Distil base services files
* `catalystcloud.distil.postdeploy_api` - Run post-deploy tasks only for Distil API
* `catalystcloud.distil.postdeploy_manage` - Run post-deploy tasks only for Distil Manage
* `catalystcloud.distil.postdeploy_exporter` - Run post-deploy tasks only for Distil Exporter
* `catalystcloud.distil.postdeploy_collector` - Run post-deploy tasks only for Distil Collector
* `catalystcloud.distil.postdeploy_openstack` - Run post-deploy tasks only for Distil OpenStack resources (e.g. Keystone)

## Roles

### Main Roles

The following main roles are available for general use to manage the main Distil services.

* `catalystcloud.distil.base` - Manage Distil base files (common to all services).
* `catalystcloud.distil.api` - Manage Distil API.
* `catalystcloud.distil.manage` - Manage Distil Manage.
* `catalystcloud.distil.exporter` - Manage Distil Exporter.
* `catalystcloud.distil.collector` - Manage Distil Collector.
* `catalystcloud.distil.keystone` - Manage Distil service resources in Keystone.

By default, these roles will install/update and start the relevant service,
restarting running services if there were changes.

They also contain additional tasks used for other purposes,
which can be run using the
[`ansible.builtin.include_role`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html)
module and the `tasks_from` parameter:

* `predeploy` - Run pre-deploy tasks (usually used for shutting down old versions of services)
* `install` - Install the service onto the host (update if already installed)
* `enable` - Enable and start the service on the host (if not already enabled and running)
* `stop` - Stop the service on the host (if running), without disabling running on startup
* `disable` - Stop and disable the service on the host (if not already stopped and disabled)
* `uninstall` - Uninstall the service from the host (if not already uninstalled)
* `postdeploy` - Run post-deploy tasks (usually used for cleaning up old service files)

Some roles have additional tasks available for specific purposes.

* The `catalystcloud.distil.keystone` role contains an `authenticate` task for authentication with Keystone in the target region.
* The `catalystcloud.distil.manage` role contains a `migrate` role for migrating the Distil database.

### Other Roles

The following roles are also available in this collection, but not intended to be used under normal circumstances.

* `catalystcloud.distil.common` - Provides defaults for common variables.
    * Called internally by the main roles, so this role should not be used directly.

## Testing

This repository contains [pre-commit hooks](https://pre-commit.com) for linting purposes,
and a [Molecule](https://ansible.readthedocs.io/projects/molecule) test suite for
running the collection and verifying the results are correct.

Both of them are run automatically using GitHub Actions for pull requests
and the `main` branch.
