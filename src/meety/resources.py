import importlib.resources as resources


def get_icon_path(filename):
    from meety.static import icons as static_icons
    return get_static_path(static_icons, filename)


def get_config_path(filename):
    from meety.static import config as static_config
    return get_static_path(static_config, filename)


def get_spec_path(filename):
    from meety.static import spec as static_spec
    return get_static_path(static_spec, filename)


def get_desktop_path(filename):
    from meety.static import desktop as static_desktop
    return get_static_path(static_desktop, filename)


def get_static_path(module, filename):
    with resources.path(module, filename) as path:
        return str(path)
