tweetjobs
=========

Tools for manipulating Twitter data.

Python

-  ``json2ttv2`` converts directories full of Twitter ``.json`` files
   into ``.ttv2`` files, bzip2'ing them, and ensuring that the result is
   within a reasonable size of the source (greater than 2%, but less
   than 6%) before deleting the original json.
-  ``twitter-user`` pulls down the ~3,200 (max) tweets that are
   accessible for a given user (also depends on the ``~/.twitter`` auth
   file).

TTV2
----

TTV2 is the Tweet tab-separated format version 2, the specification is
below. Fields are 1-indexed for easy AWKing (see Markdown source for
0-indexing).

0.  tweet\_id
1.  created\_at parsed into YYYYMMDDTHHMMSS, implicitly UTC
2.  text, newlines and tabs converted to spaces, html entities replaced,
    t.co urls resolved
3.  lon,lat
4.  place\_id
5.  place\_str
6.  in\_reply\_to\_status\_id
7.  in\_reply\_to\_screen\_name
8.  retweet\_id id of the original tweet
9.  retweet\_count
10. user.screen\_name
11. user.id
12. user.created\_at parsed into YYYYMMDDTHHMMSS
13. user.name
14. user.description
15. user.location
16. user.url
17. user.statuses\_count
18. user.followers\_count
19. user.friends\_count
20. user.favourites\_count
21. user.geo\_enabled
22. user.default\_profile
23. user.time\_zone
24. user.lang
25. user.utc\_offset

This format is not the default, and will be the output only when you use
the ``--ttv2`` option.

Python contents vs. Javascript contents
---------------------------------------

::

    easy_install -U tweetjobs

The Python and Javascript components are mostly complementary. The
Javascript offers crawlers, Python provides post-processing.

Testing with Travis CI
----------------------

The tested CLI commands now check for OAuth in specific environment
variables before reading the given ``--accounts`` file or the default
one (``~/.twitter``).

To get tests to run on Travis CI, we can use ``travis`` command line
tool to encrypt a quad of valid Twitter OAuth credentials so that only
Travis CI can see them.

Put together a file that looks like this (call it ``twilight.env``):

::

    consumer_key=bepLTQD5ftZCjqhXgkuJW
    consumer_secret=jZ4HEYgNRKwJykbh5ptmcqV7v0o2WODdiMTF1fl6B9X
    access_token=167246169-e1XTUxZqLnRaEyBF8KwOJtbID26gifMpAjukN5vz
    access_token_secret=OVm7fJt8oY0C9kBsvych6Duq5pNIUxwagG143HdR

And then, from within the root directory of this git repository, run the
following sequence:

::

    gem install travis
    travis encrypt -s -a < twilight.env

``.travis.yml`` should now have those variables, but encrypted with
Travis CI's public key.

License
-------

Copyright © 2011–2013 Christopher Brown. `MIT
Licensed <https://github.com/chbrown/twilight/blob/master/LICENSE>`__.
