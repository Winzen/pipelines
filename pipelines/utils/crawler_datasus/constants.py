# -*- coding: utf-8 -*-
"""
Constant values for the datasets projects
"""


from enum import Enum


class constants(Enum):  # pylint: disable=c0103
    """
    Constant values for the crawler_datasus project
    """

    # to build paths
    PATH = [
        "/tmp/br_ms_cnes/input/",
        "/tmp/br_ms_cnes/output/",
    ]

    # to download files from datasus FTP server
    DATASUS_DATABASE = {
        "br_ms_cnes": "CNES",
        "br_ms_sia": "SIA"
    }

    DATASUS_DATABASE_TABLE = {
        #CNES
        "estabelecimento": "ST",
        "profissional": "PF",
        "equipamento": "EQ",
        "leito": "LT",
        "equipe": "EP",
        "estabelecimento_ensino": "EE",
        "dados_complementares": "DC",
        "estabelecimento_filantropico": "EF",
        "gestao_metas": "GM",
        "habilitacao": "HB",
        "incentivos": "IN",
        "regra_contratual": "RC",
        "servico_especializado": "SR",
        #SIA
        "producao_ambulatorial": "PA",
    }


    COLUMNS_TO_KEEP = {
        # equipamento
        "EP": [
            "CODUFMUN",
            "CNES",
            "TIPEQUIP",
            "CODEQUIP",
            "QT_EXIST",
            "QT_USO",
            "IND_SUS",
            "IND_NSUS",
        ],
        # leito
        "LT": ["CNES", "TP_LEITO", "CODLEITO", "QT_EXIST", "QT_CONTR", "QT_SUS"],
        # equipe
        "EQ": [
            "CODUFMUN",
            "CNES",
            "ID_EQUIPE",
            "TIPO_EQP",
            "NOME_EQP",
            "ID_AREA",
            "NOMEAREA",
            "ID_SEGM",
            "DESCSEGM",
            "TIPOSEGM",
            "DT_ATIVA",
            "DT_DESAT",
            "MOTDESAT",
            "TP_DESAT",
            "QUILOMBO",
            "ASSENTAD",
            "POPGERAL",
            "ESCOLA",
            "INDIGENA",
            "PRONASCI",
        ],
        # profissional
        "PF": [
            "COMPETEN",
            "CNES",
            "UFMUNRES",
            "NOMEPROF",
            "CNS_PROF",
            "CBO",
            "REGISTRO",
            "CONSELHO",
            "TERCEIRO",
            "VINCULAC",
            "VINCUL_C",
            "VINCUL_A",
            "VINCUL_N",
            "PROF_SUS",
            "PROFNSUS",
            "HORAOUTR",
            "HORAHOSP",
            "HORA_AMB",
        ],
        # estabelecimento_ensino
        "EE": [
            "CODUFMUN",
            "CNES",
            "CMPT_INI",
            "CMPT_FIM",
            "SGRUPHAB",
            "DTPORTAR",
            "PORTARIA",
            "MAPORTAR",
        ],
        # estabelecimento_filantropico
        "EF": [
            "CODUFMUN",
            "CNES",
            "CMPT_INI",
            "CMPT_FIM",
            "SGRUPHAB",
            "DTPORTAR",
            "PORTARIA",
            "MAPORTAR",
        ],
        # gestao_metas
        "GM": [
            "CODUFMUN",
            "CNES",
            "CMPT_INI",
            "CMPT_FIM",
            "SGRUPHAB",
            "DTPORTAR",
            "PORTARIA",
            "MAPORTAR",
        ],
        # habilitacao
        "HB": [
            "CODUFMUN",
            "CNES",
            "NAT_JUR",
            "NULEITOS",
            "SGRUPHAB",
            "CMPT_INI",
            "CMPT_FIM",
            "DTPORTAR",
            "PORTARIA",
            "MAPORTAR",
        ],
        # incentivos
        "IN": [
            "CODUFMUN",
            "CNES",
            "CMPT_INI",
            "CMPT_FIM",
            "SGRUPHAB",
            "DTPORTAR",
            "PORTARIA",
            "MAPORTAR",
        ],
        # regra_contratual
        "RC": [
            "CODUFMUN",
            "CNES",
            "CMPT_INI",
            "CMPT_FIM",
            "SGRUPHAB",
            "DTPORTAR",
            "PORTARIA",
            "MAPORTAR",
        ],
        # servico_especializado
        "SR": [
            "CODUFMUN",
            "CNES",
            "SERV_ESP",
            "CLASS_SR",
            "SRVUNICO",
            "CARACTER",
            "AMB_NSUS",
            "AMB_SUS",
            "HOSP_NSUS",
            "HOSP_SUS",
            "CONTSRVU",
            "CNESTERC",
        ],
        # dados complementares
        "DC": [
            "CODUFMUN",
            "CNES",
            "S_HBSAGP",
            "S_HBSAGN",
            "S_DPI",
            "S_DPAC",
            "S_REAGP",
            "S_REAGN",
            "S_REHCV",
            "MAQ_PROP",
            "MAQ_OUTR",
            "F_AREIA",
            "F_CARVAO",
            "ABRANDAD",
            "DEIONIZA",
            "OSMOSE_R",
            "OUT_TRAT",
            "CNS_NEFR",
            "DIALISE",
            "SIMUL_RD",
            "PLANJ_RD",
            "ARMAZ_FT",
            "CONF_MAS",
            "SALA_MOL",
            "BLOCOPER",
            "S_ARMAZE",
            "S_PREPAR",
            "S_QCDURA",
            "S_QLDURA",
            "S_CPFLUX",
            "S_SIMULA",
            "S_ACELL6",
            "S_ALSEME",
            "S_ALCOME",
            "ORTV1050",
            "ORV50150",
            "OV150500",
            "UN_COBAL",
            "EQBRBAIX",
            "EQBRMEDI",
            "EQBRALTA",
            "EQ_MAREA",
            "EQ_MINDI",
            "EQSISPLN",
            "EQDOSCLI",
            "EQFONSEL",
            "CNS_ADM",
            "CNS_OPED",
            "CNS_CONC",
            "CNS_OCLIN",
            "CNS_MRAD",
            "CNS_FNUC",
            "QUIMRADI",
            "S_RECEPC",
            "S_TRIHMT",
            "S_TRICLI",
            "S_COLETA",
            "S_AFERES",
            "S_PREEST",
            "S_PROCES",
            "S_ESTOQU",
            "S_DISTRI",
            "S_SOROLO",
            "S_IMUNOH",
            "S_PRETRA",
            "S_HEMOST",
            "S_CONTRQ",
            "S_BIOMOL",
            "S_IMUNFE",
            "S_TRANSF",
            "S_SGDOAD",
            "QT_CADRE",
            "QT_CENRE",
            "QT_REFSA",
            "QT_CONRA",
            "QT_EXTPL",
            "QT_FRE18",
            "QT_FRE30",
            "QT_AGIPL",
            "QT_SELAD",
            "QT_IRRHE",
            "QT_AGLTN",
            "QT_MAQAF",
            "QT_REFRE",
            "QT_REFAS",
            "QT_CAPFL",
            "CNS_HMTR",
            "CNS_HMTL",
            "CNS_CRES",
            "CNS_RTEC",
            "HEMOTERA",
        ],
    }

    GENERATE_MONTH_TO_PARSE = {
        12: "11",
        1: "12",
        2: "01",
        3: "02",
        4: "03",
        5: "04",
        6: "05",
        7: "06",
        8: "07",
        9: "08",
        10: "09",
        11: "10",
    }
