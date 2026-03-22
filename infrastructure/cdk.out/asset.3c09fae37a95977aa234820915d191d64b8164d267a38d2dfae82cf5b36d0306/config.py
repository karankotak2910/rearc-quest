BUCKET_NAME = "rearc-data-quest-karan"

BLS_URL = "https://download.bls.gov/pub/time.series/pr/"

POPULATION_API = (
    "https://honolulu-api.datausa.io/tesseract/data.jsonrecords"
    "?cube=acs_yg_total_population_1"
    "&drilldowns=Year%2CNation"
    "&locale=en"
    "&measures=Population"
)

HEADERS = {
    "User-Agent": "rearc-data-quest (contact: karankotak64@gmail.com)",
    "Accept": "*/*"
} # adding headers to comply with BLS data policies - mentioned in hint