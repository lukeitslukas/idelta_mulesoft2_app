import import_declare_test

import sys

from splunklib import modularinput as smi
from discovery_input_helper import stream_events, validate_input


class DISCOVERY_INPUT(smi.Script):
    def __init__(self):
        super(DISCOVERY_INPUT, self).__init__()

    def get_scheme(self):
        scheme = smi.Scheme('discovery_input')
        scheme.description = 'discovery input'
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True
        scheme.use_single_instance = False

        scheme.add_argument(
            smi.Argument(
                'account',
                title='account',
                description='The name used to login',
                required_on_create=True
            )
        )
        
        return scheme

    def validate_input(self, definition: smi.ValidationDefinition):
        return validate_input(definition)

    def stream_events(self, inputs: smi.InputDefinition, ew: smi.EventWriter):
        return stream_events(inputs, ew)


if __name__ == '__main__':
    exit_code = DISCOVERY_INPUT().run(sys.argv)
    sys.exit(exit_code)
