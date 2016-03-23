supermercado
============

|Build Status| |codecov.io|

``supermercado`` extends the functionality of ``mercantile`` with
additional powerful (though more dependency heavy) commands

Installation
------------

.. code:: bash

    pip install supermercado

Usage
-----

::

    Usage: supermercado [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      burn   Burn a stream of GeoJSON into a output...
      edges  For a stream of [<x>, <y>, <z>] tiles, return...
      union  Returns the unioned shape of a steeam of...

``supermercado burn``
~~~~~~~~~~~~~~~~~~~~~

Takes an input stream of GeoJSON and returns a stream of intersecting
``[x, y, z]``\ s for a given zoom.

::

     GEOJSON      ------------     BURNTILES
    {       }     supermercado     [x, y, z]
    ...       ==>    burn      ==> ...
    {      }     ------------     [x, y, z] 

.. figure:: https://cloud.githubusercontent.com/assets/5084513/14003508/94bc0994-f110-11e5-8e99-e9aadf07bf8d.png
   :alt: image

   image

::

    cat ellada.geojson | supermercado burn 10 | mercantile shapes | fio collect

.. figure:: https://cloud.githubusercontent.com/assets/5084513/14003559/d5427ba6-f110-11e5-80d5-a2aba6433e77.png
   :alt: image

   image

``supermercado edges``
~~~~~~~~~~~~~~~~~~~~~~

Outputs a stream of ``[x, y, z]``\ s representing the edge tiles of an
input stream. Edge tile = any tile that is either directly adjacent to a
tile that does not exist, or diagonal to an empty tile.

::

    cat ellada.geojson | supermercado burn 10 | supermercado edges | mercantile shapes | fio collect | geojsonio

.. figure:: https://cloud.githubusercontent.com/assets/5084513/14003587/01e8e370-f111-11e5-8df4-ac3ae07bbf92.png
   :alt: image

   image

::

      TILES       ------------     EDGETILES
    [x, y, z]     supermercado     [x, y, z]
    ...       ==>    edges     ==> ...
    [x, y, z]     ------------     [x, y, z] 

``supermercado union``
~~~~~~~~~~~~~~~~~~~~~~

Outputs a stream of unioned GeoJSON. Like ``mercantile shapes`` but as
an overall footprint instead of individual shapes for each tile.

::

    cat ellada.geojson | supermercado burn 10 | supermercado union | fio collect | geojsonio

.. figure:: https://cloud.githubusercontent.com/assets/5084513/14003622/365af88c-f111-11e5-8712-28f42253e270.png
   :alt: image

   image

::

      TILES       ------------      GEOJSON
    [x, y, z]     supermercado      Feature
    ...       ==>    union     ==> collection
    [x, y, z]     ------------     of shape

.. |Build Status| image:: https://travis-ci.com/mapbox/supermercado.svg?token=5hEJ9x9Ljj2yfkNFpMu5&branch=master
   :target: https://travis-ci.com/mapbox/supermercado
.. |codecov.io| image:: https://codecov.io/github/mapbox/supermercado/coverage.svg?token=qkqtUNdabO&branch=master
   :target: https://codecov.io/github/mapbox/supermercado?branch=master
