# KenPom scraper 🏀

![tests](https://github.com/stvsmth/kenpom/workflows/tests/badge.svg)

A bit of Python to scrape the front page of the wonderfully useful
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

You will probably forget this and never even care. However, if your search returns more
or fewer schools than you were expecting, this might be why.

### Examples

#### Interactive mode

All the following examples will work in the interactive mode as well.

To leave interactive mode type `q`, `quit`, or `exit`. For clarity, we'll remove the
`Data through` footer for the remaining examples.

    (kenpom) $ python kenpom.py
    Top `n`, code(s), conference(s), or school(s) [25]: 5
        Team   Code  Rank  Off / Def    Rec  Conf
    ---------------------------------------------
     Gonzaga   GONZ     1    1 /  11   17-0   WCC
      Baylor    BAY     2    3 /   2   16-0   B12
    Michigan   MICH     3    8 /   5   13-1   B10
        Iowa   IOWA     4    2 /  97   12-4   B10
     Houston    HOU     5   17 /   3   14-1  Amer

     Data through games of Saturday, January 30  (2603 games)

    Top `n`, code(s), conference(s), or school(s) [25]: quit

[//]: # (Edit doc-gen.txt rather than the following content)
#### Search by school code, 'cause typing is hard
    (kenpom) $ python kenpom.py umbc
    Team   Code  Rank  Off / Def    Rec  Conf
    -----------------------------------------
    UMBC   UMBC   178  240 / 136   10-3    AE


[//]: # (Edit doc-gen.txt rather than the following content)
#### Probably the most useful mode ... compare two teams that are playing
    (kenpom) $ python kenpom.py sfbk,sfpa
             Team   Code  Rank  Off / Def    Rec  Conf
    --------------------------------------------------
    St Francis PA   SFPA   271  270 / 260    5-9   NEC
    St Francis NY   SFBK   297  262 / 302    4-4   NEC


[//]: # (Edit doc-gen.txt rather than the following content)
#### Get the top `n` teams
    (kenpom) $ python kenpom.py 7
         Team   Code  Rank  Off / Def    Rec  Conf
    ----------------------------------------------
      Gonzaga   GONZ     1    1 /  11   17-0   WCC
       Baylor    BAY     2    3 /   2   16-0   B12
     Michigan   MICH     3    8 /   5   13-1   B10
         Iowa   IOWA     4    2 /  97   12-4   B10
      Houston    HOU     5   17 /   3   14-1  Amer
    Villanova   NOVA     6    4 /  38   11-1    BE
     Illinois    ILL     7    7 /  18   11-5   B10


[//]: # (Edit doc-gen.txt rather than the following content)
#### Find all teams with `Valley` in the title ...
    (kenpom) $ python kenpom.py Valley
                     Team   Code  Rank  Off / Def    Rec  Conf
    ----------------------------------------------------------
     UT Rio Grande Valley    RIO   222  299 / 144    8-3   WAC
              Utah Valley    UVU   254  244 / 262    6-7   WAC
    Mississippi Valley St   MVSU   357  357 / 357   0-14  SWAC


[//]: # (Edit doc-gen.txt rather than the following content)
#### ... include `southern` matches too
    (kenpom) $ python kenpom.py valley,SOUTHERN
                     Team   Code  Rank  Off / Def    Rec  Conf
    ----------------------------------------------------------
            Southern Utah    SUU   196  130 / 291   11-3  BSky
        Southern Illinois    SIU   209  197 / 241    7-6   MVC
     UT Rio Grande Valley    RIO   222  299 / 144    8-3   WAC
            Southern Miss    USM   246  305 / 181   7-10  CUSA
           Texas Southern   TXSO   247  250 / 249    4-7  SWAC
              Utah Valley    UVU   254  244 / 262    6-7   WAC
         Georgia Southern   GASO   266  314 / 193   11-8    SB
                 Southern    SOU   276  317 / 196    4-6  SWAC
      Charleston Southern   CHSO   343  342 / 311   1-15  BSth
    Mississippi Valley St   MVSU   357  357 / 357   0-14  SWAC


[//]: # (Edit doc-gen.txt rather than the following content)
#### Partial names matches, 'cause typing is hard ...
    (kenpom) $ python kenpom.py colo
        Team   Code  Rank  Off / Def    Rec  Conf
    ---------------------------------------------
    Colorado   COLO    17   12 /  46   13-5   P12


[//]: # (Edit doc-gen.txt rather than the following content)
#### ... Whoops, colo is a school code, so expand the search term.
    (kenpom) $ python kenpom.py color
                 Team   Code  Rank  Off / Def    Rec  Conf
    ------------------------------------------------------
             Colorado   COLO    17   12 /  46   13-5   P12
          Colorado St    CSU    67   70 /  67   12-4   MWC
    Northern Colorado   UNCO   234  241 / 226    8-8  BSky


[//]: # (Edit doc-gen.txt rather than the following content)
#### Use quotes to find a name with spaces
    (kenpom) $ python kenpom.py "virginia tech"
             Team   Code  Rank  Off / Def    Rec  Conf
    --------------------------------------------------
    Virginia Tech     VT    29   50 /  21   13-3   ACC


[//]: # (Edit doc-gen.txt rather than the following content)
#### ... or single quotes ...
    (kenpom) $ python kenpom.py 'NORTH DAKOTA'
               Team   Code  Rank  Off / Def    Rec  Conf
    ----------------------------------------------------
    North Dakota St   NDSU   153  188 / 133   10-8   Sum
       North Dakota    UND   319  311 / 292   5-14   Sum


[//]: # (Edit doc-gen.txt rather than the following content)
#### ... or plus sign if you forget to start with a quote
    (kenpom) $ python kenpom.py Virginia+Tech
             Team   Code  Rank  Off / Def    Rec  Conf
    --------------------------------------------------
    Virginia Tech     VT    29   50 /  21   13-3   ACC


[//]: # (Edit doc-gen.txt rather than the following content)
#### Search by a conference
    (kenpom) $ python kenpom.py meac
                      Team   Code  Rank  Off / Def    Rec  Conf
    -----------------------------------------------------------
                Norfolk St   NORF   241  220 / 268    9-6  MEAC
    North Carolina Central   NCCU   258  269 / 244    2-3  MEAC
                 Morgan St   MORG   259  247 / 266    9-4  MEAC
               Florida A&M   FAMU   299  325 / 219    2-7  MEAC
        North Carolina A&T   NCAT   307  286 / 301    7-9  MEAC
                    Howard    HOW   309  236 / 338    1-4  MEAC
                 Coppin St   COPP   322  345 / 194   6-10  MEAC
           Bethune Cookman   COOK   347  340 / 339    0-0  MEAC
               Delaware St    DSU   352  335 / 354   0-11  MEAC
    Maryland Eastern Shore   UMES   354  355 / 331    0-0  MEAC
         South Carolina St   SCST   355  353 / 348   0-13  MEAC


[//]: # (Edit doc-gen.txt rather than the following content)
#### ... or several conferences
    (kenpom) $ python kenpom.py b12,ACC,B10
              Team   Code  Rank  Off / Def    Rec  Conf
    ---------------------------------------------------
            Baylor    BAY     2    3 /   2   16-0   B12
          Michigan   MICH     3    8 /   5   13-1   B10
              Iowa   IOWA     4    2 /  97   12-4   B10
          Illinois    ILL     7    7 /  18   11-5   B10
          Virginia    UVA     9   11 /  16   11-3   ACC
             Texas    TEX    10   19 /   9   11-3   B12
            [snip]    ...   ...  ...   ....   ...   ...
          Nebraska    NEB   124  134 / 119    4-8   B10
           Iowa St    ISU   131  139 / 130    2-9   B12
         Kansas St    KSU   183  191 / 203   5-13   B12
