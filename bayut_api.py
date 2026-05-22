import aiohttp
from logger import logger
from config import Config

class BayutClient:
    # Map friendly location names to Bayut location slugs
    LOCATION_MAP = {
        "Dubai Marina": "/abu-dhabi/al-reem-island/shams-abu-dhabi/shams-gate-district/the-gate-tower/the-gate-tower-2",
        "Downtown Dubai": "/abu-dhabi/al-reem-island/shams-abu-dhabi/shams-gate-district/the-gate-tower/the-gate-tower-2",
        "JVC": "/abu-dhabi/al-reem-island/shams-abu-dhabi/shams-gate-district/the-gate-tower/the-gate-tower-2",
        "Business Bay": "/abu-dhabi/al-reem-island/shams-abu-dhabi/shams-gate-district/the-gate-tower/the-gate-tower-2",
    }

    def __init__(self):
        # Base URL for Bayut API on RapidAPI
        self.base_url = "https://uae-real-estate2.p.rapidapi.com/floorplans"
        self.headers = {
            "x-rapidapi-key": Config.BAYUT_API_KEY,
            "x-rapidapi-host": "uae-real-estate2.p.rapidapi.com"
        }

    def _get_location_slug(self, location: str) -> str:
        """Map the friendly location name to Bayut location slug."""
        return self.LOCATION_MAP.get(location, "/dubai/dubai-marina")

    async def fetch_properties(self, location: str, purpose: str = "for-sale", hitsPerPage: int = 5):
        """
        Fetch property listings from Bayut floorplans API based on user search criteria.
        """
        if not Config.BAYUT_API_KEY:
            logger.warning("No BAYUT_API_KEY provided. Returning dummy data for testing.")
            return self._get_dummy_data(location, purpose)

        location_slug = self._get_location_slug(location)
        querystring = {
            "location_slug": location_slug,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, headers=self.headers, params=querystring) as response:
                    response_text = await response.text()
                    if response.status == 200:
                        data = await response.json()
                        floorplans = data.get("floorplans", [])
                        if not floorplans:
                            logger.warning(
                                "Bayut API returned no floorplans for location=%s slug=%s",
                                location,
                                location_slug,
                            )
                        return floorplans
                    logger.error(
                        "Bayut API error: Status %s, Response: %s",
                        response.status,
                        response_text,
                    )
                    return []
        except Exception as e:
            logger.error(f"Error connecting to Bayut API: {e}")
            return []

    def _get_dummy_data(self, location: str, purpose: str):
        """Return dummy data for testing when no API key is provided."""
        return [
            {
                "id": 1,
                "title": f"Luxury Apartment in {location}",
                "price": 1500000 if purpose == "for-sale" else 120000,
                "rooms": 2,
                "baths": 2,
                "area": 1200,
                "agency": {"name": "Test Agency"},
                "coverPhoto": {"url": "https://via.placeholder.com/400x300"}
            },
            {
                "id": 2,
                "title": f"Spacious Studio in {location}",
                "price": 800000 if purpose == "for-sale" else 60000,
                "rooms": 0,
                "baths": 1,
                "area": 500,
                "agency": {"name": "Test Agency"},
                "coverPhoto": {"url": "https://via.placeholder.com/400x300"}
            }
        ]

bayut_client = BayutClient()
