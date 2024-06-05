==================================
Catalystcloud.Distil Release Notes
==================================

.. contents:: Topics

v1.0.1
======

Release Summary
---------------

This release fixes a bug with Keystone endpoint generation when SSL is disabled, and changes variable defaults so that the collection is easier to run on standard deployments made using Kolla-Ansible.

Minor Changes
-------------

- Add a new ``distil_api_url`` inventory variable for dynamically generating (or overriding) the "public facing" Distil API URL. ``distil_keystone_endpoint_url`` now references this new variable.
- Change the default value for ``distil_keystone_user_project`` to ``service``, to make it easier to set up the collection to deploy to OpenStack deployments created using Kolla-Ansible.

Bugfixes
--------

- When SSL is disabled for Distil API, make sure the Keystone service endpoint URL is generated as an HTTP URL, instead of HTTPS.

v1.0.0
======

Release Summary
---------------

Initial release of the Ansible collection for OpenStack Distil.
