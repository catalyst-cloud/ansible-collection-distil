==================================
Catalystcloud.Distil Release Notes
==================================

.. contents:: Topics

v1.0.1
======

Release Summary
---------------

This release fixes a number of bugs, and adds/modifies the options for the collection to make configuring Distil more flexible.

Minor Changes
-------------

- Add a new ``distil_api_url`` inventory variable for dynamically generating (or overriding) the "public facing" Distil API URL. ``distil_keystone_endpoint_url`` now references this new variable.
- Add the ``distil_collector_driver`` inventory variable for changing the driver Distil Collector uses to back usage collection.
- Change the default value for ``distil_keystone_user_project`` to ``service``, to make it easier to set up the collection to deploy to OpenStack deployments created using Kolla-Ansible.
- Make it possible to dynamically configure the RBAC policy using the ``distil_rbac_policy`` inventory variable.

Bugfixes
--------

- Set the RBAC policy file in Distil so that it looks at ``policy.yaml``, instead of the default ``policy.json``.
- When SSL is disabled for Distil API, make sure the Keystone service endpoint URL is generated as an HTTP URL, instead of HTTPS.

v1.0.0
======

Release Summary
---------------

Initial release of the Ansible collection for OpenStack Distil.
