# KenPom scraper

A little bit of Python to scrape the front page of the wonderfully useful
[KenPom](https://kenpom.com) site for NCAA basketball statistics. This tool assumes
you are comfortable on the command-line.

Why scrape? Well, if your team rarely haunts the top 25 and/or your curious how your
team ranks against other non-ranked teams, KenPom is one way to compare relative
strengths.  I find I this tool particularly useful on my iPhone with
[Pythonista](http://omz-software.com/pythonista/).

This may run on Python 3.5 or earlier, but I find f-strings delightful, so I'm only
testing 3.6 and greater.

![tests](https://github.com/stvsmth/kenpom/workflows/tests/badge.svg)

## Installation

This is tool primarily uses [requests](https://requests.readthedocs.io/en/master/)
and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). While not
required, using virtual environments is almost always the smart thing to do. Also, we
use some pre-commit hooks to keep things formatted nicely and avoid some silly mistakes.

```bash
git clone https://github.com/stvsmth/kenpom.git
python3 -m venv kenpom
cd kenpom && source bin/activate
pip install -r requirements.txt
pre-commit install
pytest tests
```

## Usage

You can pass filtering options in via command-line arguments or as prompted. We'll
filter on conference(s), school names(s), or the top `n` schools. Conference and
school names are case insensitive. While conference names must match exactly, school
names will match on any string. For example, `irgini` will match schools with `Virginia`
in the name.

#### Conference name vs school name searches
Conference searches take precedence over school name searches.

You will probably forget this and never even care. Unless, that is, you're fond of
American University (for which searching `amer` will return the American Athletic
Conference schools) or short search strings like `be` (Big East). Generally speaking,
you should **use four characters or more for school name searches**. You've been warned.

#### Basic usage: show all rankings in descending order

    (kenpom) $ python kenpom.py
    Top `n`, 0 for all, or conference list [0]: acc,sec

                Duke     2   17-3  ACC
          Louisville    10   17-3  ACC
          Florida St    18   17-3  ACC
            Kentucky    25   15-4  SEC
            Arkansas    28   15-4  SEC
                 LSU    33   15-4  SEC
               [snip]  ...    ...  ...
      Boston College   166  10-10  ACC
          Vanderbilt   183   8-11  SEC

    Data through games of Tuesday, January 28
     (3802 games)

We'll be leaving out the footer for the remaining examples.

#### Searching for schools by name(s)

This is probably the most useful mode. Your team is playing Duke? How do they match up?

    (kenpom) $ python kenpom.py duke,woff

        Duke     2   17-3  ACC
     Wofford   147   14-8  SC

#### Searching for schools by full name(s)

Searching for schools by full name, when that name includes a space, requires some care.
You can either quote the school name(s):

    (kenpom) $ python kenpom.py "virginia tech","florida st"

        Florida St    21   17-3  ACC
     Virginia Tech    72   14-7  ACC

Or you can use a plus sign (+) in lieu of a space. This is handy if you start typing and
are too lazy to go back and add a leading quote.

    (kenpom) $ python kenpom.py virginia+tech

     Virginia Tech    72   14-7  ACC


#### Schools in one or more conferences

    (kenpom) $ python kenpom.py wyom,woff

         Wofford   147   14-8  SC
         Wyoming   297   5-17  MWC

#### Fetch the top `n` teams

    (kenpom) $ python kenpom.py 7

            Kansas     1   17-3  B12
              Duke     2   17-3  ACC
           Gonzaga     3   21-1  WCC
            Baylor     4   17-1  B12
            Dayton     5   18-2  A10
     West Virginia     6   16-3  B12
       Michigan St     7   15-5  B10

#### Schools in one or more conferences
    (kenpom) $ python kenpom.py acc

               Duke     2   17-3
         Louisville    10   17-3
         Florida St    18   17-3
             [snip]   ...    ...
           Miami FL   112   11-9
     Boston College   166  10-10

    (kenpom) $ python kenpom.py ACC,SEC

                Duke     2   17-3  ACC
          Louisville    10   17-3  ACC
          Florida St    18   17-3  ACC
            Kentucky    25   15-4  SEC
            Arkansas    28   15-4  SEC
                 LSU    33   15-4  SEC
               [snip]  ...    ...  ...
      Boston College   166  10-10  ACC
          Vanderbilt   183   8-11  SEC

#### Explicitly fetch all rankings

    (kenpom) $ python kenpom.py 0

             Kansas     1   17-3  B12
               Duke     2   17-3  ACC
            Gonzaga     3   21-1  WCC
             [snip]   ...    ...  ...
         Chicago St   353   4-18  WAC
