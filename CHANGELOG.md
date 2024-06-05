# Catalystcloud\.Distil Release Notes

**Topics**

- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary-1">Release Summary</a>

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="release-summary"></a>
### Release Summary

This release fixes a bug with Keystone endpoint generation when SSL is disabled\, and changes variable defaults so that the collection is easier to run on standard deployments made using Kolla\-Ansible\.

<a id="minor-changes"></a>
### Minor Changes

* Add a new <code>distil\_api\_url</code> inventory variable for dynamically generating \(or overriding\) the \"public facing\" Distil API URL\. <code>distil\_keystone\_endpoint\_url</code> now references this new variable\.
* Change the default value for <code>distil\_keystone\_user\_project</code> to <code>service</code>\, to make it easier to set up the collection to deploy to OpenStack deployments created using Kolla\-Ansible\.

<a id="bugfixes"></a>
### Bugfixes

* When SSL is disabled for Distil API\, make sure the Keystone service endpoint URL is generated as an HTTP URL\, instead of HTTPS\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary-1"></a>
### Release Summary

Initial release of the Ansible collection for OpenStack Distil\.
