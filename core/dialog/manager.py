import random

from core.nlp.engine import NLPEngine
from core.dialog.responses import *


class DialogManger:
    def __init__(self):
        self.engine = NLPEngine()
        
    def process_message(self, message):
        intent, entities = self.engine.predict(message)
        return self.engine.synthesis_text(self.get_response(intent, entities))
    
    def get_response(self, intent, entities):
        print(intent)
        
        if intent == "close_time":
            if "park" in entities:
                return random.choice(AMUSEMENT_PARK_TIME)
            elif "mall" in entities:
                return random.choice(BIGGEST_MALL_TIME)
            elif "museum" in entities:
                return random.choice(MUSEUM_TIME)
            else:
                return random.choice(MUSEUM_TIME)
        elif intent == "hologram_museum":
            return random.choice(HOLOGRAM_MUSEUM)
        elif intent == "weather":
            return "weather"
        elif intent == "location":
            if "park" in entities:
                return random.choice(AMUSEMENT_PARK_LOCATION)
            elif "mall" in entities:
                return random.choice(BIGGEST_MALL_LOCATION)
            elif "museum" in entities:
                return random.choice(MUSEUM_LOCATION)
            else:
                return random.choice(MUSEUM_LOCATION)
        elif intent == "greeting":
            return random.choice(GREATING)
        elif intent == "open_time":
            if "park" in entities:
                return random.choice(AMUSEMENT_PARK_TIME)
            elif "mall" in entities:
                return random.choice(BIGGEST_MALL_TIME)
            elif "museum" in entities:
                return random.choice(MUSEUM_TIME)
            else:
                return random.choice(MUSEUM_TIME)
        elif intent == "landmark":
            return random.choice(LANDMARK)
        elif intent == "hotel":
            return random.choice(HOTEL)
        elif intent == "high_rated":
            if "hotel" in entities:
                return random.choice(HOTEL_HIGH_RATED)
            elif "restaurant" in entities:
                return random.choice(RESTAURANT_HIGH_RATED)
            else:
                return random.choice(HOTEL_HIGH_RATED)
        elif intent == "famous":
            return random.choice(ZOO_FAMOUS)
        elif intent == "beach":
            return random.choice(BEACH)
        elif intent == "entrance_fee":
            return random.choice(MUSEUM_ENTRANCE_FEE)
        else:
            return "Sorry I didn't get that."
