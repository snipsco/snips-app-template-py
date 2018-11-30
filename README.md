## snips-app-template-py
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/snipsco/snips-app-template-py/blob/master/LICENSE)

> This template is made for ***python 2.7***

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
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
​
from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
​
CONFIG_INI = "config.ini"
​
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))
​
class Template(object):
    """Class used to wrap action code with mqtt connection

        Please change the name refering to your application
    """
​
    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None
​
        # start listening to MQTT
        self.start_blocking()

    # --> Sub callback function, one per intent
    def intent_1_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
​
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id,
                                                    "Action1 has been done")
​
    def intent_2_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
​
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
​
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id,
                                                    "Action2 has been done")
​
    # More callback function goes here...
​
    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'intent_1':
            self.intent_1_callback(hermes, intent_message)
        if coming_intent == 'intent_2':
            self.intent_2_callback(hermes, intent_message)
​
        # more callback and if condition goes here...
​
    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()
​
if __name__ == "__main__":
    Template()
```

The beginning is similar to most Python codes, it imports all the necessary dependencies / modules. It also defines the config file name (Usually set to `config.ini` and put this file as the same directory with this code file) and MQTT connection info. If the App you are making is supposed to run on a satellite or some other devices, we recommend that the MQTT connection info should be loaded from the external `config.ini` file instead of fixing it in the code.

The main part of this code is composed of one class - `Template`, which is used to bind App related action code with MQTT bus. This class should be named corresponding to the App.

There are mainly two kinds of callback functions in the code, `master_intent_callback` and sub callback functions such as `intent_1_callback`, `inent_2_callback`. The former one is self-explained, it will be called when an intent is successfully detected. Inside this master callback, there are several sub callback functions, which will be called referring to the specific intent.
Inside each sub callback function is the place to write the App related code.

> For each sub callback function, it's better to terminate the session first if there is no need continuing it. This can prevent other snips components (Like dialog-manager, hotword..) from being blocked by the action code.

`start_blocking()` is used to register master callback function and then starts to listen on MQTT bus.

At the beginning of `__init__()`, `SnipsConfigParser` is called to provide a configuration dictionary. This part is not mandatory and can be removed if not needed.

### `snipsTools.py`
This file provides some common useful class but is not part of the action code. For the moment, it only has the `SnipsConfigParser`.

#### `read_configuration_file`
(configuration_file)
```
Read configuration file and return a dictionary.
​
:param configuration_file: configuration file. E.g. "config.ini".
:return: the dictionary representation of the config file.
```

#### `write_configuration_file`
(configuration_file, data)
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

You may notice that the config file required by `action-app_template.py` is named `confing.ini` but `config.ini.default`. This is because if we make `config.ini` file tracked by git, then the user setting will be rewritten to default during each update pull. The solution here is using `setup.py`, it will copy `config.ini.default` to `config.ini` only if the later one does not exist.

Initially, there are several configuration lines shown as the example, this should be changed. This file is not mandatory for a template. If the action code never uses configuration, this file can be removed.

> ***Beware! Do not use any space to separate key, value and the "=" sign.***

### `requirements.txt`
 This file is holding the project dependencies.
```bash
# Bindings for the hermes protocol
hermes-python>=0.1
```

If there some libraries that needs to be installed in your code, append it here.

### `setup.sh`
This file is used to set up the running environment for the action code. Most of the time, you don't need to modify it.

```bash
#/usr/bin/env bash -e
​
if [ ! -e "./config.ini" ]
then
    cp config.ini.default config.ini
fi

VENV=venv
​
if [ ! -d "$VENV" ]
then
​
    PYTHON=`which python2`
​
    if [ ! -f $PYTHON ]
    then
        echo "could not find python"
    fi
    virtualenv -p $PYTHON $VENV
​
fi
​
. $VENV/bin/activate
​
pip install -r requirements.txt
```

## An Example APP

A Joke App based on this template is documented [here](https://docs.snips.ai/guides/raspberry-pi-guides/create-an-app/python-template#example-joke-app).

## Contributing

Please see the [Contribution Guidelines](https://github.com/snipsco/snips-app-template-py/blob/master/CONTRIBUTING.md).

## Copyright

This library is provided by [Snips](https://www.snips.ai) as Open Source software. See [LICENSE](https://github.com/snipsco/snips-app-template-py/blob/master/LICENSE) for more information.