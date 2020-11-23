# Meety - quickly start online meetings from YAML

**Problem.**
Online meetings provide a useful means to communicate with others. With an increasing number of meetings, however, it can get difficult to remember or pick the right meeting location, user id, password and so on.

**Goal.**
_Meety_ aims to provide a quick and easy way to start the right online meeting from a list of predefined meetings. Meetings are defined in YAML, a clean and simple format that is well readable for humans and machines alike. Thus, you can

- view and edit the meetings with your favourite text editor and
- sensibly share them with other users, even if they don't use _Meety_.
  (Think of conferences, lectures, ...)
  

**Features.**
_Meety_ can can load meetings from one or multiple YAML files. The meetings can be filtered by time preferences and/or keywords. After choosing a meeting, _Meety_ will try to connect to it based on the information the meeting provides. 

Out of the box, _Meety_ supports meetings via the browser and via the _Zoom_ app. However, the application can easily be configured to handle other types of meetings too, as described in the documentation.

_Meety_ ships with a graphical user interface (program `meety`) and with a command line interface (program `cmeety`).

Meetings are specified in YAML and may look like this.

```text
# FIRST MEETING (Coffee round with colleagues, every morning)
- name: Coffee
  zoom-url: https://zoom.us/j/123456789
  prefer: Monday to Friday, 9 to 10 o'clock
  # short format for time specifications (also for other languages)

# SECOND MEETING (lecture, each Tuesday and Thursday)
- name: My favourite lecture
  url: https://my-university.edu/my-fav-lecture
  prefer:
    - weekday: Tuesday
      time: 12:00 - 14:00
      date: 2020-10-01 - 2021-03-31
    - weekday: Thursday
      time: 14:00 - 16:00
      date: 2020-10-01 - 2021-03-31
  # explicit format for time specifications (also for other languages)

# THIRD MEETING (without time preferences)
- name: Another meeting
  zoom-id: 987-654-321
```

**More information** can be found in the extended [README on GitHub](https://github.com/GaetanoGeck/meety).
