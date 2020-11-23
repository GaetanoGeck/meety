# Select YAML files

_Meety_ can load meeting specifications from multiple YAML files. This way, you can, for example, manage the meetings for _Conference A_ and those for _Lecture B_ in different files.

## Options

**By default,** _Meety_ attempts to load all files with extensions `.yaml` or `.yml`

- in the current working directory of the application and
- in the user's home directory, usually
    - `/home/<username>/` on Linux,
    - `/Users/<username>/` on MacOS and
    - `C:\Users\<username>\` on Windows

You can prevent this by using the option `--only-explicit` or `-e` when you invoke _Meety_.

**Explicit loading of files.** Via the option `-f FILE` or `--file FILE` you can explicitly define a YAML file `FILE` from which _Meety_ loads meeting specifications. This option can be used repeatedly.

**Explicit loading from directories.** In a similar fashion you can ask _Meety_ to load all YAML files from a given directory using the `-d DIRECTORY` or `--directory DIRECTORY` option. This option can be used repeatedly too.

**Permanently set paths.** Instead of providing options on every invocation of _Meety_ you can add them to the configuration file. This way, they are used automatically on each invocation. This is described in more detail in the [section on default arguments](./configuration.md#default-arguments) of the configuration documentation.

## Example

As an example let us assume that the following files and directories are in your home directory.

```
friends.yaml
work.yaml
meetings/
    conferenceA.yaml
    lectureB.yaml
```

Let us consider some combinations of options (assuming that you invoke _Meety_ in the home directory):

- No options. Both files in the home directory are loaded:
    - `friends.yaml`
    - `work.yaml`
- Explicit files (`-f meetings/lectureB.yaml`). The named file is loaded additionally, resulting in three loaded files:
    - `friends.yaml`
    - `work.yaml`
    - `meetings/lectureB.yaml`
- Only explicit file (`-e -f meetings/lectureB.yaml`). The files in the home directory are not loaded anymore, resulting in a single loaded file:
    - `meetings/lectureB.yaml`
- Explicit directory (`-d meetings`). All files in the given directory are loaded additionally, resulting in four loaded files:
    - `friends.yaml`
    - `work.yaml`
    - `meetings/conferenceA.yaml`
    - `meetings/lectureB.yaml`
