import xml.etree.cElementTree as ET


class Territory:
    """
    Represents all static information about a territory
    """

    # neighbors list has the target and conditions
    # conditions could be 'edge' class which asks if its passable

    def __init__(self, territory_name, ipc_value, is_seazone, is_capital=""):
        self.name = territory_name
        self.neighbors = []
        self.ipc = ipc_value
        self.is_water = is_seazone
        self.is_capital = is_capital
        self.original_owner = ''


class Unit:
    """
    Provides a basic template for a unit
    """
    # arbitrarily high default weight so most units cannot be transported

    def __init__(self, unit_name, unit_type, cost, attack, defense, movement, transport_weight=100, carrier_weight=100,
                 transport_capacity=0, carrier_capacity=0):
        self.name = unit_name

        self.unit_type = unit_type
        self.cost = cost

        self.attack = attack
        self.defense = defense
        self.movement = movement

        self.transport_weight = transport_weight
        self.transport_capacity = transport_capacity
        self.carrier_weight = carrier_weight
        self.carrier_capacity = carrier_capacity

    def power(self, attack_or_defense):
        return self.attack if attack_or_defense == 'attack' else self.defense  # determines which power to use


class Rules:
    """
    Contains static game data: a board representing territories, assignment of neighbors
    for each territory (which is contained within a dictionary from string to
    territory), and prototypes for units.
    """

    # defines all the prototypes for units. definitions
    # also says all territories and how they are connected.
    # if has __ tech, attack ++
    # rules.get_unit_type (tank)

    def __init__(self):
        self.board = {"1 Sea Zone": Territory("1 Sea Zone", 0, True),
                      "2 Sea Zone": Territory("2 Sea Zone", 0, True),
                      "3 Sea Zone": Territory("2 Sea Zone", 0, True),
                      "4 Sea Zone": Territory("4 Sea Zone", 0, True),
                      "5 Sea Zone": Territory("5 Sea Zone", 0, True),
                      "6 Sea Zone": Territory("6 Sea Zone", 0, True),
                      "7 Sea Zone": Territory("7 Sea Zone", 0, True),
                      "8 Sea Zone": Territory("8 Sea Zone", 0, True),
                      "9 Sea Zone": Territory("9 Sea Zone", 0, True),
                      "10 Sea Zone": Territory("10 Sea Zone", 0, True),
                      "11 Sea Zone": Territory("11 Sea Zone", 0, True),
                      "12 Sea Zone": Territory("12 Sea Zone", 0, True),
                      "13 Sea Zone": Territory("13 Sea Zone", 0, True),
                      "14 Sea Zone": Territory("14 Sea Zone", 0, True),
                      "15 Sea Zone": Territory("15 Sea Zone", 0, True),
                      "16 Sea Zone": Territory("16 Sea Zone", 0, True),
                      "17 Sea Zone": Territory("17 Sea Zone", 0, True),
                      "18 Sea Zone": Territory("18 Sea Zone", 0, True),
                      "19 Sea Zone": Territory("19 Sea Zone", 0, True),
                      "20 Sea Zone": Territory("20 Sea Zone", 0, True),
                      "21 Sea Zone": Territory("21 Sea Zone", 0, True),
                      "22 Sea Zone": Territory("22 Sea Zone", 0, True),
                      "23 Sea Zone": Territory("23 Sea Zone", 0, True),
                      "24 Sea Zone": Territory("24 Sea Zone", 0, True),
                      "25 Sea Zone": Territory("25 Sea Zone", 0, True),
                      "26 Sea Zone": Territory("26 Sea Zone", 0, True),
                      "27 Sea Zone": Territory("27 Sea Zone", 0, True),
                      "28 Sea Zone": Territory("28 Sea Zone", 0, True),
                      "29 Sea Zone": Territory("29 Sea Zone", 0, True),
                      "30 Sea Zone": Territory("30 Sea Zone", 0, True),
                      "31 Sea Zone": Territory("31 Sea Zone", 0, True),
                      "32 Sea Zone": Territory("32 Sea Zone", 0, True),
                      "33 Sea Zone": Territory("33 Sea Zone", 0, True),
                      "34 Sea Zone": Territory("34 Sea Zone", 0, True),
                      "35 Sea Zone": Territory("35 Sea Zone", 0, True),
                      "36 Sea Zone": Territory("36 Sea Zone", 0, True),
                      "37 Sea Zone": Territory("37 Sea Zone", 0, True),
                      "38 Sea Zone": Territory("38 Sea Zone", 0, True),
                      "39 Sea Zone": Territory("39 Sea Zone", 0, True),
                      "40 Sea Zone": Territory("40 Sea Zone", 0, True),
                      "41 Sea Zone": Territory("41 Sea Zone", 0, True),
                      "42 Sea Zone": Territory("42 Sea Zone", 0, True),
                      "43 Sea Zone": Territory("43 Sea Zone", 0, True),
                      "44 Sea Zone": Territory("44 Sea Zone", 0, True),
                      "45 Sea Zone": Territory("45 Sea Zone", 0, True),
                      "46 Sea Zone": Territory("46 Sea Zone", 0, True),
                      "47 Sea Zone": Territory("47 Sea Zone", 0, True),
                      "48 Sea Zone": Territory("48 Sea Zone", 0, True),
                      "49 Sea Zone": Territory("49 Sea Zone", 0, True),
                      "50 Sea Zone": Territory("50 Sea Zone", 0, True),
                      "51 Sea Zone": Territory("51 Sea Zone", 0, True),
                      "52 Sea Zone": Territory("52 Sea Zone", 0, True),
                      "53 Sea Zone": Territory("53 Sea Zone", 0, True),
                      "54 Sea Zone": Territory("54 Sea Zone", 0, True),
                      "55 Sea Zone": Territory("55 Sea Zone", 0, True),
                      "56 Sea Zone": Territory("56 Sea Zone", 0, True),
                      "57 Sea Zone": Territory("57 Sea Zone", 0, True),
                      "58 Sea Zone": Territory("58 Sea Zone", 0, True),
                      "59 Sea Zone": Territory("59 Sea Zone", 0, True),
                      "60 Sea Zone": Territory("60 Sea Zone", 0, True),
                      "61 Sea Zone": Territory("61 Sea Zone", 0, True),
                      "62 Sea Zone": Territory("62 Sea Zone", 0, True),
                      "63 Sea Zone": Territory("63 Sea Zone", 0, True),
                      "64 Sea Zone": Territory("64 Sea Zone", 0, True),
                      "65 Sea Zone": Territory("65 Sea Zone", 0, True),
                      "Afghanistan": Territory("Afghanistan", 1, False),
                      "Alaska": Territory("Alaska", 2, False),
                      "Algeria": Territory("Algeria", 1, False),
                      "Anglo-Egyptian Sudan": Territory("Anglo-Egyptian Sudan", 0, False),
                      "Angola": Territory("Angola", 0, False),  # NEUTRAL
                      "Anhwei": Territory("Anhwei", 1, False),
                      "Archangel": Territory("Archangel", 1, False),
                      "Baltic States": Territory("Baltic States", 2, False),
                      "Belgian Congo": Territory("Belgian Congo", 1, False),
                      "Belorussia": Territory("Belorussia", 2, False),
                      "Borneo": Territory("Borneo", 4, False),
                      "Brazil": Territory("Brazil", 3, False),
                      "Bulgaria Romania": Territory("Bulgaria Romania", 2, False),
                      "Burma": Territory("Burma", 1, False),
                      "Buryatia S.S.R.": Territory("Buryatia S.S.R.", 1, False),
                      "Caroline Islands": Territory("Caroline Islands", 0, False),
                      "Caucasus": Territory("Caucasus", 4, False),
                      "Central America": Territory("Central America", 1, False),
                      "Central United States": Territory("Central United States", 6, False),
                      "Chile": Territory("Chile", 0, False),  # NEUTRAL
                      "Colombia Equador": Territory("Colombia Equador", 0, False),  # NEUTRAL
                      "East Indies": Territory("East Indies", 4, False),
                      "East Mexico": Territory("East Mexico", 0, False),
                      "Eastern Australia": Territory("Eastern Australia", 1, False),
                      "Eastern Canada": Territory("Eastern Canada", 3, False),
                      "Eastern United States": Territory("Eastern United States", 12, False, "America"),
                      "Egypt": Territory("Egypt", 2, False),
                      "Eire": Territory("Eire", 0, False),  # NEUTRAL
                      "Evenki National Okrug": Territory("Evenki National Okrug", 1, False),
                      "Finland": Territory("Finland", 1, False),
                      "Formosa": Territory("Formosa", 0, False),
                      "France": Territory("France", 6, False),
                      "French Equatorial Africa": Territory("French Equatorial Africa", 1, False),
                      "French Indo-China Thailand": Territory("French Indo-China Thailand", 2, False),
                      "French Madagascar": Territory("French Madagascar", 1, False),
                      "French West Africa": Territory("French West Africa", 1, False),
                      "Germany": Territory("Germany", 10, False, "Germany"),
                      "Gibraltar": Territory("Gibraltar", 0, False),
                      "Greenland": Territory("Greenland", 0, False),
                      "Hawaiian Islands": Territory("Hawaiian Islands", 1, False),
                      "Himalaya": Territory("Himalaya", 0, False),  # NEUTRAL
                      "Iceland": Territory("Iceland", 0, False),
                      "India": Territory("India", 3, False),
                      "Italian East Africa": Territory("Italian East Africa", 1, False),
                      "Italy": Territory("Italy", 3, False),
                      "Iwo Jima": Territory("Iwo Jima", 0, False),
                      "Japan": Territory("Japan", 8, False, "Japan"),
                      "Karelia S.S.R.": Territory("Karelia S.S.R.", 2, False),
                      "Kazakh S.S.R.": Territory("Kazakh S.S.R.", 2, False),
                      "Kiangsu": Territory("Kiangsu", 2, False),
                      "Kwangtung": Territory("Kwangtung", 2, False),
                      "Libya": Territory("Libya", 1, False),
                      "Malaya": Territory("Malaya", 1, False),
                      "Manchuria": Territory("Manchuria", 3, False),
                      "Mexico": Territory("Mexico", 2, False),
                      "Midway": Territory("Midway", 0, False),
                      "Mongolia": Territory("Mongolia", 0, False),  # NEUTRAL
                      "Morocco": Territory("Morocco", 1, False),
                      "Mozambique": Territory("Mozambique", 0, False),  # NEUTRAL
                      "New Guinea": Territory("New Guinea", 1, False),
                      "New Zealand": Territory("New Zealand", 1, False),
                      "Northwestern Europe": Territory("Northwestern Europe", 2, False),
                      "Norway": Territory("Norway", 2, False),
                      "Novosibirsk": Territory("Novosibirsk", 1, False),
                      "Okinawa": Territory("Okinawa", 0, False),
                      "Persia": Territory("Persia", 1, False),
                      "Peru Argentina": Territory("Peru Argentina", 0, False),  # NEUTRAL
                      "Philippine Islands": Territory("Philippine Islands", 3, False),
                      "Poland": Territory("Poland", 2, False),
                      "Rhodesia": Territory("Rhodesia", 1, False),
                      "Russia": Territory("Russia", 8, False, "Russia"),
                      "Sahara": Territory("Sahara", 0, False),  # NEUTRAL
                      "Saudi Arabia": Territory("Saudi Arabia", 0, False),  # NEUTRAL
                      "Sinkiang": Territory("Sinkiang", 1, False),
                      "Solomon Islands": Territory("Solomon Islands", 0, False),
                      "Southern Europe": Territory("Southern Europe", 2, False),
                      "Soviet Far East": Territory("Soviet Far East", 1, False),
                      "Spain Portugal": Territory("Spain Portugal", 0, False),  # NEUTRAL
                      "Sweden": Territory("Sweden", 0, False),  # NEUTRAL
                      "Switzerland": Territory("Switzerland", 0, False),  # NEUTRAL
                      "Szechwan": Territory("Szechwan", 1, False),
                      "Trans-Jordan": Territory("Trans-Jordan", 1, False),
                      "Turkey": Territory("Turkey", 0, False),  # NEUTRAL
                      "Ukraine S.S.R.": Territory("Ukraine S.S.R.", 2, False),
                      "Union of South Africa": Territory("Union of South Africa", 2, False),
                      "United Kingdom": Territory("United Kingdom", 8, False, "Britain"),
                      "Venezuela": Territory("Venezuela", 0, False),  # NEUTRAL
                      "Vologda": Territory("Vologda", 2, False),
                      "Wake Island": Territory("Wake Island", 0, False),
                      "West Indies": Territory("West Indies", 1, False),
                      "West Russia": Territory("West Russia", 2, False),
                      "Western Australia": Territory("Western Australia", 1, False),
                      "Western Canada": Territory("Western Canada", 1, False),
                      "Western United States": Territory("Western United States", 10, False),
                      "Yakut S.S.R.": Territory("Yakut S.S.R.", 1, False),
                      "Yunnan": Territory("Yunnan", 1, False)}

        # Connections List to be used to make neighbors

        self.connections = [("1 Sea Zone", "2 Sea Zone"),
                            ("1 Sea Zone", "10 Sea Zone"),
                            ("1 Sea Zone", "Eastern Canada"),
                            ("2 Sea Zone", "3 Sea Zone"),
                            ("2 Sea Zone", "9 Sea Zone"),
                            ("2 Sea Zone", "7 Sea Zone"),
                            ("2 Sea Zone", "10 Sea Zone"),
                            ("2 Sea Zone", "Greenland"),
                            ("3 Sea Zone", "6 Sea Zone"),
                            ("3 Sea Zone", "Norway"),
                            ("3 Sea Zone", "Finland"),
                            ("3 Sea Zone", "7 Sea Zone"),
                            ("3 Sea Zone", "4 Sea Zone"),
                            ("3 Sea Zone", "Iceland"),
                            ("4 Sea Zone", "Archangel"),
                            ("4 Sea Zone", "Karelia S.S.R."),
                            ("5 Sea Zone", "6 Sea Zone"),
                            ("5 Sea Zone", "Northwestern Europe"),
                            ("5 Sea Zone", "Sweden"),
                            ("5 Sea Zone", "Norway"),
                            ("5 Sea Zone", "Finland"),
                            ("5 Sea Zone", "Karelia S.S.R."),
                            ("5 Sea Zone", "Baltic States"),
                            ("5 Sea Zone", "Germany"),
                            ("6 Sea Zone", "Northwestern Europe"),
                            ("6 Sea Zone", "Norway"),
                            ("6 Sea Zone", "7 Sea Zone"),
                            ("6 Sea Zone", "United Kingdom"),
                            ("6 Sea Zone", "8 Sea Zone"),
                            ("7 Sea Zone", "9 Sea Zone"),
                            ("7 Sea Zone", "Eire"),
                            ("7 Sea Zone", "United Kingdom"),
                            ("7 Sea Zone", "8 Sea Zone"),
                            ("8 Sea Zone", "Northwestern Europe"),
                            ("8 Sea Zone", "9 Sea Zone"),
                            ("8 Sea Zone", "Eire"),
                            ("8 Sea Zone", "United Kingdom"),
                            ("8 Sea Zone", "13 Sea Zone"),
                            ("8 Sea Zone", "France"),
                            ("9 Sea Zone", "12 Sea Zone"),
                            ("9 Sea Zone", "13 Sea Zone"),
                            ("9 Sea Zone", "10 Sea Zone"),
                            ("10 Sea Zone", "11 Sea Zone"),
                            ("10 Sea Zone", "12 Sea Zone"),
                            ("10 Sea Zone", "Eastern Canada"),
                            ("11 Sea Zone", "Central United States"),
                            ("11 Sea Zone", "Eastern United States"),
                            ("11 Sea Zone", "18 Sea Zone"),
                            ("11 Sea Zone", "12 Sea Zone"),
                            ("11 Sea Zone", "East Mexico"),
                            ("12 Sea Zone", "22 Sea Zone"),
                            ("12 Sea Zone", "23 Sea Zone"),
                            ("12 Sea Zone", "18 Sea Zone"),
                            ("12 Sea Zone", "13 Sea Zone"),
                            ("13 Sea Zone", "14 Sea Zone"),
                            ("13 Sea Zone", "Gibraltar"),
                            ("13 Sea Zone", "Morocco"),
                            ("13 Sea Zone", "23 Sea Zone"),
                            ("13 Sea Zone", "Spain Portugal"),
                            ("14 Sea Zone", "Gibraltar"),
                            ("14 Sea Zone", "Morocco"),
                            ("14 Sea Zone", "15 Sea Zone"),
                            ("14 Sea Zone", "Algeria"),
                            ("14 Sea Zone", "France"),
                            ("14 Sea Zone", "Spain Portugal"),
                            ("15 Sea Zone", "17 Sea Zone"),
                            ("15 Sea Zone", "Turkey"),
                            ("15 Sea Zone", "16 Sea Zone"),
                            ("15 Sea Zone", "Italy"),
                            ("15 Sea Zone", "Southern Europe"),
                            ("15 Sea Zone", "Libya"),
                            ("16 Sea Zone", "Bulgaria Romania"),
                            ("16 Sea Zone", "Turkey"),
                            ("16 Sea Zone", "Ukraine S.S.R."),
                            ("16 Sea Zone", "Caucasus"),
                            ("17 Sea Zone", "Turkey"),
                            ("17 Sea Zone", "Egypt"),
                            ("17 Sea Zone", "Trans-Jordan"),
                            ("17 Sea Zone", "34 Sea Zone"),
                            ("18 Sea Zone", "Central America"),
                            ("18 Sea Zone", "Venezuela"),
                            ("18 Sea Zone", "22 Sea Zone"),
                            ("18 Sea Zone", "West Indies"),
                            ("18 Sea Zone", "Colombia Equador"),
                            ("18 Sea Zone", "East Mexico"),
                            ("18 Sea Zone", "19 Sea Zone"),
                            ("19 Sea Zone", "Central America"),
                            ("19 Sea Zone", "20 Sea Zone"),
                            ("19 Sea Zone", "55 Sea Zone"),
                            ("19 Sea Zone", "Colombia Equador"),
                            ("19 Sea Zone", "East Mexico"),
                            ("19 Sea Zone", "Peru Argentina"),
                            ("20 Sea Zone", "42 Sea Zone"),
                            ("20 Sea Zone", "Chile"),
                            ("20 Sea Zone", "21 Sea Zone"),
                            ("21 Sea Zone", "22 Sea Zone"),
                            ("21 Sea Zone", "26 Sea Zone"),
                            ("21 Sea Zone", "Peru Argentina"),
                            ("21 Sea Zone", "41 Sea Zone"),
                            ("21 Sea Zone", "Chile"),
                            ("21 Sea Zone", "25 Sea Zone"),
                            ("22 Sea Zone", "23 Sea Zone"),
                            ("22 Sea Zone", "Brazil"),
                            ("22 Sea Zone", "25 Sea Zone"),
                            ("23 Sea Zone", "24 Sea Zone"),
                            ("23 Sea Zone", "French West Africa"),
                            ("23 Sea Zone", "25 Sea Zone"),
                            ("23 Sea Zone", "Sahara"),
                            ("24 Sea Zone", "27 Sea Zone"),
                            ("24 Sea Zone", "Belgian Congo"),
                            ("24 Sea Zone", "French Equatorial Africa"),
                            ("24 Sea Zone", "25 Sea Zone"),
                            ("25 Sea Zone", "27 Sea Zone"),
                            ("25 Sea Zone", "26 Sea Zone"),
                            ("26 Sea Zone", "27 Sea Zone"),
                            ("27 Sea Zone", "28 Sea Zone"),
                            ("27 Sea Zone", "Angola"),
                            ("27 Sea Zone", "Union of South Africa"),
                            ("28 Sea Zone", "Mozambique"),
                            ("28 Sea Zone", "Union of South Africa"),
                            ("28 Sea Zone", "33 Sea Zone"),
                            ("28 Sea Zone", "29 Sea Zone"),
                            ("28 Sea Zone", "French Madagascar"),
                            ("29 Sea Zone", "31 Sea Zone"),
                            ("29 Sea Zone", "French Madagascar"),
                            ("29 Sea Zone", "30 Sea Zone"),
                            ("29 Sea Zone", "32 Sea Zone"),
                            ("30 Sea Zone", "38 Sea Zone"),
                            ("30 Sea Zone", "37 Sea Zone"),
                            ("30 Sea Zone", "31 Sea Zone"),
                            ("31 Sea Zone", "37 Sea Zone"),
                            ("31 Sea Zone", "35 Sea Zone"),
                            ("31 Sea Zone", "32 Sea Zone"),
                            ("32 Sea Zone", "33 Sea Zone"),
                            ("32 Sea Zone", "35 Sea Zone"),
                            ("32 Sea Zone", "French Madagascar"),
                            ("32 Sea Zone", "34 Sea Zone"),
                            ("33 Sea Zone", "Rhodesia"),
                            ("33 Sea Zone", "Mozambique"),
                            ("33 Sea Zone", "French Madagascar"),
                            ("33 Sea Zone", "34 Sea Zone"),
                            ("33 Sea Zone", "Italian East Africa"),
                            ("34 Sea Zone", "Saudi Arabia"),
                            ("34 Sea Zone", "Anglo-Egyptian Sudan"),
                            ("34 Sea Zone", "Persia"),
                            ("34 Sea Zone", "35 Sea Zone"),
                            ("34 Sea Zone", "Egypt"),
                            ("34 Sea Zone", "Trans-Jordan"),
                            ("34 Sea Zone", "Italian East Africa"),
                            ("35 Sea Zone", "37 Sea Zone"),
                            ("35 Sea Zone", "36 Sea Zone"),
                            ("35 Sea Zone", "India"),
                            ("36 Sea Zone", "French Indo-China Thailand"),
                            ("36 Sea Zone", "48 Sea Zone"),
                            ("36 Sea Zone", "37 Sea Zone"),
                            ("36 Sea Zone", "61 Sea Zone"),
                            ("36 Sea Zone", "Burma"),
                            ("36 Sea Zone", "47 Sea Zone"),
                            ("36 Sea Zone", "Malaya"),
                            ("37 Sea Zone", "38 Sea Zone"),
                            ("37 Sea Zone", "46 Sea Zone"),
                            ("37 Sea Zone", "47 Sea Zone"),
                            ("37 Sea Zone", "East Indies"),
                            ("38 Sea Zone", "46 Sea Zone"),
                            ("38 Sea Zone", "Western Australia"),
                            ("38 Sea Zone", "39 Sea Zone"),
                            ("39 Sea Zone", "40 Sea Zone"),
                            ("39 Sea Zone", "45 Sea Zone"),
                            ("39 Sea Zone", "Eastern Australia"),
                            ("40 Sea Zone", "43 Sea Zone"),
                            ("40 Sea Zone", "New Zealand"),
                            ("40 Sea Zone", "44 Sea Zone"),
                            ("40 Sea Zone", "41 Sea Zone"),
                            ("40 Sea Zone", "45 Sea Zone"),
                            ("41 Sea Zone", "43 Sea Zone"),
                            ("41 Sea Zone", "42 Sea Zone"),
                            ("42 Sea Zone", "43 Sea Zone"),
                            ("42 Sea Zone", "54 Sea Zone"),
                            ("42 Sea Zone", "55 Sea Zone"),
                            ("43 Sea Zone", "54 Sea Zone"),
                            ("43 Sea Zone", "44 Sea Zone"),
                            ("43 Sea Zone", "53 Sea Zone"),
                            ("44 Sea Zone", "50 Sea Zone"),
                            ("44 Sea Zone", "52 Sea Zone"),
                            ("44 Sea Zone", "45 Sea Zone"),
                            ("44 Sea Zone", "53 Sea Zone"),
                            ("44 Sea Zone", "49 Sea Zone"),
                            ("44 Sea Zone", "Solomon Islands"),
                            ("45 Sea Zone", "46 Sea Zone"),
                            ("45 Sea Zone", "49 Sea Zone"),
                            ("45 Sea Zone", "Eastern Australia"),
                            ("46 Sea Zone", "Western Australia"),
                            ("46 Sea Zone", "47 Sea Zone"),
                            ("46 Sea Zone", "49 Sea Zone"),
                            ("47 Sea Zone", "Borneo"),
                            ("47 Sea Zone", "48 Sea Zone"),
                            ("47 Sea Zone", "49 Sea Zone"),
                            ("48 Sea Zone", "51 Sea Zone"),
                            ("48 Sea Zone", "50 Sea Zone"),
                            ("48 Sea Zone", "Philippine Islands"),
                            ("48 Sea Zone", "61 Sea Zone"),
                            ("48 Sea Zone", "60 Sea Zone"),
                            ("48 Sea Zone", "49 Sea Zone"),
                            ("49 Sea Zone", "New Guinea"),
                            ("49 Sea Zone", "50 Sea Zone"),
                            ("50 Sea Zone", "51 Sea Zone"),
                            ("50 Sea Zone", "Caroline Islands"),
                            ("50 Sea Zone", "52 Sea Zone"),
                            ("51 Sea Zone", "59 Sea Zone"),
                            ("51 Sea Zone", "Okinawa"),
                            ("51 Sea Zone", "60 Sea Zone"),
                            ("51 Sea Zone", "52 Sea Zone"),
                            ("52 Sea Zone", "59 Sea Zone"),
                            ("52 Sea Zone", "57 Sea Zone"),
                            ("52 Sea Zone", "53 Sea Zone"),
                            ("52 Sea Zone", "Wake Island"),
                            ("53 Sea Zone", "54 Sea Zone"),
                            ("53 Sea Zone", "56 Sea Zone"),
                            ("53 Sea Zone", "57 Sea Zone"),
                            ("53 Sea Zone", "Hawaiian Islands"),
                            ("54 Sea Zone", "56 Sea Zone"),
                            ("54 Sea Zone", "55 Sea Zone"),
                            ("55 Sea Zone", "56 Sea Zone"),
                            ("55 Sea Zone", "Mexico"),
                            ("56 Sea Zone", "57 Sea Zone"),
                            ("56 Sea Zone", "65 Sea Zone"),
                            ("56 Sea Zone", "Western United States"),
                            ("57 Sea Zone", "59 Sea Zone"),
                            ("57 Sea Zone", "65 Sea Zone"),
                            ("57 Sea Zone", "58 Sea Zone"),
                            ("57 Sea Zone", "Midway"),
                            ("57 Sea Zone", "64 Sea Zone"),
                            ("58 Sea Zone", "59 Sea Zone"),
                            ("58 Sea Zone", "63 Sea Zone"),
                            ("58 Sea Zone", "60 Sea Zone"),
                            ("58 Sea Zone", "64 Sea Zone"),
                            ("59 Sea Zone", "60 Sea Zone"),
                            ("59 Sea Zone", "Iwo Jima"),
                            ("60 Sea Zone", "61 Sea Zone"),
                            ("60 Sea Zone", "Japan"),
                            ("60 Sea Zone", "63 Sea Zone"),
                            ("60 Sea Zone", "62 Sea Zone"),
                            ("61 Sea Zone", "Kwangtung"),
                            ("61 Sea Zone", "Kiangsu"),
                            ("61 Sea Zone", "Yunnan"),
                            ("61 Sea Zone", "Formosa"),
                            ("61 Sea Zone", "62 Sea Zone"),
                            ("62 Sea Zone", "Manchuria"),
                            ("62 Sea Zone", "Buryatia S.S.R."),
                            ("62 Sea Zone", "Japan"),
                            ("62 Sea Zone", "63 Sea Zone"),
                            ("63 Sea Zone", "Soviet Far East"),
                            ("63 Sea Zone", "Buryatia S.S.R."),
                            ("63 Sea Zone", "64 Sea Zone"),
                            ("64 Sea Zone", "65 Sea Zone"),
                            ("64 Sea Zone", "Alaska"),
                            ("65 Sea Zone", "Western Canada"),
                            ("65 Sea Zone", "Alaska"),
                            ("Afghanistan", "Persia"),
                            ("Afghanistan", "Szechwan"),
                            ("Afghanistan", "Kazakh S.S.R."),
                            ("Afghanistan", "Himalaya"),
                            ("Afghanistan", "India"),
                            ("Alaska", "Western Canada"),
                            ("Algeria", "Morocco"),
                            ("Algeria", "Libya"),
                            ("Algeria", "Sahara"),
                            ("Anglo-Egyptian Sudan", "Rhodesia"),
                            ("Anglo-Egyptian Sudan", "Belgian Congo"),
                            ("Anglo-Egyptian Sudan", "Egypt"),
                            ("Anglo-Egyptian Sudan", "French Equatorial Africa"),
                            ("Anglo-Egyptian Sudan", "Italian East Africa"),
                            ("Anglo-Egyptian Sudan", "Sahara"),
                            ("Angola", "Union of South Africa"),
                            ("Angola", "Belgian Congo"),
                            ("Anhwei", "Manchuria"),
                            ("Anhwei", "Mongolia"),
                            ("Anhwei", "Kwangtung"),
                            ("Anhwei", "Kiangsu"),
                            ("Anhwei", "Szechwan"),
                            ("Anhwei", "Sinkiang"),
                            ("Archangel", "Evenki National Okrug"),
                            ("Archangel", "West Russia"),
                            ("Archangel", "Karelia S.S.R."),
                            ("Archangel", "Russia"),
                            ("Archangel", "Vologda"),
                            ("Baltic States", "Belorussia"),
                            ("Baltic States", "Poland"),
                            ("Baltic States", "Karelia S.S.R."),
                            ("Baltic States", "Germany"),
                            ("Belgian Congo", "Rhodesia"),
                            ("Belgian Congo", "Union of South Africa"),
                            ("Belgian Congo", "French Equatorial Africa"),
                            ("Belorussia", "Ukraine S.S.R."),
                            ("Belorussia", "Poland"),
                            ("Belorussia", "West Russia"),
                            ("Belorussia", "Karelia S.S.R."),
                            ("Brazil", "Venezuela"),
                            ("Brazil", "Colombia Equador"),
                            ("Brazil", "Peru Argentina"),
                            ("Bulgaria Romania", "Turkey"),
                            ("Bulgaria Romania", "Ukraine S.S.R."),
                            ("Bulgaria Romania", "Poland"),
                            ("Bulgaria Romania", "Southern Europe"),
                            ("Bulgaria Romania", "Germany"),
                            ("Burma", "French Indo-China Thailand"),
                            ("Burma", "Yunnan"),
                            ("Burma", "Himalaya"),
                            ("Burma", "India"),
                            ("Buryatia S.S.R.", "Manchuria"),
                            ("Buryatia S.S.R.", "Mongolia"),
                            ("Buryatia S.S.R.", "Soviet Far East"),
                            ("Buryatia S.S.R.", "Yakut S.S.R."),
                            ("Caucasus", "Turkey"),
                            ("Caucasus", "Persia"),
                            ("Caucasus", "Ukraine S.S.R."),
                            ("Caucasus", "Kazakh S.S.R."),
                            ("Caucasus", "West Russia"),
                            ("Caucasus", "Russia"),
                            ("Central America", "Colombia Equador"),
                            ("Central America", "East Mexico"),
                            ("Central United States", "Eastern United States"),
                            ("Central United States", "East Mexico"),
                            ("Central United States", "Western United States"),
                            ("Central United States", "Eastern Canada"),
                            ("Chile", "Peru Argentina"),
                            ("Colombia Equador", "Venezuela"),
                            ("Colombia Equador", "Peru Argentina"),
                            ("East Mexico", "Mexico"),
                            ("Eastern Australia", "Western Australia"),
                            ("Eastern Canada", "Eastern United States"),
                            ("Eastern Canada", "Western Canada"),
                            ("Egypt", "Trans-Jordan"),
                            ("Egypt", "Libya"),
                            ("Egypt", "Sahara"),
                            ("Eire", "United Kingdom"),
                            ("Evenki National Okrug", "Mongolia"),
                            ("Evenki National Okrug", "Yakut S.S.R."),
                            ("Evenki National Okrug", "Novosibirsk"),
                            ("Evenki National Okrug", "Sinkiang"),
                            ("Evenki National Okrug", "Vologda"),
                            ("Finland", "Sweden"),
                            ("Finland", "Norway"),
                            ("Finland", "Karelia S.S.R."),
                            ("France", "Northwestern Europe"),
                            ("France", "Italy"),
                            ("France", "Spain Portugal"),
                            ("France", "Switzerland"),
                            ("France", "Germany"),
                            ("French Equatorial Africa", "French West Africa"),
                            ("French Equatorial Africa", "Sahara"),
                            ("French Indo-China Thailand", "Yunnan"),
                            ("French Indo-China Thailand", "Malaya"),
                            ("French West Africa", "Sahara"),
                            ("Germany", "Northwestern Europe"),
                            ("Germany", "Poland"),
                            ("Germany", "Italy"),
                            ("Germany", "Southern Europe"),
                            ("Germany", "Switzerland"),
                            ("Gibraltar", "Spain Portugal"),
                            ("Himalaya", "Szechwan"),
                            ("Himalaya", "Yunnan"),
                            ("Himalaya", "India"),
                            ("India", "Persia"),
                            ("Italian East Africa", "Rhodesia"),
                            ("Italy", "Southern Europe"),
                            ("Italy", "Switzerland"),
                            ("Karelia S.S.R.", "West Russia"),
                            ("Kazakh S.S.R.", "Persia"),
                            ("Kazakh S.S.R.", "Szechwan"),
                            ("Kazakh S.S.R.", "Novosibirsk"),
                            ("Kazakh S.S.R.", "Sinkiang"),
                            ("Kazakh S.S.R.", "Russia"),
                            ("Kiangsu", "Manchuria"),
                            ("Kiangsu", "Kwangtung"),
                            ("Kwangtung", "Szechwan"),
                            ("Kwangtung", "Yunnan"),
                            ("Libya", "Sahara"),
                            ("Manchuria", "Mongolia"),
                            ("Mexico", "Western United States"),
                            ("Mongolia", "Yakut S.S.R."),
                            ("Mongolia", "Sinkiang"),
                            ("Morocco", "Sahara"),
                            ("Mozambique", "Rhodesia"),
                            ("Mozambique", "Union of South Africa"),
                            ("Norway", "Sweden"),
                            ("Novosibirsk", "Sinkiang"),
                            ("Novosibirsk", "Russia"),
                            ("Novosibirsk", "Vologda"),
                            ("Persia", "Turkey"),
                            ("Persia", "Trans-Jordan"),
                            ("Poland", "Ukraine S.S.R."),
                            ("Rhodesia", "Union of South Africa"),
                            ("Russia", "West Russia"),
                            ("Russia", "Vologda"),
                            ("Saudi Arabia", "Trans-Jordan"),
                            ("Sinkiang", "Szechwan"),
                            ("Southern Europe", "Turkey"),
                            ("Soviet Far East", "Yakut S.S.R."),
                            ("Szechwan", "Yunnan"),
                            ("Trans-Jordan", "Turkey"),
                            ("Ukraine S.S.R.", "West Russia"),
                            ("Western Canada", "Western United States")]

        for item in self.connections:
            self.board[item[0]].neighbors.append(item[1])
            self.board[item[1]].neighbors.append(item[0])

        self.units = [Unit("infantry", "land", 3, 1, 2, 1, 2), Unit("artillery", "land", 4, 2, 2, 1, 3),
                      Unit("tank", "land", 6, 3, 3, 2, 3), Unit("aa", "land", 6, 0, 0, 1, 3),
                      Unit("factory", "land", 15, 0, 0, 0), Unit("transport", "sea", 7, 0, 0, 2, 100, 100, 5),
                      Unit("sub", "sea", 6, 2, 1, 2), Unit("destroyer", "sea", 8, 2, 2, 2),
                      Unit("cruiser", "sea", 12, 3, 3, 2), Unit("carrier", "sea", 14, 1, 2, 2, 100, 100, 0, 10),
                      Unit("battleship", "sea", 20, 4, 4, 2), Unit("fighter", "air", 10, 3, 4, 4, 100, 5),
                      Unit("bomber", "air", 12, 4, 1, 6)]

        self.teams = {"America": "Allies",
                      "Britain": "Allies",
                      "Russia": "Allies",
                      "Germany": "Axis",
                      "Japan": "Axis",
                      "Neutral": "Neutral"}

        self.turn_order = {"Russia": "Germany",
                           "Germany": "Britain",
                           "Britain": "Japan",
                           "Japan": "America",
                           "America": "Russia"}
        
        self.win_cons = ["France", "Germany", "Italy", "Karelia S.S.R.", "United Kingdom", "Eastern United States", 
                         "Western United States", "Russia", "India", "Kiangsu", "Japan", "Philippine Islands", "Hawaiian Islands"]

        self.aa_flyover = True

    def get_unit(self, index):
        return self.units[index]

    def enemy_team(self, player='', team=''):
        if team:
            return 'Allies' if team == 'Axis' else 'Axis'
        else:
            return 'Allies' if self.teams[player] == 'Axis' else 'Axis'


class TerritoryState:
    """
    Object representing all fluid information about a territory
    """

    def __init__(self, territory_owner, unit_list=None, just_captured=False):
        self.owner = territory_owner
        self.just_captured = just_captured
        self.built_units = 0

        self.unit_state_list = list()
        if unit_list:
            self.unit_state_list = unit_list


class UnitState:
    """
    Provides fluid information for units
    """

    def __init__(self, owner, type_number, attached_units=None, attached_to=None, moves_used=0, damage=0, moved_from=None,
                 shots_taken=0):
        self.owner = owner
        self.type_index = type_number
        self.moves_used = moves_used
        self.damaged = damage
        if attached_units:
            self.attached_units = attached_units
        else:
            self.attached_units = list()
        self.attached_to = attached_to
        if moved_from:
            self.moved_from = moved_from
        else:
            self.moved_from = list()
        self.shots_taken = shots_taken
        self.retreated = False
        if self.type_index == 4:
            self.retreated = True


class TurnState:
    """
    Stores information on the state of the game,
    including the round, player, and phase.
    """

    def __init__(self, round_num, player, phase):
        self.round_num = round_num
        self.player = player
        self.phase = phase


class Player:
    """
    object to store info for each player
    """

    def __init__(self, name, capital, ipc=0, tech_tokens=0):
        self.name = name
        self.ipc = ipc
        self.total_income = ipc
        self.tech_tokens = tech_tokens
        self.capital = capital


class Game:
    """
    Represents the game as a whole, including all static and fluid
    information.
    """

    # converts unit-state numbers to units using rules.get_unit.

    def __init__(self):

        self.rules = Rules()
        # player 0 = russia, 1 = germany, 2 = britain, 3 = japan, 4 = us
        # phase 0 = tech, 1 = repair, 2 = buy, 3 = combat move, 4 = combat phase, 5 = non-combat, 6 = place, 7 = cleanup
        self.turn_state = TurnState(1, "Russia", 2)
        self.players = {"America": Player('America', 'Eastern United States', 42),  # This implementation of capitals is redundant
                        "Britain": Player('Britain', 'United Kingdom', 31),         # But other implementation requires searching through entire
                        "Russia": Player('Russia', 'Russia', 24),                   # game board any time you need a certain player's capital
                        "Germany": Player('Germany', 'Germany', 41),
                        "Japan": Player('Japan', 'Japan', 30)}
        self.purchased_units = {player: list() for player in self.players.keys()}
        # dictionary from territory names to territory states (containing unit_states)
        self.state_dict = {"1 Sea Zone": TerritoryState("Sea Zone", []),
                           "2 Sea Zone": TerritoryState("Sea Zone", []),
                           "3 Sea Zone": TerritoryState("Sea Zone", []),
                           "4 Sea Zone": TerritoryState("Sea Zone", [UnitState("Russia", 6)]),
                           "5 Sea Zone": TerritoryState("Sea Zone", [UnitState("Germany", 5), UnitState("Germany", 6),
                                                                     UnitState("Germany", 8)]),
                           "6 Sea Zone": TerritoryState("Sea Zone", []),
                           "7 Sea Zone": TerritoryState("Sea Zone", [UnitState("Britain", 5), UnitState("Britain", 7),
                                                                     UnitState("Britain", 10)]),
                           "8 Sea Zone": TerritoryState("Sea Zone", []),
                           "9 Sea Zone": TerritoryState("Sea Zone", [UnitState("Germany", 6), UnitState("Germany", 6)]),
                           "10 Sea Zone": TerritoryState("Sea Zone",
                                                         [UnitState("Britain", 5), UnitState("Britain", 7)]),
                           "11 Sea Zone": TerritoryState("Sea Zone", [UnitState("America", 5), UnitState("America", 5),
                                                                      UnitState("America", 7)]),
                           "12 Sea Zone": TerritoryState("Sea Zone", []),
                           "13 Sea Zone": TerritoryState("Sea Zone", [UnitState("Britain", 8)]),
                           "14 Sea Zone": TerritoryState("Sea Zone", []),
                           "15 Sea Zone": TerritoryState("Sea Zone",
                                                         [UnitState("Germany", 5), UnitState("Germany", 10)]),
                           "16 Sea Zone": TerritoryState("Sea Zone", []),
                           "17 Sea Zone": TerritoryState("Sea Zone", [UnitState("Britain", 7)]),
                           "18 Sea Zone": TerritoryState("Sea Zone", []),
                           "19 Sea Zone": TerritoryState("Sea Zone", [UnitState("America", 8)]),
                           "20 Sea Zone": TerritoryState("Sea Zone", []),
                           "21 Sea Zone": TerritoryState("Sea Zone", []),
                           "22 Sea Zone": TerritoryState("Sea Zone", []),
                           "23 Sea Zone": TerritoryState("Sea Zone", []),
                           "24 Sea Zone": TerritoryState("Sea Zone", []),
                           "25 Sea Zone": TerritoryState("Sea Zone", []),
                           "26 Sea Zone": TerritoryState("Sea Zone", []),
                           "27 Sea Zone": TerritoryState("Sea Zone", []),
                           "28 Sea Zone": TerritoryState("Sea Zone", []),
                           "29 Sea Zone": TerritoryState("Sea Zone", []),
                           "30 Sea Zone": TerritoryState("Sea Zone", []),
                           "31 Sea Zone": TerritoryState("Sea Zone", []),
                           "32 Sea Zone": TerritoryState("Sea Zone", []),
                           "33 Sea Zone": TerritoryState("Sea Zone", []),
                           "34 Sea Zone": TerritoryState("Sea Zone", []),
                           "35 Sea Zone": TerritoryState("Sea Zone", [UnitState("Britain", 5), UnitState("Britain", 8),
                                                                      UnitState("Britain", 9),
                                                                      UnitState("Britain", 11)]),
                           "36 Sea Zone": TerritoryState("Sea Zone", []),
                           "37 Sea Zone": TerritoryState("Sea Zone", [UnitState("Japan", 9), UnitState("Japan", 10),
                                                                      UnitState("Japan", 11),
                                                                      UnitState("Japan", 11)]),
                           "38 Sea Zone": TerritoryState("Sea Zone", []),
                           "39 Sea Zone": TerritoryState("Sea Zone", [UnitState("Britain", 5), UnitState("Britain", 6),
                                                                      UnitState("Britain", 8)]),
                           "40 Sea Zone": TerritoryState("Sea Zone", []),
                           "41 Sea Zone": TerritoryState("Sea Zone", []),
                           "42 Sea Zone": TerritoryState("Sea Zone", []),
                           "43 Sea Zone": TerritoryState("Sea Zone", []),
                           "44 Sea Zone": TerritoryState("Sea Zone", [UnitState("Japan", 6)]),
                           "45 Sea Zone": TerritoryState("Sea Zone", []),
                           "46 Sea Zone": TerritoryState("Sea Zone", []),
                           "47 Sea Zone": TerritoryState("Sea Zone", []),
                           "48 Sea Zone": TerritoryState("Sea Zone", []),
                           "49 Sea Zone": TerritoryState("Sea Zone", []),
                           "50 Sea Zone": TerritoryState("Sea Zone", [UnitState("Japan", 8), UnitState("Japan", 9),
                                                                      UnitState("Japan", 11)]),
                           "51 Sea Zone": TerritoryState("Sea Zone", []),
                           "52 Sea Zone": TerritoryState("Sea Zone", []),
                           "53 Sea Zone": TerritoryState("Sea Zone", [UnitState("America", 6), UnitState("America", 7),
                                                                      UnitState("America", 9),
                                                                      UnitState("America", 11)]),
                           "54 Sea Zone": TerritoryState("Sea Zone", []),
                           "55 Sea Zone": TerritoryState("Sea Zone", []),
                           "56 Sea Zone": TerritoryState("Sea Zone", [UnitState("America", 5), UnitState("America", 7),
                                                                      UnitState("America", 10)]),
                           "57 Sea Zone": TerritoryState("Sea Zone", []),
                           "58 Sea Zone": TerritoryState("Sea Zone", []),
                           "59 Sea Zone": TerritoryState("Sea Zone", []),
                           "60 Sea Zone": TerritoryState("Sea Zone", [UnitState("Japan", 5), UnitState("Japan", 7),
                                                                      UnitState("Japan", 10)]),
                           "61 Sea Zone": TerritoryState("Sea Zone", [UnitState("Japan", 5), UnitState("Japan", 7)]),
                           "62 Sea Zone": TerritoryState("Sea Zone", []),
                           "63 Sea Zone": TerritoryState("Sea Zone", []),
                           "64 Sea Zone": TerritoryState("Sea Zone", []),
                           "65 Sea Zone": TerritoryState("Sea Zone", []),
                           "Afghanistan": TerritoryState("Neutral", []),
                           "Alaska": TerritoryState("America", [UnitState("America", 0)]),
                           "Algeria": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 1)]),
                           "Anglo-Egyptian Sudan": TerritoryState("Britain", []),
                           "Angola": TerritoryState("Neutral", []),
                           "Anhwei": TerritoryState("America", [UnitState("America", 0), UnitState("America", 0)]),
                           "Archangel": TerritoryState("Russia", [UnitState("Russia", 0), UnitState("Russia", 2)]),
                           "Baltic States": TerritoryState("Germany",
                                                           [UnitState("Germany", 0), UnitState("Germany", 2)]),
                           "Belgian Congo": TerritoryState("Britain", []),
                           "Belorussia": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 0),
                                                                    UnitState("Germany", 0)]),
                           "Borneo": TerritoryState("Japan", [UnitState("Japan", 0)]),
                           "Brazil": TerritoryState("America", []),
                           "Bulgaria Romania": TerritoryState("Germany",
                                                              [UnitState("Germany", 0), UnitState("Germany", 0),
                                                               UnitState("Germany", 2),
                                                               UnitState("Germany", 11)]),
                           "Burma": TerritoryState("Britain", [UnitState("Britain", 0)]),
                           "Buryatia S.S.R.": TerritoryState("Russia",
                                                             [UnitState("Russia", 0), UnitState("Russia", 0)]),
                           "Caroline Islands": TerritoryState("Japan", [UnitState("Japan", 0)]),
                           "Caucasus": TerritoryState("Russia", [UnitState("Russia", 0), UnitState("Russia", 0),
                                                                 UnitState("Russia", 0),
                                                                 UnitState("Russia", 1), UnitState("Russia", 2),
                                                                 UnitState("Russia", 3),
                                                                 UnitState("Russia", 4)]),
                           "Central America": TerritoryState("America", []),
                           "Central United States": TerritoryState("America", [UnitState("America", 0)]),
                           "Chile": TerritoryState("Neutral", []),
                           "Colombia Equador": TerritoryState("Neutral", []),
                           "East Indies": TerritoryState("Japan", [UnitState("Japan", 0), UnitState("Japan", 0)]),
                           "East Mexico": TerritoryState("America", []),
                           "Eastern Australia": TerritoryState("Britain",
                                                               [UnitState("Britain", 0), UnitState("Britain", 0)]),
                           "Eastern Canada": TerritoryState("Britain", [UnitState("Britain", 2)]),
                           "Eastern United States": TerritoryState("America",
                                                                   [UnitState("America", 0), UnitState("America", 0),
                                                                    UnitState("America", 1), UnitState("America", 2),
                                                                    UnitState("America", 3), UnitState("America", 4),
                                                                    UnitState("America", 11),
                                                                    UnitState("America", 12)]),
                           "Egypt": TerritoryState("Britain", [UnitState("Britain", 0), UnitState("Britain", 1),
                                                               UnitState("Britain", 2),
                                                               UnitState("Britain", 11)]),
                           "Eire": TerritoryState("Neutral", []),
                           "Evenki National Okrug": TerritoryState("Russia",
                                                                   [UnitState("Russia", 0), UnitState("Russia", 0)]),
                           "Finland": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 0),
                                                                 UnitState("Germany", 0)]),
                           "Formosa": TerritoryState("Japan", []),
                           "France": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 2),
                                                                UnitState("Germany", 2),
                                                                UnitState("Germany", 3)]),
                           "French Equatorial Africa": TerritoryState("Britain", []),
                           "French Indo-China Thailand": TerritoryState("Japan",
                                                                        [UnitState("Japan", 0), UnitState("Japan", 0),
                                                                         UnitState("Japan", 1),
                                                                         UnitState("Japan", 11)]),
                           "French Madagascar": TerritoryState("Britain", []),
                           "French West Africa": TerritoryState("Britain", []),
                           "Germany": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 0),
                                                                 UnitState("Germany", 0),
                                                                 UnitState("Germany", 2), UnitState("Germany", 2),
                                                                 UnitState("Germany", 3),
                                                                 UnitState("Germany", 4), UnitState("Germany", 11)]),
                           "Gibraltar": TerritoryState("Britain", []),
                           "Greenland": TerritoryState("America", []),
                           "Hawaiian Islands": TerritoryState("America",
                                                              [UnitState("America", 0), UnitState("America", 11)]),
                           "Himalaya": TerritoryState("Neutral", []),
                           "Iceland": TerritoryState("Britain", []),
                           "India": TerritoryState("Britain", [UnitState("Britain", 0), UnitState("Britain", 0),
                                                               UnitState("Britain", 0),
                                                               UnitState("Britain", 0), UnitState("Britain", 0),
                                                               UnitState("Britain", 3),
                                                               UnitState("Britain", 4)]),
                           "Italian East Africa": TerritoryState("Britain", []),
                           "Italy": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 2),
                                                               UnitState("Germany", 3), UnitState("Germany", 4)]),
                           "Iwo Jima": TerritoryState("Japan", [UnitState("Japan", 0)]),
                           "Japan": TerritoryState("Japan",
                                                   [UnitState("Japan", 0), UnitState("Japan", 0), UnitState("Japan", 0),
                                                    UnitState("Japan", 0),
                                                    UnitState("Japan", 1), UnitState("Japan", 2), UnitState("Japan", 3),
                                                    UnitState("Japan", 4),
                                                    UnitState("Japan", 11), UnitState("Japan", 12)]),
                           "Karelia S.S.R.": TerritoryState("Russia", [UnitState("Russia", 0), UnitState("Russia", 0),
                                                                       UnitState("Russia", 0),
                                                                       UnitState("Russia", 0), UnitState("Russia", 1),
                                                                       UnitState("Russia", 4),
                                                                       UnitState("Russia", 11)]),
                           "Kazakh S.S.R.": TerritoryState("Russia", [UnitState("Russia", 0)]),
                           "Kiangsu": TerritoryState("Japan", [UnitState("Japan", 0), UnitState("Japan", 0),
                                                               UnitState("Japan", 0),
                                                               UnitState("Japan", 0)]),
                           "Kwangtung": TerritoryState("Japan", [UnitState("Japan", 0), UnitState("Japan", 1)]),
                           "Libya": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 2)]),
                           "Malaya": TerritoryState("Japan", [UnitState("Japan", 0)]),
                           "Manchuria": TerritoryState("Japan", [UnitState("Japan", 0), UnitState("Japan", 0),
                                                                 UnitState("Japan", 0),
                                                                 UnitState("Japan", 11)]),
                           "Mexico": TerritoryState("America", []),
                           "Midway": TerritoryState("America", [UnitState("America", 0)]),
                           "Mongolia": TerritoryState("Neutral", []),
                           "Morocco": TerritoryState("Germany", [UnitState("Germany", 0)]),
                           "Mozambique": TerritoryState("Neutral", []),
                           "New Guinea": TerritoryState("Japan", [UnitState("Japan", 0)]),
                           "New Zealand": TerritoryState("Britain", [UnitState("Britain", 0)]),
                           "Northwestern Europe": TerritoryState("Germany",
                                                                 [UnitState("Germany", 0), UnitState("Germany", 2),
                                                                  UnitState("Germany", 11)]),
                           "Norway": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 0),
                                                                UnitState("Germany", 11)]),
                           "Novosibirsk": TerritoryState("Russia", [UnitState("Russia", 0)]),
                           "Okinawa": TerritoryState("Japan", [UnitState("Japan", 0)]),
                           "Persia": TerritoryState("Britain", [UnitState("Britain", 0)]),
                           "Peru Argentina": TerritoryState("Neutral", []),
                           "Philippine Islands": TerritoryState("Japan",
                                                                [UnitState("Japan", 0), UnitState("Japan", 1)]),
                           "Poland": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 0),
                                                                UnitState("Germany", 2),
                                                                UnitState("Germany", 11)]),
                           "Rhodesia": TerritoryState("Britain", []),
                           "Russia": TerritoryState("Russia", [UnitState("Russia", 0), UnitState("Russia", 0),
                                                               UnitState("Russia", 0),
                                                               UnitState("Russia", 0), UnitState("Russia", 1),
                                                               UnitState("Russia", 2),
                                                               UnitState("Russia", 2), UnitState("Russia", 3),
                                                               UnitState("Russia", 4),
                                                               UnitState("Russia", 11)]),
                           "Sahara": TerritoryState("Neutral", []),
                           "Saudi Arabia": TerritoryState("Neutral", []),
                           "Sinkiang": TerritoryState("America", []),
                           "Solomon Islands": TerritoryState("Japan", [UnitState("Japan", 0)]),
                           "Southern Europe": TerritoryState("Germany",
                                                             [UnitState("Germany", 0), UnitState("Germany", 1)]),
                           "Soviet Far East": TerritoryState("Russia",
                                                             [UnitState("Russia", 0), UnitState("Russia", 0)]),
                           "Spain Portugal": TerritoryState("Neutral", []),
                           "Sweden": TerritoryState("Neutral", []),
                           "Switzerland": TerritoryState("Neutral", []),
                           "Szechwan": TerritoryState("America", [UnitState("America", 0), UnitState("America", 0),
                                                                  UnitState("America", 11)]),
                           "Trans-Jordan": TerritoryState("Britain", [UnitState("Britain", 0)]),
                           "Turkey": TerritoryState("Neutral", []),
                           "Ukraine S.S.R.": TerritoryState("Germany",
                                                            [UnitState("Germany", 0), UnitState("Germany", 0),
                                                             UnitState("Germany", 0),
                                                             UnitState("Germany", 1), UnitState("Germany", 2),
                                                             UnitState("Germany", 11), UnitState("Germany", 12)]),
                           "Union of South Africa": TerritoryState("Britain", [UnitState("Britain", 0)]),
                           "United Kingdom": TerritoryState("Britain",
                                                            [UnitState("Britain", 0), UnitState("Britain", 0),
                                                             UnitState("Britain", 1),
                                                             UnitState("Britain", 2), UnitState("Britain", 3),
                                                             UnitState("Britain", 4),
                                                             UnitState("Britain", 11), UnitState("Britain", 11),
                                                             UnitState("Britain", 12)]),
                           "Venezuela": TerritoryState("Neutral", []),
                           "Vologda": TerritoryState("Russia", []),
                           "Wake Island": TerritoryState("Japan", [UnitState("Japan", 0)]),
                           "West Indies": TerritoryState("America", []),
                           "West Russia": TerritoryState("Germany", [UnitState("Germany", 0), UnitState("Germany", 0),
                                                                     UnitState("Germany", 0),
                                                                     UnitState("Germany", 1), UnitState("Germany", 2)]),
                           "Western Australia": TerritoryState("Britain", [UnitState("Britain", 0)]),
                           "Western Canada": TerritoryState("Britain", [UnitState("Britain", 0)]),
                           "Western United States": TerritoryState("America",
                                                                   [UnitState("America", 0), UnitState("America", 0),
                                                                    UnitState("America", 3),
                                                                    UnitState("America", 4), UnitState("America", 11)]),
                           "Yakut S.S.R.": TerritoryState("Russia", [UnitState("Russia", 0)]),
                           "Yunnan": TerritoryState("America", [UnitState("America", 0), UnitState("America", 0)])}

        # Set original owners
        for k, v in self.state_dict.items():
            self.rules.board[k].original_owner = v.owner
    
    def has_won(self):
        axis_victory_cities = 0
        allies_victory_cities = 0
        for territory_name in self.rules.win_cons:
            if self.rules.teams[self.state_dict[territory_name].owner] == "Allies":
                allies_victory_cities += 1
            elif self.rules.teams[self.state_dict[territory_name].owner] == "Axis":
                axis_victory_cities += 1
        if axis_victory_cities >= 9:
            return "Axis"
        elif allies_victory_cities >= 10:
            return "Allies"
        else:
            return ""                      

    def export_reader(self, xml_file):
        # Read xml
        root = ET.parse(xml_file).getroot()
        turn = root.find("turn")
        captured_territories = root.find("capturedTerritories").findall("territory")
        players = root.find("players").findall("player")
        territories = root.find("territories").findall("territory")
        units = root.find("units").findall("unit")

        # Set turn state
        player_phase = turn.get("phase")
        i = 0
        while player_phase[i].islower():
            i += 1
        player, phase = player_phase[:i], player_phase[i:]
        turn_state_indices = {"russian": 'Russia', "german": 'Germany', "british": 'Britain', "japanese": 'Japan', "american": 'America',
                              "Tech": 2, "Purchase": 2, "CombatMove": 3, "Battle": 4, "NonCombatMove": 5, "Place": 6,
                              "TechActivation": 6, "EndTurn": 6}  # Why are there several things attatched to each number
        self.turn_state = TurnState(int(turn.get("round")), turn_state_indices[player], turn_state_indices[phase])

        # Set resources
        country_names = {"Americans": "America", "British": "Britain", "Germans": "Germany", "Japanese": "Japan",
                         "Russians": "Russia", "Neutral": "Neutral"}
        for elem in players:
            player = self.players[country_names[elem.get("name")]]
            for resource in elem.findall("resource"):
                if resource.get("name") == "PUs":
                    player.ipc = int(resource.get("quantity"))
                elif resource.get("name") == "techTokens":
                    player.tech_tokens = int(resource.get("quantity"))

        # Set territory owners
        for territory in territories:
            name, owner = territory.get("name"), country_names[territory.get("owner")]
            if 'Sea Zone' in name and owner == 'Neutral':
                owner = 'Sea Zone'
            self.state_dict[name].owner = owner

        # Reset territory units and values
        for territory in self.state_dict.values():
            territory.unit_state_list.clear()
            territory.just_captured = False

        # Mark territories which were captured this turn (i.e. planes can't land in them)
        for territory in captured_territories:
            self.state_dict[territory.get("name")].just_captured = True

        # Set units #This was used earlier, do you need to move this before the unit initialization thing or is that only for c++
        unit_indices = {"infantry": 0, "artillery": 1, "armour": 2, "fighter": 11, "bomber": 12, "transport": 5,
                        "submarine": 6, "destroyer": 7,
                        "cruiser": 8, "carrier": 9, "battleship": 10, "aaGun": 3, "factory": 4}
        all_units = dict()
        # First pass through the list to initialize all units and attach them to their territory
        for unit in units:
            # Get values from the xml file
            unit_type, owner, territory = unit_indices[unit.get("type")], country_names[unit.get("owner")], unit.get(
                "territory")
            unit_id, moves_used = unit.get("id"), self.rules.get_unit(unit_type).movement - int(unit.get("movesLeft"))
            transport, damage = None if unit.get("transport") == "null" else unit.get("transport"), int(
                unit.get("damage"))
            # Attach to territory
            self.state_dict[territory].unit_state_list.append(
                UnitState(owner, unit_type, moves_used=moves_used, damage=damage))
            # Keep track of where this unit is for later
            all_units[unit_id] = (territory, self.state_dict[territory].unit_state_list[-1], transport)

        # Second pass through list to attach units to transports
        for ter, land_unit, transport in all_units.values():
            if transport:
                transport_unit = all_units[transport][1]
                transport_unit.attached_units.append(land_unit)
                land_unit.attached_to = transport_unit

        return all_units

    def controls_suez(self, team=''):
        if not team:
            team = self.rules.teams[self.turn_state.player]
        return (self.rules.teams[self.state_dict["Egypt"].owner] == team) and (self.rules.teams[self.state_dict["Trans-Jordan"].owner] == team)

    def controls_panama(self, team=''):
        if not team:
            team = self.rules.teams[self.turn_state.player]
        return self.rules.teams[self.state_dict["Central America"].owner] == team

    def calc_movement(self, unit_state, current_territory, goal_territory, phase=-1):
        """
        a function that will check if a theoretical move is valid, and returns the movement required to move there, as well as the path taken.
        Returns -1 if impossible
        This replaces the old "passable" function
        """
        if unit_state not in self.state_dict[current_territory].unit_state_list:
            return -1, list()

        # Check if it would be possible to move to goal territory at all before doing BFS
        unit = self.rules.get_unit(unit_state.type_index)
        goal_territory_state = self.state_dict[goal_territory]
        if phase == -1:
            phase = self.turn_state.phase

        # Can't move into neutral territories
        if goal_territory_state.owner == "Neutral":
            return -1, list()

        # Deal with some planes landing stuff
        if phase == 5 and unit.unit_type == 'air':
            if self.rules.board[goal_territory].is_water:
                if unit_state.type_index == 12:
                    return -1, list()
                open_spots = 0
                for us in goal_territory_state.unit_state_list:
                    if self.rules.teams[unit_state.owner] == self.rules.teams[us.owner]:
                        if us.type_index == 11:
                            open_spots -= 1
                        elif us.type_index == 9:
                            open_spots += 2
                if open_spots <= 0:
                    return -1, list()
            elif self.rules.teams[goal_territory_state.owner] != self.rules.teams[unit_state.owner] or goal_territory_state.just_captured:
                return -1, list()

        if current_territory == goal_territory:
            return 0, [goal_territory]

        # Can't move if no movement left
        if unit_state.moves_used == unit.movement:
            return -1, list()

        # AA guns can't move in combat turns
        if phase == 3 and unit.name == 'aa':
            return -1, list()

        # Sea units can only move to sea, and land can only move to land
        # Unless land units move to an adjacent transport
        if self.rules.board[goal_territory].is_water:
            if unit.unit_type == "land":
                if unit_state.moves_used > 0 or goal_territory not in self.rules.board[current_territory].neighbors:
                    return -1, list()  # Tanks can move 2, wouldn't moves used be greater than 1 to end turn?
                for other_unit_state in goal_territory_state.unit_state_list:
                    # Check for allied transports
                    if other_unit_state.type_index == 5 and self.rules.teams[other_unit_state.owner] == \
                            self.rules.teams[unit_state.owner]:
                        # Check if the transport has space
                        if len(other_unit_state.attached_units) == 0 or (len(other_unit_state.attached_units) == 1 and (
                                unit_state.type_index == 0 or other_unit_state.attached_units[0].type_index == 0)):
                            return 0, [current_territory, goal_territory]
                return -1, list()
        else:
            if unit.unit_type == 'sea':
                return -1, list()

        # Non-combat movement
        if phase == 5:
            # Can't move into enemy territory
            if goal_territory_state.owner != "Sea Zone" and self.rules.teams[goal_territory_state.owner] != \
                    self.rules.teams[unit_state.owner]:
                return -1, list()
            # Can't move into territories with enemy units, unless sub, transport or factory
            for other_unit_state in goal_territory_state.unit_state_list:
                if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                    if not 4 <= other_unit_state.type_index <= 6:  # Can move through factories, transports, and subs
                        if unit.name != 'sub' or other_unit_state.type_index == 7:  # Subs can move through anything except destroyers
                            return -1, list()

        # Transported units can only move to adjacent land
        if unit_state.attached_to:
            # Must move to land, with all of their movement, and to an adjacent space
            if self.rules.board[goal_territory].is_water or unit_state.moves_used > 0\
                    or goal_territory not in self.rules.board[current_territory].neighbors:
                return -1, list()
            # If it is the non-combat move phase, and there are enemy units, it can't move
            if phase == 5:
                for other_unit_state in goal_territory_state.unit_state_list:
                    if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                        return -1, list()
            # Otherwise, it can move there
            return unit.movement, [current_territory, goal_territory]

        # Breadth-First Search to find shortest path
        path = self.bfs(unit_state, current_territory, goal_territory, unit.movement - unit_state.moves_used, phase=phase)
        if not path:
            return -1, list()

        # Land/sea units can't move after combat, so use all remaining movement
        if phase == 3 and unit.unit_type != 'air':
            # Check for enemy units/destroyers
            enemy_units, enemy_destroyer = False, False
            for other_unit_state in goal_territory_state.unit_state_list:
                if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                    if other_unit_state.type_index < 4 or other_unit_state.type_index > 6:  # Ignore subs/transports/factories
                        if not other_unit_state.attached_to:  # Ignore transported units
                            enemy_units = True
                            if self.rules.get_unit(other_unit_state.type_index).name == 'destroyer':
                                enemy_destroyer = True
            if enemy_units:
                if not (unit.name == "sub" and not enemy_destroyer):
                    return unit.movement - unit_state.moves_used, path

        # Check if air units can return (only necessary if combat move)
        if unit.unit_type == 'air' and phase == 3:
            # Check where carriers are able to move (for fighters only). This is inefficient and bad and wrong
            if unit.name == 'fighter':
                possible_carrier_spots = set()
                for name, territory in self.state_dict.items():
                    # For each territory, get a list of allied carriers and fighters within it
                    carriers, fighters = list(), list()
                    for other_unit_state in territory.unit_state_list:
                        if self.rules.teams[other_unit_state.owner] == self.rules.teams[unit_state.owner]:
                            if other_unit_state.type_index == 9:
                                carriers.append(other_unit_state)
                            elif other_unit_state.type_index == 11 and other_unit_state != unit_state:
                                fighters.append(other_unit_state)
                    # If there is an empty space available, find the carrier/fighter combo with the most available movement
                    if len(carriers) * 2 > len(fighters):
                        if len(carriers) * 2 == len(fighters) + 1:
                            # Case 1: Exactly one open spot
                            max_movement = min(
                                self.rules.units[9].movement - min([carrier.moves_used for carrier in carriers]),
                                self.rules.units[11].movement - min([fighter.moves_used for fighter in fighters]))
                        else:
                            # Case 2: At least one carrier has no fighters
                            max_movement = self.rules.units[9].movement - min(
                                [carrier.moves_used for carrier in carriers])
                        # BFS to find all possible spots this carrier could move to
                        queue = [name]
                        checked = {name}
                        possible_carrier_spots.add(name)
                        for _ in range(max_movement):
                            next_queue = list()
                            # Go through all territories in the queue
                            while queue:
                                ter = queue.pop()
                                # Go through each neighbor
                                for neighbor in self.rules.board[ter].neighbors:
                                    # See if this neighbor has already been checked, and is water
                                    if self.rules.board[neighbor].is_water and neighbor not in checked:
                                        checked.add(neighbor)
                                        # Can't move through enemies
                                        has_enemies = False
                                        for other_unit_state in self.state_dict[neighbor].unit_state_list:
                                            if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                                                has_enemies = True
                                                break
                                        if not has_enemies:
                                            next_queue.append(neighbor)
                                            possible_carrier_spots.add(neighbor)
                            queue = next_queue
                return_path = self.bfs(unit_state, goal_territory, None, unit.movement - unit_state.moves_used - (len(path) - 1),
                                       carrier_spots=possible_carrier_spots, phase=phase)
            else:
                return_path = self.bfs(unit_state, goal_territory, None, unit.movement - unit_state.moves_used - (len(path) - 1), phase=phase)
            if not return_path:
                return -1, list()

        # We want number of edges, not number of nodes, so subtract 1 <Dont know what this means
        return len(path) - 1, path

    def bfs(self, unit_state, root, target, max_dist, carrier_spots=None, phase=-1):
        """
        a function that uses breadth-first search to find the shortest path between two nodes, within the movement limit of the unit
        if target is None, then search for available landing spot for plane
        """
        # Simultaneously keep track of parent nodes and visited nodes
        parents = {root: None}
        # FIFO queue to determine order to check nodes, as well as distance to reach them
        queue = [(root, 0)]

        # Check current territory first
        if (not target and self.passable(unit_state, root, root, True, carrier_spots, phase=5)) or \
                (root == target and self.passable(unit_state, root, root, True, carrier_spots, phase=phase)):
            return [root]

        while queue:
            # Dequeue node and check every neighbor
            current, dist = queue.pop(0)
            for neighbor in self.rules.board[current].neighbors:
                # Must be within movement range
                if dist < max_dist:
                    # Check if current neighbor is the target
                    if (not target and self.passable(unit_state, current, neighbor, True, carrier_spots, phase=5)) \
                            or (neighbor == target and self.passable(unit_state, current, neighbor, True, carrier_spots, phase=phase)):
                        # Could just return distance, but path may be useful for debugging
                        path = [neighbor, current]
                        while path[-1] != root:
                            path.append(parents[path[-1]])
                        return path[::-1]
                    # If not valid target, check if it can be moved through, and hasn't yet been visited
                    if neighbor not in parents.keys():
                        if self.passable(unit_state, current, neighbor, phase=phase):
                            parents[neighbor] = current
                            queue.append((neighbor, dist + 1))

        # No path found within the movement limit, so return empty list
        return list()

    def passable(self, unit_state, current_territory_name, goal_territory_name, final_move=False, carrier_spots=None, phase=-1):
        """
        a function that will check if a unit can move over this territory.
        Used by calc_movement function
        """
        if phase == -1:
            phase = self.turn_state.phase

        unit = self.rules.get_unit(unit_state.type_index)
        territory_state = self.state_dict[goal_territory_name]

        # Land units can't move through water. Planes handled later
        if self.rules.board[goal_territory_name].is_water:
            if unit.unit_type == "land":
                return False

        # Sea units can't move on land
        elif unit.unit_type == "sea":
            return False

        # Can't move into neutral territories
        if territory_state.owner == "Neutral":
            return False

        # Check Suez canal
        if (current_territory_name == "17 Sea Zone" and goal_territory_name == "34 Sea Zone") or \
                (current_territory_name == "34 Sea Zone" and goal_territory_name == "17 Sea Zone"):
            if not self.controls_suez():
                return False

        # Check panama canal
        if (current_territory_name == "18 Sea Zone" and goal_territory_name == "19 Sea Zone") or \
                (current_territory_name == "19 Sea Zone" and goal_territory_name == "18 Sea Zone"):
            if not self.controls_panama():
                return False

        # Plane movement
        if unit.unit_type == "air":
            # Can move anywhere (except neutrals, handled above)
            # But must end non-combat turn on friendly territory (not captured this turn) or on friendly carrier (fighters only)
            if phase == 5 and final_move:
                # Can't land in water, unless fighter + carrier
                if territory_state.owner == "Sea Zone":
                    if unit.name == "bomber":
                        return False
                    elif unit.name == "fighter":
                        # When checking for a return trip on a combat turn, account for carrier movement
                        if carrier_spots is not None:
                            if goal_territory_name not in carrier_spots:
                                return False
                        # In non combat moves, carriers need to be moved prior to fighters landing on them
                        else:
                            num_carriers = 0
                            num_fighters = 0
                            # Check every unit in territory for other carriers and fighters
                            for other_unit_state in territory_state.unit_state_list:
                                if self.rules.teams[other_unit_state.owner] == self.rules.teams[unit_state.owner]:
                                    if self.rules.get_unit(other_unit_state.type_index).name == 'carrier':
                                        num_carriers += 1
                                    elif self.rules.get_unit(other_unit_state.type_index).name == 'fighter':
                                        num_fighters += 1
                            # Each carrier can carry up to 2 fighters
                            if num_fighters >= num_carriers * 2:
                                return False
                # Can't land in enemy territory
                elif self.rules.teams[territory_state.owner] != self.rules.teams[unit_state.owner]:
                    return False
                # Check if territory was captured this turn
                elif territory_state.just_captured:
                    return False
        # Non-plane movement
        else:
            # Non-combat movement
            if phase == 5:
                # Can't move into enemy territory
                if territory_state.owner != "Sea Zone" and \
                        self.rules.teams[territory_state.owner] != self.rules.teams[unit_state.owner]:
                    return False
                # Can't move into territories with enemy units
                for other_unit_state in territory_state.unit_state_list:
                    if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                        if not 4 <= other_unit_state.type_index <= 6:  # Can move through factories, transports, and subs
                            if unit.name != 'sub' or other_unit_state.type_index == 7:  # Subs can move through anything except destroyers
                                return False
            # Combat movement
            elif phase == 3:
                # AA guns can't move in combat phase
                if unit.name == "aa":
                    return False

                # Land/sea units must stop moving if there are enemy units (with exception for subs, and moving past subs/transports/factories)
                # But this only matters if this is not the unit's final move
                if not final_move:
                    # Check for enemy units/destroyers
                    enemy_units, enemy_destroyer = False, False
                    for other_unit_state in territory_state.unit_state_list:
                        if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                            if other_unit_state.type_index < 4 or other_unit_state.type_index > 6:  # Ignore subs/transports/factories
                                if not other_unit_state.attached_to:  # Ignore transported units
                                    enemy_units = True
                                    if self.rules.get_unit(other_unit_state.type_index).name == 'destroyer':
                                        enemy_destroyer = True

                    # Land/sea units must stop moving if there are enemy units (with exception for subs)
                    if enemy_units:
                        if not (unit.name == "sub" and not enemy_destroyer):
                            return False

        # Otherwise, can move here
        return True

    def check_unit_transport(self, land_unit_state, land_unit_territory, transport_state,
                             transport_territory, goal_territory, phase=-1, return_paths=False):
        if phase == -1:
            phase = self.turn_state.phase

        # AA guns can't move in combat
        if phase == 3 and land_unit_state.type_index == 3:
            return list() if return_paths else False

        # Check if already on a different transport
        if land_unit_state.attached_to and land_unit_state.attached_to != transport_state:
            return list() if return_paths else False

        # Unit must have all movement to load onto a transport
        if land_unit_state.moves_used > 0:
            return list() if return_paths else False

        # Get all territories that the unit can be loaded into
        loadable_territories = [neighbor for neighbor in self.rules.board[land_unit_territory].neighbors if self.rules.board[neighbor].is_water]
        # Get all territories that the unit can be unloaded into (or wants to move to)
        if self.rules.board[goal_territory].is_water:
            unloadable_territories = [goal_territory]
        else:
            unloadable_territories = [neighbor for neighbor in self.rules.board[goal_territory].neighbors if self.rules.board[neighbor].is_water]
            if not unloadable_territories:
                return list() if return_paths else False
            # Check if unit can even unload here
            if not self.passable(land_unit_state, unloadable_territories[0], goal_territory, phase=phase, final_move=True):
                return list() if return_paths else False

        # Already attached to/next to transport, so don't bother checking other loadable territories
        if land_unit_state.attached_to == transport_state or transport_territory in loadable_territories:
            loadable_territories = [transport_territory]

        # If not next to water, then obviously can't transport
        if not loadable_territories:
            return list() if return_paths else False

        # Check all possible territory combinations and see which ones are possible
        paths = list()
        for territory_1 in loadable_territories:
            for territory_2 in unloadable_territories:
                if transport_territory == territory_1 == territory_2:
                    paths.append([transport_territory])
                elif transport_territory == territory_1 or territory_1 == territory_2:
                    if transport_territory in self.rules.board[territory_2].neighbors:
                        if self.passable(transport_state, transport_territory, territory_2, phase=phase):
                            paths.append([transport_territory, territory_2])
                    else:
                        for mid in self.rules.board[transport_territory].neighbors:
                            if mid in self.rules.board[territory_2].neighbors:
                                if self.passable(transport_state, transport_territory, mid, phase=phase) \
                                        and self.passable(transport_state, mid, territory_2, phase=phase):
                                    paths.append([transport_territory, mid, territory_2])
                else:
                    if transport_territory in self.rules.board[territory_1].neighbors and territory_2 in self.rules.board[territory_1].neighbors:
                        if self.passable(transport_state, transport_territory, territory_1, phase=phase) \
                                and self.passable(transport_state, territory_1, territory_2, phase=phase):
                            paths.append([transport_territory, territory_1, territory_2])

        for i in range(len(paths)-1, -1, -1):
            if len(paths[i]) > 3 - transport_state.moves_used:
                paths.pop(i)

        return paths if return_paths else (len(paths) > 0)

    def check_two_unit_transport(self, land_unit_state_1, land_unit_territory_1, land_unit_state_2, land_unit_territory_2, transport_state,
                                 transport_territory, goal_territory, phase=-1, return_paths=False):
        # Check if they both fit on the transport
        if land_unit_state_1.type_index > 0 and land_unit_state_2.type_index > 0:
            return list() if return_paths else False

        # Check each land unit individually
        paths_1 = self.check_unit_transport(land_unit_state_1, land_unit_territory_1, transport_state,
                                            transport_territory, goal_territory, phase=phase, return_paths=True)
        if not paths_1:
            return list() if return_paths else False
        paths_2 = self.check_unit_transport(land_unit_state_2, land_unit_territory_2, transport_state,
                                            transport_territory, goal_territory, phase=phase, return_paths=True)
        if not paths_2:
            return list() if return_paths else False

        # In order to merge two paths into one:
        # The two paths must have the same starting location (always true, since it starts in transport territory)
        # And the same ending location (can't unload from different spots)
        # The max length of each path is 3 (3 territories = 2 moves). If both are length 3, they must be identical.
        # If either is length 2 (or less), then by the first two conditions, it must be a subset of the longer path

        # First separate by ending location
        ending_spots = dict()
        for path in paths_1:
            if path[-1] not in ending_spots:
                ending_spots[path[-1]] = [[], []]
            ending_spots[path[-1]][0].append(path)
        for path in paths_2:
            if path[-1] not in ending_spots:
                ending_spots[path[-1]] = [[], []]
            ending_spots[path[-1]][1].append(path)

        # For each ending location, check for paths of length 2. If found, the entire other list of paths is valid
        # Otherwise, add paths that match exactly
        paths = list()
        for p1, p2 in ending_spots.values():
            if p1 and p2:
                if min(len(path) for path in p1) < 3:
                    # All of p2 is valid
                    for path in p2:
                        if p2 not in paths:
                            paths.append(path)
                if min(len(path) for path in p2) < 3:
                    # All of p1 is valid
                    for path in p1:
                        if p1 not in paths:
                            paths.append(path)
                # Get identical paths
                for path in p1:
                    if path in p2 and path not in paths:
                        paths.append(path)

        return paths if return_paths else (len(paths) > 0)
