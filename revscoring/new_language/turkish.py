import sys

import enchant

from .space_delimited import SpaceDelimited

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('turkish'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' corpora. " +
                      "See http://www.nltk.org/data.html")

badwords = [
    r"ağzına sıçayım", r"ahlaksız", r"ahmak", r"am", r"amcık", r"amın oğlu",
        r"amına koyayım", r"amına koyyim", r"amk", r"aptal",
    r"beyinsiz", r"bok", r"boktan",
    r"çük",
    r"dedeler",
    r"embesil",
    r"gerizekalı", r"gerzek", r"göt", r"göt oğlanı", r"götlek", r"götoğlanı",
        r"götveren",
    r"haysiyetsiz",
    r"ibne", r"inci", r"it", r"it oğlu it",
    r"kıç",
    r"mal", r"meme",
    r"nobrain",
    r"oğlan", r"oğlancı", r"orospu", r"orospu çocuğu", r"orospunun evladı",
    r"pezevengin evladı", r"pezevenk", r"piç", r"puşt",
    r"salak", r"şerefsiz", r"sik", r"siktir",
    r"yarrak",
    # TODO: merge these two lists and Regexify
    # TODO: WTF is this: "[ss][ııii][ççcc][aa][rryy][iiıı][mm]",
    "adamın dib", "adamın dip",
    "ahlaksız",
    "ahmak",
    "allahsız",
    "am", "amcık",
    "amk", "amq",
    "amın oğlu",
    "amına", "amına koy", "amına koyayım", "amına koyyim",
    "amını",
    "ananı",
    "ananın am", "ananın dölü",
    "ananızın", "ananızın am",
    "anasını",
    "anasının am",
    "antisemitic",
    "aptal",
    "asdf",
    "ağzına sıçayım",
    "beyinsiz",
    "bi bok", "bok", "boktan", "bokça",
    "dedeler",
    "dinci", "dinsiz",
    "dönek",
    "dıcks",
    "embesil",
    "eshek",
    "gerizekalı",
    "gerzek",
    "godoş",
    "gotten",
    "göt", "göt deliği", "göt oğlanı", "götlek", "götoğlanı", "götveren",
        "götü", "götün",
    "hacked", "hacked by",
    "haysiyetsiz",
    "heval", "hewal",
    "huur",
    "i.b.n.e", "ibne", "ibnedir", "ibneli k", "ibnelik",
    "inci",
    "israil köpektir",
    "it oğlu it",
    "kaltak",
    "kaşar",
    "kevaşe",
    "kıç",
    "liboş",
    "mal",
    "meme",
    "nesi kaşar",
    "nobrain",
    "o. çocuğ",
    "orospu", "orospu cocugu", "orospu çoc", "orospu çocuğu",
        "orospu çocuğudur", "orospudur", "orospunun", "orospunun evladı",
        "orospuçocuğu",
    "oğlan", "oğlancı",
    "pezeven","pezeveng", "pezevengin evladı", "pezevenk",
    "pisliktir",
    "piç",
    "puşt", "puşttur",
    "pıgs",
    "reyiz",
    "sahip",
    "serkan",
    "salak",
    "sik", "sikem", "siken", "siker", "sikerim", "sikey", "sikici", "sikik",
        "sikil", "sikiş", "sikişme", "sikm", "sikseydin", "sikseyidin",
        "sikt", "siktim", "siktir", "siktir lan",
    "sokarım", "sokayım",
    "swicht şamandra",
    "tipini s.k", "tipinizi s.keyim",
    "veled", "weled",
    "woltağym",
    "woğtim",
    "wulftim",
    "yarrak", "yarrağ",
    "yavş", "yavşak",
    "yavşaktır",
    "zippo dünyanın en boktan çakmağıdır",
    "zortlamasi",
    "zıkkımım",
    "zıonısm",
    "çük",
    "ıbnelık",
    "ın tröst we trust",
    "şerefsiz"
]

informals = [
    "achtırma",
    "achıyorlardı",
    "arkadashlar",
    "arkadashım",
    "basharamıyor",
    "basharan",
    "basharıla",
    "bashka",
    "bashlangıc",
    "bashlıyor",
    "bashıma",
    "bashının",
    "beshinci",
    "beshtane",
    "chalıshmıshlar", "chalıshıldıgında", "chalıshılınırsa", "chalıshıyorlar",
        "chalıshıyorsun", "chalıshıyorum",
    "chamashırlar",
    "charpmadan",
    "charptı", "charpınca",
    "chevirsin", "chevırdım",
    "chimdirecem",
    "choluk",
    "chorusdan", "choruslar",
    "chıka", "chıkacak", "chıkmadı", "chıksa", "chıktı", "chıkıp", "chıkısh",
    "chıplak",
    "degishen", "degishiklik", "degishiyor",
    "dönüshü",
    "eastblacksea",
    "eshekoglu",
    "eshkıyanın",
    "gardash", "gardashlık", "gardaslık",
    "gecherken",
    "gechirdi", "gechirmeyeyeyim", "gechiyor", "gechti", "gechtim",
    "genish",
    "gerchegi",
    "ichimde", "ichimden", "ichin", "ichine", "ichini",
    "ichlerinde",
    "ishler",
    "kalmısh",
    "kardeshlerini", "kardeshlerinizde",
    "karshı",
    "keshke",
    "kishiler", "kishilerin", "kishinin", "kishiye", "kishiyle",
    "konushmalrını", "konushmuyor", "konushuldugunda", "konushur",
    "koshan", "koshtu", "koshuyor",
    "nıshanlı",
    "saatchide",
    "sachlı",
    "sanatchılarını",
    "shansin", "shansın",
    "shashırtma", "shashırtmaya",
    "sheytanlar",
    "takabeg",
    "theır",
    "uchakdan",
    "uzanmıshsın",
    "yaklashdıkdan",
    "yakıshıklı",
    "yaratılmısh",
    "yashamak", "yashatıyorsun", "yashta", "yashıyorsun",
    "yerleshtiriyorum",
    "yozgatfm",
    "üch",
    "ıchın",
    "ıshıksız"
]


sys.modules[__name__] = SpaceDelimited(
    __name__,
    badwords=badwords,
    informals=informals,
    stopwords=stopwords
)
