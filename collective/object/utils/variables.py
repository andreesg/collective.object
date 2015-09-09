

##
## Global definition of navigation tree variables
##

PERSON_INSTITUTION_FOLDER = '/zm/nl/personen-en-instellingen/personen-en-instellingen'
OBJECT_FOLDER = '/zm/nl/collectie'
EXHIBITION_FOLDER = '/zm/nl/bezoek-het-museum'
ARCHIVE_FOLDER = '/zm/nl/archiefstukken/archiefstukken'
INCOMINGLOAN_FOLDER = '/zm/nl/binnenkomende-bruiklenen/binnenkomende-bruiklenen/folder_contents'
OUTGOINGLOAN_FOLDER = '/zm/nl/uitgaande-bruiklenen/uitgaande-bruiklenen'
ARTICLE_FOLDER = "/zm/nl/bibliotheek/artikelen"
OBJECTENTRY_FOLDER = "/zm/nl/collectie/binnenkomst-objecten"
BIBLIOTHEEK_FOLDER = "/zm/nl/bibliotheek"

GENERAL_WIDGETS = {
        "identification": [
            {"name": "identification_objectName_objectname", "position": 9},
            {"name": "identification_objectName_category", "position": 9},
            {"name": "identification_identification_collections", "position": 3},
        ],
        
        "production_dating": [
        	{"name":"productionDating_productionDating", "position": 0},
			{"name":"productionDating_production_schoolStyles", "position":2},
			{"name":"productionDating_production_periods", "position": 4}
        ],
        
        "physical_characteristics": [
        	{"name":"physicalCharacteristics_keyword", "position": 1},
        	{"name":"physicalCharacteristics_technique", "position": 2},
			{"name":"physicalCharacteristics_material", "position": 3},
			{"name":"physicalCharacteristics_dimension", "position": 4},
        ],

        "iconography": [
			{"name":"iconography_generalSearchCriteria_generalthemes", "position": 1},
			{"name":"iconography_generalSearchCriteria_specificthemes", "position": 2},
			{"name":"iconography_contentSubjects", "position": 7},
			{"name":"iconography_contentPeriodDates", "position": 8}
        ],

        "associations": [
            {"name":"associations_associatedSubjects"},
            {"name":"associations_associatedPeriods"},
            {"name":"associations_associatedPersonInstitutions"}
        ],

        "value_insurance": [
            {"name":"valueInsurance_valuations"}

        ],

        "condition_conservation": [
            {"name":"conditionConservation_conditions"},
            {"name":"conditionConservation_preservationForm"}
        ],

        "acquisition": [
            {"name":"acquisition_methods"},
            {"name":"acquisition_places"},
            {"name":"acquisition_costs_offer_price_currency"},
            {"name":"acquisition_costs_purchase_price_currency"},
            {"name":"acquisition_fundings"}
        ],

        "disposal": [
            {"name":"disposal_finance_currency"}
        ],

        "ownership_history": [
            {"name":"ownershipHistory_history_exchangeMethod"},
            {"name":"ownershipHistory_history_place"},
            {"name":"ownershipHistory_historyOwner"}
        ],

        "location": [
            {"name":"location_normalLocation_normalLocation"},
            {"name":"location_currentLocation"}
        ],

        "field_collection": [
            {"name":"fieldCollection_fieldCollection_collectors"},
            {"name":"fieldCollection_fieldCollection_events"},
            {"name":"fieldCollection_fieldCollection_methods"},
            {"name":"fieldCollection_fieldCollection_places"},
            {"name":"fieldCollection_fieldCollection_placeFeatures"},
            {"name":"fieldCollection_fieldCollection_placeCodes"},
            {"name":"fieldCollection_habitatStratigraphy_stratigrafie"}
        ],

        "numbers_relationships": [
            {"name":"numbersRelationships_relationshipsWithOtherObjects_relatedObjects"}
        ]
}


"""identification_objectName_objectname
identification_objectName_category
identification_identification_collections
iconography_generalSearchCriteria_generalThemes
iconography_generalSearchCriteria_generalthemes
iconography_generalSearchCriteria_specificthemes
iconography_generalSearchCriteria_specificThemes
iconography_contentSubjects
iconography_contentPeriodDates
inscriptionsMarkings_inscriptionsAndMarkings
associations_associatedSubjects
associations_associatedPeriods
associations_associatedPersonInstitutions
valueInsurance_valuations
conditionConservation_conditions
conditionConservation_preservationForm
acquisition_methods
acquisition_places
acquisition_costs_offer_price_currency
acquisition_costs_purchase_price_currency
acquisition_fundings
disposal_finance_currency
ownershipHistory_history_exchangeMethod
ownershipHistory_history_place
ownershipHistory_historyOwner
location_normalLocation_normalLocation
location_currentLocation
fieldCollection_fieldCollection_collectors
fieldCollection_fieldCollection_events
fieldCollection_fieldCollection_methods
fieldCollection_fieldCollection_places
fieldCollection_fieldCollection_placeFeatures
fieldCollection_fieldCollection_placeCodes
fieldCollection_habitatStratigraphy_stratigrafie
numbersRelationships_relationshipsWithOtherObjects_relatedObjects"""

