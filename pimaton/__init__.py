import sys
import logging
import argparse
from time import sleep


from .Pimaton import Pimaton
from .PimatonCam import PimatonCam
from .PimatonImage import PimatonImage
from .PimatonInput import PimatonInput
from .PimatonExceptions import PimatonExceptions, PimatonImageExceptions, PimatonCamExceptions
from .Singleton import Singleton
from ._version import version_str

logging.basicConfig()
logger = logging.getLogger("Pimaton")


def main():
    """
    Main program loop
    """

    try:
        args = retrieve_arguments(sys.argv[1:])
    except SystemExit:
        sys.exit(1)

    configure_logging(args.debug)
    logger.info('*** Welcome to pimaton! ***')

    # configure
    logger.info('*** Starting configuring Pimaton ***')

    try:
        # Config app.
        pimaton = Pimaton(args.config_file)

        # start app
        logger.info('*** Starting Pimaton Application ***')
        pimaton.run()
    except Exception as e:
        logger.critical('An error occured: %s' % e)
        sys.exit(1)


def retrieve_arguments(args):
    parser = argparse.ArgumentParser(description='Pimaton.')
    parser.add_argument("--debug", action='store_true',
                        help="Show debug output")
    parser.add_argument(
        "--config-file",
        help="Full path of the config file to load")
    parser.add_argument('-v', '--version', help="Display Pimaton version",
                        action='version', version='Pimaton ' + version_str)

    return parser.parse_args(args)


def configure_logging(debug=None):
    """
    Prepare log folder in current home directory.
    :param debug: If true, set the lof level to debug
    """
    logger = logging.getLogger("Pimaton")
    logger.addFilter(AppFilter())
    logger.propagate = False

    formatter = logging.Formatter(
        '%(asctime)s :: %(app_version)s :: %(message)s',
        "%Y-%m-%d %H:%M:%S")

    syslog = logging.StreamHandler()
    syslog.setFormatter(formatter)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # add the handlers to logger
    logger.addHandler(syslog)
    logger.debug("Logger ready")


class AppFilter(logging.Filter):
    """
    Class used to add a custom entry into the logger
    """

    def filter(self, record):
        record.app_version = "Pimaton-%s" % version_str
        return True
