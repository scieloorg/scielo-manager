Setup
=====

This project now targets **Python 3.13+**.

Create a database (preferably PostgreSQL) and configure
``scielomanager/settings_local.include``.

Then run ``make setup``.

Docker (validation)
===================

To validate the project in containers:

1. ``docker compose up --build``
2. Access app at ``http://localhost:8000``
3. Access Mailhog at ``http://localhost:8025``

The compose stack includes: app, PostgreSQL, Redis and Mailhog.

Docs
====

See more information about this project in http://docs.scielo.org

Build status
============

.. image:: https://travis-ci.org/scieloorg/scielo-manager.svg?branch=beta
    :target: https://travis-ci.org/scieloorg/scielo-manager


i18n status
===========

**Current internationalization status**

.. image:: https://www.transifex.com/projects/p/scielomanager/resource/english/chart/image_png
`Help with translations <https://www.transifex.com/projects/p/scielomanager/resource/english/>`_


Use License
===========

FreeBSD 2-clause::

    Copyright (c) 2012, SciELO <scielo-dev@googlegroups.com>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

        Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.

        Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
    NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
    OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
    OF SUCH DAMAGE.
