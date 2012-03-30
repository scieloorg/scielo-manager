.. _ReSTQuickRef: http://docutils.sourceforge.net/docs/user/rst/quickref.html#definition-lists

How to deal with help texts
===========================

Help texts are used at form field level to, like the name suggests, help the user
recognize and enter data in a desired format. There are cases where we expect data conforming
certain standards, like ISO, and we found to be proper to offer a more sophisticated help
description for these fields.

We decided to separate help texts in two levels: The Short and the Detailed description versions.


Short Description
-----------------

The help texts that users will see next to form fields.

In order to edit, remove or add new short descriptions, follow the steps:

1. Edit <app>/helptexts.py;
2. Search for the block of help definitions you will deal with. Blocks are grouped by the model
   class name;
3. Follow the naming convention for the help text identifier: CLASSNAME__FIELD_NAME (classname
   in uppercase, plus double underscores, plus the attribute name the text refers to in uppercase)


Example::

  #models.JournalParallellTitles.form

  JOURNALPARALLELTITLES__FORM = _("""Enter parallel titles in accordance with the sequence and
    typography in which they appear on the title page or its substitute.""")


Detailed Description
--------------------

When a more detailed level of information is needed, we must follow the steps:

1. Create a `Short Description`_ for the given help text;
2. Edit ``docs/en/glossary.rst`` and add a new definition entry. See ReSTQuickRef_ for more
   details about the syntax.
3. Push to the project's main repository and the documentation will be built automagically.


Template Tag
------------

Uses the custom template tag ``{% load journalmanager_template_tags %}``.

In order to add the help widget, you need to use the ``field_help`` django template tag::

  {% field_help <label> <help_text> <glossary-term> %}

Example, for the ``title`` field would be::

  {% field_help add_form.title.label add_form.title.help_text term-title %}