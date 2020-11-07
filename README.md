# KenPom scraper 🏀

![tests](https://github.com/stvsmth/kenpom/workflows/tests/badge.svg)

A little bit of Python to scrape the front page of the wonderfully useful
[KenPom](https://kenpom.com) site for NCAA basketball statistics. This tool assumes
you are comfortable on the command-line and basic Python tooling like `pip`. It's
not really useful unless you like tinkering with Python.

Why scrape? Well, if your team rarely haunts the top 25 and/or your curious how your
team ranks against other non-ranked teams, KenPom is one way to compare relative
strengths.

This requires Python 3.8 or greater.

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
filter on conference(s), school name(s), or the top `n` schools. With no input we
simply print the top 25 teams. School codes and conference names must match exactly.
School names will match on any string. See the examples below for the finer points.

### Search order precedence
If any school code (KU, UK, OKLA, etc) is present, then the entire search will
proceed as a code search. Conference searches are executed with the same rules: if any
conference is supplied, we'll perform a conference search.

Only after checking for school code(s) and conference code(s) will we match on school
name(s).

You will probably forget this and never even care. But if your search returns more or
fewer schools than you were expecting, this is probably why.

### Examples

#### Interactive mode

All the following examples will work in interactive mode as well.

To leave interactive mode type `q`, `quit`, or `exit`. For clarity we'll remove the
`Data through` footer for the remaining examples.

    (kenpom) $ python kenpom.py
    Top `n`, code(s), conference(s), or schools(s) [25]: 5

          Kansas     KU     1   23-3  B12
          Baylor    BAY     2   24-1  B12
         Gonzaga   GONZ     3   26-1  WCC
    San Diego St   SDSU     4   26-0  MWC
            Duke   DUKE     5   22-4  ACC

     Data includes 10 of 55 games played on Thursday, February 20


    Top `n`, code(s), conference(s), or schools(s) [25]: quit

[//]: # (Edit doc-gen.txt rather than the following content)
#### Search by school code, 'cause typing is hard
    (kenpom) $ python kenpom.py umbc

    UMBC   UMBC   275  12-14  AE

[//]: # (Edit doc-gen.txt rather than the following content)
#### Probably the most useful mode ... compare two teams that are playing
    (kenpom) $ python kenpom.py sfbk,sfpa

    St Francis PA   SFPA   178   18-8  NEC
    St Francis NY   SFBK   303  12-14  NEC


[//]: # (Edit doc-gen.txt rather than the following content)
#### Get the top `n` teams
    (kenpom) $ python kenpom.py 7

           Kansas     KU     1   23-3  B12
           Baylor    BAY     2   24-1  B12
          Gonzaga   GONZ     3   26-1  WCC
     San Diego St   SDSU     4   26-0  MWC
             Duke   DUKE     5   22-4  ACC
           Dayton    DAY     6   24-2  A10
    West Virginia    WVU     7   19-7  B12

[//]: # (Edit doc-gen.txt rather than the following content)
#### Find all teams with `Valley` in the title ...
    (kenpom) $ python kenpom.py Valley

     UT Rio Grande Valley    RIO   237  12-14  WAC
              Utah Valley    UVU   263   9-17  WAC
    Mississippi Valley St   MVSU   352   3-23  SWAC

[//]: # (Edit doc-gen.txt rather than the following content)
#### ... include `southern` matches too
    (kenpom) $ python kenpom.py valley,SOUTHERN

            Southern Utah    SUU   151  14-11  BSky
         Georgia Southern   GASO   153  16-11  SB
        Southern Illinois    SIU   166  15-12  MVC
     UT Rio Grande Valley    RIO   237  12-14  WAC
            Southern Miss    USM   241   9-18  CUSA
           Texas Southern   TXSO   252  12-13  SWAC
              Utah Valley    UVU   263   9-17  WAC
                 Southern    SOU   307  11-15  SWAC
      Charleston Southern   CHSO   309  13-14  BSth
    Mississippi Valley St   MVSU   352   3-23  SWAC

[//]: # (Edit doc-gen.txt rather than the following content)
#### Partial names matches, 'cause typing is hard ...
    (kenpom) $ python kenpom.py colo

    Colorado   COLO    17   20-6  P12

[//]: # (Edit doc-gen.txt rather than the following content)
#### ... Whoops, colo is a school code, so expand the search term.
    (kenpom) $ python kenpom.py color

             Colorado   COLO    17   20-6  P12
    Northern Colorado   UNCO    82   17-8  BSky
          Colorado St    CSU    94  18-10  MWC

[//]: # (Edit doc-gen.txt rather than the following content)
#### Use quotes to find a name with spaces
    (kenpom) $ python kenpom.py "virginia tech"

    Virginia Tech     VT    95  15-11  ACC

[//]: # (Edit doc-gen.txt rather than the following content)
#### .. or single quotes ...
    (kenpom) $ python kenpom.py 'NORTH DAKOTA'

    North Dakota St   NDSU   122   20-7  Sum
       North Dakota    UND   234  12-15  Sum

[//]: # (Edit doc-gen.txt rather than the following content)
#### ... or plus sign if you forget to start with a quote
    (kenpom) $ python kenpom.py Virginia+Tech

    Virginia Tech     VT    95  15-11  ACC

[//]: # (Edit doc-gen.txt rather than the following content)
#### Search by a conference
    (kenpom) $ python kenpom.py meac

                Norfolk St   NORF   240  13-13  MEAC
    North Carolina Central   NCCU   276  12-13  MEAC
        North Carolina A&T   NCAT   280  13-14  MEAC
           Bethune Cookman   COOK   294  13-13  MEAC
                 Morgan St   MORG   311  14-14  MEAC
               Florida A&M   FAMU   314  10-14  MEAC
                 Coppin St   COPP   330   8-20  MEAC
         South Carolina St   SCST   334  11-13  MEAC
    Maryland Eastern Shore   UMES   346   5-21  MEAC
               Delaware St    DSU   348   3-22  MEAC
                    Howard    HOW   350   2-24  MEAC

[//]: # (Edit doc-gen.txt rather than the following content)
#### ... or several conferences
    (kenpom) $ python kenpom.py b12,ACC,B10

            Kansas     KU     1   23-3  B12
            Baylor    BAY     2   24-1  B12
              Duke   DUKE     5   22-4  ACC
            [snip]    ...   ...    ...  ...
      Northwestern     NW   124   6-19  B10
          Nebraska    NEB   136   7-18  B10
    Boston College     BC   161  13-14  ACC
