# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.api_secrets import coinmarketcap_api_key

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class ActionCoinRateAPI(Action):

    def name(self) -> Text:
        return "action_coin_rate_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
        'symbol':tracker.slots["coin"]
        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coinmarketcap_api_key,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            #print(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        if data.get("data", None):
            dispatcher.utter_message(text="El último valor de %s es de %.2f USD" % (tracker.slots["coin"], data["data"][tracker.slots["coin"]]["quote"]["USD"]["price"]))
        else:
            dispatcher.utter_message(text="Ha habido un error recuperando el valor de la moneda %s." % tracker.slots["coin"])
            dispatcher.utter_message(text="Comprueba que es un símbolo válido y que está bien escrito.")

        return []
