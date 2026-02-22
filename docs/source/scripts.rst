Scripts Documentation
=====================

This section documents shell scripts currently used in batemanRecords.

bateman.sh
----------

.. literalinclude:: ../../app/bateman.sh
   :language: bash
   :linenos:
   :caption: app/bateman.sh

Runs the CLI entrypoint with Poetry.

.. code-block:: bash

   ./app/bateman.sh "<YOUTUBE_URL>"


Video Generation Scripts
------------------------

combineAudioVideo.sh
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../app/scripts/combineAudioVideo.sh
   :language: bash
   :linenos:
   :caption: app/scripts/combineAudioVideo.sh

Combines generated video with downloaded audio and applies the chosen audio offset.

.. code-block:: bash

   ./app/scripts/combineAudioVideo.sh input_audio.mp3 input_video.mp4 0


generateVideoYoutube.sh
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../app/scripts/generateVideoYoutube.sh
   :language: bash
   :linenos:
   :caption: app/scripts/generateVideoYoutube.sh

Generates the Bateman background-composited video from a thumbnail image.

.. code-block:: bash

   ./app/scripts/generateVideoYoutube.sh [bgImagePath]
