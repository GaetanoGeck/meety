# Command-line interface

After loading the meetings specifications, the command-line interface shows all _matching_ meetings. Below, we demonstrate the main options to influence the rating process for the three example meetings below.

```text
# Example meeting specifications in YAML
# Text after '#' is ignored by the application

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

## Only time preferences

**Summary:** Don't provide a search query
- `cmeety` show only meetings with matching time preference
- `cmeety --all` show all meetings but ranked by matching factor

```text
```text
# -- On a Tuesday at 11:00
> cmeety
No meeting found. Goodbye!

# -- On a Tuesday at 12:05
> cmeety
There's one matching meeting: My favourite lecture
Really connect (y/N)?

# -- On a Tuesday at 12:05
> cmeety --all                           # or '-a' for short
There are multiple matches:
  [1] My favourite lecture
  [2] Coffee
  [3] Another meeting
Which one do you want to choose?
```
Note that _My favourite lecture_ is the first entry (because it has a matching time preference while others have not).

## Time preferences and search query

**Summary:** Provide a search query (e.g. "meet")
- `cmeety meet` show only meetings with matching time or query preference
- `cmeety meet --all` show all meetings but ranked by matching factor

```text
# -- On a Tuesday at 11:00
> cmeety meet
There's one matching meeting: Another meeting
Really connect (y/N)?

# -- On a Tuesday at 12:05
> cmeety meet
There are multiple matches:
  [1] Another meeting
  [2] My favourite lecture
Which one do you want to choose?

# -- On a Tuesday at 12:05
> cmeety meet --all                     # or '-a' for short
There are multiple matches:
  [1] Another meeting
  [2] My favourite lecture
  [3] Coffee
Which one do you want to choose?
```
Now, _Another meeting_ is listed first because it matches the query _meet_. Meeting _My favourite lecture_ is listed second because of its matching time preference.

## Filter results

The list of matching meetings can be shortened in many cases with the use of one of the next two options:

- show only meeting with a maximal rating (`-b` or `--best`) or, even more restricted,
- show only the very first meeting (`-1` or `--first`) with a maximal rating.

## Further options

There are further options. You can get a quick overview with `cmeety --help`.
