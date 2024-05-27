# `catalystcloud.distil.api`

An Ansible role for managing Distil API.

Distil API runs the OpenStack rating service API, which can be queried
using the `openstack rating` commands provided by the
[`python-distilclient`](https://pypi.org/project/python-distilclient) package,
or via the dashboard using the [Distil UI](https://opendev.org/x/distil-ui) plugin for Horizon.

Distil API uses a configurable ERP driver for a number of functions:

* Querying for invoices from previous months
* Fetching a list of products with prices, for generating the current month's quotations

The Ansible collection configures Distil to use the `jsonfile` ERP driver by default.
This reads a list of products and prices from a `products.json` file that is installed
with the configuration, and allows Distil to work in test environments without a functioning
Odoo installation.

To use Distil with Odoo, the ERP driver will need to be changed to `odoo` using the inventory,
as documented below.

By default, a service container named `distil-api` will be created on the host.

Distil API is run as a WSGI app within [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest),
serving HTTPS to port 9999 by default, with 3 workers and 3 concurrent threads per worker.

For more information, check the documentation for the `catalystcloud.distil` collection.
