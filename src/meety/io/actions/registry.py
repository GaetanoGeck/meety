from meety.logging import log

_action_classes = {}
_actions = []


def reset_options():
    global _actions
    _actions = []


def set_options(actions):
    if not isinstance(actions, list):
        log.expected("list", "actions", actions)
    else:
        for data in actions:
            try_to_add_action(data)


def register_action_class(name, action_class):
    log.debug(f"Register action class '{action_class.name}'.")
    _action_classes[name] = action_class


def get_action_class(data):
    action_name = data.get("action")
    if not action_name:
        log.expected("action name", "attribute 'action'", data)
    return _action_classes.get(action_name)


def get_actions():
    return _actions


def try_to_add_action(data):
    action_class = get_action_class(data)
    if not action_class:
        log.warning(f"Unknown action '{data}'.")
    else:
        _try_to_add_action_for_known_class(
            action_class,
            data
        )


def _try_to_add_action_for_known_class(action_class, data):
    try:
        action = action_class.create(data)
    except Exception as e:
        name = action_class.name
        log.warning(f"Cannot add {name} action '{data}'.")
        log.warning(str(e))
    else:
        action.set_conditions_from_dict(data)
        _actions.append(
            lambda d, level:
            action.apply(d, level)
        )
