## snips-app-template-py

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/snipsco/snips-app-template-py/blob/master/LICENSE)

> This template is made for **_python >= 3.7_**

This is a template helping you build the first Snips Voice App quickly.

> This template is modified from [an origin python template](https://github.com/snipsco/snips-actions-templates) but using a riche action code structure. The origin template is made for connecting to snippets, you can use it to build action for a single intent easily. However, if you already know how snips action code works with bundles, feel free to choice the one you you like best!

## Template Organisation

Files listed below are required as a minimum construction, which ensures that this action code can be managed by `snips-skill-server`. But it does not mean you should only have these files.
With a simple action, it can be written in the `action-app_example.py` file. However with some more complicated action code, it's better to have a specific class file for it.

```bash
└── snips-app-template-py
    ├── action-app_template.py          # main handler for intents
    ├── snipsTools.py                   # some useful tools
    ├── config.ini.default              # default app configuration
    ├── requirements.txt                # required dependencies
    └── setup.sh                        # setup script
```

## Files Explanation in Detail

### `action-app_template.py`

This is the file used to bind your action codes with MQTT bus. It helps to read the configuration file, setup MQTT connection, subscribe to Specific topics and setup callback functions.

A simplified code is shown below:

```python
#!/usr/bin/env python3.7

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes

# imported to get type check and IDE completion
from hermes_python.ontology.dialogue.intent import IntentMessage

CONFIG_INI = "config.ini"

# if this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
#
# hint: MQTT server is always running on the master device
MQTT_IP_ADDR: str = "localhost"
MQTT_PORT: int = 1883
MQTT_ADDR: str = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


class Template:
    """class used to wrap action code with mqtt connection
       please change the name referring to your application
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
    def intent_1_callback(hermes: Hermes,
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
    def intent_2_callback(hermes: Hermes,
                          intent_message: IntentMessage):

        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(
            intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(
            intent_message.site_id,
            "Action 2", "")

    # register callback function to its intent and start listen to MQTT bus
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intent('intent_1', self.intent_1_callback)\
            .subscribe_intent('intent_2', self.intent_2_callback)\
            .loop_forever()


if __name__ == "__main__":
    Template()
```

Note: because we can now use type check, and IDE can use that to give better completion, we import necessary definition and add types in methods.

The beginning is similar to most Python codes, it imports all the necessary dependencies / modules. It also defines the config file name (Usually set to `config.ini` and put this file as the same directory with this code file) and MQTT connection info. If the App you are making is supposed to run on a satellite or some other devices, we recommend that the MQTT connection info should be loaded from the external `config.ini` file instead of fixing it in the code.

The main part of this code is composed of one class - `Template`, which is used to bind App related action code with MQTT bus. This class should be named corresponding to the App.

The code is mainly composed by different intent callback functions such as `intent_1_callback`, `inent_2_callback`. Inside each callback function is the place to write the intent related action code.

> For the intent callback function, it's better to terminate the session first if there is no need to continue. This can prevent other snips components (Like dialog-manager, hotword..) from being blocked by the action code.

`start_blocking()` is used to register callback functions with its associated intents then starts to listen on MQTT bus.

At the beginning of `__init__()`, `SnipsConfigParser` is called to provide a configuration dictionary. This part is not mandatory and can be removed if not needed.

### `snipsTools.py`

This file provides some common useful class but is not part of the action code. For the moment, it only has the `SnipsConfigParser`.

#### `read_configuration_file (configuration_file)`

```
Read configuration file and return a dictionary.
​
:param configuration_file: configuration file. E.g. "config.ini".
:return: the dictionary representation of the config file.
```

#### `write_configuration_file (configuration_file, data)`

```
Write configuration dictionary to config file.
​
:param configuration_file: configuration file. E.g. "config.ini".
:data: the dictionary contains the data to save.
:return: False if failed to write.
```

### `config.ini.default`

This is the file used to save action code configurations. An example is shown below:

```bash
# no section for preset values
actionName=example
​
[secret]
#empty value for secret values
passExample=
```

You may notice that the config file required by `action-app_template.py` is named `config.ini` but `config.ini.default`. This is because if we make `config.ini` file tracked by git, then the user setting will be rewritten to default during each update pull. The solution here is using `setup.py`, it will copy `config.ini.default` to `config.ini` only if the later one does not exist.

Initially, there are several configuration lines shown as the example, this should be changed. This file is not mandatory for a template. If the action code never uses configuration, this file can be removed.

> **_Beware! Do not use any space to separate key, value and the "=" sign._**

### `requirements.txt`

This file is holding the project dependencies.

```bash
# Bindings for the hermes protocol
hermes-python>=0.8
```

If there are some libraries that needs to be installed in your code, append it here.

### `setup.sh`

This file is used to set up the running environment for the action code. Most of the time, you don't need to modify it.

```bash
#!/usr/bin/env bash
set -e

if [ ! -e "./config.ini" ]; then
    cp config.ini.default config.ini
fi

VENV=venv

if [ ! -d $VENV ]; then
    PYTHON=`which python3.7`

    if [ -f $PYTHON ]; then
        virtualenv -p $PYTHON $VENV
    else
        echo "could not find python3.7"
    fi
fi

. $VENV/bin/activate

pip3 install -r requirements.txt
```

## An Example APP

A Joke App based on this template is documented [here](https://docs.snips.ai/guides/raspberry-pi-guides/create-an-app/python-template#example-joke-app).

## Contributing

Please see the [Contribution Guidelines](https://github.com/snipsco/snips-app-template-py/blob/master/CONTRIBUTING.md).

## Copyright

This library is provided by [Snips](https://www.snips.ai) as Open Source software. See [LICENSE](https://github.com/snipsco/snips-app-template-py/blob/master/LICENSE) for more information.
