from meety.io.actions import registry
from meety.io.actions.infer import InferAction
from meety.io.actions.replace import ReplaceAction
from meety.io.actions.strip import StripAction
from meety.io.actions.synonym import SynonymAction

InferAction.register()
StripAction.register()
SynonymAction.register()
ReplaceAction.register()
