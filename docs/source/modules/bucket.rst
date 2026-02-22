Bucket Modules
==============

Why a bucket upload step is required
------------------------------------

The generated video exists on local disk. Instagram publishing is done through
the Graph API, which expects a publicly reachable media URL during media object
creation. The bucket layer uploads the local file and returns that URL.

Provider order (current behavior)
---------------------------------

1. Primary: Imgur
2. Fallback: tmpfiles.org

If Imgur upload fails, the pipeline automatically falls back to tmpfiles.org.

Bucket Orchestrator
-------------------

.. automodule:: app.bucket.main
   :members:
   :undoc-members:
   :show-inheritance:

Imgur Provider
--------------

.. automodule:: app.bucket.imgur
   :members:
   :undoc-members:
   :show-inheritance:

tmpfiles Provider
-----------------

.. automodule:: app.bucket.tmpfiles
   :members:
   :undoc-members:
   :show-inheritance:

Additional/utility bucket modules
---------------------------------

.. automodule:: app.bucket.generate_imgur_access_token
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.bucket.giphy
   :members:
   :undoc-members:
   :show-inheritance:
