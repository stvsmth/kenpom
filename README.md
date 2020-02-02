# KenPom scraper 🏀

![tests](https://github.com/stvsmth/kenpom/workflows/tests/badge.svg)

A little bit of Python to scrape the front page of the wonderfully useful
[KenPom](https://kenpom.com) site for NCAA basketball statistics. This tool assumes
you are comfortable on the command-line and basic Python tooling like `pip`. It's
not really useful unless you like tinkering with Python.

Why scrape? Well, if your team rarely haunts the top 25 and/or your curious how your
team ranks against other non-ranked teams, KenPom is one way to compare relative
strengths. This is probably only useful to folks who like tinkering in Python.

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
filter on conference(s), school names(s), or the top `n` schools. With no input we
simply print the top 25 teams. Conference names must match exactly and school names
will match on any string. See the examples below for the finer points.

### Search order precedence
If any school code (KU, UK, OKLA, etc) is present, then the entire search will
proceed as a code search. Conference searches are executed with the same rules: if any
conference is supplied, we'll perform a conference search.

Only after checking for school code(s) and conference code(s) will we match on school
name(s).

You will probably forget this and never even care. But if your search returns more or
fewer schools than you were expecting, this is probably why.

### Examples

Without any command line options, we'll prompt you for one of three values: `n` for
a top-`n` search, a conference code, or a school name. The default is a top-25 search.

#### Interactive mode

All the following examples will work in interactive mode as well. To leave interactive
mode type `q`, `quit`, or `exit`.

    (kenpom) $ python kenpom.py
    Data through games of Saturday, February 1
    Top `n`, 0 for all, school(s), or conference(s) [25]: 5

          Kansas     1   18-3  B12
            Duke     2   18-3  ACC
          Baylor     3   19-1  B12
    San Diego St     4   23-0  MWC
         Gonzaga     5   23-1  WCC

    Top `n`, 0 for all, school(s), or conference(s) [25]: q

#### Search by school abbreviation, 'cause typing is hard
    (kenpom) $ python kenpom.py umbc
    Data includes 11 of 14 games played on Monday, February 3

    UMBC   303   9-14  AE

#### Probably the most useful mode ... compare two teams that are playing
    (kenpom) $ python kenpom.py sfbk,sfpa
    Data includes 11 of 14 games played on Monday, February 3

    St Francis PA   204   14-8  NEC
    St Francis NY   300  10-12  NEC

#### Get the top `n` teams
    (kenpom) $ python kenpom.py 7
    Data includes 11 of 14 games played on Monday, February 3

           Kansas     1   18-3  B12
             Duke     2   18-3  ACC
           Baylor     3   19-1  B12
     San Diego St     4   23-0  MWC
          Gonzaga     5   23-1  WCC
           Dayton     6   20-2  A10
    West Virginia     7   17-4  B12

#### Find all teams with `Valley` in the title ...
    (kenpom) $ python kenpom.py Valley
    Data includes 11 of 14 games played on Monday, February 3

              Utah Valley   261   9-14  WAC
     UT Rio Grande Valley   262   7-14  WAC
    Mississippi Valley St   352   2-20  SWAC

#### ... include `southern` matches too
    (kenpom) $ python kenpom.py valley,SOUTHERN
    Data includes 11 of 14 games played on Monday, February 3

            Southern Utah   137   13-8  BSky
        Southern Illinois   147  13-10  MVC
         Georgia Southern   153  13-10  SB
           Texas Southern   251  10-12  SWAC
            Southern Miss   255   7-16  CUSA
              Utah Valley   261   9-14  WAC
     UT Rio Grande Valley   262   7-14  WAC
      Charleston Southern   293  11-11  BSth
                 Southern   299   9-13  SWAC
    Mississippi Valley St   352   2-20  SWAC

#### Partial names matches, 'cause typing is hard ...
    (kenpom) $ python kenpom.py colo
    Data includes 11 of 14 games played on Monday, February 3

    Colorado    16   17-5  P12

#### ... Whoops, colo is a school code, so expand the search term.
    (kenpom) $ python kenpom.py color
    Data includes 11 of 14 games played on Monday, February 3

             Colorado    16   17-5  P12
          Colorado St    88   16-8  MWC
    Northern Colorado    91   14-7  BSky

#### Use quotes to find a name with spaces
    (kenpom) $ python kenpom.py "virginia tech"
    Data includes 11 of 14 games played on Monday, February 3

    Virginia Tech    84   14-8  ACC

#### .. or single quotes ...
    (kenpom) $ python kenpom.py 'NORTH DAKOTA'
    Data includes 11 of 14 games played on Monday, February 3

    North Dakota St   129   16-7  Sum
       North Dakota   227  10-13  Sum

#### ... or plus sign if you forget to start with a quote
    (kenpom) $ python kenpom.py Virginia+Tech
    Data includes 11 of 14 games played on Monday, February 3

    Virginia Tech    84   14-8  ACC

#### Search by a conference
    (kenpom) $ python kenpom.py meac
    Data includes 11 of 14 games played on Monday, February 3

                Norfolk St   246  10-13  MEAC
    North Carolina Central   257  10-12  MEAC
        North Carolina A&T   277  12-12  MEAC
           Bethune Cookman   279  10-12  MEAC
               Florida A&M   301   7-13  MEAC
                 Morgan St   316  12-12  MEAC
                 Coppin St   327   7-17  MEAC
         South Carolina St   333   9-12  MEAC
               Delaware St   346   3-18  MEAC
                    Howard   349   2-22  MEAC
    Maryland Eastern Shore   350   3-19  MEAC

#### ... or two conferences
    (kenpom) $ python kenpom.py b12,ACC
    Data includes 11 of 14 games played on Monday, February 3

            Kansas     1   18-3  B12
              Duke     2   18-3  ACC
            Baylor     3   19-1  B12
     West Virginia     7   17-4  B12
        Louisville     8   19-3  ACC
            [snip]   ...    ...  ...
       Wake Forest   105  10-11  ACC
          Miami FL   115  11-10  ACC
    Boston College   162  11-11  ACC
