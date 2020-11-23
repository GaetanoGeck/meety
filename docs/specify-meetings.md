# Specify meetings in YAML

Let us consider three exemplary meeting specifications for _Meety_ of increasing complexity. If you're looking for a quick reminder on the specification, consider jumping to the [last example](#example-with-more-complex-time-preferences) or the overview on [types and formats of time preferences](#types-and-formats-of-time-preferences) directly.

Furthermore, the use of [language-specific attribute names and values](#language-specific-attributes) is described at the end of the document.

## Example without time preferences

We start with a very simple specification -- one without time preferences. You can find the contents also in the file [example-no-preferences.yaml](./example-no-preferences.yaml).

```text
- name: Algorithms
  url: http://my-university.edu/algorithms
  
- name: Coffee
  zoom-id: 123456789
  password: 1234
```

This file describes two meetings. On the top-level a meeting specification is a list of meetings where each meeting is started with a dash. Every meeting can (and should) provide additional information like

- a name,
- a password,
- connection information.

In the example above, the first meeting has attributes for keys `name` and `url`. The keys are followed by a colon (`:`) and the attribute's value. Note the indentation: `name` and  `url` start in the same column.

**Name.**
Each entry is required to have a attribute `name` as the corresponding value is used by _Meety_ to refer to the meeting. This entry can be explicit in the specification or implicitly derived. The latter happens, for example, if you have the additional configuration `lang_es` (for basic support of the Spanish language) activated that derives attribute `name: <VALUE>` if an attribute like `nombre: <VALUE>` occurs in the meeting specification.

**Password.**
If you specify a password via the `password` attribute, then _Meety_ can copy the password to the clipboard automatically if you tell it to do so. This way you do not have to remember (or even type) passwords.

**Other attributes.**
Apart from `name` and `password`, no other attributes are strictly required although you usually want to provide some information on how to connect to the meeting. _Meety_ successively tries some _connection handlers_. Each handler requires some specific information, for instance

- the default web handler requires a attribute `url` and would be applicable to the first meeting (but not to the second),
- a _Zoom_ handler requires a attribute `zoom-id` and would be applicable to the second meeting (but not to the first),
- another _Zoom_ handler requires a attribute `zoom-url` and would not be applicable to any of these meetings.

For [more information on connection handlers](./docs/configuration.md#supported-connections) see the documentation.

## Example with simple time preferences

Now, let us consider a slightly more complicated example. Here, we add _time preferences_ to both meetings from above. You can find the contents also in the file [example-simple-preferences.yaml](./example-simple-preferences.yaml).

Time preferences are used to filter and reorder the list of meetings: meetings whose time preference is matched at the time of querying are ranked higher than those where it is _not_ matched (if we exclude matching queries).

```text
- name: Algorithms
  url: http://my-university.edu/algorithms
  prefer:
    weekday: Tuesday
    time: 12:15 - 13:45

- name: Coffee
  zoom-id: 123456789
  password: 1234
  prefer:
    weekday: Monday - Friday
    time: 09:00 - 09:30
```

Let's assume that the first meeting belongs to a lecture that is held regularly every Tuesday afternoon. By providing the time preference

```text
weekday: Tuesday
time: 12:15 - 13:45
```

you indicate that _Meety_ can ignore this meeting on, say, a Monday, or on a Tuesday morning, late afternoon, and so on. At least, if it is not relevant for other reasons (a matching user query).

Please note that we use **explicit specifications for time preferences** here for the ease of description. These descriptions can be replaced by  one or more **specifications in [short format](#short-formats)**. For example, the explicit specification above can be replaced by `Tuesday, 12:15 - 13:45` or even `Tuesday, from 12:15 to 13:45`.

## Example with more complex time preferences

We conclude our small tour on example specifications for meetings by extending the previous YAML file once more. You can find the resulting contents in the file [example-complex-preferences.yaml](./example-complex-preferences.yaml).

```text
- name: Algorithms
  url: http://my-university.edu/algorithms
  prefer:
    - weekday: Tuesday
      time: 12:15 - 13:45
    - weekday: Thursday
      time: 14:15 - 15:45
      
- name: Coffee
  zoom-id: 123456789
  password: 1234
  prefer:
    weekday: Monday - Friday
    time: 09:00 - 09:30
```

As you can see, a meeting can have multiple time preferences, as the first meeting above. Note that, technically, the value of attribute `prefer` is a _list_ of (two) entries now, as indicated by the dashes. _Meety_ ranks a meeting higher if at least one of its time preferences is matched (and, conversely, lower if none is matched).

## Types and formats of time preferences

Time preferences can comprise three attributes: `weekday`, `time` and `date`, which can be used arbitrarily in combination or on their own. To each of these attributes, you can assign a single value, a range or a list of single values and ranges.

Here some examples for each attribute (assuming that the English language pack is active):

- _Weekday_
    - single value: `Monday` (or `1`)
    - range: `Monday - Friday` (or `1 - 5`)
    - list: `Tuesday - Thursday, Saturday` (or `2 - 4, 6`)
- _Time_
    - single value: `22:20`
    - range: `20:15 - 21:45`
    - list: `09:00 - 09:15, 16:00 - 16:15`
- _Date_
    - single value: `2020-12-31`
    - range: `2020-04-01 - 2020-04-30`
    - list: `2020-04-01 - 2020-04-30, 2020-12-31`

### Short formats

Time preferences can often be specified more naturally in a _short format_ as a string instead of a dictionary. If _Meety_ finds a time preference that is not a dictionary but a string, it tries to convert the string into a dictionary. This process depends on the language packs that are active. For instance a short specification like `Monday to Friday, 12 to 14 o'clock` is

1. split into parts `Monday to Friday` and `12 to 14 o'clock` by the commas;
2. then _Meety_ tries to find
    - a specification of for the `weekday` attribute,
    - a specification of for the `date` attribute and
    - a specification of for the `time` attribute.
    
In step 2, all parts are considered successively until _Meety_ is successful for one. In the example above, _Meety_ is successful for the `weekday` attribute on the first part and successful for the `time` attribute on the second part. It is not successful for the `date` attribute, which is hence left unspecified.

Some words in the specifications are removed internally, others are replaced. With the English language pack active, the word `from` is removed and the words `to` and `till` are replaced by `-` respectively. Hence, specifications like `from Monday to Friday` and `Monday to Friday` both result in an internal representation `Monday - Friday`.

**Splitting.** Note that if a semicolon occurs in a short format, _Meety_ splits by semicolons instead of commas. This way, you can use commas in each part (e.g. `Monday, Wednesday - Friday; 12:00 - 14:00`). Alternatively, you can use commas and words like `and` (e.g. `Monday and Wednesday to Friday, 12:00 - 14:00`).

### Formats for single values

The following formats for date and time specifications are understood by _Meety_, depending on the active language packs:

- _Date_
    - by default:
        - ISO format: `%Y-%m-%d` like `2020-12-31`
        - `%d.%m.%Y` and variants like `31.12.2020`, `31.12.20` and `31.12.'20`
    - with configuration `time_dmy` active:
        - `%d/%m/%Y` like `31/12/2020`
        - `%d/%m/%y` like `31/12/20`
    - with configuration `time_mdy` active:
        - `%m/%d/%Y` like `12/31/2020`
        - `%m/%d/%y` like `12/31/20`
- _Time_
    - by default:
        - ISO format: `%H:%M` like `12:34`
        - `%H.%M` like `12.34`
        - `%H` like `12` instead of `12:00`
    - English: `%H o'clock` like `16 o'clock`
    - French: various forms like
        - `12 h`
        - `12 heures`
        - `12.34 h`
        - `12.34 heures`
        - `12 h 34`
        - `12 heures 34`
    - German: various forms like
        - `12 Uhr`
        - `12:34 Uhr`
        - `12 Uhr 34`
    - Italian:
        - `le ore %H:%M` like `le ore 12:34`
        - `le ore %H.%M` like `le ore 12.34`
    - Spanish: various forms like
        - `%H.%M horas` like `12.34 horas`
        - `las %H.%M horas` like `las 12.34 horas`

**Weekdays.**
If you have additional configurations for other languages activated, like `lang_fr` for French, then you can also write `lundi - vendredi` instead of `Monday - Friday` and so on. In fact, to understand `Monday - Friday`, _Meety_ requires configuration `lang_en` to be active. Language-specific configurations usually also support abbreviations (`Mon` for `Monday`, `Lu` for `lundi` and so on). For more detailed information, have a look at the language configuration files in the [config source directory](../src/meety/static/config/).

Numbers are always understood, even when no additional configuration is active. You can find [more information on language specific configuration](./docs/configuration.md#languages) in the documentation.

## Language-specific attributes

Each language pack defines a set of synonyms for certain attribute names and date specifications that are understood by _Meety_.

Let us consider one of the specifications from above again.

```text
- name: Algorithms
  url: http://my-university.edu/algorithms
  prefer: Tuesday, 12:15 to 13:45

- name: Coffee
  zoom-id: 123456789
  password: 1234
  prefer: Monday to Friday, 
```

Here, all attributes `name`, `url`, `prefer` and so on have a special meaning to _Meety_. Instead of `name` it could be more natural in some descriptions to use the word `title` or `meeting` and indeed _Meety_ automatically renames attributes with the latter name internally to `name` so that they can be processed accordingly.

The following is a list of possible synonyms for attributes (by language pack):

- **name:**
    - English: _title_ and _meeting_
    - French: _nom_ and _titre_
    - German: _Titel_ and _Meeting_
    - Italian: _nome_ and _titolo_
    - Spanish: _nombre_ and _título_
- **password:**
    - English: _pwd_ and phrases containing _passcode_
    - French: _mot de passe_, _mdp_ and _code d'accès_
    - German: phrases containing _kennwort_ and _passwort_
    - Italian: none
    - Spanish: none
- **zoom-id:**
    - English: _meeting id_
    - French: none
    - German: none
    - Italian: none
    - Spanish: none
- **prefer:**
    - English: _time_, _times_, _timing_ and _when_
    - French: _temps_ and _quand_
    - German: _Zeit_, _Zeiten_ und _wann_
    - Italian: _tempo_ and _quando_
    - Spanish: _tiempo_ and _cuándo_
- **weekday:**
    - English: _day_ and _days_
    - French: _jour_ and _jours_
    - German: _Wochentag_, _Tag_ und _Tage_
    - Italian: _giorno_ and _giornos_
    - Spanish: _día_ and _días_
- **date:**
    - English: none
    - French: none
    - German: _Datum_
    - Italian: _data_
    - Spanish: _fecha_
- **time:** (only under `prefer`)
    - English: none
    - French: _jour_ and _jours_
    - German: _Zeit_ und _Zeiten_
    - Italian: _tempo_
    - Spanish: _tiempo_
