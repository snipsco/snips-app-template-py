#!/usr/bin/env python3

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes

# imported to get type check and IDE completion
from hermes_python.ontology.dialogue.intent import IntentMessage

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR: str = "localhost"
MQTT_PORT: int = 1883
MQTT_ADDR: str = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


class Template(object):
    """Class used to wrap action code with mqtt connection
       Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except Exception:
            self.config = None

        # start listening to MQTT
        self.start_blocking()

    @staticmethod
    def intent_1_callback(self,
                          hermes: Hermes,
                          intent_message: IntentMessage):

        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(
            intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(
                intent_message.site_id,
                "Action 1", "")

    @staticmethod
    def intent_2_callback(self,
                          hermes: Hermes,
                          intent_message: IntentMessage):

        # terminate the session first if not continue
        hermes.publish_end_session()
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(
            intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(
                intent_message.site_id,
                "Action 2", "")

    @staticmethod
    def master_intent_callback(self,
                               hermes: Hermes,
                               intent_message: IntentMessage,):

        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'intent_1':
            self.intent_1_callback(hermes, intent_message)
        if coming_intent == 'intent_2':
            self.intent_2_callback(hermes, intent_message)

        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()


if __name__ == "__main__":
    Template()
