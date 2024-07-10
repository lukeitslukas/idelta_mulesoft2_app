import sys

import import_declare_test
from splunklib import modularinput as smi
from app_logs_input_helper import stream_events, validate_input


class APP_LOGS_INPUT(smi.Script):
    def __init__(self):
        super(APP_LOGS_INPUT, self).__init__()

    def get_scheme(self):
        scheme = smi.Scheme('app_logs_input')
        scheme.description = 'app logs input'
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
        
        scheme.add_argument(
            smi.Argument(
                'organisation',
                title='organisation',
                description='The organisation the application is in',
                required_on_create=True
            )
        )
        
        scheme.add_argument(
            smi.Argument(
                'environment',
                title='environment',
                description='The environment the application is in',
                required_on_create=True
            )
        )
        
        return scheme

    def validate_input(self, definition: smi.ValidationDefinition):
        return validate_input(definition)

    def stream_events(self, inputs: smi.InputDefinition, ew: smi.EventWriter):
        return stream_events(inputs, ew)


if __name__ == '__main__':
    exit_code = APP_LOGS_INPUT().run(sys.argv)
    sys.exit(exit_code)
