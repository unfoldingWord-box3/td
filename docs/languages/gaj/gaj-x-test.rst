.. _gaj-x-test:

Gadsup Text
===========

.. include:: /includes/note_private_use.txt

.. code-block:: yaml

    ---

    dublin_core:
        conformsto: 'rc0.2'
        contributor:
            - 'A Contributor'
            - 'Another Contributor'
        creator: 'Wycliffe Associates'
        description: 'The Unlocked Literal Bible is an open-licensed version of the Bible that is intended to provide a form-centric translation of the Bible.'
        format: 'text/usfm'
        identifier: 'ulb'
        issued: '2015-12-17'
        language:
            identifier: 'en'
            title: 'English'
            direction: 'ltr'
        modified: '2015-12-22T12:01:30-05:00'
        publisher: 'Door43'
        relation:
            - 'en/udb'
            - 'en/tn'
            - 'en/tq'
            - 'en/tw'
        rights: 'CC BY-SA 4.0'
        source:
            -
                identifier: 'asv'
                language: 'en'
                version: '1901'
        subject: 'Bible translation'
        title: 'Unlocked Literal Bible'
        type: 'book'
        version: '3'

    checking:
        checking_entity:
            - 'Wycliffe Associates'
        checking_level: '3'

    projects:
        -
            categories:
                - 'bible-ot'
            identifier: 'gen'
            path: './content'
            sort: 1
            title: 'Genesis'
            versification: 'kjv'
