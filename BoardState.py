# Make array representing board state
# must be editable by reading exported files 
# (either from xml or sheet)


class Territory:
        """
        Represents all static information about a territory
        """
        
        #neighbors list has the target and conditions
        #conditions could be 'edge' class which asks if its passible
        
        def __init__(self, territory_name, ipc_value, is_seazone):
                self.name = territory_name
                self.neighbors = []
                self.ipc = ipc_value
                self.is_water = is_seazone
                
class Unit:# Make array representing board state
# must be editable by reading exported files 
# (either from xml or sheet)


class Territory:
        """
        Represents all static information about a territory
        """
        
        #neighbors list has the target and conditions
        #conditions could be 'edge' class which asks if its passible
        
        def __init__(self, territory_name, ipc_value, is_seazone):
                self.name = territory_name
                self.neighbors = []
                self.ipc = ipc_value
                self.is_water = is_seazone
                
class Unit:
        """
        Provides a basic template for a unit
        """
        
        # movement ability
        # attack defense
        # transport capacity

        def __init__(self, unit_name, unit_type, cost, attack, defense, movement, transport = False, carrier = False):
                self.name = unit_name
                
                self.unit_type = unit_type
                self.cost = cost
                
                self.attack = attack
                self.defense = defense
                self.movement = movement
                
                self.is_transport = transport
                # FIGURE OUT HOW TO REPRESENT FULL TRANSPORTS. IS THE UNIT DIRECTLY ATTACHED?
                self.is_carrier = carrier
        
        
class Rules:
        """
        Contains static game data: a board representing territories, assignment of neighbors 
        for each territory (which is contained within a dictionary from string to
        territory), and prototypes for units.
        """
        
        # defines all the prototypes for units. definitions
        # also says all territorries and how they are conneted.
        # if has __ tech, attack ++
        # rules.get_unit_type (tank)
        
        def __init__(self):
                self.board = {"1 Sea Zone" : Territory("1 Sea Zone", 0, 1), \
                "2 Sea Zone" : Territory("2 Sea Zone", 0, 1), \
                "3 Sea Zone" : Territory("2 Sea Zone", 0, 1), \
                "4 Sea Zone" : Territory("4 Sea Zone", 0, 1), \
                "5 Sea Zone" : Territory("5 Sea Zone", 0, 1), \
                "6 Sea Zone" : Territory("6 Sea Zone", 0, 1), \
                "7 Sea Zone" : Territory("7 Sea Zone", 0, 1), \
                "8 Sea Zone" : Territory("8 Sea Zone", 0, 1), \
                "9 Sea Zone" : Territory("9 Sea Zone", 0, 1), \
                "10 Sea Zone" : Territory("10 Sea Zone", 0, 1), \
                "11 Sea Zone" : Territory("11 Sea Zone", 0, 1), \
                "12 Sea Zone" : Territory("12 Sea Zone", 0, 1), \
                "13 Sea Zone" : Territory("13 Sea Zone", 0, 1), \
                "14 Sea Zone" : Territory("14 Sea Zone", 0, 1), \
                "15 Sea Zone" : Territory("15 Sea Zone", 0, 1), \
                "16 Sea Zone" : Territory("16 Sea Zone", 0, 1), \
                "17 Sea Zone" : Territory("17 Sea Zone", 0, 1), \
                "18 Sea Zone" : Territory("18 Sea Zone", 0, 1), \
                "19 Sea Zone" : Territory("19 Sea Zone", 0, 1), \
                "20 Sea one" : Territory("20 Sea Zone", 0, 1), \
                "21 Sea Zone" : Territory("21 Sea Zone", 0, 1), \
                "22 Sea Zone" : Territory("22 Sea Zone", 0, 1), \
                "23 Sea Zone" : Territory("23 Sea Zone", 0, 1), \
                "24 Sea Zone" : Territory("24 Sea Zone", 0, 1), \
                "25 Sea Zone" : Territory("25 Sea Zone", 0, 1), \
                "26 Sea Zone" : Territory("26 Sea Zone", 0, 1), \
                "27 Sea Zone" : Territory("27 Sea Zone", 0, 1), \
                "28 Sea Zone" : Territory("28 Sea Zone", 0, 1), \
                "29 Sea Zone" : Territory("29 Sea Zone", 0, 1), \
                "30 Sea Zone" : Territory("30 Sea Zone", 0, 1), \
                "31 Sea Zone" : Territory("31 Sea Zone", 0, 1), \
                "32 Sea Zone" : Territory("32 Sea Zone", 0, 1), \
                "33 Sea Zone" : Territory("33 Sea Zone", 0, 1), \
                "34 Sea Zone" : Territory("34 Sea Zone", 0, 1), \
                "35 Sea Zone" : Territory("35 Sea Zone", 0, 1), \
                "36 Sea Zone" : Territory("36 Sea Zone", 0, 1), \
                "37 Sea Zone" : Territory("37 Sea Zone", 0, 1), \
                "38 Sea Zone" : Territory("38 Sea Zone", 0, 1), \
                "39 Sea Zone" : Territory("39 Sea Zone", 0, 1), \
                "40 Sea Zone" : Territory("40 Sea Zone", 0, 1), \
                "41 Sea Zone" : Territory("41 Sea Zone", 0, 1), \
                "42 Sea Zone" : Territory("42 Sea Zone", 0, 1), \
                "43 Sea Zone" : Territory("43 Sea Zone", 0, 1), \
                "44 Sea Zone" : Territory("44 Sea Zone", 0, 1), \
                "45 Sea Zone" : Territory("45 Sea Zone", 0, 1), \
                "46 Sea Zone" : Territory("46 Sea Zone", 0, 1), \
                "47 Sea Zone" : Territory("47 Sea Zone", 0, 1), \
                "48 Sea Zone" : Territory("48 Sea Zone", 0, 1), \
                "49 Sea Zone" : Territory("49 Sea Zone", 0, 1), \
                "50 Sea Zone" : Territory("50 Sea Zone", 0, 1), \
                "51 Sea Zone" : Territory("51 Sea Zone", 0, 1), \
                "52 Sea Zone" : Territory("52 Sea Zone", 0, 1), \
                "53 Sea Zone" : Territory("53 Sea Zone", 0, 1), \
                "54 Sea Zone" : Territory("54 Sea Zone", 0, 1), \
                "55 Sea Zone" : Territory("55 Sea Zone", 0, 1), \
                "56 Sea Zone" : Territory("56 Sea Zone", 0, 1), \
                "57 Sea Zone" : Territory("57 Sea Zone", 0, 1), \
                "58 Sea Zone" : Territory("58 Sea Zone", 0, 1), \
                "59 Sea Zone" : Territory("59 Sea Zone", 0, 1), \
                "60 Sea Zone" : Territory("60 Sea Zone", 0, 1), \
                "61 Sea Zone" : Territory("61 Sea Zone", 0, 1), \
                "62 Sea Zone" : Territory("62 Sea Zone", 0, 1), \
                "63 Sea Zone" : Territory("63 Sea Zone", 0, 1), \
                "64 Sea Zone" : Territory("64 Sea Zone", 0, 1), \
                "65 Sea Zone" : Territory("65 Sea Zone", 0, 1), \
                "Afghanistan" : Territory("Afghanistan", 1, 0), \
                "Alaska" : Territory("Alaska", 2, 0), \
                "Algeria" : Territory("Algeria", 1, 0), \
                "Anglo-Egyptian Sudan" : Territory("Anglo-Egyptian Sudan", 0, 0), \
                "Angola" : Territory("Angola", 0, 0), \
                # NEUTRAL ^
                "Anhwei" : Territory("Anhwei", 1, 0), \
                "Archangel" : Territory("Archangel", 1, 0), \
                "Baltic States" : Territory("Baltic States", 2, 0), \
                "Belgian Congo" : Territory("Belgian Congo", 1, 0), \
                "Belorussia" : Territory("Belorussia", 2, 0), \
                "Borneo" : Territory("Borneo", 4, 0), \
                "Brazil" : Territory("Brazil", 3, 0), \
                "Bulgaria Romania" : Territory("Bulgaria Romania", 2, 0), \
                "Burma" : Territory("Burma", 1, 0), \
                "Buryatia S.S.R." : Territory("Buryatia S.S.R.", 1, 0), \
                "Caroline Islands" : Territory("Caroline Islands", 0, 0), \
                "Caucasus" : Territory("Caucasus", 4, 0), \
                "Central America" : Territory("Central America", 1, 0), \
                "Central United States" : Territory("Central United States", 6, 0), \
                "Chile" : Territory("Chile", 0, 0), \
                # NEUTRAL ^
                "Colombia Equador" : Territory("Colombia Equador", 0, 0), \
                # NEUTRAL ^
                "East Indies" : Territory("East Indies", 4, 0), \
                "East Mexico" : Territory("East Mexico", 0, 0), \
                "Eastern Australia" : Territory("Eastern Australia", 1, 0), \
                "Eastern Canada" : Territory("Eastern Canada", 3, 0), \
                "Eastern United States" : Territory("Eastern United States", 12, 0), \
                "Egypt" : Territory("Egypt", 2, 0), \
                "Eire" : Territory("Eire", 0, 0), \
                # NEUTRAL ^
                "Evenki National Okrug" : Territory("Evenki National Okrug", 1, 0), \
                "Finland" : Territory("Finland", 1, 0), \
                "Formosa" : Territory("Formosa", 0, 0), \
                "France" : Territory("France", 6, 0), \
                "French Equatorial Africa" : Territory("French Equatorial Africa", 1, 0), \
                "French Indo-China Thailand" : Territory("French Indo-China Thailand", 2, 0), \
                "French Madagascar" : Territory("French Madagascar", 1, 0), \
                "French West Africa" : Territory("French West Africa", 1, 0), \
                "Germany" : Territory("Germany", 10, 0), \
                "Gibraltar" : Territory("Gibraltar", 0, 0), \
                "Greenland" : Territory("Greenland", 0, 0), \
                "Hawaiian Islands" : Territory("Hawaiian Islands", 1, 0), \
                "Himalaya" : Territory("Himalaya", 0, 0), \
                # NEUTRAL ^
                "Iceland" : Territory("Iceland", 0, 0), \
                "India" : Territory("India", 3, 0), \
                "Italian East Africa" : Territory("Italian East Africa", 1, 0), \
                "Italy" : Territory("Italy", 3, 0), \
                "Iwo Jima" : Territory("Iwo Jima", 0, 0), \
                "Japan" : Territory("Japan", 8, 0), \
                "Karelia S.S.R." : Territory("Karelia S.S.R.", 2, 0), \
                "Kazakh S.S.R." : Territory("Kazakh S.S.R.", 2, 0), \
                "Kiangsu" : Territory("Kiangsu", 2, 0), \
                "Kwangtung" : Territory("Kwangtung", 2, 0), \
                "Libya" : Territory("Libya", 1, 0), \
                "Malaya" : Territory("Malaya", 1, 0), \
                "Manchuria" : Territory("Manchuria", 3, 0), \
                "Mexico" : Territory("Mexico", 2, 0), \
                "Midway" : Territory("Midway", 0, 0), \
                "Mongolia" : Territory("Mongolia", 0, 0), \
                # NEUTRAL ^
                "Morocco" : Territory("Morocco", 1, 0), \
                "Mozambique" : Territory("Mozambique", 0, 0), \
                # NEUTRAL ^
                "New Guinea" : Territory("New Guinea", 1, 0), \
                "New Zealand" : Territory("New Zealand", 1, 0), \
                "Northwestern Europe" : Territory("Northwestern Europe", 2, 0), \
                "Norway" : Territory("Norway", 2, 0), \
                "Novosibirsk" : Territory("Novosibirsk", 1, 0), \
                "Okinawa" : Territory("Okinawa", 0, 0), \
                "Persia" : Territory("Persia", 1, 0), \
                "Peru Argentina" : Territory("Peru Argentina", 0, 0), \
                # NEUTRAL ^
                "Philippine Islands" : Territory("Philippine Islands", 3, 0), \
                "Poland" : Territory("Poland", 2, 0), \
                "Rhodesia" : Territory("Rhodesia", 1, 0), \
                "Russia" : Territory("Russia", 8, 0), \
                "Sahara" : Territory("Sahara", 0, 0), \
                # NEUTRAL ^
                "Saudi Arabia" : Territory("Saudi Arabia", 0, 0), \
                # NEUTRAL ^
                "Sinkiang" : Territory("Sinkiang", 1, 0), \
                "Solomon Islands" : Territory("Solomon Islands", 0, 0), \
                "Southern Europe" : Territory("Southern Europe", 2, 0), \
                "Soviet Far East" : Territory("Soviet Far East", 1, 0), \
                "Spain Portugal" : Territory("Spain Portugal", 0, 0), \
                # NEUTRAL ^
                "Sweden" : Territory("Sweden", 0, 0), \
                # NEUTRAL ^
                "Switzerland" : Territory("Switzerland", 0, 0), \
                # NEUTRAL ^
                "Szechwan" : Territory("Szechwan", 1, 0), \
                "Trans-Jordan" : Territory("Trans-Jordan", 1, 0), \
                "Turkey" : Territory("Turkey", 0, 0), \
                # NEUTRAL ^
                "Ukraine S.S.R." : Territory("Ukraine S.S.R.", 2, 0), \
                "Union of South Africa" : Territory("Union of South Africa", 2, 0), \
                "United Kingdom" : Territory("United Kingdom", 8, 0), \
                "Venezuela" : Territory("Venezuela", 0, 0), \
                # NEUTRAL ^
                "Vologda" : Territory("Vologda", 2, 0), \
                "Wake Island" : Territory("Wake Island", 0, 0), \
                "West Indies" : Territory("West Indies", 1, 0), \
                "West Russia" : Territory("West Russia", 2, 0), \
                "Western Australia" : Territory("Western Australia", 1, 0), \
                "Western Canada" : Territory("Western Canada", 1, 0), \
                "Western United States" : Territory("Western United States", 10, 0), \
                "Yakut S.S.R." : Territory("Yakut S.S.R.", 1, 0), \
                "Yunnan" : Territory("Yunnan", 1, 0) }
                
                
                #Connections List to be used to make neighbors 
                
                self.connections = [("1 Sea Zone", "2 Sea Zone"), \
                ("1 Sea Zone", "10 Sea Zone"), \
                ("1 Sea Zone", "Eastern Canada"), \
                ("2 Sea Zone", "3 Sea Zone"), \
                ("2 Sea Zone", "9 Sea Zone"), \
                ("2 Sea Zone", "7 Sea Zone"), \
                ("2 Sea Zone", "10 Sea Zone"), \
                ("2 Sea Zone", "Greenland"), \
                ("3 Sea Zone", "6 Sea Zone"), \
                ("3 Sea Zone", "Norway"), \
                ("3 Sea Zone", "Finland"), \
                ("3 Sea Zone", "7 Sea Zone"), \
                ("3 Sea Zone", "4 Sea Zone"), \
                ("3 Sea Zone", "Iceland"), \
                ("4 Sea Zone", "Archangel"), \
                ("4 Sea Zone", "Karelia S.S.R."), \
                ("5 Sea Zone", "6 Sea Zone"), \
                ("5 Sea Zone", "Northwestern Europe"), \
                ("5 Sea Zone", "Sweden"), \
                ("5 Sea Zone", "Norway"), \
                ("5 Sea Zone", "Finland"), \
                ("5 Sea Zone", "Karelia S.S.R."), \
                ("5 Sea Zone", "Baltic States"), \
                ("5 Sea Zone", "Germany"), \
                ("6 Sea Zone", "Northwestern Europe"), \
                ("6 Sea Zone", "Norway"), \
                ("6 Sea Zone", "7 Sea Zone"), \
                ("6 Sea Zone", "United Kingdom"), \
                ("6 Sea Zone", "8 Sea Zone"), \
                ("7 Sea Zone", "9 Sea Zone"), \
                ("7 Sea Zone", "Eire"), \
                ("7 Sea Zone", "United Kingdom"), \
                ("7 Sea Zone", "8 Sea Zone"), \
                ("8 Sea Zone", "Northwestern Europe"), \
                ("8 Sea Zone", "9 Sea Zone"), \
                ("8 Sea Zone", "Eire"), \
                ("8 Sea Zone", "United Kingdom"), \
                ("8 Sea Zone", "13 Sea Zone"), \
                ("8 Sea Zone", "France"), \
                ("9 Sea Zone", "12 Sea Zone"), \
                ("9 Sea Zone", "13 Sea Zone"), \
                ("9 Sea Zone", "10 Sea Zone"), \
                ("10 Sea Zone", "11 Sea Zone"), \
                ("10 Sea Zone", "12 Sea Zone"), \
                ("10 Sea Zone", "Eastern Canada"), \
                ("11 Sea Zone", "Central United States"), \
                ("11 Sea Zone", "Eastern United States"), \
                ("11 Sea Zone", "18 Sea Zone"), \
                ("11 Sea Zone", "12 Sea Zone"), \
                ("11 Sea Zone", "East Mexico"), \
                ("12 Sea Zone", "22 Sea Zone"), \
                ("12 Sea Zone", "23 Sea Zone"), \
                ("12 Sea Zone", "18 Sea Zone"), \
                ("12 Sea Zone", "13 Sea Zone"), \
                ("13 Sea Zone", "14 Sea Zone"), \
                ("13 Sea Zone", "Gibraltar"), \
                ("13 Sea Zone", "Morocco"), \
                ("13 Sea Zone", "23 Sea Zone"), \
                ("13 Sea Zone", "Spain Portugal"), \
                ("14 Sea Zone", "Gibraltar"), \
                ("14 Sea Zone", "Morocco"), \
                ("14 Sea Zone", "15 Sea Zone"), \
                ("14 Sea Zone", "Algeria"), \
                ("14 Sea Zone", "France"), \
                ("14 Sea Zone", "Spain Portugal"), \
                ("15 Sea Zone", "17 Sea Zone"), \
                ("15 Sea Zone", "Turkey"), \
                ("15 Sea Zone", "16 Sea Zone"), \
                ("15 Sea Zone", "Italy"), \
                ("15 Sea Zone", "Southern Europe"), \
                ("15 Sea Zone", "Libya"), \
                ("16 Sea Zone", "Bulgaria Romania"), \
                ("16 Sea Zone", "Turkey"), \
                ("16 Sea Zone", "Ukraine S.S.R."), \
                ("16 Sea Zone", "Caucasus"), \
                ("17 Sea Zone", "Turkey"), \
                ("17 Sea Zone", "Egypt"), \
                ("17 Sea Zone", "Trans-Jordan"), \
                ("17 Sea Zone", "34 Sea Zone"), \
                ("18 Sea Zone", "Central America"), \
                ("18 Sea Zone", "Venezuela"), \
                ("18 Sea Zone", "22 Sea Zone"), \
                ("18 Sea Zone", "West Indies"), \
                ("18 Sea Zone", "Colombia Equador"), \
                ("18 Sea Zone", "East Mexico"), \
                ("18 Sea Zone", "19 Sea Zone"), \
                ("19 Sea Zone", "Central America"), \
                ("19 Sea Zone", "20 Sea Zone"), \
                ("19 Sea Zone", "55 Sea Zone"), \
                ("19 Sea Zone", "Colombia Equador"), \
                ("19 Sea Zone", "East Mexico"), \
                ("19 Sea Zone", "Peru Argentina"), \
                ("20 Sea Zone", "42 Sea Zone"), \
                ("20 Sea Zone", "Chile"), \
                ("20 Sea Zone", "21 Sea Zone"), \
                ("21 Sea Zone", "22 Sea Zone"), \
                ("21 Sea Zone", "26 Sea Zone"), \
                ("21 Sea Zone", "Peru Argentina"), \
                ("21 Sea Zone", "41 Sea Zone"), \
                ("21 Sea Zone", "Chile"), \
                ("21 Sea Zone", "25 Sea Zone"), \
                ("22 Sea Zone", "23 Sea Zone"), \
                ("22 Sea Zone", "Brazil"), \
                ("22 Sea Zone", "25 Sea Zone"), \
                ("23 Sea Zone", "24 Sea Zone"), \
                ("23 Sea Zone", "French West Africa"), \
                ("23 Sea Zone", "25 Sea Zone"), \
                ("23 Sea Zone", "Sahara"), \
                ("24 Sea Zone", "27 Sea Zone"), \
                ("24 Sea Zone", "Belgian Congo"), \
                ("24 Sea Zone", "French Equatorial Africa"), \
                ("24 Sea Zone", "25 Sea Zone"), \
                ("25 Sea Zone", "27 Sea Zone"), \
                ("25 Sea Zone", "26 Sea Zone"), \
                ("26 Sea Zone", "27 Sea Zone"), \
                ("27 Sea Zone", "28 Sea Zone"), \
                ("27 Sea Zone", "Angola"), \
                ("27 Sea Zone", "Union of South Africa"), \
                ("28 Sea Zone", "Mozambique"), \
                ("28 Sea Zone", "Union of South Africa"), \
                ("28 Sea Zone", "33 Sea Zone"), \
                ("28 Sea Zone", "29 Sea Zone"), \
                ("28 Sea Zone", "French Madagascar"), \
                ("29 Sea Zone", "31 Sea Zone"), \
                ("29 Sea Zone", "French Madagascar"), \
                ("29 Sea Zone", "30 Sea Zone"), \
                ("29 Sea Zone", "32 Sea Zone"), \
                ("30 Sea Zone", "38 Sea Zone"), \
                ("30 Sea Zone", "37 Sea Zone"), \
                ("30 Sea Zone", "31 Sea Zone"), \
                ("31 Sea Zone", "37 Sea Zone"), \
                ("31 Sea Zone", "35 Sea Zone"), \
                ("31 Sea Zone", "32 Sea Zone"), \
                ("32 Sea Zone", "33 Sea Zone"), \
                ("32 Sea Zone", "35 Sea Zone"), \
                ("32 Sea Zone", "French Madagascar"), \
                ("32 Sea Zone", "34 Sea Zone"), \
                ("33 Sea Zone", "Rhodesia"), \
                ("33 Sea Zone", "Mozambique"), \
                ("33 Sea Zone", "French Madagascar"), \
                ("33 Sea Zone", "34 Sea Zone"), \
                ("33 Sea Zone", "Italian East Africa"), \
                ("34 Sea Zone", "Saudi Arabia"), \
                ("34 Sea Zone", "Anglo-Egyptian Sudan"), \
                ("34 Sea Zone", "Persia"), \
                ("34 Sea Zone", "35 Sea Zone"), \
                ("34 Sea Zone", "Egypt"), \
                ("34 Sea Zone", "Trans-Jordan"), \
                ("34 Sea Zone", "Italian East Africa"), \
                ("35 Sea Zone", "37 Sea Zone"), \
                ("35 Sea Zone", "36 Sea Zone"), \
                ("35 Sea Zone", "India"), \
                ("36 Sea Zone", "French Indo-China Thailand"), \
                ("36 Sea Zone", "48 Sea Zone"), \
                ("36 Sea Zone", "37 Sea Zone"), \
                ("36 Sea Zone", "61 Sea Zone"), \
                ("36 Sea Zone", "Burma"), \
                ("36 Sea Zone", "47 Sea Zone"), \
                ("36 Sea Zone", "Malaya"), \
                ("37 Sea Zone", "38 Sea Zone"), \
                ("37 Sea Zone", "46 Sea Zone"), \
                ("37 Sea Zone", "47 Sea Zone"), \
                ("37 Sea Zone", "East Indies"), \
                ("38 Sea Zone", "46 Sea Zone"), \
                ("38 Sea Zone", "Western Australia"), \
                ("38 Sea Zone", "39 Sea Zone"), \
                ("39 Sea Zone", "40 Sea Zone"), \
                ("39 Sea Zone", "45 Sea Zone"), \
                ("39 Sea Zone", "Eastern Australia"), \
                ("40 Sea Zone", "43 Sea Zone"), \
                ("40 Sea Zone", "New Zealand"), \
                ("40 Sea Zone", "44 Sea Zone"), \
                ("40 Sea Zone", "41 Sea Zone"), \
                ("40 Sea Zone", "45 Sea Zone"), \
                ("41 Sea Zone", "43 Sea Zone"), \
                ("41 Sea Zone", "42 Sea Zone"), \
                ("42 Sea Zone", "43 Sea Zone"), \
                ("42 Sea Zone", "54 Sea Zone"), \
                ("42 Sea Zone", "55 Sea Zone"), \
                ("43 Sea Zone", "54 Sea Zone"), \
                ("43 Sea Zone", "44 Sea Zone"), \
                ("43 Sea Zone", "53 Sea Zone"), \
                ("44 Sea Zone", "50 Sea Zone"), \
                ("44 Sea Zone", "52 Sea Zone"), \
                ("44 Sea Zone", "45 Sea Zone"), \
                ("44 Sea Zone", "53 Sea Zone"), \
                ("44 Sea Zone", "49 Sea Zone"), \
                ("44 Sea Zone", "Solomon Islands"), \
                ("45 Sea Zone", "46 Sea Zone"), \
                ("45 Sea Zone", "49 Sea Zone"), \
                ("45 Sea Zone", "Eastern Australia"), \
                ("46 Sea Zone", "Western Australia"), \
                ("46 Sea Zone", "47 Sea Zone"), \
                ("46 Sea Zone", "49 Sea Zone"), \
                ("47 Sea Zone", "Borneo"), \
                ("47 Sea Zone", "48 Sea Zone"), \
                ("47 Sea Zone", "49 Sea Zone"), \
                ("48 Sea Zone", "51 Sea Zone"), \
                ("48 Sea Zone", "50 Sea Zone"), \
                ("48 Sea Zone", "Philippine Islands"), \
                ("48 Sea Zone", "61 Sea Zone"), \
                ("48 Sea Zone", "60 Sea Zone"), \
                ("48 Sea Zone", "49 Sea Zone"), \
                ("49 Sea Zone", "New Guinea"), \
                ("49 Sea Zone", "50 Sea Zone"), \
                ("50 Sea Zone", "51 Sea Zone"), \
                ("50 Sea Zone", "Caroline Islands"), \
                ("50 Sea Zone", "52 Sea Zone"), \
                ("51 Sea Zone", "59 Sea Zone"), \
                ("51 Sea Zone", "Okinawa"), \
                ("51 Sea Zone", "60 Sea Zone"), \
                ("51 Sea Zone", "52 Sea Zone"), \
                ("52 Sea Zone", "59 Sea Zone"), \
                ("52 Sea Zone", "57 Sea Zone"), \
                ("52 Sea Zone", "53 Sea Zone"), \
                ("52 Sea Zone", "Wake Island"), \
                ("53 Sea Zone", "54 Sea Zone"), \
                ("53 Sea Zone", "56 Sea Zone"), \
                ("53 Sea Zone", "57 Sea Zone"), \
                ("53 Sea Zone", "Hawaiian Islands"), \
                ("54 Sea Zone", "56 Sea Zone"), \
                ("54 Sea Zone", "55 Sea Zone"), \
                ("55 Sea Zone", "56 Sea Zone"), \
                ("55 Sea Zone", "Mexico"), \
                ("56 Sea Zone", "57 Sea Zone"), \
                ("56 Sea Zone", "65 Sea Zone"), \
                ("56 Sea Zone", "Western United States"), \
                ("57 Sea Zone", "59 Sea Zone"), \
                ("57 Sea Zone", "65 Sea Zone"), \
                ("57 Sea Zone", "58 Sea Zone"), \
                ("57 Sea Zone", "Midway"), \
                ("57 Sea Zone", "64 Sea Zone"), \
                ("58 Sea Zone", "59 Sea Zone"), \
                ("58 Sea Zone", "63 Sea Zone"), \
                ("58 Sea Zone", "60 Sea Zone"), \
                ("58 Sea Zone", "64 Sea Zone"), \
                ("59 Sea Zone", "60 Sea Zone"), \
                ("59 Sea Zone", "Iwo Jima"), \
                ("60 Sea Zone", "61 Sea Zone"), \
                ("60 Sea Zone", "Japan"), \
                ("60 Sea Zone", "63 Sea Zone"), \
                ("60 Sea Zone", "62 Sea Zone"), \
                ("61 Sea Zone", "Kwangtung"), \
                ("61 Sea Zone", "Kiangsu"), \
                ("61 Sea Zone", "Yunnan"), \
                ("61 Sea Zone", "Formosa"), \
                ("61 Sea Zone", "62 Sea Zone"), \
                ("62 Sea Zone", "Manchuria"), \
                ("62 Sea Zone", "Buryatia S.S.R."), \
                ("62 Sea Zone", "Japan"), \
                ("62 Sea Zone", "63 Sea Zone"), \
                ("63 Sea Zone", "Soviet Far East"), \
                ("63 Sea Zone", "Buryatia S.S.R."), \
                ("63 Sea Zone", "64 Sea Zone"), \
                ("64 Sea Zone", "65 Sea Zone"), \
                ("64 Sea Zone", "Alaska"), \
                ("65 Sea Zone", "Western Canada"), \
                ("65 Sea Zone", "Alaska"), \
                ("Afghanistan", "Persia"), \
                ("Afghanistan", "Szechwan"), \
                ("Afghanistan", "Kazakh S.S.R."), \
                ("Afghanistan", "Himalaya"), \
                ("Afghanistan", "India"), \
                ("Alaska", "Western Canada"), \
                ("Algeria", "Morocco"), \
                ("Algeria", "Libya"), \
                ("Algeria", "Sahara"), \
                ("Anglo-Egyptian Sudan", "Rhodesia"), \
                ("Anglo-Egyptian Sudan", "Belgian Congo"), \
                ("Anglo-Egyptian Sudan", "Egypt"), \
                ("Anglo-Egyptian Sudan", "French Equatorial Africa"), \
                ("Anglo-Egyptian Sudan", "Italian East Africa"), \
                ("Anglo-Egyptian Sudan", "Sahara"), \
                ("Angola", "Union of South Africa"), \
                ("Angola", "Belgian Congo"), \
                ("Anhwei", "Manchuria"), \
                ("Anhwei", "Mongolia"), \
                ("Anhwei", "Kwangtung"), \
                ("Anhwei", "Kiangsu"), \
                ("Anhwei", "Szechwan"), \
                ("Anhwei", "Sinkiang"), \
                ("Archangel", "Evenki National Okrug"), \
                ("Archangel", "West Russia"), \
                ("Archangel", "Karelia S.S.R."), \
                ("Archangel", "Russia"), \
                ("Archangel", "Vologda"), \
                ("Baltic States", "Belorussia"), \
                ("Baltic States", "Poland"), \
                ("Baltic States", "Karelia S.S.R."), \
                ("Baltic States", "Germany"), \
                ("Belgian Congo", "Rhodesia"), \
                ("Belgian Congo", "Union of South Africa"), \
                ("Belgian Congo", "French Equatorial Africa"), \
                ("Belorussia", "Ukraine S.S.R."), \
                ("Belorussia", "Poland"), \
                ("Belorussia", "West Russia"), \
                ("Belorussia", "Karelia S.S.R."), \
                ("Brazil", "Venezuela"), \
                ("Brazil", "Colombia Equador"), \
                ("Brazil", "Peru Argentina"), \
                ("Bulgaria Romania", "Turkey"), \
                ("Bulgaria Romania", "Ukraine S.S.R."), \
                ("Bulgaria Romania", "Poland"), \
                ("Bulgaria Romania", "Southern Europe"), \
                ("Bulgaria Romania", "Germany"), \
                ("Burma", "French Indo-China Thailand"), \
                ("Burma", "Yunnan"), \
                ("Burma", "Himalaya"), \
                ("Burma", "India"), \
                ("Buryatia S.S.R.", "Manchuria"), \
                ("Buryatia S.S.R.", "Mongolia"), \
                ("Buryatia S.S.R.", "Soviet Far East"), \
                ("Buryatia S.S.R.", "Yakut S.S.R."), \
                ("Caucasus", "Turkey"), \
                ("Caucasus", "Persia"), \
                ("Caucasus", "Ukraine S.S.R."), \
                ("Caucasus", "Kazakh S.S.R."), \
                ("Caucasus", "West Russia"), \
                ("Caucasus", "Russia"), \
                ("Central America", "Colombia Equador"), \
                ("Central America", "East Mexico"), \
                ("Central United States", "Eastern United States"), \
                ("Central United States", "East Mexico"), \
                ("Central United States", "Western United States"), \
                ("Central United States", "Eastern Canada"), \
                ("Chile", "Peru Argentina"), \
                ("Colombia Equador", "Venezuela"), \
                ("Colombia Equador", "Peru Argentina"), \
                ("East Mexico", "Mexico"), \
                ("Eastern Australia", "Western Australia"), \
                ("Eastern Canada", "Eastern United States"), \
                ("Eastern Canada", "Western Canada"), \
                ("Egypt", "Trans-Jordan"), \
                ("Egypt", "Libya"), \
                ("Egypt", "Sahara"), \
                ("Eire", "United Kingdom"), \
                ("Evenki National Okrug", "Mongolia"), \
                ("Evenki National Okrug", "Yakut S.S.R."), \
                ("Evenki National Okrug", "Novosibirsk"), \
                ("Evenki National Okrug", "Sinkiang"), \
                ("Evenki National Okrug", "Vologda"), \
                ("Finland", "Sweden"), \
                ("Finland", "Norway"), \
                ("Finland", "Karelia S.S.R."), \
                ("France", "Northwestern Europe"), \
                ("France", "Italy"), \
                ("France", "Spain Portugal"), \
                ("France", "Switzerland"), \
                ("France", "Germany"), \
                ("French Equatorial Africa", "French West Africa"), \
                ("French Equatorial Africa", "Sahara"), \
                ("French Indo-China Thailand", "Yunnan"), \
                ("French Indo-China Thailand", "Malaya"), \
                ("French West Africa", "Sahara"), \
                ("Germany", "Northwestern Europe"), \
                ("Germany", "Poland"), \
                ("Germany", "Italy"), \
                ("Germany", "Southern Europe"), \
                ("Germany", "Switzerland"), \
                ("Gibraltar", "Spain Portugal"), \
                ("Himalaya", "Szechwan"), \
                ("Himalaya", "Yunnan"), \
                ("Himalaya", "India"), \
                ("India", "Persia"), \
                ("Italian East Africa", "Rhodesia"), \
                ("Italy", "Southern Europe"), \
                ("Italy", "Switzerland"), \
                ("Karelia S.S.R.", "West Russia"), \
                ("Kazakh S.S.R.", "Persia"), \
                ("Kazakh S.S.R.", "Szechwan"), \
                ("Kazakh S.S.R.", "Novosibirsk"), \
                ("Kazakh S.S.R.", "Sinkiang"), \
                ("Kazakh S.S.R.", "Russia"), \
                ("Kiangsu", "Manchuria"), \
                ("Kiangsu", "Kwangtung"), \
                ("Kwangtung", "Szechwan"), \
                ("Kwangtung", "Yunnan"), \
                ("Libya", "Sahara"), \
                ("Manchuria", "Mongolia"), \
                ("Mexico", "Western United States"), \
                ("Mongolia", "Yakut S.S.R."), \
                ("Mongolia", "Sinkiang"), \
                ("Morocco", "Sahara"), \
                ("Mozambique", "Rhodesia"), \
                ("Mozambique", "Union of South Africa"), \
                ("Norway", "Sweden"), \
                ("Novosibirsk", "Sinkiang"), \
                ("Novosibirsk", "Russia"), \
                ("Novosibirsk", "Vologda"), \
                ("Persia", "Turkey"), \
                ("Persia", "Trans-Jordan"), \
                ("Poland", "Ukraine S.S.R."), \
                ("Rhodesia", "Union of South Africa"), \
                ("Russia", "West Russia"), \
                ("Russia", "Vologda"), \
                ("Saudi Arabia", "Trans-Jordan"), \
                ("Sinkiang", "Szechwan"), \
                ("Southern Europe", "Turkey"), \
                ("Soviet Far East", "Yakut S.S.R."), \
                ("Szechwan", "Yunnan"), \
                ("Trans-Jordan", "Turkey"), \
                ("Ukraine S.S.R.", "West Russia"), \
                ("Western Canada", "Western United States")]
                
                for key in self.board:
                        for item in self.connections: 
                                if (key == item[0]):
                                        self.board[key].neighbors.append(item[1])
                                if (key == item[1]):
                                        self.board[key].neighbors.append(item[0])
                
                
                self.units = [Unit("infantry", "land", 3, 1, 2, 1), Unit("artillary", "land", 4, 1, 2, 1), \
                              Unit("tank", "land", 6, 1, 2, 1), Unit("aa", "land", 6, 0, 0, 1), \
                              Unit("factory", "land", 15, 0, 0, 0), Unit("transport", "sea", 7, 0, 0, 2, True), \
                              Unit("sub", "sea", 6, 2, 1, 2), Unit("destroyer", "sea", 8, 2, 2, 2), \
                              Unit("cruiser", "sea", 12, 3, 3, 2), Unit("carrier", "sea", 14, 1, 2, False, True), \
                              Unit("battleship", "sea", 20, 2, 1, 2), Unit("fighter", "10", 10, 3, 4, 4), \
                              Unit("bomber", "air", 12, 4, 1, 6)]
                              
        def get_unit(self, index):
                return self.units[index]
                
class Territory_state:
        """
        Object representing all fluid information about a territory
        """
        
        def __init__(self, territory_owner, unit_list = []):
                self.owner = territory_owner
        
                self.unit_state_list =  unit_list

class Unit_state:
        """
        Provides a basic template for a unit
        """
        
        def __init__(self, owner, type_number, moves_remaining, damage = 0):
                self.owner = owner
                self.type_index = type_number
                self.moves_remaining = moves_remaining
                self.damaged = damage
                
class Game:
        """
        IN PROGRESS. Trying to represent the game as a whole, including all static and fluid
        information (including turn phase and turn ownership -- not yet defined anywhere).
        Will want to be able to make changes as game progresses.
        """
                              
        #convery unit-state numbers to units using rules.get_unit.
                              
        def __init__(self):
                
                rules = Rules()
                
                #dictionary from territory names to territory states
                self.state_dict = {"1 Sea Zone" : Territory_State("Neutral", []), \
                "2 Sea Zone" : Territory_State("Neutral", []), \ 
                "3 Sea Zone" : Territory_State("Neutral", []), \
                "4 Sea Zone" : Territory_State("Neutral", []), \ 
                "5 Sea Zone" : Territory_State("Neutral", []), \
                "6 Sea Zone" : Territory_State("Neutral", []), \ 
                "7 Sea Zone" : Territory_State("Neutral", []), \
                "8 Sea Zone" : Territory_State("Neutral", []), \
                "9 Sea Zone" : Territory_State("Neutral", []), \ 
                "10 Sea Zone" : Territory_State("Neutral", []), \ 
                "11 Sea Zone" : Territory_State("Neutral", []), \ 
                "12 Sea Zone" : Territory_State("Neutral", []), \
                "13 Sea Zone" : Territory_State("Neutral", []), \ 
                "14 Sea Zone" : Territory_State("Neutral", []), \
                "15 Sea Zone" : Territory_State("Neutral", []), \ 
                "16 Sea Zone" : Territory_State("Neutral", []), \ 
                "17 Sea Zone" : Territory_State("Neutral", []), \ 
                "18 Sea Zone" : Territory_State("Neutral", []), \ 
                "19 Sea Zone" : Territory_State("Neutral", []), \ 
                "20 Sea one" : Territory_State("Neutral", []), \
                "21 Sea Zone" : Territory_State("Neutral", []), \
                "22 Sea Zone" : Territory_State("Neutral", []), \ 
                "23 Sea Zone" : Territory_State("Neutral", []), \ 
                "24 Sea Zone" : Territory_State("Neutral", []), \ 
                "25 Sea Zone" : Territory_State("Neutral", []), \
                "26 Sea Zone" : Territory_State("Neutral", []), \
                "27 Sea Zone" : Territory_State("Neutral", []), \
                "28 Sea Zone" : Territory_State("Neutral", []), \
                "29 Sea Zone" : Territory_State("Neutral", []), \
                "30 Sea Zone" : Territory_State("Neutral", []), \
                "31 Sea Zone" : Territory_State("Neutral", []), \
                "32 Sea Zone" : Territory_State("Neutral", []), \ 
                "33 Sea Zone" : Territory_State("Neutral", []), \ 
                "34 Sea Zone" : Territory_State("Neutral", []), \
                "35 Sea Zone" : Territory_State("Neutral", []), \ 
                "36 Sea Zone" : Territory_State("Neutral", []), \
                "37 Sea Zone" : Territory_State("Neutral", []), \ 
                "38 Sea Zone" : Territory_State("Neutral", []), \
                "39 Sea Zone" : Territory_State("Neutral", []), \
                "40 Sea Zone" : Territory_State("Neutral", []), \ 
                "41 Sea Zone" : Territory_State("Neutral", []), \ 
                "42 Sea Zone" : Territory_State("Neutral", []), \
                "43 Sea Zone" : Territory_State("Neutral", []), \
                "44 Sea Zone" : Territory_State("Neutral", []), \
                "45 Sea Zone" : Territory_State("Neutral", []), \
                "46 Sea Zone" : Territory_State("Neutral", []), \ 
                "47 Sea Zone" : Territory_State("Neutral", []), \
                "48 Sea Zone" : Territory_State("Neutral", []), \
                "49 Sea Zone" : Territory_State("Neutral", []), \
                "50 Sea Zone" : Territory_State("Neutral", []), \
                "51 Sea Zone" : Territory_State("Neutral", []), \
                "52 Sea Zone" : Territory_State("Neutral", []), \
                "53 Sea Zone" : Territory_State("Neutral", []), \
                "54 Sea Zone" : Territory_State("Neutral", []), \
                "55 Sea Zone" : Territory_State("Neutral", []), \
                "56 Sea Zone" : Territory_State("Neutral", []), \
                "57 Sea Zone" : Territory_State("Neutral", []), \
                "58 Sea Zone" : Territory_State("Neutral", []), \
                "59 Sea Zone" : Territory_State("Neutral", []), \
                "60 Sea Zone" : Territory_State("Neutral", []), \
                "61 Sea Zone" : Territory_State("Neutral", []), \
                "62 Sea Zone" : Territory_State("Neutral", []), \
                "63 Sea Zone" : Territory_State("Neutral", []), \
                "64 Sea Zone" : Territory_State("Neutral", []), \ 
                "65 Sea Zone" : Territory_State("Neutral", []), \
                "Afghanistan" : Territory_State("Neutral", []), \
                "Alaska" : Territory_State("Neutral", []), \
                "Algeria" : Territory_State("Neutral", []), \
                "Anglo-Egyptian Sudan" : Territory_State("Neutral", []), \
                "Angola" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Anhwei" : Territory_State("Neutral", []), \
                "Archangel" : Territory_State("Neutral", []), \
                "Baltic States" : Territory_State("Neutral", []), \
                "Belgian Congo" : Territory_State("Neutral", []), \
                "Belorussia" : Territory_State("Neutral", []), \
                "Borneo" : Territory_State("Neutral", []), \
                "Brazil" : Territory_State("Neutral", []), \
                "Bulgaria Romania" : Territory_State("Neutral", []), \
                "Burma" : Territory_State("Neutral", []), \
                "Buryatia S.S.R." : Territory_State("Neutral", []), \
                "Caroline Islands" : Territory_State("Neutral", []), \
                "Caucasus" : Territory_State("Neutral", []), \
                "Central America" : Territory_State("Neutral", []), \
                "Central United States" : Territory_State("Neutral", []), \
                "Chile" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Colombia Equador" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "East Indies" : Territory_State("Neutral", []), \ 
                "East Mexico" : Territory_State("Neutral", []), \
                "Eastern Australia" : Territory_State("Neutral", []), \
                "Eastern Canada" : Territory_State("Neutral", []), \
                "Eastern United States" : Territory_State("Neutral", []), \
                "Egypt" : Territory_State("Neutral", []), \
                "Eire" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Evenki National Okrug" : Territory_State("Neutral", []), \ 
                "Finland" : Territory_State("Neutral", []), \
                "Formosa" : Territory_State("Neutral", []), \
                "France" : Territory_State("Neutral", []), \
                "French Equatorial Africa" : Territory_State("Neutral", []), \
                "French Indo-China Thailand" : Territory_State("Neutral", []), \
                "French Madagascar" : Territory_State("Neutral", []), \
                "French West Africa" : Territory_State("Neutral", []), \
                "Germany" : Territory_State("Neutral", []), \
                "Gibraltar" : Territory_State("Neutral", []), \
                "Greenland" : Territory_State("Neutral", []), \
                "Hawaiian Islands" : Territory_State("Neutral", []), \
                "Himalaya" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Iceland" : Territory_State("Neutral", []), \
                "India" : Territory_State("Neutral", []), \
                "Italian East Africa" : Territory_State("Neutral", []), \
                "Italy" : Territory_State("Neutral", []), \
                "Iwo Jima" : Territory_State("Neutral", []), \
                "Japan" : Territory_State("Neutral", []), \
                "Karelia S.S.R." : Territory_State("Neutral", []), \
                "Kazakh S.S.R." : Territory_State("Neutral", []), \
                "Kiangsu" : Territory_State("Neutral", []), \
                "Kwangtung" : Territory_State("Neutral", []), \
                "Libya" : Territory_State("Neutral", []), \ 
                "Malaya" : Territory_State("Neutral", []), \
                "Manchuria" : Territory_State("Neutral", []), \
                "Mexico" : Territory_State("Neutral", []), \
                "Midway" : Territory_State("Neutral", []), \
                "Mongolia" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Morocco" : Territory_State("Neutral", []), \
                "Mozambique" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "New Guinea" : Territory_State("Neutral", []), \
                "New Zealand" : Territory_State("Neutral", []), \
                "Northwestern Europe" : Territory_State("Neutral", []), \
                "Norway" : Territory_State("Neutral", []), \
                "Novosibirsk" : Territory_State("Neutral", []), \
                "Okinawa" : Territory_State("Neutral", []), \
                "Persia" : Territory_State("Neutral", []), \
                "Peru Argentina" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Philippine Islands" : Territory_State("Neutral", []), \
                "Poland" : Territory_State("Neutral", []), \
                "Rhodesia" : Territory_State("Neutral", []), \
                "Russia" : Territory_State("Neutral", []), \
                "Sahara" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Saudi Arabia" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Sinkiang" : Territory_State("Neutral", []), \
                "Solomon Islands" : Territory_State("Neutral", []), \
                "Southern Europe" : Territory_State("Neutral", []), \
                "Soviet Far East" : Territory_State("Neutral", []), \
                "Spain Portugal" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Sweden" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Switzerland" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Szechwan" : Territory_State("Neutral", []), \
                "Trans-Jordan" : Territory_State("Neutral", []), \
                "Turkey" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Ukraine S.S.R." : Territory_State("Neutral", []), \
                "Union of South Africa" : Territory_State("Neutral", []), \
                "United Kingdom" : Territory_State("Neutral", []), \
                "Venezuela" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Vologda" : Territory_State("Neutral", []), \
                "Wake Island" : Territory_State("Neutral", []), \
                "West Indies" : Territory_State("Neutral", []), \
                "West Russia" : Territory_State("Neutral", []), \
                "Western Australia" : Territory_State("Neutral", []), \
                "Western Canada" : Territory_State("Neutral", []), \
                "Western United States" : Territory_State("Neutral", []), \ 
                "Yakut S.S.R." : Territory_State("Neutral", []),
                "Yunnan" : Territory_State("Neutral", [])  }


#ADD IN TERRITORY OWNERSHIP AND ACCOUNT FOR IT IN THE PASSABLE FUNCTION
# neutrals cant move to, and enemy must be during combat phase. Tanks end all movement if battle
# check phase

def passable(unit, current_territory, goal_territory):
        """
        a function that will check if a theoretical move is valid.
        """
                            
        if (unit.unit_type == "land"):
                if (goal_territory.is_water == 0 and (goal_territory.name in current_territory.neighbors)):
                        return True
                else:
                        return False
        elif (unit.unit_type == "sea"):
                if (goal_territory.is_water == 1 and (goal_territory.name in current_territory.neighbors)):
                        return True
                else:
                        return False
        elif (unit.unit_type == "air"):
                if (goal_territory.is_water == 0 and (goal_territory.name in current_territory.neighbors)):
                        return True                
        


# classic pathfinding = dijkstra search or A*

# Make a distance function

# Is_Reachable

     # Make an Is_ land_reachable function

     # Is_sea_reachable

     # Plane_has_retreat

     # Controls strait.
     
# Find a way to impliment the battle calculator

# Is_bordering_enemy

# Is_threatened by enemy

        """
        Provides a basic template for a unit
        """
        
        # movement ability
        # attack defense
        # transport capacity

        def __init__(self, unit_name, unit_type, cost, attack, defense, movement, transport = False, carrier = False):
                self.name = unit_name
                
                self.unit_type = unit_type
                self.cost = cost
                
                self.attack = attack
                self.defense = defense
                self.movement = movement
                
                self.is_transport = transport
                # FIGURE OUT HOW TO REPRESENT FULL TRANSPORTS. IS THE UNIT DIRECTLY ATTACHED?
                self.is_carrier = carrier
        
        
class Rules:
        """
        Contains static game data: a board representing territories, assignment of neighbors 
        for each territory (which is contained within a dictionary from string to
        territory), and prototypes for units.
        """
        
        # defines all the prototypes for units. definitions
        # also says all territorries and how they are conneted.
        # if has __ tech, attack ++
        # rules.get_unit_type (tank)
        
        def __init__(self):
                self.board = {"1 Sea Zone" : Territory("1 Sea Zone", 0, 1), \
                "2 Sea Zone" : Territory("2 Sea Zone", 0, 1), \
                "3 Sea Zone" : Territory("2 Sea Zone", 0, 1), \
                "4 Sea Zone" : Territory("4 Sea Zone", 0, 1), \
                "5 Sea Zone" : Territory("5 Sea Zone", 0, 1), \
                "6 Sea Zone" : Territory("6 Sea Zone", 0, 1), \
                "7 Sea Zone" : Territory("7 Sea Zone", 0, 1), \
                "8 Sea Zone" : Territory("8 Sea Zone", 0, 1), \
                "9 Sea Zone" : Territory("9 Sea Zone", 0, 1), \
                "10 Sea Zone" : Territory("10 Sea Zone", 0, 1), \
                "11 Sea Zone" : Territory("11 Sea Zone", 0, 1), \
                "12 Sea Zone" : Territory("12 Sea Zone", 0, 1), \
                "13 Sea Zone" : Territory("13 Sea Zone", 0, 1), \
                "14 Sea Zone" : Territory("14 Sea Zone", 0, 1), \
                "15 Sea Zone" : Territory("15 Sea Zone", 0, 1), \
                "16 Sea Zone" : Territory("16 Sea Zone", 0, 1), \
                "17 Sea Zone" : Territory("17 Sea Zone", 0, 1), \
                "18 Sea Zone" : Territory("18 Sea Zone", 0, 1), \
                "19 Sea Zone" : Territory("19 Sea Zone", 0, 1), \
                "20 Sea one" : Territory("20 Sea Zone", 0, 1), \
                "21 Sea Zone" : Territory("21 Sea Zone", 0, 1), \
                "22 Sea Zone" : Territory("22 Sea Zone", 0, 1), \
                "23 Sea Zone" : Territory("23 Sea Zone", 0, 1), \
                "24 Sea Zone" : Territory("24 Sea Zone", 0, 1), \
                "25 Sea Zone" : Territory("25 Sea Zone", 0, 1), \
                "26 Sea Zone" : Territory("26 Sea Zone", 0, 1), \
                "27 Sea Zone" : Territory("27 Sea Zone", 0, 1), \
                "28 Sea Zone" : Territory("28 Sea Zone", 0, 1), \
                "29 Sea Zone" : Territory("29 Sea Zone", 0, 1), \
                "30 Sea Zone" : Territory("30 Sea Zone", 0, 1), \
                "31 Sea Zone" : Territory("31 Sea Zone", 0, 1), \
                "32 Sea Zone" : Territory("32 Sea Zone", 0, 1), \
                "33 Sea Zone" : Territory("33 Sea Zone", 0, 1), \
                "34 Sea Zone" : Territory("34 Sea Zone", 0, 1), \
                "35 Sea Zone" : Territory("35 Sea Zone", 0, 1), \
                "36 Sea Zone" : Territory("36 Sea Zone", 0, 1), \
                "37 Sea Zone" : Territory("37 Sea Zone", 0, 1), \
                "38 Sea Zone" : Territory("38 Sea Zone", 0, 1), \
                "39 Sea Zone" : Territory("39 Sea Zone", 0, 1), \
                "40 Sea Zone" : Territory("40 Sea Zone", 0, 1), \
                "41 Sea Zone" : Territory("41 Sea Zone", 0, 1), \
                "42 Sea Zone" : Territory("42 Sea Zone", 0, 1), \
                "43 Sea Zone" : Territory("43 Sea Zone", 0, 1), \
                "44 Sea Zone" : Territory("44 Sea Zone", 0, 1), \
                "45 Sea Zone" : Territory("45 Sea Zone", 0, 1), \
                "46 Sea Zone" : Territory("46 Sea Zone", 0, 1), \
                "47 Sea Zone" : Territory("47 Sea Zone", 0, 1), \
                "48 Sea Zone" : Territory("48 Sea Zone", 0, 1), \
                "49 Sea Zone" : Territory("49 Sea Zone", 0, 1), \
                "50 Sea Zone" : Territory("50 Sea Zone", 0, 1), \
                "51 Sea Zone" : Territory("51 Sea Zone", 0, 1), \
                "52 Sea Zone" : Territory("52 Sea Zone", 0, 1), \
                "53 Sea Zone" : Territory("53 Sea Zone", 0, 1), \
                "54 Sea Zone" : Territory("54 Sea Zone", 0, 1), \
                "55 Sea Zone" : Territory("55 Sea Zone", 0, 1), \
                "56 Sea Zone" : Territory("56 Sea Zone", 0, 1), \
                "57 Sea Zone" : Territory("57 Sea Zone", 0, 1), \
                "58 Sea Zone" : Territory("58 Sea Zone", 0, 1), \
                "59 Sea Zone" : Territory("59 Sea Zone", 0, 1), \
                "60 Sea Zone" : Territory("60 Sea Zone", 0, 1), \
                "61 Sea Zone" : Territory("61 Sea Zone", 0, 1), \
                "62 Sea Zone" : Territory("62 Sea Zone", 0, 1), \
                "63 Sea Zone" : Territory("63 Sea Zone", 0, 1), \
                "64 Sea Zone" : Territory("64 Sea Zone", 0, 1), \
                "65 Sea Zone" : Territory("65 Sea Zone", 0, 1), \
                "Afghanistan" : Territory("Afghanistan", 1, 0), \
                "Alaska" : Territory("Alaska", 2, 0), \
                "Algeria" : Territory("Algeria", 1, 0), \
                "Anglo-Egyptian Sudan" : Territory("Anglo-Egyptian Sudan", 0, 0), \
                "Angola" : Territory("Angola", 0, 0), \
                # NEUTRAL ^
                "Anhwei" : Territory("Anhwei", 1, 0), \
                "Archangel" : Territory("Archangel", 1, 0), \
                "Baltic States" : Territory("Baltic States", 2, 0), \
                "Belgian Congo" : Territory("Belgian Congo", 1, 0), \
                "Belorussia" : Territory("Belorussia", 2, 0), \
                "Borneo" : Territory("Borneo", 4, 0), \
                "Brazil" : Territory("Brazil", 3, 0), \
                "Bulgaria Romania" : Territory("Bulgaria Romania", 2, 0), \
                "Burma" : Territory("Burma", 1, 0), \
                "Buryatia S.S.R." : Territory("Buryatia S.S.R.", 1, 0), \
                "Caroline Islands" : Territory("Caroline Islands", 0, 0), \
                "Caucasus" : Territory("Caucasus", 4, 0), \
                "Central America" : Territory("Central America", 1, 0), \
                "Central United States" : Territory("Central United States", 6, 0), \
                "Chile" : Territory("Chile", 0, 0), \
                # NEUTRAL ^
                "Colombia Equador" : Territory("Colombia Equador", 0, 0), \
                # NEUTRAL ^
                "East Indies" : Territory("East Indies", 4, 0), \
                "East Mexico" : Territory("East Mexico", 0, 0), \
                "Eastern Australia" : Territory("Eastern Australia", 1, 0), \
                "Eastern Canada" : Territory("Eastern Canada", 3, 0), \
                "Eastern United States" : Territory("Eastern United States", 12, 0), \
                "Egypt" : Territory("Egypt", 2, 0), \
                "Eire" : Territory("Eire", 0, 0), \
                # NEUTRAL ^
                "Evenki National Okrug" : Territory("Evenki National Okrug", 1, 0), \
                "Finland" : Territory("Finland", 1, 0), \
                "Formosa" : Territory("Formosa", 0, 0), \
                "France" : Territory("France", 6, 0), \
                "French Equatorial Africa" : Territory("French Equatorial Africa", 1, 0), \
                "French Indo-China Thailand" : Territory("French Indo-China Thailand", 2, 0), \
                "French Madagascar" : Territory("French Madagascar", 1, 0), \
                "French West Africa" : Territory("French West Africa", 1, 0), \
                "Germany" : Territory("Germany", 10, 0), \
                "Gibraltar" : Territory("Gibraltar", 0, 0), \
                "Greenland" : Territory("Greenland", 0, 0), \
                "Hawaiian Islands" : Territory("Hawaiian Islands", 1, 0), \
                "Himalaya" : Territory("Himalaya", 0, 0), \
                # NEUTRAL ^
                "Iceland" : Territory("Iceland", 0, 0), \
                "India" : Territory("India", 3, 0), \
                "Italian East Africa" : Territory("Italian East Africa", 1, 0), \
                "Italy" : Territory("Italy", 3, 0), \
                "Iwo Jima" : Territory("Iwo Jima", 0, 0), \
                "Japan" : Territory("Japan", 8, 0), \
                "Karelia S.S.R." : Territory("Karelia S.S.R.", 2, 0), \
                "Kazakh S.S.R." : Territory("Kazakh S.S.R.", 2, 0), \
                "Kiangsu" : Territory("Kiangsu", 2, 0), \
                "Kwangtung" : Territory("Kwangtung", 2, 0), \
                "Libya" : Territory("Libya", 1, 0), \
                "Malaya" : Territory("Malaya", 1, 0), \
                "Manchuria" : Territory("Manchuria", 3, 0), \
                "Mexico" : Territory("Mexico", 2, 0), \
                "Midway" : Territory("Midway", 0, 0), \
                "Mongolia" : Territory("Mongolia", 0, 0), \
                # NEUTRAL ^
                "Morocco" : Territory("Morocco", 1, 0), \
                "Mozambique" : Territory("Mozambique", 0, 0), \
                # NEUTRAL ^
                "New Guinea" : Territory("New Guinea", 1, 0), \
                "New Zealand" : Territory("New Zealand", 1, 0), \
                "Northwestern Europe" : Territory("Northwestern Europe", 2, 0), \
                "Norway" : Territory("Norway", 2, 0), \
                "Novosibirsk" : Territory("Novosibirsk", 1, 0), \
                "Okinawa" : Territory("Okinawa", 0, 0), \
                "Persia" : Territory("Persia", 1, 0), \
                "Peru Argentina" : Territory("Peru Argentina", 0, 0), \
                # NEUTRAL ^
                "Philippine Islands" : Territory("Philippine Islands", 3, 0), \
                "Poland" : Territory("Poland", 2, 0), \
                "Rhodesia" : Territory("Rhodesia", 1, 0), \
                "Russia" : Territory("Russia", 8, 0), \
                "Sahara" : Territory("Sahara", 0, 0), \
                # NEUTRAL ^
                "Saudi Arabia" : Territory("Saudi Arabia", 0, 0), \
                # NEUTRAL ^
                "Sinkiang" : Territory("Sinkiang", 1, 0), \
                "Solomon Islands" : Territory("Solomon Islands", 0, 0), \
                "Southern Europe" : Territory("Southern Europe", 2, 0), \
                "Soviet Far East" : Territory("Soviet Far East", 1, 0), \
                "Spain Portugal" : Territory("Spain Portugal", 0, 0), \
                # NEUTRAL ^
                "Sweden" : Territory("Sweden", 0, 0), \
                # NEUTRAL ^
                "Switzerland" : Territory("Switzerland", 0, 0), \
                # NEUTRAL ^
                "Szechwan" : Territory("Szechwan", 1, 0), \
                "Trans-Jordan" : Territory("Trans-Jordan", 1, 0), \
                "Turkey" : Territory("Turkey", 0, 0), \
                # NEUTRAL ^
                "Ukraine S.S.R." : Territory("Ukraine S.S.R.", 2, 0), \
                "Union of South Africa" : Territory("Union of South Africa", 2, 0), \
                "United Kingdom" : Territory("United Kingdom", 8, 0), \
                "Venezuela" : Territory("Venezuela", 0, 0), \
                # NEUTRAL ^
                "Vologda" : Territory("Vologda", 2, 0), \
                "Wake Island" : Territory("Wake Island", 0, 0), \
                "West Indies" : Territory("West Indies", 1, 0), \
                "West Russia" : Territory("West Russia", 2, 0), \
                "Western Australia" : Territory("Western Australia", 1, 0), \
                "Western Canada" : Territory("Western Canada", 1, 0), \
                "Western United States" : Territory("Western United States", 10, 0), \
                "Yakut S.S.R." : Territory("Yakut S.S.R.", 1, 0), \
                "Yunnan" : Territory("Yunnan", 1, 0) }
                
                
                #Connections List to be used to make neighbors 
                
                self.connections = [("1 Sea Zone", "2 Sea Zone"), \
                ("1 Sea Zone", "10 Sea Zone"), \
                ("1 Sea Zone", "Eastern Canada"), \
                ("2 Sea Zone", "3 Sea Zone"), \
                ("2 Sea Zone", "9 Sea Zone"), \
                ("2 Sea Zone", "7 Sea Zone"), \
                ("2 Sea Zone", "10 Sea Zone"), \
                ("2 Sea Zone", "Greenland"), \
                ("3 Sea Zone", "6 Sea Zone"), \
                ("3 Sea Zone", "Norway"), \
                ("3 Sea Zone", "Finland"), \
                ("3 Sea Zone", "7 Sea Zone"), \
                ("3 Sea Zone", "4 Sea Zone"), \
                ("3 Sea Zone", "Iceland"), \
                ("4 Sea Zone", "Archangel"), \
                ("4 Sea Zone", "Karelia S.S.R."), \
                ("5 Sea Zone", "6 Sea Zone"), \
                ("5 Sea Zone", "Northwestern Europe"), \
                ("5 Sea Zone", "Sweden"), \
                ("5 Sea Zone", "Norway"), \
                ("5 Sea Zone", "Finland"), \
                ("5 Sea Zone", "Karelia S.S.R."), \
                ("5 Sea Zone", "Baltic States"), \
                ("5 Sea Zone", "Germany"), \
                ("6 Sea Zone", "Northwestern Europe"), \
                ("6 Sea Zone", "Norway"), \
                ("6 Sea Zone", "7 Sea Zone"), \
                ("6 Sea Zone", "United Kingdom"), \
                ("6 Sea Zone", "8 Sea Zone"), \
                ("7 Sea Zone", "9 Sea Zone"), \
                ("7 Sea Zone", "Eire"), \
                ("7 Sea Zone", "United Kingdom"), \
                ("7 Sea Zone", "8 Sea Zone"), \
                ("8 Sea Zone", "Northwestern Europe"), \
                ("8 Sea Zone", "9 Sea Zone"), \
                ("8 Sea Zone", "Eire"), \
                ("8 Sea Zone", "United Kingdom"), \
                ("8 Sea Zone", "13 Sea Zone"), \
                ("8 Sea Zone", "France"), \
                ("9 Sea Zone", "12 Sea Zone"), \
                ("9 Sea Zone", "13 Sea Zone"), \
                ("9 Sea Zone", "10 Sea Zone"), \
                ("10 Sea Zone", "11 Sea Zone"), \
                ("10 Sea Zone", "12 Sea Zone"), \
                ("10 Sea Zone", "Eastern Canada"), \
                ("11 Sea Zone", "Central United States"), \
                ("11 Sea Zone", "Eastern United States"), \
                ("11 Sea Zone", "18 Sea Zone"), \
                ("11 Sea Zone", "12 Sea Zone"), \
                ("11 Sea Zone", "East Mexico"), \
                ("12 Sea Zone", "22 Sea Zone"), \
                ("12 Sea Zone", "23 Sea Zone"), \
                ("12 Sea Zone", "18 Sea Zone"), \
                ("12 Sea Zone", "13 Sea Zone"), \
                ("13 Sea Zone", "14 Sea Zone"), \
                ("13 Sea Zone", "Gibraltar"), \
                ("13 Sea Zone", "Morocco"), \
                ("13 Sea Zone", "23 Sea Zone"), \
                ("13 Sea Zone", "Spain Portugal"), \
                ("14 Sea Zone", "Gibraltar"), \
                ("14 Sea Zone", "Morocco"), \
                ("14 Sea Zone", "15 Sea Zone"), \
                ("14 Sea Zone", "Algeria"), \
                ("14 Sea Zone", "France"), \
                ("14 Sea Zone", "Spain Portugal"), \
                ("15 Sea Zone", "17 Sea Zone"), \
                ("15 Sea Zone", "Turkey"), \
                ("15 Sea Zone", "16 Sea Zone"), \
                ("15 Sea Zone", "Italy"), \
                ("15 Sea Zone", "Southern Europe"), \
                ("15 Sea Zone", "Libya"), \
                ("16 Sea Zone", "Bulgaria Romania"), \
                ("16 Sea Zone", "Turkey"), \
                ("16 Sea Zone", "Ukraine S.S.R."), \
                ("16 Sea Zone", "Caucasus"), \
                ("17 Sea Zone", "Turkey"), \
                ("17 Sea Zone", "Egypt"), \
                ("17 Sea Zone", "Trans-Jordan"), \
                ("17 Sea Zone", "34 Sea Zone"), \
                ("18 Sea Zone", "Central America"), \
                ("18 Sea Zone", "Venezuela"), \
                ("18 Sea Zone", "22 Sea Zone"), \
                ("18 Sea Zone", "West Indies"), \
                ("18 Sea Zone", "Colombia Equador"), \
                ("18 Sea Zone", "East Mexico"), \
                ("18 Sea Zone", "19 Sea Zone"), \
                ("19 Sea Zone", "Central America"), \
                ("19 Sea Zone", "20 Sea Zone"), \
                ("19 Sea Zone", "55 Sea Zone"), \
                ("19 Sea Zone", "Colombia Equador"), \
                ("19 Sea Zone", "East Mexico"), \
                ("19 Sea Zone", "Peru Argentina"), \
                ("20 Sea Zone", "42 Sea Zone"), \
                ("20 Sea Zone", "Chile"), \
                ("20 Sea Zone", "21 Sea Zone"), \
                ("21 Sea Zone", "22 Sea Zone"), \
                ("21 Sea Zone", "26 Sea Zone"), \
                ("21 Sea Zone", "Peru Argentina"), \
                ("21 Sea Zone", "41 Sea Zone"), \
                ("21 Sea Zone", "Chile"), \
                ("21 Sea Zone", "25 Sea Zone"), \
                ("22 Sea Zone", "23 Sea Zone"), \
                ("22 Sea Zone", "Brazil"), \
                ("22 Sea Zone", "25 Sea Zone"), \
                ("23 Sea Zone", "24 Sea Zone"), \
                ("23 Sea Zone", "French West Africa"), \
                ("23 Sea Zone", "25 Sea Zone"), \
                ("23 Sea Zone", "Sahara"), \
                ("24 Sea Zone", "27 Sea Zone"), \
                ("24 Sea Zone", "Belgian Congo"), \
                ("24 Sea Zone", "French Equatorial Africa"), \
                ("24 Sea Zone", "25 Sea Zone"), \
                ("25 Sea Zone", "27 Sea Zone"), \
                ("25 Sea Zone", "26 Sea Zone"), \
                ("26 Sea Zone", "27 Sea Zone"), \
                ("27 Sea Zone", "28 Sea Zone"), \
                ("27 Sea Zone", "Angola"), \
                ("27 Sea Zone", "Union of South Africa"), \
                ("28 Sea Zone", "Mozambique"), \
                ("28 Sea Zone", "Union of South Africa"), \
                ("28 Sea Zone", "33 Sea Zone"), \
                ("28 Sea Zone", "29 Sea Zone"), \
                ("28 Sea Zone", "French Madagascar"), \
                ("29 Sea Zone", "31 Sea Zone"), \
                ("29 Sea Zone", "French Madagascar"), \
                ("29 Sea Zone", "30 Sea Zone"), \
                ("29 Sea Zone", "32 Sea Zone"), \
                ("30 Sea Zone", "38 Sea Zone"), \
                ("30 Sea Zone", "37 Sea Zone"), \
                ("30 Sea Zone", "31 Sea Zone"), \
                ("31 Sea Zone", "37 Sea Zone"), \
                ("31 Sea Zone", "35 Sea Zone"), \
                ("31 Sea Zone", "32 Sea Zone"), \
                ("32 Sea Zone", "33 Sea Zone"), \
                ("32 Sea Zone", "35 Sea Zone"), \
                ("32 Sea Zone", "French Madagascar"), \
                ("32 Sea Zone", "34 Sea Zone"), \
                ("33 Sea Zone", "Rhodesia"), \
                ("33 Sea Zone", "Mozambique"), \
                ("33 Sea Zone", "French Madagascar"), \
                ("33 Sea Zone", "34 Sea Zone"), \
                ("33 Sea Zone", "Italian East Africa"), \
                ("34 Sea Zone", "Saudi Arabia"), \
                ("34 Sea Zone", "Anglo-Egyptian Sudan"), \
                ("34 Sea Zone", "Persia"), \
                ("34 Sea Zone", "35 Sea Zone"), \
                ("34 Sea Zone", "Egypt"), \
                ("34 Sea Zone", "Trans-Jordan"), \
                ("34 Sea Zone", "Italian East Africa"), \
                ("35 Sea Zone", "37 Sea Zone"), \
                ("35 Sea Zone", "36 Sea Zone"), \
                ("35 Sea Zone", "India"), \
                ("36 Sea Zone", "French Indo-China Thailand"), \
                ("36 Sea Zone", "48 Sea Zone"), \
                ("36 Sea Zone", "37 Sea Zone"), \
                ("36 Sea Zone", "61 Sea Zone"), \
                ("36 Sea Zone", "Burma"), \
                ("36 Sea Zone", "47 Sea Zone"), \
                ("36 Sea Zone", "Malaya"), \
                ("37 Sea Zone", "38 Sea Zone"), \
                ("37 Sea Zone", "46 Sea Zone"), \
                ("37 Sea Zone", "47 Sea Zone"), \
                ("37 Sea Zone", "East Indies"), \
                ("38 Sea Zone", "46 Sea Zone"), \
                ("38 Sea Zone", "Western Australia"), \
                ("38 Sea Zone", "39 Sea Zone"), \
                ("39 Sea Zone", "40 Sea Zone"), \
                ("39 Sea Zone", "45 Sea Zone"), \
                ("39 Sea Zone", "Eastern Australia"), \
                ("40 Sea Zone", "43 Sea Zone"), \
                ("40 Sea Zone", "New Zealand"), \
                ("40 Sea Zone", "44 Sea Zone"), \
                ("40 Sea Zone", "41 Sea Zone"), \
                ("40 Sea Zone", "45 Sea Zone"), \
                ("41 Sea Zone", "43 Sea Zone"), \
                ("41 Sea Zone", "42 Sea Zone"), \
                ("42 Sea Zone", "43 Sea Zone"), \
                ("42 Sea Zone", "54 Sea Zone"), \
                ("42 Sea Zone", "55 Sea Zone"), \
                ("43 Sea Zone", "54 Sea Zone"), \
                ("43 Sea Zone", "44 Sea Zone"), \
                ("43 Sea Zone", "53 Sea Zone"), \
                ("44 Sea Zone", "50 Sea Zone"), \
                ("44 Sea Zone", "52 Sea Zone"), \
                ("44 Sea Zone", "45 Sea Zone"), \
                ("44 Sea Zone", "53 Sea Zone"), \
                ("44 Sea Zone", "49 Sea Zone"), \
                ("44 Sea Zone", "Solomon Islands"), \
                ("45 Sea Zone", "46 Sea Zone"), \
                ("45 Sea Zone", "49 Sea Zone"), \
                ("45 Sea Zone", "Eastern Australia"), \
                ("46 Sea Zone", "Western Australia"), \
                ("46 Sea Zone", "47 Sea Zone"), \
                ("46 Sea Zone", "49 Sea Zone"), \
                ("47 Sea Zone", "Borneo"), \
                ("47 Sea Zone", "48 Sea Zone"), \
                ("47 Sea Zone", "49 Sea Zone"), \
                ("48 Sea Zone", "51 Sea Zone"), \
                ("48 Sea Zone", "50 Sea Zone"), \
                ("48 Sea Zone", "Philippine Islands"), \
                ("48 Sea Zone", "61 Sea Zone"), \
                ("48 Sea Zone", "60 Sea Zone"), \
                ("48 Sea Zone", "49 Sea Zone"), \
                ("49 Sea Zone", "New Guinea"), \
                ("49 Sea Zone", "50 Sea Zone"), \
                ("50 Sea Zone", "51 Sea Zone"), \
                ("50 Sea Zone", "Caroline Islands"), \
                ("50 Sea Zone", "52 Sea Zone"), \
                ("51 Sea Zone", "59 Sea Zone"), \
                ("51 Sea Zone", "Okinawa"), \
                ("51 Sea Zone", "60 Sea Zone"), \
                ("51 Sea Zone", "52 Sea Zone"), \
                ("52 Sea Zone", "59 Sea Zone"), \
                ("52 Sea Zone", "57 Sea Zone"), \
                ("52 Sea Zone", "53 Sea Zone"), \
                ("52 Sea Zone", "Wake Island"), \
                ("53 Sea Zone", "54 Sea Zone"), \
                ("53 Sea Zone", "56 Sea Zone"), \
                ("53 Sea Zone", "57 Sea Zone"), \
                ("53 Sea Zone", "Hawaiian Islands"), \
                ("54 Sea Zone", "56 Sea Zone"), \
                ("54 Sea Zone", "55 Sea Zone"), \
                ("55 Sea Zone", "56 Sea Zone"), \
                ("55 Sea Zone", "Mexico"), \
                ("56 Sea Zone", "57 Sea Zone"), \
                ("56 Sea Zone", "65 Sea Zone"), \
                ("56 Sea Zone", "Western United States"), \
                ("57 Sea Zone", "59 Sea Zone"), \
                ("57 Sea Zone", "65 Sea Zone"), \
                ("57 Sea Zone", "58 Sea Zone"), \
                ("57 Sea Zone", "Midway"), \
                ("57 Sea Zone", "64 Sea Zone"), \
                ("58 Sea Zone", "59 Sea Zone"), \
                ("58 Sea Zone", "63 Sea Zone"), \
                ("58 Sea Zone", "60 Sea Zone"), \
                ("58 Sea Zone", "64 Sea Zone"), \
                ("59 Sea Zone", "60 Sea Zone"), \
                ("59 Sea Zone", "Iwo Jima"), \
                ("60 Sea Zone", "61 Sea Zone"), \
                ("60 Sea Zone", "Japan"), \
                ("60 Sea Zone", "63 Sea Zone"), \
                ("60 Sea Zone", "62 Sea Zone"), \
                ("61 Sea Zone", "Kwangtung"), \
                ("61 Sea Zone", "Kiangsu"), \
                ("61 Sea Zone", "Yunnan"), \
                ("61 Sea Zone", "Formosa"), \
                ("61 Sea Zone", "62 Sea Zone"), \
                ("62 Sea Zone", "Manchuria"), \
                ("62 Sea Zone", "Buryatia S.S.R."), \
                ("62 Sea Zone", "Japan"), \
                ("62 Sea Zone", "63 Sea Zone"), \
                ("63 Sea Zone", "Soviet Far East"), \
                ("63 Sea Zone", "Buryatia S.S.R."), \
                ("63 Sea Zone", "64 Sea Zone"), \
                ("64 Sea Zone", "65 Sea Zone"), \
                ("64 Sea Zone", "Alaska"), \
                ("65 Sea Zone", "Western Canada"), \
                ("65 Sea Zone", "Alaska"), \
                ("Afghanistan", "Persia"), \
                ("Afghanistan", "Szechwan"), \
                ("Afghanistan", "Kazakh S.S.R."), \
                ("Afghanistan", "Himalaya"), \
                ("Afghanistan", "India"), \
                ("Alaska", "Western Canada"), \
                ("Algeria", "Morocco"), \
                ("Algeria", "Libya"), \
                ("Algeria", "Sahara"), \
                ("Anglo-Egyptian Sudan", "Rhodesia"), \
                ("Anglo-Egyptian Sudan", "Belgian Congo"), \
                ("Anglo-Egyptian Sudan", "Egypt"), \
                ("Anglo-Egyptian Sudan", "French Equatorial Africa"), \
                ("Anglo-Egyptian Sudan", "Italian East Africa"), \
                ("Anglo-Egyptian Sudan", "Sahara"), \
                ("Angola", "Union of South Africa"), \
                ("Angola", "Belgian Congo"), \
                ("Anhwei", "Manchuria"), \
                ("Anhwei", "Mongolia"), \
                ("Anhwei", "Kwangtung"), \
                ("Anhwei", "Kiangsu"), \
                ("Anhwei", "Szechwan"), \
                ("Anhwei", "Sinkiang"), \
                ("Archangel", "Evenki National Okrug"), \
                ("Archangel", "West Russia"), \
                ("Archangel", "Karelia S.S.R."), \
                ("Archangel", "Russia"), \
                ("Archangel", "Vologda"), \
                ("Baltic States", "Belorussia"), \
                ("Baltic States", "Poland"), \
                ("Baltic States", "Karelia S.S.R."), \
                ("Baltic States", "Germany"), \
                ("Belgian Congo", "Rhodesia"), \
                ("Belgian Congo", "Union of South Africa"), \
                ("Belgian Congo", "French Equatorial Africa"), \
                ("Belorussia", "Ukraine S.S.R."), \
                ("Belorussia", "Poland"), \
                ("Belorussia", "West Russia"), \
                ("Belorussia", "Karelia S.S.R."), \
                ("Brazil", "Venezuela"), \
                ("Brazil", "Colombia Equador"), \
                ("Brazil", "Peru Argentina"), \
                ("Bulgaria Romania", "Turkey"), \
                ("Bulgaria Romania", "Ukraine S.S.R."), \
                ("Bulgaria Romania", "Poland"), \
                ("Bulgaria Romania", "Southern Europe"), \
                ("Bulgaria Romania", "Germany"), \
                ("Burma", "French Indo-China Thailand"), \
                ("Burma", "Yunnan"), \
                ("Burma", "Himalaya"), \
                ("Burma", "India"), \
                ("Buryatia S.S.R.", "Manchuria"), \
                ("Buryatia S.S.R.", "Mongolia"), \
                ("Buryatia S.S.R.", "Soviet Far East"), \
                ("Buryatia S.S.R.", "Yakut S.S.R."), \
                ("Caucasus", "Turkey"), \
                ("Caucasus", "Persia"), \
                ("Caucasus", "Ukraine S.S.R."), \
                ("Caucasus", "Kazakh S.S.R."), \
                ("Caucasus", "West Russia"), \
                ("Caucasus", "Russia"), \
                ("Central America", "Colombia Equador"), \
                ("Central America", "East Mexico"), \
                ("Central United States", "Eastern United States"), \
                ("Central United States", "East Mexico"), \
                ("Central United States", "Western United States"), \
                ("Central United States", "Eastern Canada"), \
                ("Chile", "Peru Argentina"), \
                ("Colombia Equador", "Venezuela"), \
                ("Colombia Equador", "Peru Argentina"), \
                ("East Mexico", "Mexico"), \
                ("Eastern Australia", "Western Australia"), \
                ("Eastern Canada", "Eastern United States"), \
                ("Eastern Canada", "Western Canada"), \
                ("Egypt", "Trans-Jordan"), \
                ("Egypt", "Libya"), \
                ("Egypt", "Sahara"), \
                ("Eire", "United Kingdom"), \
                ("Evenki National Okrug", "Mongolia"), \
                ("Evenki National Okrug", "Yakut S.S.R."), \
                ("Evenki National Okrug", "Novosibirsk"), \
                ("Evenki National Okrug", "Sinkiang"), \
                ("Evenki National Okrug", "Vologda"), \
                ("Finland", "Sweden"), \
                ("Finland", "Norway"), \
                ("Finland", "Karelia S.S.R."), \
                ("France", "Northwestern Europe"), \
                ("France", "Italy"), \
                ("France", "Spain Portugal"), \
                ("France", "Switzerland"), \
                ("France", "Germany"), \
                ("French Equatorial Africa", "French West Africa"), \
                ("French Equatorial Africa", "Sahara"), \
                ("French Indo-China Thailand", "Yunnan"), \
                ("French Indo-China Thailand", "Malaya"), \
                ("French West Africa", "Sahara"), \
                ("Germany", "Northwestern Europe"), \
                ("Germany", "Poland"), \
                ("Germany", "Italy"), \
                ("Germany", "Southern Europe"), \
                ("Germany", "Switzerland"), \
                ("Gibraltar", "Spain Portugal"), \
                ("Himalaya", "Szechwan"), \
                ("Himalaya", "Yunnan"), \
                ("Himalaya", "India"), \
                ("India", "Persia"), \
                ("Italian East Africa", "Rhodesia"), \
                ("Italy", "Southern Europe"), \
                ("Italy", "Switzerland"), \
                ("Karelia S.S.R.", "West Russia"), \
                ("Kazakh S.S.R.", "Persia"), \
                ("Kazakh S.S.R.", "Szechwan"), \
                ("Kazakh S.S.R.", "Novosibirsk"), \
                ("Kazakh S.S.R.", "Sinkiang"), \
                ("Kazakh S.S.R.", "Russia"), \
                ("Kiangsu", "Manchuria"), \
                ("Kiangsu", "Kwangtung"), \
                ("Kwangtung", "Szechwan"), \
                ("Kwangtung", "Yunnan"), \
                ("Libya", "Sahara"), \
                ("Manchuria", "Mongolia"), \
                ("Mexico", "Western United States"), \
                ("Mongolia", "Yakut S.S.R."), \
                ("Mongolia", "Sinkiang"), \
                ("Morocco", "Sahara"), \
                ("Mozambique", "Rhodesia"), \
                ("Mozambique", "Union of South Africa"), \
                ("Norway", "Sweden"), \
                ("Novosibirsk", "Sinkiang"), \
                ("Novosibirsk", "Russia"), \
                ("Novosibirsk", "Vologda"), \
                ("Persia", "Turkey"), \
                ("Persia", "Trans-Jordan"), \
                ("Poland", "Ukraine S.S.R."), \
                ("Rhodesia", "Union of South Africa"), \
                ("Russia", "West Russia"), \
                ("Russia", "Vologda"), \
                ("Saudi Arabia", "Trans-Jordan"), \
                ("Sinkiang", "Szechwan"), \
                ("Southern Europe", "Turkey"), \
                ("Soviet Far East", "Yakut S.S.R."), \
                ("Szechwan", "Yunnan"), \
                ("Trans-Jordan", "Turkey"), \
                ("Ukraine S.S.R.", "West Russia"), \
                ("Western Canada", "Western United States")]
                
                for key in self.board:
                        for item in self.connections: 
                                if (key == item[0]):
                                        self.board[key].neighbors.append(item[1])
                                if (key == item[1]):
                                        self.board[key].neighbors.append(item[0])
                
                
                self.units = [Unit("infantry", "land", 3, 1, 2, 1), Unit("artillary", "land", 4, 1, 2, 1)
                self.tank = Unit("tank", "land", 6, 1, 2, 1)
                self.aa = Unit("aa", "land", 6, 0, 0, 1)
                self.factory = Unit("factory", "land", 15, 0, 0, 0)
                
                #sea units
                self.transport = Unit("sub", "sea", 7, 0, 0, 2)
                self.transport.is_transport = 1 #FIX
                self.sub = Unit("sub", "sea", 6, 2, 1, 2)
                self.destroyer = Unit("destroyer", "sea", 8, 2, 2, 2)
                self.cruiser = Unit("cruiser", "sea", 12, 3, 3, 2)
                self.carrier = Unit("carrier", "sea", 14, 1, 2)
                self.carrier.is_carrier = 1
                self.battleship = Unit("battleship", "sea", 20, 2, 1, 2)
                
                #air units
                self.fighter = Unit("fighter", "10", 10, 3, 4, 4)
                self.bomber = Unit("bomber", "air", 12, 4, 1, 6)
                              
        def get_unit(index)
                              returns prototype
                
class Territory_state:
        """
        Object representing all fluid information about a territory
        """
        
        def __init__(self, territory_owner, list = []):
                self.owner = territory_owner
        
                #LIST OF UNIT STATES
                self.infantry_count = 0
                self.artillary_count = 0
                self.tank_count = 0
                self.aa_count = 0
                self.factorty_count = 0
        
                self.transport_count = 0
                self.sub_count = 0
                self.destroyer_count = 0
                self.cruiser_count = 0
                self.carrier_count = 0
                self.battleship_count = 0
        
                self.fighter_count = 0
                self.bomber_count = 0        

class Unit_state:
        """
        Provides a basic template for a unit
        """
        
        def __init__(self, type_number):
                self.owner = 
                self.damaged = 
                self.moves_remaining =
                self.type = type_number
                
class Game:
        """
        IN PROGRESS. Trying to represent the game as a whole, including all static and fluid
        information (including turn phase and turn ownership -- not yet defined anywhere).
        Will want to be able to make changes as game progresses.
        """
                              
        #convery unit-state numbers to units using rules.get_unit.
                              
        def __init__(self, rules):
                
                #dictionary from territory_str to territory state
                
                rules.board = board_dict
                territory_state_dict = {}
                
                #basic framwork of the dict so I dont get confused
                for key in board_dict:
                        territory_state_dict[board_dict[key]] = Territory_state("Neutral")
                      
                #updates the dict with correct unit values and ownership 
                for territory_key in territory_state_dict:
                        if (territory_key == 
                        

#ADD IN TERRITORY OWNERSHIP AND ACCOUNT FOR IT IN THE PASSABLE FUNCTION
# neutrals cant move to, and enemy must be during combat phase. Tanks end all movement if battle
# check phase

def passable(unit, current_territory, goal_territory):
        """
        a function that will check if a theoretical move is valid.
        """
                            
        if (unit.unit_type == "land"):
                if (goal_territory.is_water == 0 and (goal_territory.name in current_territory.neighbors)):
                        return True
                else:
                        return False
        elif (unit.unit_type == "sea"):
                if (goal_territory.is_water == 1 and (goal_territory.name in current_territory.neighbors)):
                        return True
                else:
                        return False
        elif (unit.unit_type == "air"):
                if (goal_territory.is_water == 0 and (goal_territory.name in current_territory.neighbors)):
                        return True                
        


# classic pathfinding = dijkstra search or A*

# Make a distance function

# Is_Reachable

     # Make an Is_ land_reachable function

     # Is_sea_reachable

     # Plane_has_retreat

     # Controls strait.
     
# Find a way to impliment the battle calculator

# Is_bordering_enemy

# Is_threatened by enemy
