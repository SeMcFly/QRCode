#error correction level define
ERROR_CORRECTION_L = 1
ERROR_CORRECTION_M = 0
ERROR_CORRECTION_Q = 2
ERROR_CORRECTION_H = 3

#data mode type define
NUM_MODE = 1 << 0
ALP_MODE = 1 << 1
BYTE_MODE = 1 << 2
KANJI_MODE = 1 << 3

SMALL_SIZE = {NUM_MODE:10,ALP_MODE:9,BYTE_MODE:8,KANJI_MODE:8}
MIDDLE_SIZE = {NUM_MODE:12,ALP_MODE:11,BYTE_MODE:16,KANJI_MODE:10}
LAGRT_SIZE = {NUM_MODE:14,ALP_MODE:12,BYTE_MODE:16,KANJI_MODE:12}
ALPH = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:']

def getModeNum(version,mode):
    if version < 10:
        len = SMALL_SIZE[mode]
    elif version < 27:
        len = MIDDLE_SIZE[mode]
    else:
        len =  LAGRT_SIZE[mode]
    return len

#align pettern position
ALIGNPATTERN = [
    [],
    [6,18],
    [6,22],
    [6,26],
    [6,30],
    [6,34],
    [6,22,38],
    [6,24,42],
    [6,26,46],
    [6,28,50],
    [6,30,54],
    [6,32,58],
    [6,34,62],
    [6,26,46,66],
    [6,26,48,70],
    [6,26,50,74],
    [6,30,54,78],
    [6,30,56,82],
    [6,30,58,86],
    [6,34,62,90],
    [6,28,50,72,94],
    [6,26,50,74,98],
    [6,30,54,78,102],
    [6,28,54,80,106],
    [6,32,58,84,110],
    [6,30,58,86,114],
    [6,34,62,90,118],
    [6,26,50,74,98,122],
    [6,30,54,78,102,126],
    [6,26,52,78,104,130],
    [6,30,56,82,108,134],
    [6,34,60,86,112,138],
    [6,30,58,86,114,142],
    [6,34,62,90,118,146],
    [6,30,54,78,102,126,150],
    [6,24,50,76,102,128,154],
    [6,28,54,80,106,132,158],
    [6,32,58,84,110,136,162],
    [6,26,54,82,110,138,166],
    [6,30,58,86,114,142,170]
]

def getPosAlin(version):
    return ALIGNPATTERN[version-1]

MaskFunc = [lambda r,c:(r + c) % 2 == 0,#000
            lambda r,c: r % 2 == 0,#001
            lambda r,c: c % 3 == 0,#010
            lambda r,c:(r + c) % 3 == 0,#011
            lambda r,c:(( r / 2) + (c / 3)) % 2 == 0,#100
            lambda r,c:(r * c) % 2 + (r * c) % 3 == 0,#101
            lambda r,c:(((r * c) % 2 + (r * c) % 3) % 2) == 0,#110
            lambda r,c:(((r * c) % 2 + (r + c) % 3) % 3) == 0 #111 error no identi
 ]
def getMaskPattenFunc(maskPatten):
        return MaskFunc[maskPatten]

FormtInfo = [[0x5412,0x5125,0x5e7c,0x5b4b,0x45f9,0x40ce,0x4f97,0x4aa0],
             [0x77c4,0x72f3,0x7daa,0x789d,0x662f,0x6318,0x6c41,0x6979],
             [0x1689,0x13be,0x1ce7,0x19d0,0x0762,0x0255,0x0d0c,0x083b],
             [0x355f,0x3068,0x3f31,0x3a06,0x24b4,0x2183,0x2eda,0x2bed]]

def getFormtInfo(ecl,mask):
    return FormtInfo[ecl][mask]

VersionInfo = [0x07c94,
               0x085bc,
               0x09a99,
               0x0a4d3,
               0x0bbf6,
               0x0c762,
               0x0d847,
               0x0e60d,
               0x0f928,
               0x10b78,
               0x1145d,
               0x12a17,
               0x13532,
               0x149a6,
               0x15683,
               0x168c9,
               0x177ec,
               0x18ec4,
               0x191e1,
               0x1afab,
               0x1b08e,
               0x1cc1a,
               0x1d33f,
               0x1ed75,
               0x1f250,
               0x209d5,
               0x216f0,
               0x228ba,
               0x2379f,
               0x24b0b,
               0x2542e,
               0x26a64,
               0x27541,
               0x28c69]

def getVersionInfo(version):
    return VersionInfo[version - 7]