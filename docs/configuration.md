# Configuration

The behaviour of _Meety_ can be configured in several ways, so that it hopefully helps you best.

_Meety's_ behaviour depends on the arguments on program invocation and on the contents of the configuration files. This document describes the latter (for an overview of the former, run `meety --help` or `cmeety --help` in your shell).

## Overview

This document describes in particular:

- [Which configuration files are loaded](#loaded-configuration-files)
- [How to create a configuration file](#initial-user-configuration-file)
- [How to define default arguments](#default-arguments)
- [How to allow other languages](#languages)
- [How to change the colour scheme](#colour-schemes)
- [How to clean/extend meeting data](#meeting-data)
- [Which connections are supported](#supported-connections) and [how to support new connections](#modify-connection-handlers)

## Loaded configuration files

_Meety_ usually loads multiple configuration files. On program start, _Meety_ loads
1. the default configuration provided by the application,
2. the user configuration and
3. all enabled _additional configurations_ (for languages and colour schemes).

Settings in a configuration file can overwrite settings of those configuration files that have been loaded earlier.

## Default configuration file

The [default configuration](../src/meety/static/config/defaults.yaml) makes _Meety_ usable out of the box. Among other things, it
- enables the English language pack `lang_en`;
- enables the "Magenta" colour pack `col_magenta`;
- extends bounds for time preferences slightly, by
    - five minutes for `time` specifications and
    - one hour for `date` specifications;
- provides connection handlers for
    - the _Zoom_ application, if installed, based on
        - _Zoom_-URLs of the form `https://<subdomain.>zoom.us/j/12345678?pwd=<PASSWORD_HASH>`,
        - _Zoom_-URLs of the form `https://<subdomain.>zoom.us/my/<USER_NAME>?pwd=<PASSWORD_HASH>`<br/>
          if a _Zoom_-ID like `123456789` is provided that can be used to replace the `<USERNAME>`,
        - _Zoom_-IDs of the form `123456789`;
    - arbitrary URLs opened by the default application on your system (usually a browser).

## Initial user configuration file

_Meety_ tries to load a user configuration file named `config.yaml` in a system-dependent directory, usually
- `/home/<username>/.config/meety/` on Linux,
- `/Users/<username>/Library/Application Support/meety` on MacOS and
- `C:\Users\<username>\AppData\Local\meety\meety` on Windows.

When this file does not exist, _Meety_ copies an [inactive template](../src/meety/static/config/user.yaml) to the directory on invocation. You can edit this template according to your needs.

Each user configuration has the following top-level entries:

```text
additional_config:
    # languages and colour schemes
    # ...
cli:
    # settings for 'cmeety', the command-line interface
    # ...
gui:
    # settings for 'meety', the graphical user interface
    # ...
meetings:
    # settings for the polishing of meeting specifications
    # and the rating of meetings
    # ...
connect:
    # settings for the connection handlers
    # (used to start meetings)
    # ...
```

## Additional configuration files

The attribute `additional_config` can contain dictionaries that describe which language and colour scheme configurations are loaded after the default and the user configuration. For example, the default configuration provides the following dictionary.
  
```text
  lang_de: yes # German
  lang_en: yes # English
  lang_es: yes # Spanish
  lang_fr: yes # French
  lang_it: yes # Italian
  col_magenta: yes
```

Now, assume that the following defines the `additional_config` in your user configuration.

```text
  lang_de: yes
  lang_es: no
  lang_fr: no
  lang_it: no
  col_magenta: no
  col_blue: yes
```

Then, _Meety_ loads the additional configuration files

- `language_en`,
- `language_de` and
- `col_blue`

because `col_magenta` is deactivated in the user configuration, which is applied _after_ the default configuration, where it is activated. Note also that both language configurations, `lang_en` and `lang_de` are active even though `lang_en` is not mentioned in the user configuration. If you want to deactivate `lang_en`, you have to overwrite the setting explicitly in the user configuration by adding `lang_en: no`, as is illustrated for Spanish, French and Italian here.

### Languages

Currently, _Meety_ provides only the following language packs.

- English (`lang_en`)
- French (`lang_fr`)
- German (`lang_de`)
- Italian (`lang_it`)
- Spanish (`lang_es`)

All language packs are active by default, as this probably does not hurt in most cases (and requires less configuration by the average user).

#### Intention
Language-specific settings only allow _Meety_ to understand other keys than `name`, `password` and so on in meeting specifications. The application interfaces so far use English only (although internationalisation is a goal for the future). Language configurations like this allow, for instance, to specify meetings like the following for a course at a German university and use it with _Meety_ without modifications.

```text
- Titel: Vorlesung Analysis
  URL: https://foo.bar.de/analysis
  Passwort: Cauchy
  Zeiten:
    Wochentag: Montag
  
- Titel: Übung Analysis
  URL: https://foo.bar.de/analysis-uebung
  Passwort: Weierstraß
```

This way, you can deploy the information more naturally to a target audience, even if this audience does _not_ use _Meety_ while those that use it, can directly connect to meetings (assuming that the respective language pack is enabled).

#### Details

Two aspects can be configured: names of weekdays (for time preferences) and keys of (all) meeting attributes.

If you want to register you own weekday names, add entries like the following to attribute `meetings.preferences.weekday.names` in your user configuration.
```text
meetings:
  preferences:
    weekday:
      names:
        1: [Monday, Mon]
        2: [Tuesday, Tue]
        3: [Wednesday, Wed]
        4: [Thursday, Thu, Thur, Thurs]
        5: [Friday, Fri]
        6: [Saturday, Sat]
        7: [Sunday, Sun]
```
Note that each weekday number expects a list of possible names. Such lists can be written like `[Monday, Mon]` or, alternatively, as follows.
```text
        1:
          - Monday
          - Mon
```

Additional keys can be made understood by the `synonym` action (further actions are [described below](#meeting-data)). The following is again an excerpt from `lang_en`.

```text
  # also belongs to the 'meetings' entry above
  attributes:
    - action: synonym
      output: name
      inputs:
        - title
        - meeting

    - action: synonym
      output: password
      inputs:
        - pwd
        - "*passcode*"
```

With these settings active, a meeting specification like

```text
- meeting: Jour Fixe
  url: anyhwere.com/
  pwd: 1234PASS
```

is internally handled as

```text
- name: Jour Fixe
  url: anyhwere.com/
  password: 1234PASS
```

by _Meety_ (without changing the file that specifies the meeting).

### Colour schemes

_Meety_ styles entries in meeting lists according to their matching status (matches a query, matches only a time preference, doesn't match). Out of the box, _Meety_ provides three colour schemes `col_blue`, `col_green` and `col_magenta`. The latter, `col_magenta` is enabled by default and defined as follows.

```text
cli:
  styles:
    matching_query:
      color: white
      background: on_magenta
      attrs: ["bold"]
    matching_preference:
      #color: white
      #background: on_magenta
      attrs: ["bold"]
    #others:
      #color: white            # default: None
      #background: on_magenta  # default: None
      #attrs: ["bold"]         # default: []

gui:
  styles:
    matching_query:
      color: "#ea195d"
      background: "#eee"
      attrs: ["bold"]
      selected: "#ddd"
    matching_preference:
      color: "#444"
      background: "#eee"
      attrs: ["bold"]
      selected: "#ddd"
    others:
      color: "#888"
      background: "#eee"
      attrs: ["bold"]
      selected: "#ddd"
```

The values for the command-line interface, under `cli.styles`, are passed to the [termcolor module](https://pypi.org/project/termcolor/). Have a look at the module's documentation for possible values.

The values for the graphical user interface, under `gui.styles`, are passed to functions from the _Qt module_. Currently, the only supported attribute for the latter is `bold`. Colours can be defined by some names (`black`, `blue`, ...) and hex codes (like `#RGB`, `#RRGGBB`, ...).

## Default arguments

If you want to apply some arguments on every invocation of `cmeety` or `meety`, you can add them to `cli.args` or `gui.args`, respectively. As an example, the following configuration makes both programs only load meetings from subdirectory `my-meetings` in the user's home directory (or from other paths, if specified explicitly on program invocation). Furthermore, provided passwords are automatically copied to the clipboard when a meeting is started.

```text
cli:
  args:
    - "--best"
    - "--copy-password"
    - "--only-explicit"
    - "--d ~/my-meetings"
gui:
  args:
    - "--copy-password"
    - "--only-explicit"
    - "--d ~/my-meetings"
    - "--window-width 800"
    - "--window-height 400"
```

## Meeting data

To simplify the specification of meetings in YAML, _Meety_ supports so-called "attribute actions". These actions can change the input data or infer new attributes from it. Currently, there are only four types of actions: `strip`, `infer`, `synonym` and `replace`. The `synonym` action is a restricted form of the `replace` action, which is [described above](#languages).

The next excerpt is an example of such actions, which we describe further below.

```text
meetings:
  attributes:
    - action: strip
      texts: ["-", " "]
      input: zoom-id

    - action: infer
      name: zoom-url
      value: https://zoom.us/j/{zoom-id}
```

### Strip action

The strip action allows to remove every text in a list of texts from an attribute _value_. The action above, for instance, removes all spaces as well as all dashes in attribute `zoom-id`. This way, _Meety_ will internally always work with value `123456789`, whether you specify it as `123-456-789` or `123 456 789` or `123456789`.

### Infer action

An infer action allows to add an attribute to a meeting based on other attributes. The name of the inferred attribute has to be specified and it will only be added to the meeting if there is _not already_ an attribute with that key. As an example, consider the following two meetings specifications.

```text
- name: Without URL
  zoom-id: 123-456-789
  
- name: With URL
  zoom-url: https://zoom.us/j/234567890
```

When exactly the two actions defined above are applied, _Meety_ internally handles the following meetings.

```text
- name: Without URL
  zoom-id: 123456789
  zoom-url: https://zoom.us/j/123456789  # automatically inferred
  
- name: With URL
  zoom-url: https://zoom.us/j/234567890
```

### Replace action

The replace action allows to replace existing attributes in meeting specifications conditionally. The condition is defined by a [regular expression](https://docs.python.org/3/library/re.html) passed to the action as attribute `expression`. The replacement only takes place if the value of attribute `substitute` is completely defined by the meeting specification. 

As an example, the next action deals with "personal" _Zoom_-URLs, which the _Zoom_ app seemingly does not know to handle correctly. _Note the use of single quotes_ to prevent the interpretation of escape sequences by the YAML loader.

```text
    - action: replace
      input: zoom-url
      expression: '(https://[^/]+)/my/[^?]+\?(.*)'
      substitute: '\1/{zoom-id}?\2'
```

Now, consider the next two meeting specifications.

```text
- name: My meeting
  zoom-url: https://zoom.us/my/my.name?pwd=safe
  zoom-id: 123456789
  
- name: Your meeting
  zoom-url: https://zoom.us/my/your.name?pwd=efas
```

Application of the replace action defined above, let's _Meety_ replace the first URL while keeping the second (as the corresponding meeting does not provide an attribute with key `zoom-id`). Hence, _Meety_ effectively works on the following specification.

```text
- name: My meeting
  zoom-url: https://zoom.us/j/123456789?pwd=safe  # replaced
  zoom-id: 123456789
  
- name: Your meeting
  zoom-url: https://zoom.us/my/your.name?pwd=efas
```

## Connections

The main goal of _Meety_ is to find the right meeting quickly out of a list of meetings and _to start it_. Whether a meeting can be started and _how_ it is started depends on

1. the _internal_ attributes of the meeting specification (after cleaning and inference) and
2. the active connection handlers.

Actions that change and extend a meeting specification internally have been described above. We now turn to the configuration of connection handlers.

### Supported connections

When the user chooses to start a meeting, _Meety_ considers, in a specific order, every connection handler that is

- _active_ and
- _passed all required information_ by the meeting.

Depending on the settings and the user's actions in the application interface, either the _first_ connection handler is used or the user selects one of the handlers explicitly.

To be _active_, a connection handler has to be defined and to appear in the order of connection handlers. If a handler is defined, it is automatically added to the order of connection handlers but it can be removed from the order later (to disable it, while keeping the definition).

Using the command-line interface, `cmeety --list-connection-handlers`, it is easy to determine all defined connection handlers and their order. As an example, on a Linux box where the _Zoom_ app is installed (i.e., `which zoom` is successful), _Meety_ is configured as follows by the default configuration.

```text
Handler definitions (3):
  - Zoom (app): zoom --url={zoom-url}
  - Zoom (browser): xdg-open {zoom-url}
  - Web (URL): xdg-open {url}

Order definitions (3):
  - Zoom (app)
  - Zoom (browser)
  - Web (URL)
```

The text after the colon in each entry of the handler definitions is the command that is executed by the handler. This command usually depends on attributes of the meeting specification, given in curly braces (e.g. `{zoom-url}` for the value of the attribute with key `zoom-url`). The order of definitions here shows that _Meety_ will first try to use the _Zoom_ app, which is possible if the meeting specification provides attribute `zoom-url`.

### Modify connection handlers

Via the user configuration file, you can

- [disable an already registered handler](#remove-connection-handler),
- [add a new connection handlers](#register-connection-handler) and
- [change the order of handlers](#change-connection-handler-order).

The following excerpt demonstrates the actions on `connect.handlers` briefly.

```text
connect:
  handlers:
    - action: remove
      name: zoom*

    - action: register
      name: test
      command: my-app {my-app-url}

    - action: prepend
      name: test
```

The type of the action is determined by the value of the attribute with key `action`. Below, the action types `remove`, `register` as well as `prepend` (and `append`) are explained.

#### Remove connection handler

A _remove_ action requires an attribute `name`. All registered handlers whose name match the given name _pattern_ are removed. The matching is case-insensitive. The first action above, for instance, would lead to the removal of the _Zoom_ handlers named `Zoom (app)` or `Zoom (browser)`, provided by the default configuration.

#### Register connection handler

A _register_ action requires an attribute `name` and an attribute `command`. The latter is executed on application of the handler. The command can refer to attributes of the meeting as to `my-app-url` above by the use of curly braces.

Optionally, via attributes `system` and `installed`, connection handlers can be registered conditionally, only when _Meety_ is running on the given system and/or the given application can be found.

#### Change connection handler order

Handlers can be added to the end or to the beginning of the connection handler list by actions `append` and `prepend`, respectively.

Note that _Meety_ prevents multiple occurrences of the same handler in the list of connection handlers. If you append an already registered handler, the append action is ignored. If you really want to move the handler to the end, remove it first and append it afterwards. If you prepend an already registered handler, the latter occurrence is removed.
