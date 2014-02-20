Rapp
====

Rapp infers `rocon_app` or `robot_app` used in `Robotics in Concert`_

.. _`Robotics in Concert`: http://www.robotconcert.org

Meta Rapp is a virtual rapp which does not have launch information



Export
------

Rapp is exported via package.xml. Indexer searches for `rocon_app` in export tag to collect all available rapps.

.. code-block:: xml

    ...
    <export>
      <rocon_app>apps/chirp/chirp.rapp</rocon_app>
    </export>
    ...

