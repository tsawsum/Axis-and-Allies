from stackqueue import *
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import urllib
import urllib
import ssl
import time
import xml.etree.cElementTree as ET


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
                # TODO: FIGURE OUT HOW TO REPRESENT FULL TRANSPORTS AND CARRIERS. IS THE UNIT DIRECTLY ATTACHED?
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
                self.board = {"1 Sea Zone" : Territory("1 Sea Zone", 0, True), \
                "2 Sea Zone" : Territory("2 Sea Zone", 0, True), \
                "3 Sea Zone" : Territory("2 Sea Zone", 0, True), \
                "4 Sea Zone" : Territory("4 Sea Zone", 0, True), \
                "5 Sea Zone" : Territory("5 Sea Zone", 0, True), \
                "6 Sea Zone" : Territory("6 Sea Zone", 0, True), \
                "7 Sea Zone" : Territory("7 Sea Zone", 0, True), \
                "8 Sea Zone" : Territory("8 Sea Zone", 0, True), \
                "9 Sea Zone" : Territory("9 Sea Zone", 0, True), \
                "10 Sea Zone" : Territory("10 Sea Zone", 0, True), \
                "11 Sea Zone" : Territory("11 Sea Zone", 0, True), \
                "12 Sea Zone" : Territory("12 Sea Zone", 0, True), \
                "13 Sea Zone" : Territory("13 Sea Zone", 0, True), \
                "14 Sea Zone" : Territory("14 Sea Zone", 0, True), \
                "15 Sea Zone" : Territory("15 Sea Zone", 0, True), \
                "16 Sea Zone" : Territory("16 Sea Zone", 0, True), \
                "17 Sea Zone" : Territory("17 Sea Zone", 0, True), \
                "18 Sea Zone" : Territory("18 Sea Zone", 0, True), \
                "19 Sea Zone" : Territory("19 Sea Zone", 0, True), \
                "20 Sea Zone" : Territory("20 Sea Zone", 0, True), \
                "21 Sea Zone" : Territory("21 Sea Zone", 0, True), \
                "22 Sea Zone" : Territory("22 Sea Zone", 0, True), \
                "23 Sea Zone" : Territory("23 Sea Zone", 0, True), \
                "24 Sea Zone" : Territory("24 Sea Zone", 0, True), \
                "25 Sea Zone" : Territory("25 Sea Zone", 0, True), \
                "26 Sea Zone" : Territory("26 Sea Zone", 0, True), \
                "27 Sea Zone" : Territory("27 Sea Zone", 0, True), \
                "28 Sea Zone" : Territory("28 Sea Zone", 0, True), \
                "29 Sea Zone" : Territory("29 Sea Zone", 0, True), \
                "30 Sea Zone" : Territory("30 Sea Zone", 0, True), \
                "31 Sea Zone" : Territory("31 Sea Zone", 0, True), \
                "32 Sea Zone" : Territory("32 Sea Zone", 0, True), \
                "33 Sea Zone" : Territory("33 Sea Zone", 0, True), \
                "34 Sea Zone" : Territory("34 Sea Zone", 0, True), \
                "35 Sea Zone" : Territory("35 Sea Zone", 0, True), \
                "36 Sea Zone" : Territory("36 Sea Zone", 0, True), \
                "37 Sea Zone" : Territory("37 Sea Zone", 0, True), \
                "38 Sea Zone" : Territory("38 Sea Zone", 0, True), \
                "39 Sea Zone" : Territory("39 Sea Zone", 0, True), \
                "40 Sea Zone" : Territory("40 Sea Zone", 0, True), \
                "41 Sea Zone" : Territory("41 Sea Zone", 0, True), \
                "42 Sea Zone" : Territory("42 Sea Zone", 0, True), \
                "43 Sea Zone" : Territory("43 Sea Zone", 0, True), \
                "44 Sea Zone" : Territory("44 Sea Zone", 0, True), \
                "45 Sea Zone" : Territory("45 Sea Zone", 0, True), \
                "46 Sea Zone" : Territory("46 Sea Zone", 0, True), \
                "47 Sea Zone" : Territory("47 Sea Zone", 0, True), \
                "48 Sea Zone" : Territory("48 Sea Zone", 0, True), \
                "49 Sea Zone" : Territory("49 Sea Zone", 0, True), \
                "50 Sea Zone" : Territory("50 Sea Zone", 0, True), \
                "51 Sea Zone" : Territory("51 Sea Zone", 0, True), \
                "52 Sea Zone" : Territory("52 Sea Zone", 0, True), \
                "53 Sea Zone" : Territory("53 Sea Zone", 0, True), \
                "54 Sea Zone" : Territory("54 Sea Zone", 0, True), \
                "55 Sea Zone" : Territory("55 Sea Zone", 0, True), \
                "56 Sea Zone" : Territory("56 Sea Zone", 0, True), \
                "57 Sea Zone" : Territory("57 Sea Zone", 0, True), \
                "58 Sea Zone" : Territory("58 Sea Zone", 0, True), \
                "59 Sea Zone" : Territory("59 Sea Zone", 0, True), \
                "60 Sea Zone" : Territory("60 Sea Zone", 0, True), \
                "61 Sea Zone" : Territory("61 Sea Zone", 0, True), \
                "62 Sea Zone" : Territory("62 Sea Zone", 0, True), \
                "63 Sea Zone" : Territory("63 Sea Zone", 0, True), \
                "64 Sea Zone" : Territory("64 Sea Zone", 0, True), \
                "65 Sea Zone" : Territory("65 Sea Zone", 0, True), \
                "Afghanistan" : Territory("Afghanistan", 1, False), \
                "Alaska" : Territory("Alaska", 2, False), \
                "Algeria" : Territory("Algeria", 1, False), \
                "Anglo-Egyptian Sudan" : Territory("Anglo-Egyptian Sudan", 0, False), \
                "Angola" : Territory("Angola", 0, False), \
                # NEUTRAL ^
                "Anhwei" : Territory("Anhwei", 1, False), \
                "Archangel" : Territory("Archangel", 1, False), \
                "Baltic States" : Territory("Baltic States", 2, False), \
                "Belgian Congo" : Territory("Belgian Congo", 1, False), \
                "Belorussia" : Territory("Belorussia", 2, False), \
                "Borneo" : Territory("Borneo", 4, False), \
                "Brazil" : Territory("Brazil", 3, False), \
                "Bulgaria Romania" : Territory("Bulgaria Romania", 2, False), \
                "Burma" : Territory("Burma", 1, False), \
                "Buryatia S.S.R." : Territory("Buryatia S.S.R.", 1, False), \
                "Caroline Islands" : Territory("Caroline Islands", 0, False), \
                "Caucasus" : Territory("Caucasus", 4, False), \
                "Central America" : Territory("Central America", 1, False), \
                "Central United States" : Territory("Central United States", 6, False), \
                "Chile" : Territory("Chile", 0, False), \
                # NEUTRAL ^
                "Colombia Equador" : Territory("Colombia Equador", 0, False), \
                # NEUTRAL ^
                "East Indies" : Territory("East Indies", 4, False), \
                "East Mexico" : Territory("East Mexico", 0, False), \
                "Eastern Australia" : Territory("Eastern Australia", 1, False), \
                "Eastern Canada" : Territory("Eastern Canada", 3, False), \
                "Eastern United States" : Territory("Eastern United States", 12, False), \
                "Egypt" : Territory("Egypt", 2, False), \
                "Eire" : Territory("Eire", 0, False), \
                # NEUTRAL ^
                "Evenki National Okrug" : Territory("Evenki National Okrug", 1, False), \
                "Finland" : Territory("Finland", 1, False), \
                "Formosa" : Territory("Formosa", 0, False), \
                "France" : Territory("France", 6, False), \
                "French Equatorial Africa" : Territory("French Equatorial Africa", 1, False), \
                "French Indo-China Thailand" : Territory("French Indo-China Thailand", 2, False), \
                "French Madagascar" : Territory("French Madagascar", 1, False), \
                "French West Africa" : Territory("French West Africa", 1, False), \
                "Germany" : Territory("Germany", 10, False), \
                "Gibraltar" : Territory("Gibraltar", 0, False), \
                "Greenland" : Territory("Greenland", 0, False), \
                "Hawaiian Islands" : Territory("Hawaiian Islands", 1, False), \
                "Himalaya" : Territory("Himalaya", 0, False), \
                # NEUTRAL ^
                "Iceland" : Territory("Iceland", 0, False), \
                "India" : Territory("India", 3, False), \
                "Italian East Africa" : Territory("Italian East Africa", 1, False), \
                "Italy" : Territory("Italy", 3, False), \
                "Iwo Jima" : Territory("Iwo Jima", 0, False), \
                "Japan" : Territory("Japan", 8, False), \
                "Karelia S.S.R." : Territory("Karelia S.S.R.", 2, False), \
                "Kazakh S.S.R." : Territory("Kazakh S.S.R.", 2, False), \
                "Kiangsu" : Territory("Kiangsu", 2, False), \
                "Kwangtung" : Territory("Kwangtung", 2, False), \
                "Libya" : Territory("Libya", 1, False), \
                "Malaya" : Territory("Malaya", 1, False), \
                "Manchuria" : Territory("Manchuria", 3, False), \
                "Mexico" : Territory("Mexico", 2, False), \
                "Midway" : Territory("Midway", 0, False), \
                "Mongolia" : Territory("Mongolia", 0, False), \
                # NEUTRAL ^
                "Morocco" : Territory("Morocco", 1, False), \
                "Mozambique" : Territory("Mozambique", 0, False), \
                # NEUTRAL ^
                "New Guinea" : Territory("New Guinea", 1, False), \
                "New Zealand" : Territory("New Zealand", 1, False), \
                "Northwestern Europe" : Territory("Northwestern Europe", 2, False), \
                "Norway" : Territory("Norway", 2, False), \
                "Novosibirsk" : Territory("Novosibirsk", 1, False), \
                "Okinawa" : Territory("Okinawa", 0, False), \
                "Persia" : Territory("Persia", 1, False), \
                "Peru Argentina" : Territory("Peru Argentina", 0, False), \
                # NEUTRAL ^
                "Philippine Islands" : Territory("Philippine Islands", 3, False), \
                "Poland" : Territory("Poland", 2, False), \
                "Rhodesia" : Territory("Rhodesia", 1, False), \
                "Russia" : Territory("Russia", 8, False), \
                "Sahara" : Territory("Sahara", 0, False), \
                # NEUTRAL ^
                "Saudi Arabia" : Territory("Saudi Arabia", 0, False), \
                # NEUTRAL ^
                "Sinkiang" : Territory("Sinkiang", 1, False), \
                "Solomon Islands" : Territory("Solomon Islands", 0, False), \
                "Southern Europe" : Territory("Southern Europe", 2, False), \
                "Soviet Far East" : Territory("Soviet Far East", 1, False), \
                "Spain Portugal" : Territory("Spain Portugal", 0, False), \
                # NEUTRAL ^
                "Sweden" : Territory("Sweden", 0, False), \
                # NEUTRAL ^
                "Switzerland" : Territory("Switzerland", 0, False), \
                # NEUTRAL ^
                "Szechwan" : Territory("Szechwan", 1, False), \
                "Trans-Jordan" : Territory("Trans-Jordan", 1, False), \
                "Turkey" : Territory("Turkey", 0, False), \
                # NEUTRAL ^
                "Ukraine S.S.R." : Territory("Ukraine S.S.R.", 2, False), \
                "Union of South Africa" : Territory("Union of South Africa", 2, False), \
                "United Kingdom" : Territory("United Kingdom", 8, False), \
                "Venezuela" : Territory("Venezuela", 0, False), \
                # NEUTRAL ^
                "Vologda" : Territory("Vologda", 2, False), \
                "Wake Island" : Territory("Wake Island", 0, False), \
                "West Indies" : Territory("West Indies", 1, False), \
                "West Russia" : Territory("West Russia", 2, False), \
                "Western Australia" : Territory("Western Australia", 1, False), \
                "Western Canada" : Territory("Western Canada", 1, False), \
                "Western United States" : Territory("Western United States", 10, False), \
                "Yakut S.S.R." : Territory("Yakut S.S.R.", 1, False), \
                "Yunnan" : Territory("Yunnan", 1, False) }
                
                
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

                for item in self.connections:
                        self.board[item[0]].neighbors.append(item[1])
                        self.board[item[1]].neighbors.append(item[0])

                self.units = [Unit("infantry", "land", 3, 1, 2, 1), Unit("artillery", "land", 4, 1, 2, 1), \
                              Unit("tank", "land", 6, 1, 2, 1), Unit("aa", "land", 6, 0, 0, 1), \
                              Unit("factory", "land", 15, 0, 0, 0), Unit("transport", "sea", 7, 0, 0, 2, True), \
                              Unit("sub", "sea", 6, 2, 1, 2), Unit("destroyer", "sea", 8, 2, 2, 2), \
                              Unit("cruiser", "sea", 12, 3, 3, 2), Unit("carrier", "sea", 14, 1, 2, False, True), \
                              Unit("battleship", "sea", 20, 2, 1, 2), Unit("fighter", "air", 10, 3, 4, 4), \
                              Unit("bomber", "air", 12, 4, 1, 6)]

                self.teams = {"America": "Allies",
                              "Britain": "Allies",
                              "Russia": "Allies",
                              "Germany": "Axis",
                              "Japan": "Axis",
                              "Neutral": "Neutral"}
                              
        def get_unit(self, index):
                return self.units[index]
                
class Territory_State:
        """
        Object representing all fluid information about a territory
        """
        
        def __init__(self, territory_owner, unit_list = []):
                self.owner = territory_owner
        
                self.unit_state_list =  unit_list

class Unit_state:
        """
        Provides fluid information for units
        """
        
        def __init__(self, owner, type_number, moves_used = 0, damage = 0):
                self.owner = owner
                self.type_index = type_number
                self.moves_used = moves_used
                self.damaged = damage
                
class Turn_state:
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
        
        def __init__(self, name, ipc = 0, tech_tokens = 0):
                self.name = name
                self.ipc = ipc
                self.tech_tokens = tech_tokens        
                
class Game:
        """
        IN PROGRESS. Trying to represent the game as a whole, including all static and fluid
        information (including turn phase and turn ownership -- not yet defined anywhere).
        Will want to be able to make changes as game progresses.
        """
                              
        #converts unit-state numbers to units using rules.get_unit.
                              
        def __init__(self):
                
                self.rules = Rules()
                #player 0 = russia, 1 = germany, 2 = britain, 3 = japan, 4 = us
                # phase 0 = tech, 1 = repair, 2 = buy, 3 = combat move, 4 = combat phase, 5 = non-combat, 6 = place
                self.turn_state = Turn_state(1, "Russia", 0)
                
                #dictionary from territory names to territory states
                self.state_dict = {"1 Sea Zone" : Territory_State("Sea Zone", []), \
                "2 Sea Zone" : Territory_State("Sea Zone", []), \
                "3 Sea Zone" : Territory_State("Sea Zone", []), \
                "4 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Russia", 7)]), \
                "5 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Germany", 6), Unit_state("Germany", 7), Unit_state("Germany", 9)]), \
                "6 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Britain", 6), Unit_state("Britain", 8), Unit_state("Britain", 11)]), \
                "7 Sea Zone" : Territory_State("Sea Zone", []), \
                "8 Sea Zone" : Territory_State("Sea Zone", []), \
                "9 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Germany", 7), Unit_state("Germany", 7)]), \
                "10 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Britain", 6), Unit_state("Britain", 8)]), \
                "11 Sea Zone" : Territory_State("Sea Zone", [Unit_state("America", 6), Unit_state("America", 6), Unit_state("America", 8)]), \
                "12 Sea Zone" : Territory_State("Sea Zone", []), \
                "13 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Britain", 9)]), \
                "14 Sea Zone" : Territory_State("Sea Zone", []), \
                "15 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Germany", 6), Unit_state("Germany", 11)]), \
                "16 Sea Zone" : Territory_State("Sea Zone", []), \
                "17 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Britain", 8)]), \
                "18 Sea Zone" : Territory_State("Sea Zone", []), \
                "19 Sea Zone" : Territory_State("Sea Zone", [Unit_state("America", 9)]), \
                "20 Sea one" : Territory_State("Sea Zone", []), \
                "21 Sea Zone" : Territory_State("Sea Zone", []), \
                "22 Sea Zone" : Territory_State("Sea Zone", []), \
                "23 Sea Zone" : Territory_State("Sea Zone", []), \
                "24 Sea Zone" : Territory_State("Sea Zone", []), \
                "25 Sea Zone" : Territory_State("Sea Zone", []), \
                "26 Sea Zone" : Territory_State("Sea Zone", []), \
                "27 Sea Zone" : Territory_State("Sea Zone", []), \
                "28 Sea Zone" : Territory_State("Sea Zone", []), \
                "29 Sea Zone" : Territory_State("Sea Zone", []), \
                "30 Sea Zone" : Territory_State("Sea Zone", []), \
                "31 Sea Zone" : Territory_State("Sea Zone", []), \
                "32 Sea Zone" : Territory_State("Sea Zone", []), \
                "33 Sea Zone" : Territory_State("Sea Zone", []), \
                "34 Sea Zone" : Territory_State("Sea Zone", []), \
                "35 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Britain", 6), Unit_state("Britain", 9), Unit_state("Britain", 10), Unit_state("Britain", 12)]), \
                "36 Sea Zone" : Territory_State("Sea Zone", []), \
                "37 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Japan", 10), Unit_state("Japan", 11), Unit_state("Japan", 12), Unit_state("Japan", 12)]), \
                "38 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Britain", 6), Unit_state("Britain", 7), Unit_state("Britain", 9)]), \
                "39 Sea Zone" : Territory_State("Sea Zone", []), \
                "40 Sea Zone" : Territory_State("Sea Zone", []), \
                "41 Sea Zone" : Territory_State("Sea Zone", []), \
                "42 Sea Zone" : Territory_State("Sea Zone", []), \
                "43 Sea Zone" : Territory_State("Sea Zone", []), \
                "44 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Japan", 7)]), \
                "45 Sea Zone" : Territory_State("Sea Zone", []), \
                "46 Sea Zone" : Territory_State("Sea Zone", []), \
                "47 Sea Zone" : Territory_State("Sea Zone", []), \
                "48 Sea Zone" : Territory_State("Sea Zone", []), \
                "49 Sea Zone" : Territory_State("Sea Zone", []), \
                "50 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Japan", 9), Unit_state("Japan", 10), Unit_state("Japan", 12)]), \
                "51 Sea Zone" : Territory_State("Sea Zone", []), \
                "52 Sea Zone" : Territory_State("Sea Zone", []), \
                "53 Sea Zone" : Territory_State("Sea Zone", [Unit_state("America", 7), Unit_state("America", 8), Unit_state("America", 10), Unit_state("America", 12)]), \
                "54 Sea Zone" : Territory_State("Sea Zone", []), \
                "55 Sea Zone" : Territory_State("Sea Zone", []), \
                "56 Sea Zone" : Territory_State("Sea Zone", [Unit_state("America", 6), Unit_state("America", 8), Unit_state("America", 11)]), \
                "57 Sea Zone" : Territory_State("Sea Zone", []), \
                "58 Sea Zone" : Territory_State("Sea Zone", []), \
                "59 Sea Zone" : Territory_State("Sea Zone", []), \
                "60 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Japan", 6), Unit_state("Japan", 8), Unit_state("Japan", 11)]), \
                "61 Sea Zone" : Territory_State("Sea Zone", [Unit_state("Japan", 6), Unit_state("Japan", 8)]), \
                "62 Sea Zone" : Territory_State("Sea Zone", []), \
                "63 Sea Zone" : Territory_State("Sea Zone", []), \
                "64 Sea Zone" : Territory_State("Sea Zone", []), \
                "65 Sea Zone" : Territory_State("Sea Zone", []), \
                "Afghanistan" : Territory_State("Neutral", []), \
                # Neutral ^
                "Alaska" : Territory_State("America", [Unit_state("America", 1)]), \
                "Algeria" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 2)]), \
                "Anglo-Egyptian Sudan" : Territory_State("Britain", []), \
                "Angola" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Anhwei" : Territory_State("America", [Unit_state("America", 1), Unit_state("America", 1)]), \
                "Archangel" : Territory_State("Russia", [Unit_state("Russia", 1), Unit_state("Russia", 3)]), \
                "Baltic States" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 3)]), \
                "Belgian Congo" : Territory_State("Britain", []), \
                "Belorussia" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 1)]), \
                "Borneo" : Territory_State("Japan", [Unit_state("Japan", 1)]), \
                "Brazil" : Territory_State("America", []), \
                "Bulgaria Romania" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 3), Unit_state("Germany", 12)]), \
                "Burma" : Territory_State("Britain", [Unit_state("Britain", 1)]), \
                "Buryatia S.S.R." : Territory_State("Russia", [Unit_state("Russia", 1), Unit_state("Russia", 1)]), \
                "Caroline Islands" : Territory_State("Japan", [Unit_state("Japan", 1)]), \
                "Caucasus" : Territory_State("Russia", [Unit_state("Russia", 1), Unit_state("Russia", 1), Unit_state("Russia", 1), Unit_state("Russia", 2), Unit_state("Russia", 3), Unit_state("Russia", 4), Unit_state("Russia", 5)]), \
                "Central America" : Territory_State("America", []), \
                "Central United States" : Territory_State("America", [Unit_state("America", 1)]), \
                "Chile" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Colombia Equador" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "East Indies" : Territory_State("Britain", [Unit_state("Japan", 1), Unit_state("Japan", 1)]), \
                "East Mexico" : Territory_State("America", []), \
                "Eastern Australia" : Territory_State("Britain", [Unit_state("Britain", 1), Unit_state("Britain", 1)]), \
                "Eastern Canada" : Territory_State("Britain", [Unit_state("Britain", 3)]), \
                "Eastern United States" : Territory_State("America", [Unit_state("America", 1), Unit_state("America", 2), Unit_state("America", 3), Unit_state("America", 4), Unit_state("America", 5), Unit_state("America", 12), Unit_state("America", 13)]), \
                "Egypt" : Territory_State("Britain", [Unit_state("Britain", 1), Unit_state("Britain", 2), Unit_state("Britain", 3), Unit_state("Britain", 12)]), \
                "Eire" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Evenki National Okrug" : Territory_State("Russia", [Unit_state("Russia", 1), Unit_state("Russia", 1)]), \
                "Finland" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 1)]), \
                "Formosa" : Territory_State("Japan", []), \
                "France" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 3), Unit_state("Germany", 3), Unit_state("Germany", 4)]), \
                "French Equatorial Africa" : Territory_State("Britain", []), \
                "French Indo-China Thailand" : Territory_State("Japan", [Unit_state("Japan", 1), Unit_state("Japan", 1), Unit_state("Japan", 2), Unit_state("Japan", 12)]), \
                "French Madagascar" : Territory_State("Britain", []), \
                "French West Africa" : Territory_State("Britain", []), \
                "Germany" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 3), Unit_state("Germany", 3), Unit_state("Germany", 4), Unit_state("Germany", 5), Unit_state("Germany", 12)]), \
                "Gibraltar" : Territory_State("Britain", []), \
                "Greenland" : Territory_State("America", []), \
                "Hawaiian Islands" : Territory_State("America", [Unit_state("America", 1), Unit_state("America", 12)]), \
                "Himalaya" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Iceland" : Territory_State("Britain", []), \
                "India" : Territory_State("Britain", [Unit_state("Britain", 1), Unit_state("Britain", 1), Unit_state("Britain", 1), Unit_state("Britain", 1), Unit_state("Britain", 1), Unit_state("Britain", 4), Unit_state("Britain", 5)]), \
                "Italian East Africa" : Territory_State("Britain", []), \
                "Italy" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 3), Unit_state("Germany", 4)]), \
                "Iwo Jima" : Territory_State("Japan", [Unit_state("Japan", 1)]), \
                "Japan" : Territory_State("Japan", [Unit_state("Japan", 1), Unit_state("Japan", 1), Unit_state("Japan", 1), Unit_state("Japan", 1), Unit_state("Japan", 2), Unit_state("Japan", 3), Unit_state("Japan", 4), Unit_state("Japan", 5), Unit_state("Japan", 12), Unit_state("Japan", 13)]), \
                "Karelia S.S.R." : Territory_State("Russia", [Unit_state("Russia", 1), Unit_state("Russia", 1), Unit_state("Russia", 1), Unit_state("Russia", 1), Unit_state("Russia", 2), Unit_state("Russia", 5), Unit_state("Russia", 12)]), \
                "Kazakh S.S.R." : Territory_State("Russia", [Unit_state("Russia", 1)]), \
                "Kiangsu" : Territory_State("Japan", [Unit_state("Japan", 1), Unit_state("Japan", 1), Unit_state("Japan", 1), Unit_state("Japan", 1)]), \
                "Kwangtung" : Territory_State("Japan", [Unit_state("Japan", 1), Unit_state("Japan", 2)]), \
                "Libya" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 3)]), \
                "Malaya" : Territory_State("Britain", [Unit_state("Japan", 1)]), \
                "Manchuria" : Territory_State("Japan", [Unit_state("Japan", 1), Unit_state("Japan", 1), Unit_state("Japan", 1), Unit_state("Japan", 12)]), \
                "Mexico" : Territory_State("America", []), \
                "Midway" : Territory_State("America", [Unit_state("America", 1)]), \
                "Mongolia" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Morocco" : Territory_State("Germany", [Unit_state("Germany", 1)]), \
                "Mozambique" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "New Guinea" : Territory_State("Japan", [Unit_state("Japan", 1)]), \
                "New Zealand" : Territory_State("Britain", [Unit_state("Britain", 1)]), \
                "Northwestern Europe" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 3), Unit_state("Germany", 12)]), \
                "Norway" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 12)]), \
                "Novosibirsk" : Territory_State("Russia", [Unit_state("Russia", 1)]), \
                "Okinawa" : Territory_State("Japan", [Unit_state("Japan", 1)]), \
                "Persia" : Territory_State("Britain", [Unit_state("Britain", 1)]), \
                "Peru Argentina" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Philippine Islands" : Territory_State("Japan", [Unit_state("Japan", 1), Unit_state("Japan", 2)]), \
                "Poland" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 3), Unit_state("Germany", 12)]), \
                "Rhodesia" : Territory_State("Britain", []), \
                "Russia" : Territory_State("Russia", [Unit_state("Russia", 1), Unit_state("Russia", 1), Unit_state("Russia", 1), Unit_state("Russia", 1), Unit_state("Russia", 2), Unit_state("Russia", 3), Unit_state("Russia", 3), Unit_state("Russia", 4), Unit_state("Russia", 5), Unit_state("Russia", 12)]), \
                "Sahara" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Saudi Arabia" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Sinkiang" : Territory_State("America", []), \
                "Solomon Islands" : Territory_State("Japan", [Unit_state("Japan", 1)]), \
                "Southern Europe" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 2)]), \
                "Soviet Far East" : Territory_State("Russia", [Unit_state("Russia", 1), Unit_state("Russia", 1)]), \
                "Spain Portugal" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Sweden" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Switzerland" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Szechwan" : Territory_State("America", [Unit_state("America", 1), Unit_state("America", 1), Unit_state("America", 12)]), \
                "Trans-Jordan" : Territory_State("Britain", [Unit_state("Britain", 1)]), \
                "Turkey" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Ukraine S.S.R." : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 2), Unit_state("Germany", 3), Unit_state("Germany", 12), Unit_state("Germany", 13)]), \
                "Union of South Africa" : Territory_State("Britain", [Unit_state("Britain", 1)]), \
                "United Kingdom" : Territory_State("Britain", [Unit_state("Britain", 1), Unit_state("Britain", 1), Unit_state("Britain", 2), Unit_state("Britain", 3), Unit_state("Britain", 4), Unit_state("Britain", 5), Unit_state("Britain", 12), Unit_state("Britain", 12), Unit_state("Britain", 13)]), \
                "Venezuela" : Territory_State("Neutral", []), \
                # NEUTRAL ^
                "Vologda" : Territory_State("Russia", []), \
                "Wake Island" : Territory_State("America", [Unit_state("Japan", 1)]), \
                "West Indies" : Territory_State("America", []), \
                "West Russia" : Territory_State("Germany", [Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 1), Unit_state("Germany", 2), Unit_state("Germany", 3)]), \
                "Western Australia" : Territory_State("Britain", [Unit_state("Britain", 1)]), \
                "Western Canada" : Territory_State("Britain", [Unit_state("Britain", 1)]), \
                "Western United States" : Territory_State("America", [Unit_state("America", 1), Unit_state("America", 1), Unit_state("America", 4), Unit_state("America", 5), Unit_state("America", 12)]), \
                "Yakut S.S.R." : Territory_State("Russia", [Unit_state("Russia", 1)]),
                "Yunnan" : Territory_State("America", [Unit_state("America", 1), Unit_state("America", 1)])  }
                
        def export_reader(self):
                # Read xml
                # TODO: Get xml from save and export
                filename = "C:/Users/Brett/Desktop/xml_2020_07_16_World War II v5 1942 SE TR_round_1.xml"
                root = ET.parse(filename).getroot()
                territories = root.find("initialize").find("ownerInitialize").findall("territoryOwner")
                units = root.find("initialize").find("unitInitialize").findall("unitPlacement")
                resources = root.find("initialize").find("resourceInitialize").findall("resourceGiven")

                rename = {"Americans": "America", "British": "Britain", "Germans": "Germany", "Japanese": "Japan", "Russians": "Russia",
                          "infantry": 0, "artillery": 1, "armour": 2, "fighter": 11, "bomber": 12, "transport": 5, "submarine": 6, "destroyer": 7,
                          "cruiser": 8, "carrier": 9, "battleship": 10, "aaGun": 3, "factory": 4}

                # Set territory owners
                for elem in territories:
                        territory = elem.get("territory")
                        owner = rename[elem.get("owner")]
                        self.state_dict[territory].owner = owner

                # Destroy existing units
                for territory in self.state_dict.values():
                        territory.unit_state_list.clear()
                # Set units
                for elem in units:
                        unit_type = rename[elem.get("unitType")]
                        territory = elem.get("territory")
                        quantity = int(elem.get("quantity"))
                        owner = rename[elem.get("owner")]
                        for _ in range(quantity):
                                self.state_dict[territory].unit_state_list.append(Unit_state(owner, unit_type))

                # Get Production Units
                for elem in resources:
                        owner = rename[elem.get("player")]
                        quantity = int(elem.get("quantity"))
                        # TODO: Currently nowhere to keep track of PUs

                # will read through the two exports and update the above list according to the ownership and the units within

                # code to generate a file. need to learn how to command my computer to open the tripleA save and export

                # update the turn state variable
                pass
                
                
                
        def controls_suez(self):
                player = self.turn_state.player

                return (self.state_dict["Egypt"].owner == player) and (self.state_dict["Trans-Jordan"].owner == player)
                        
        def controls_panama(self):
                player = self.turn_state.player

                return self.state_dict["Central America"].owner == player

        def calc_movement(self, unit_state, current_territory, goal_territory):
                """
                a function that will check if a theoretical move is valid, and returns the movement required to move there. Returns -1 if impossible
                This replaces the old "passable" function
                """
                # Check if it would be possible to move to goal territory at all before doing BFS
                unit = self.rules.get_unit(unit_state.type_index)
                goal_territory_state = self.state_dict[goal_territory.name]

                # Sea units can only move to sea, and land and air units can only move to land
                if goal_territory.is_water != (unit.unit_type == "sea"):
                        return -1

                # Can't move into neutral territories
                if goal_territory_state.owner == "Neutral":
                        return -1

                # Non-combat movement
                if self.turn_state.phase == 5:
                        # Can't move into enemy territory
                        if goal_territory_state.owner != "Sea Zone" and \
                           self.rules.teams[goal_territory_state.owner] != self.rules.teams[unit_state.owner]:
                                return -1
                        # Can't move into territories with enemy units
                        for other_unit_state in goal_territory_state.unit_state_list:
                                if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                                        return -1

                # Breadth-First Search to find shortest path
                path = self.bfs(unit_state, current_territory.name, goal_territory.name, unit.movement - unit_state.moves_used)
                if not path:
                        return -1

                # Land/sea units can't move after combat, so use all remaining movement
                if self.turn_state.phase == 3:
                        # Check for enemy units/destroyers
                        enemy_units, enemy_destroyer = False, False
                        for other_unit_state in goal_territory.unit_state_list:
                                if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                                        enemy_units = True
                                        if self.rules.get_unit(other_unit_state.type_index).name == "destroyer":
                                                enemy_destroyer = True

                        if enemy_units:
                                # Exception for subs
                                if not (unit.name == "sub" and not enemy_destroyer):
                                        return unit.movement - unit_state.moves_used

                # Check if air units can return (only necessary if combat move)
                if unit.unit_type == 'air' and self.turn_state.phase == 3:
                        # TODO: Carriers can move to pick up fighters
                        return_path = self.bfs(unit_state, goal_territory.name, None, unit.movement - (len(path) - 1))
                        if not return_path:
                                return -1

                # We want number of edges, not number of nodes, so subtract 1
                return len(path) - 1

        def bfs(self, unit_state, root, target, max_dist):
                """
                a function that uses breadth-first search to find the shortest path between two nodes, within the movement limit of the unit
                if target is None, then search for available landing spot for plane
                """
                # Simultaneously keep track of parent nodes and visited nodes
                parents = {root: None}
                # FIFO queue to determine order to check nodes, as well as distance to reach them
                queue = [(root, 0)]

                while queue:
                        # Dequeue node and check every neighbor
                        current, dist = queue.pop(0)
                        for neighbor in self.rules.board[current].neighbors:
                                # Must be within movement range
                                if dist < max_dist:
                                        # Check if current neighbor is the target
                                        if not target or neighbor == target:
                                                if self.passable(unit_state, current, neighbor, True):
                                                        # Could just return distance, but path may be useful for debugging
                                                        path = [neighbor, current]
                                                        while path[-1] != root:
                                                                path.append(parents[path[-1]])
                                                        return path
                                        # If not valid target, check if it can be moved through, and hasn't yet been visited
                                        if neighbor not in parents.keys():
                                                if self.passable(unit_state, current, neighbor):
                                                        parents[neighbor] = current
                                                        queue.append((neighbor, dist + 1))

                # No path found within the movement limit, so return empty list
                return list()

        def passable(self, unit_state, current_territory_name, goal_territory_name, final_move=False):
                """
                a function that will check if a unit can move over this territory.
                Used by calc_movement function
                """

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
                        if self.turn_state.phase == 5 and final_move:
                                # Can't land in water, unless fighter + carrier
                                if territory_state.owner == "Sea Zone":
                                        if unit_state.name == "bomber":
                                                return False
                                        elif unit_state.name == "fighter":
                                                has_carrier = False
                                                # Check every unit in territory
                                                for other_unit_state in territory_state.unit_state_list:
                                                        if self.rules.teams[other_unit_state.owner] == self.rules.teams[unit_state.owner] and \
                                                                self.rules.get_unit(other_unit_state.type_index).is_carrier:
                                                                # TODO: How to check if carrier is full
                                                                has_carrier = True
                                                                break
                                                if not has_carrier:
                                                        return False
                                # Can't land in enemy territory
                                # TODO: How to check if territory was captured this turn
                                elif self.rules.teams[territory_state.owner] != self.rules.teams[unit_state.owner]:
                                        return False
                # Non-plane movement
                else:
                        # Non-combat movement
                        if self.turn_state.phase == 5:
                                # Can't move into enemy territory
                                if territory_state.owner != "Sea Zone" and self.rules.teams[territory_state.owner] != self.rules.teams[
                                        unit_state.owner]:
                                        return False
                                # Can't move into territories with enemy units
                                for other_unit_state in territory_state.unit_state_list:
                                        if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                                                return False
                        # Combat movement
                        elif self.turn_state.phase == 3:
                                # AA guns can't move in combat phase
                                if unit.name == "aa":
                                        return False

                                # Land/sea units must stop moving if there are enemy units (with exception for subs)
                                # But this only matters if this is not the unit's final move
                                if not final_move:
                                        # Check for enemy units/destroyers
                                        enemy_units, enemy_destroyer = False, False
                                        for other_unit_state in territory_state.unit_state_list:
                                                if self.rules.teams[other_unit_state.owner] != self.rules.teams[unit_state.owner]:
                                                        enemy_units = True
                                                        if self.rules.get_unit(other_unit_state.type_index).name == "destroyer":
                                                                enemy_destroyer = True

                                        # Land/sea units must stop moving if there are enemy units (with exception for subs)
                                        if enemy_units:
                                                if not (unit.name == "sub" and not enemy_destroyer):
                                                        return False

                # Otherwise, can move here
                return True
                        

# TODO: AA guns can shoot planes
#ADD IN TERRITORY OWNERSHIP AND ACCOUNT FOR IT IN THE PASSABLE FUNCTION
# neutrals cant move to, and enemy must be during combat phase. Tanks end all movement if battle
# check phase
#check if neighbor sea zones have ships that are not subs or trans            
        


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


def is_pomona_url (url):
    """
    checks if the url is a pomona link
    """
    
    return "pomona.edu" in url

def is_full_url (url):
    """
    checks if a url is a full link by determining if it has 'http'. Just checks
    for containnment. 
    """
    
    return "http" in url

def get_all_urls (url):
    """
    takes a url and finds all urls in the url after converitng to a string.
    Looks only at a href links. Returns a list of urls on this page.
    """
    
    try:
        context = ssl._create_unverified_context()
        page = urlopen(url, context=context)
        page = page.read().decode('ISO-8859-1') #now page is a string
    
        urls = []

        begin_index = page.find('"', page.find("a href"))
        
        while begin_index != -1:
            end_index = page.find('"', begin_index + 8)  
            #goes past the first " that starts the url. a href=" is 8 long
            if is_full_url(page[begin_index:end_index]):
                urls.append(page[(begin_index + 1):end_index])

            begin_index = page.find('"', page.find("a href", end_index))
        
        return urls

    except:
        return []
    """
    except urllib.error.HTTPError as e:
        raise ("the page you requested does not exist")    
    
    except urllib.error.URLError:
        raise ("The server does not exist")     
    """
    ## this didnt work for some reason, so I used the very blanet except
    # gave me the error encoutered enother exception in the exception.

def filter_pomona_urls (url_list):
    """
    returns a new list containing only pomona urls
    """
    #return filter(is_pomona_url, url_list)
    new_list = []
    
    for url in url_list:
        if is_pomona_url(url):
            new_list.append(url)
            
    return new_list

def crawl_pomona (start_url, to_visit, max_crawl):
    """
    Crawls through the pomona website, and returns a list of all possible links
    that can be visited from the link start_url. Max_crawl cuts it off after 
    that number of links have been crawled. To_visit is a queue.
    """
    
    to_visit.add(start_url)
    visited = []
    
    return crawl_helper(to_visit, max_crawl, visited)

def crawl_helper (to_visit, max_crawl, visited):
    """
    recursive loop that helps crawl_pomona
    """
    #print(max_crawl)
    
    if to_visit.is_empty() or max_crawl[0] == 0:
        return visited    
    
    else:
        next_url = to_visit.remove()
        
        if next_url in visited:
            crawl_helper(to_visit, max_crawl, visited)
            
        else: 
            visited.append(next_url)
            time.sleep(0.1)
            print("Crawling: " + next_url)
        
            urls = get_all_urls(next_url)
            urls = filter_pomona_urls(urls)
        
            for url in urls:
                to_visit.add(url)  #it will start from the first link
    
            max_crawl[0] -= 1
            crawl_helper(to_visit, max_crawl, visited)
        
        return visited
        
def write_pomona_urls (start_url, to_visit, max_crawl, filename):
    """
    Crawls pomona webpages and writes all the links onto a file called filename.
    """
   
    file = open(filename, "w")
    #DO NOT PUT THE NAME OF SOMETHING ALREADY EXISTANT
    
    links = crawl_pomona(start_url, to_visit, max_crawl)
    
    for link in links:
        file.write(link)
        file.write("\n")
    
    file.close()
  
#uncomment for experiement

#write_pomona_urls ("https://www.pomona.edu/", Stack(), [100], \
               #   "HURDURIMAHORSE_STACK.csv") 

#write_pomona_urls ("https://www.pomona.edu/", Queue(), [12], \
               #   "HURDURIMAHORSE_QUEUE.csv")

   
"""
DFS gives me a long list that, obviously, goes very deep first. It quickly 
becomes basically irrelevent calander links. 
Breath first search is definitely a better option here. DFS gave me tons and
tons of calander data that just went on and on for literally years. BFS gives
more pertinant links if you only have space for 100.
"""
