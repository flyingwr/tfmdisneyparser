from .tfmkeys import TfmKeys
from .transformice import Transformice

from main import endpoint
from tfmparser import Parser
parser: Parser = Parser(endpoint.is_local)

tokens = []