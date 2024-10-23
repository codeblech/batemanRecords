Scripts Documentation
=====================

This section documents the bash scripts used in batemanRecords.

bateman.sh
----------

.. literalinclude:: ../../bateman.sh
   :language: bash
   :linenos:
   :caption: bateman.sh

Runs cli.py inside poetry shell.

.. code-block:: bash

   # Example usage
   ./bateman.sh [SPOTIFY_URL]

Video Generation Scripts
------------------------

combineAudioVideo.sh
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../scripts/combineAudioVideo.sh
   :language: bash
   :linenos:
   :caption: scripts/combineAudioVideo.sh

This script combines downloaded song and generated video using ffmpeg.

.. code-block:: bash

   # Example usage
   ./scripts/combineAudioVideo.sh input_audio.mp3 input_video.mp4

generateVideoSpotify.sh
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../scripts/generateVideoSpotify.sh
   :language: bash
   :linenos:
   :caption: scripts/generateVideoSpotify.sh

This script generates Bateman video for Spotify cover art. This is specific to Spotify because the resolution is specific to Spotify, and different from YouTube & YouTube Music.

.. code-block:: bash

   # Example usage
   ./scripts/generateVideoSpotify.sh [bgImagePath]