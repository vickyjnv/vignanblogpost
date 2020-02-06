# Vignan

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b9bdd4c36bd7410abfb992069a25b610)](https://app.codacy.com/manual/oscvizag/vignanblogpost?utm_source=github.com&utm_medium=referral&utm_content=saibhaskar24/vignanblogpost&utm_campaign=Badge_Grade_Dashboard)

To run locally, do the usual:

#. Create a Python 3.5 virtualenv

#. Install dependencies::

    pip install -r requirements.txt


#. Setting up database access

##. Create a superuser::

   ./manage.py createsuperuser

Supported browsers
------------------

The goal of the site is to target various levels of browsers, depending on
their ability to use the technologies in use on the site, such as HTML5, CSS3,
SVG, webfonts.

We're following `Mozilla's example <https://wiki.mozilla.org/Support/Browser_Support>`_
when it comes to categorize browser support.

- Desktop browsers, except as noted below, are **A grade**, meaning that
  everything needs to work.

- IE < 11 is **not supported** (based on Microsoft's support).

- Mobile browsers should be considered **B grade** as well.
  Mobile Safari, Firefox on Android and the Android Browser should support
  the responsive styles as much as possible but some degredation can't be
  prevented due to the limited screen size and other platform restrictions.

File locations
--------------

Static files such as CSS, JavaScript or image files can be found in the
``vignanblogpost/static`` subdirectory.

Templates can be found in the ``vignanblogpost/templates`` subdirectory.

Styles
------

CSS is written in `Bootstrap`.

