import dataclasses


@dataclasses.dataclass
class KenPom:
    """Lightweight wrapper around all available KenPom stats."""

    rank: int
    name: str
    conf: str
    record: str
    eff_margin: float
    offense: float
    off_rank: int
    defense: float
    def_rank: int
    tempo: float
    tempo_rank: int
    luck: float
    luck_rank: int
    sos_eff_margin: float
    sos_eff_margin_rank: int
    sos_off: float
    sos_off_rank: int
    sos_def: float
    sos_def_rank: int
    sos_non_conf: float
    sos_non_conf_rank: int
    # NOTE: abbrev is NOT in source KenPom data
    # We append it so we can do searches based on score-ticker names (KU, VT, UVA, etc)
    abbrev: str

    def __post_init__(self):
        """Type incoming data.

        We're scraping DOM elements `text` values, so everything comes in as
        text, but we may want actual values (think ACC avg offence rank: 23.
        """
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                setattr(self, field.name, field.type(value))


SCHOOL_DATA_BY_ABBREV = {
    "aamu": {"conf": "swac", "name": "alabama a&m"},
    "acu": {"conf": "slnd", "name": "abilene christian"},
    "afa": {"conf": "mwc", "name": "air force"},
    "akr": {"conf": "mac", "name": "akron"},
    "ala": {"conf": "sec", "name": "alabama"},
    "alby": {"conf": "ae", "name": "albany"},
    "alcn": {"conf": "swac", "name": "alcorn st"},
    "alst": {"conf": "swac", "name": "alabama st"},
    "amcc": {"conf": "slnd", "name": "texas a&m corpus chris"},
    "amer": {"conf": "pat", "name": "american"},
    "app": {"conf": "sb", "name": "appalachian st"},
    "ariz": {"conf": "p12", "name": "arizona"},
    "ark": {"conf": "sec", "name": "arkansas"},
    "army": {"conf": "pat", "name": "army"},
    "arpb": {"conf": "swac", "name": "arkansas pine bluff"},
    "arst": {"conf": "sb", "name": "arkansas st"},
    "asu": {"conf": "p12", "name": "arizona st"},
    "aub": {"conf": "sec", "name": "auburn"},
    "ball": {"conf": "mac", "name": "ball st"},
    "bay": {"conf": "b12", "name": "baylor"},
    "bc": {"conf": "acc", "name": "boston college"},
    "bel": {"conf": "ovc", "name": "belmont"},
    "bgsu": {"conf": "mac", "name": "bowling green"},
    "bing": {"conf": "ae", "name": "binghamton"},
    "brad": {"conf": "mvc", "name": "bradley"},
    "brwn": {"conf": "ivy", "name": "brown"},
    "bry": {"conf": "nec", "name": "bryant"},
    "bsu": {"conf": "mwc", "name": "boise st"},
    "bu": {"conf": "pat", "name": "boston university"},
    "buck": {"conf": "pat", "name": "bucknell"},
    "buff": {"conf": "mac", "name": "buffalo"},
    "but": {"conf": "be", "name": "butler"},
    "byu": {"conf": "wcc", "name": "byu"},
    "cal": {"conf": "p12", "name": "california"},
    "camp": {"conf": "bsth", "name": "campbell"},
    "can": {"conf": "maac", "name": "canisius"},
    "cbu": {"conf": "wac", "name": "cal baptist"},
    "ccar": {"conf": "sb", "name": "coastal carolina"},
    "ccsu": {"conf": "nec", "name": "central connecticut"},
    "char": {"conf": "cusa", "name": "charlotte"},
    "chat": {"conf": "sc", "name": "chattanooga"},
    "chic": {"conf": "wac", "name": "chicago st"},
    "chso": {"conf": "bsth", "name": "charleston southern"},
    "cin": {"conf": "amer", "name": "cincinnati"},
    "cit": {"conf": "sc", "name": "the citadel"},
    "clem": {"conf": "acc", "name": "clemson"},
    "clev": {"conf": "horz", "name": "cleveland st"},
    "clmb": {"conf": "ivy", "name": "columbia"},
    "cmu": {"conf": "mac", "name": "central michigan"},
    "cofc": {"conf": "caa", "name": "charleston"},
    "colg": {"conf": "pat", "name": "colgate"},
    "colo": {"conf": "p12", "name": "colorado"},
    "conn": {"conf": "amer", "name": "connecticut"},
    "cook": {"conf": "meac", "name": "bethune cookman"},
    "copp": {"conf": "meac", "name": "coppin st"},
    "cor": {"conf": "ivy", "name": "cornell"},
    "cp": {"conf": "bw", "name": "cal poly"},
    "crei": {"conf": "be", "name": "creighton"},
    "csb": {"conf": "wac", "name": "cal st bakersfield"},
    "csf": {"conf": "bw", "name": "cal st fullerton"},
    "csu": {"conf": "mwc", "name": "colorado st"},
    "csun": {"conf": "bw", "name": "cal st northridge"},
    "dart": {"conf": "ivy", "name": "dartmouth"},
    "dav": {"conf": "a10", "name": "davidson"},
    "day": {"conf": "a10", "name": "dayton"},
    "del": {"conf": "caa", "name": "delaware"},
    "den": {"conf": "sum", "name": "denver"},
    "dep": {"conf": "be", "name": "depaul"},
    "det": {"conf": "horz", "name": "detroit"},
    "drex": {"conf": "caa", "name": "drexel"},
    "drke": {"conf": "mvc", "name": "drake"},
    "dsu": {"conf": "meac", "name": "delaware st"},
    "duke": {"conf": "acc", "name": "duke"},
    "duq": {"conf": "a10", "name": "duquesne"},
    "ecu": {"conf": "amer", "name": "east carolina"},
    "eiu": {"conf": "ovc", "name": "eastern illinois"},
    "eky": {"conf": "ovc", "name": "eastern kentucky"},
    "elon": {"conf": "caa", "name": "elon"},
    "emu": {"conf": "mac", "name": "eastern michigan"},
    "etsu": {"conf": "sc", "name": "east tennessee st"},
    "evan": {"conf": "mvc", "name": "evansville"},
    "ewu": {"conf": "bsky", "name": "eastern washington"},
    "fair": {"conf": "maac", "name": "fairfield"},
    "famu": {"conf": "meac", "name": "florida a&m"},
    "fau": {"conf": "cusa", "name": "florida atlantic"},
    "fdu": {"conf": "nec", "name": "fairleigh dickinson"},
    "fgcu": {"conf": "asun", "name": "florida gulf coast"},
    "fiu": {"conf": "cusa", "name": "fiu"},
    "fla": {"conf": "sec", "name": "florida"},
    "for": {"conf": "a10", "name": "fordham"},
    "fres": {"conf": "mwc", "name": "fresno st"},
    "fsu": {"conf": "acc", "name": "florida st"},
    "fur": {"conf": "sc", "name": "furman"},
    "gaso": {"conf": "sb", "name": "georgia southern"},
    "gast": {"conf": "sb", "name": "georgia st"},
    "gb": {"conf": "horz", "name": "green bay"},
    "gcu": {"conf": "wac", "name": "grand canyon"},
    "gmu": {"conf": "a10", "name": "george mason"},
    "gonz": {"conf": "wcc", "name": "gonzaga"},
    "gram": {"conf": "swac", "name": "grambling st"},
    "gt": {"conf": "acc", "name": "georgia tech"},
    "gtwn": {"conf": "be", "name": "georgetown"},
    "gwu": {"conf": "a10", "name": "george washington"},
    "hall": {"conf": "be", "name": "seton hall"},
    "hamp": {"conf": "bsth", "name": "hampton"},
    "hart": {"conf": "ae", "name": "hartford"},
    "harv": {"conf": "ivy", "name": "harvard"},
    "haw": {"conf": "bw", "name": "hawaii"},
    "hbu": {"conf": "slnd", "name": "houston baptist"},
    "hc": {"conf": "pat", "name": "holy cross"},
    "hof": {"conf": "caa", "name": "hofstra"},
    "hou": {"conf": "amer", "name": "houston"},
    "how": {"conf": "meac", "name": "howard"},
    "hpu": {"conf": "bsth", "name": "high point"},
    "idho": {"conf": "bsky", "name": "idaho"},
    "idst": {"conf": "bsky", "name": "idaho st"},
    "ill": {"conf": "b10", "name": "illinois"},
    "ilst": {"conf": "mvc", "name": "illinois st"},
    "ind": {"conf": "b10", "name": "indiana"},
    "inst": {"conf": "mvc", "name": "indiana st"},
    "iona": {"conf": "maac", "name": "iona"},
    "iowa": {"conf": "b10", "name": "iowa"},
    "isu": {"conf": "b12", "name": "iowa st"},
    "iupui": {"conf": "horz", "name": "iupui"},
    "iw": {"conf": "slnd", "name": "incarnate word"},
    "jkst": {"conf": "swac", "name": "jackson st"},
    "jmu": {"conf": "caa", "name": "james madison"},
    "joes": {"conf": "a10", "name": "saint joseph's"},
    "ju": {"conf": "asun", "name": "jacksonville"},
    "jvst": {"conf": "ovc", "name": "jacksonville st"},
    "kenn": {"conf": "asun", "name": "kennesaw st"},
    "kent": {"conf": "mac", "name": "kent st"},
    "ksu": {"conf": "b12", "name": "kansas st"},
    "ku": {"conf": "b12", "name": "kansas"},
    "l-md": {"conf": "pat", "name": "loyola md"},
    "laf": {"conf": "pat", "name": "lafayette"},
    "lam": {"conf": "slnd", "name": "lamar"},
    "las": {"conf": "a10", "name": "la salle"},
    "lbsu": {"conf": "bw", "name": "long beach st"},
    "leh": {"conf": "pat", "name": "lehigh"},
    "lib": {"conf": "asun", "name": "liberty"},
    "lip": {"conf": "asun", "name": "lipscomb"},
    "liu": {"conf": "nec", "name": "liu"},
    "lmu": {"conf": "wcc", "name": "loyola marymount"},
    "long": {"conf": "bsth", "name": "longwood"},
    "lou": {"conf": "acc", "name": "louisville"},
    "lsu": {"conf": "sec", "name": "lsu"},
    "lt": {"conf": "cusa", "name": "louisiana tech"},
    "luc": {"conf": "mvc", "name": "loyola chicago"},
    "m-oh": {"conf": "mac", "name": "miami oh"},
    "man": {"conf": "maac", "name": "manhattan"},
    "marq": {"conf": "be", "name": "marquette"},
    "mass": {"conf": "a10", "name": "massachusetts"},
    "mcns": {"conf": "slnd", "name": "mcneese st"},
    "me": {"conf": "ae", "name": "maine"},
    "mem": {"conf": "amer", "name": "memphis"},
    "mer": {"conf": "sc", "name": "mercer"},
    "mia": {"conf": "acc", "name": "miami fl"},
    "mich": {"conf": "b10", "name": "michigan"},
    "milw": {"conf": "horz", "name": "milwaukee"},
    "minn": {"conf": "b10", "name": "minnesota"},
    "miss": {"conf": "sec", "name": "mississippi"},
    "miz": {"conf": "sec", "name": "missouri"},
    "monm": {"conf": "maac", "name": "monmouth"},
    "mont": {"conf": "bsky", "name": "montana"},
    "more": {"conf": "ovc", "name": "morehead st"},
    "morg": {"conf": "meac", "name": "morgan st"},
    "most": {"conf": "mvc", "name": "missouri st"},
    "mrmk": {"conf": "nec", "name": "merrimack"},
    "mrsh": {"conf": "cusa", "name": "marshall"},
    "mrst": {"conf": "maac", "name": "marist"},
    "msm": {"conf": "nec", "name": "mount st mary's"},
    "msst": {"conf": "sec", "name": "mississippi st"},
    "msu": {"conf": "b10", "name": "michigan st"},
    "mtst": {"conf": "bsky", "name": "montana st"},
    "mtsu": {"conf": "cusa", "name": "middle tennessee"},
    "muir": {"conf": "ovc", "name": "murray st"},
    "mvsu": {"conf": "swac", "name": "mississippi valley st"},
    "nau": {"conf": "bsky", "name": "northern arizona"},
    "navy": {"conf": "pat", "name": "navy"},
    "ncat": {"conf": "meac", "name": "north carolina a&t"},
    "nccu": {"conf": "meac", "name": "north carolina central"},
    "ncst": {"conf": "acc", "name": "nc state"},
    "nd": {"conf": "acc", "name": "notre dame"},
    "ndsu": {"conf": "sum", "name": "north dakota st"},
    "ne": {"conf": "caa", "name": "northeastern"},
    "neb": {"conf": "b10", "name": "nebraska"},
    "nev": {"conf": "mwc", "name": "nevada"},
    "niag": {"conf": "maac", "name": "niagara"},
    "nich": {"conf": "slnd", "name": "nicholls st"},
    "niu": {"conf": "mac", "name": "northern illinois"},
    "njit": {"conf": "asun", "name": "njit"},
    "nku": {"conf": "horz", "name": "northern kentucky"},
    "nmsu": {"conf": "wac", "name": "new mexico st"},
    "norf": {"conf": "meac", "name": "norfolk st"},
    "nova": {"conf": "be", "name": "villanova"},
    "nw": {"conf": "b10", "name": "northwestern"},
    "nwst": {"conf": "slnd", "name": "northwestern st"},
    "oak": {"conf": "horz", "name": "oakland"},
    "odu": {"conf": "cusa", "name": "old dominion"},
    "ohio": {"conf": "mac", "name": "ohio"},
    "okla": {"conf": "b12", "name": "oklahoma"},
    "okst": {"conf": "b12", "name": "oklahoma st"},
    "oma": {"conf": "sum", "name": "nebraska omaha"},
    "ore": {"conf": "p12", "name": "oregon"},
    "orst": {"conf": "p12", "name": "oregon st"},
    "oru": {"conf": "sum", "name": "oral roberts"},
    "osu": {"conf": "b10", "name": "ohio st"},
    "pac": {"conf": "wcc", "name": "pacific"},
    "peay": {"conf": "ovc", "name": "austin peay"},
    "penn": {"conf": "ivy", "name": "penn"},
    "pepp": {"conf": "wcc", "name": "pepperdine"},
    "pfu": {"conf": "sum", "name": "purdue fort wayne"},
    "pitt": {"conf": "acc", "name": "pittsburgh"},
    "port": {"conf": "wcc", "name": "portland"},
    "pre": {"conf": "bsth", "name": "presbyterian"},
    "prin": {"conf": "ivy", "name": "princeton"},
    "prov": {"conf": "be", "name": "providence"},
    "prst": {"conf": "bsky", "name": "portland st"},
    "psu": {"conf": "b10", "name": "penn st"},
    "pur": {"conf": "b10", "name": "purdue"},
    "pv": {"conf": "swac", "name": "prairie view a&m"},
    "quin": {"conf": "maac", "name": "quinnipiac"},
    "rad": {"conf": "bsth", "name": "radford"},
    "rice": {"conf": "cusa", "name": "rice"},
    "rich": {"conf": "a10", "name": "richmond"},
    "rid": {"conf": "maac", "name": "rider"},
    "rio": {"conf": "wac", "name": "ut rio grande valley"},
    "rmu": {"conf": "nec", "name": "robert morris"},
    "rutg": {"conf": "b10", "name": "rutgers"},
    "sac": {"conf": "bsky", "name": "sacramento st"},
    "sam": {"conf": "sc", "name": "samford"},
    "sb": {"conf": "ae", "name": "stony brook"},
    "sbu": {"conf": "a10", "name": "st bonaventure"},
    "sc": {"conf": "sec", "name": "south carolina"},
    "scst": {"conf": "meac", "name": "south carolina st"},
    "scu": {"conf": "wcc", "name": "santa clara"},
    "scus": {"conf": "bsth", "name": "usc upstate"},
    "sdak": {"conf": "sum", "name": "south dakota"},
    "sdst": {"conf": "sum", "name": "south dakota st"},
    "sdsu": {"conf": "mwc", "name": "san diego st"},
    "sea": {"conf": "wac", "name": "seattle"},
    "sela": {"conf": "slnd", "name": "southeastern louisiana"},
    "semo": {"conf": "ovc", "name": "southeast missouri st"},
    "sfa": {"conf": "slnd", "name": "stephen f austin"},
    "sfbk": {"conf": "nec", "name": "st francis ny"},
    "sfpa": {"conf": "nec", "name": "st francis pa"},
    "shsu": {"conf": "slnd", "name": "sam houston st"},
    "shu": {"conf": "nec", "name": "sacred heart"},
    "sie": {"conf": "maac", "name": "siena"},
    "siu": {"conf": "mvc", "name": "southern illinois"},
    "siue": {"conf": "ovc", "name": "siu edwardsville"},
    "sjsu": {"conf": "mwc", "name": "san jose st"},
    "sju": {"conf": "be", "name": "st john's"},
    "slu": {"conf": "a10", "name": "saint louis"},
    "smc": {"conf": "wcc", "name": "saint mary's"},
    "smu": {"conf": "amer", "name": "smu"},
    "sou": {"conf": "swac", "name": "southern"},
    "spu": {"conf": "maac", "name": "saint peter's"},
    "stan": {"conf": "p12", "name": "stanford"},
    "stet": {"conf": "asun", "name": "stetson"},
    "su": {"conf": "wcc", "name": "san francisco"},
    "suu": {"conf": "bsky", "name": "southern utah"},
    "syr": {"conf": "acc", "name": "syracuse"},
    "tamu": {"conf": "sec", "name": "texas a&m"},
    "tcu": {"conf": "b12", "name": "tcu"},
    "tem": {"conf": "amer", "name": "temple"},
    "tenn": {"conf": "sec", "name": "tennessee"},
    "tex": {"conf": "b12", "name": "texas"},
    "tlsa": {"conf": "amer", "name": "tulsa"},
    "tnst": {"conf": "ovc", "name": "tennessee st"},
    "tntc": {"conf": "ovc", "name": "tennessee tech"},
    "tol": {"conf": "mac", "name": "toledo"},
    "tows": {"conf": "caa", "name": "towson"},
    "troy": {"conf": "sb", "name": "troy"},
    "ttu": {"conf": "b12", "name": "texas tech"},
    "tuln": {"conf": "amer", "name": "tulane"},
    "txso": {"conf": "swac", "name": "texas southern"},
    "txst": {"conf": "sb", "name": "texas st"},
    "uab": {"conf": "cusa", "name": "uab"},
    "ualr": {"conf": "sb", "name": "little rock"},
    "uca": {"conf": "slnd", "name": "central arkansas"},
    "ucd": {"conf": "bw", "name": "uc davis"},
    "ucf": {"conf": "amer", "name": "ucf"},
    "uci": {"conf": "bw", "name": "uc irvine"},
    "ucla": {"conf": "p12", "name": "ucla"},
    "ucr": {"conf": "bw", "name": "uc riverside"},
    "ucsb": {"conf": "bw", "name": "uc santa barbara"},
    "uga": {"conf": "sec", "name": "georgia"},
    "uic": {"conf": "horz", "name": "illinois chicago"},
    "uk": {"conf": "sec", "name": "kentucky"},
    "ul": {"conf": "sb", "name": "louisiana"},
    "ulm": {"conf": "sb", "name": "louisiana monroe"},
    "umbc": {"conf": "ae", "name": "umbc"},
    "umd": {"conf": "b10", "name": "maryland"},
    "umes": {"conf": "meac", "name": "maryland eastern shore"},
    "umkc": {"conf": "wac", "name": "umkc"},
    "uml": {"conf": "ae", "name": "umass lowell"},
    "una": {"conf": "asun", "name": "north alabama"},
    "unc": {"conf": "acc", "name": "north carolina"},
    "unca": {"conf": "bsth", "name": "unc asheville"},
    "uncg": {"conf": "sc", "name": "unc greensboro"},
    "unco": {"conf": "bsky", "name": "northern colorado"},
    "uncw": {"conf": "caa", "name": "unc wilmington"},
    "und": {"conf": "sum", "name": "north dakota"},
    "unf": {"conf": "asun", "name": "north florida"},
    "unh": {"conf": "ae", "name": "new hampshire"},
    "uni": {"conf": "mvc", "name": "northern iowa"},
    "unlv": {"conf": "mwc", "name": "unlv"},
    "unm": {"conf": "mwc", "name": "new mexico"},
    "uno": {"conf": "slnd", "name": "new orleans"},
    "unt": {"conf": "cusa", "name": "north texas"},
    "uri": {"conf": "a10", "name": "rhode island"},
    "usa": {"conf": "sb", "name": "south alabama"},
    "usc": {"conf": "p12", "name": "usc"},
    "usd": {"conf": "wcc", "name": "san diego"},
    "usf": {"conf": "amer", "name": "south florida"},
    "usm": {"conf": "cusa", "name": "southern miss"},
    "usu": {"conf": "mwc", "name": "utah st"},
    "uta": {"conf": "sb", "name": "ut arlington"},
    "utah": {"conf": "p12", "name": "utah"},
    "utep": {"conf": "cusa", "name": "utep"},
    "utm": {"conf": "ovc", "name": "tennessee martin"},
    "utsa": {"conf": "cusa", "name": "utsa"},
    "uva": {"conf": "acc", "name": "virginia"},
    "uvm": {"conf": "ae", "name": "vermont"},
    "uvu": {"conf": "wac", "name": "utah valley"},
    "valp": {"conf": "mvc", "name": "valparaiso"},
    "van": {"conf": "sec", "name": "vanderbilt"},
    "vcu": {"conf": "a10", "name": "vcu"},
    "vmi": {"conf": "sc", "name": "vmi"},
    "vt": {"conf": "acc", "name": "virginia tech"},
    "w&m": {"conf": "caa", "name": "william & mary"},
    "wag": {"conf": "nec", "name": "wagner"},
    "wake": {"conf": "acc", "name": "wake forest"},
    "wash": {"conf": "p12", "name": "washington"},
    "wcu": {"conf": "sc", "name": "western carolina"},
    "web": {"conf": "bsky", "name": "weber st"},
    "webb": {"conf": "bsth", "name": "gardner webb"},
    "wich": {"conf": "amer", "name": "wichita st"},
    "win": {"conf": "bsth", "name": "winthrop"},
    "wis": {"conf": "b10", "name": "wisconsin"},
    "wiu": {"conf": "sum", "name": "western illinois"},
    "wku": {"conf": "cusa", "name": "western kentucky"},
    "wmu": {"conf": "mac", "name": "western michigan"},
    "wof": {"conf": "sc", "name": "wofford"},
    "wrst": {"conf": "horz", "name": "wright st"},
    "wsu": {"conf": "p12", "name": "washington st"},
    "wvu": {"conf": "b12", "name": "west virginia"},
    "wyo": {"conf": "mwc", "name": "wyoming"},
    "xav": {"conf": "be", "name": "xavier"},
    "yale": {"conf": "ivy", "name": "yale"},
    "ysu": {"conf": "horz", "name": "youngstown st"},
}

SCHOOL_DATA_BY_NAME = {
    s["name"]: {"conf": s["conf"], "abbrev": k}
    for k, s in SCHOOL_DATA_BY_ABBREV.items()
}

SCHOOL_ABBREVS = set(SCHOOL_DATA_BY_ABBREV.keys())
SCHOOL_NAMES = {s["name"] for s in SCHOOL_DATA_BY_ABBREV.values()}
CONF_NAMES = {s["conf"] for s in SCHOOL_DATA_BY_ABBREV.values()}
