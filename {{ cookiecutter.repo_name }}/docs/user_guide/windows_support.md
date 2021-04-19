# Windows support

This project includes useful functionality such as loading secrets as environment variables, but ignoring them from
version control. However, some of this functionality is Unix-based, and not supported natively on Windows. This page
covers how to configure your Windows system to use this Unix-based functionality in its entirety.

```{contents}
:local:
:depth: 2
```

## Requirements

```{warning}
We have only tested Windows support with the following requirements. Your experience may differ!
```

- Windows 10 64-bit system; this process _may_ work for other Windows versions
- Git for Windows [installed with the correct settings](#git-for-windows-setup)
- [Using ``load_dotenvrc`` in all files](#using-the-load_dotenvrc-function) or using the Windows release of `direnv`
  [set up](#setting-up-direnv)
  - If using `direnv`, you will need a user account with administrator privileges
    - Might be able to use an account with
      [`SeCreateSymbolicLinkPrivilege` privilege][microsoft-security-symbolic-links] privileges (untested)
- Set up `Make` via `git-bash`
  - This provides optional helper functions, but may require the same privileges as setting up `direnv` above

## Git for Windows setup

If you do not have [Git for Windows][git-for-windows], following the [fresh installs instructions](#fresh-installs).
Otherwise, check the configuration options for your [existing install](#existing-installs).

### Fresh installs

1. [Download Git for Windows][git-for-windows] on to your machine
2. In the folder containing the download, double-click on the executable `.exe` file
   - The file should be called `Git-<<<VERSION>>>-64-bit.exe`, where `<<<VERSION>>>` is the version of Git for Windows
3. Go through all the installation instructions until Step 10 "Configuring extra options", and check the
   `Enable symbolic links` checkbox
4. Continue with the rest of the installation instructions, and finish the installation
5. Check that symbolic links have been configured, as [outlined in the next section](#existing-installs)

### Existing installs

1. Open the Run dialog box (shortcut: Win + R), and type `%PROGRAMDATA%/Git` and press the "OK" button
2. In the File Explorer, you should see a file called `config`. Open this in your favourite text editor, and check that
   the `symlinks` variable is set to `true`
    - If not, you will need to re-open the `config` file in your text editor with administrator privileges to change
      the `symlinks` value to `true`

Once complete, you can now [set up `direnv`](#setting-up-direnv)

## Using the `load_dotenvrc` function

In the `src.utils` package there is a function called `load_dotenvrc`. This parses the `.envrc` file, creates a `.env`
file suitable and then loads the environment variables using the [`python-dotenv`][python-dotenv] package.
It will also load any `.envrc`-like file, such as the `.secrets` file, as has (limited) support for the `direnv`
`source_env` and `source_env_if_exists` commands (see the `direnv` [documentation][direnv-source-env] for more details).
Note, by default, it will override any existing environment variables with the same names.

To use this function, at the top of each script and/or notebook that uses environment variables from `.envrc`, add the
following lines:

```python
from src.utils import load_dotenvrc
load_dotenvrc()
```

See the docstrings/documentation for `load_dotenvrc` for further information.

## Setting up `direnv`

Once you have [set up Git for Windows](#git-for-windows-setup), you need to [download](#download-direnv) the Windows
release of [`direnv`][direnv] locally, and [set up symbolic links to the `direnv`
command](#set-up-direnv-symbolic-link).

### Download `direnv`

Go to the [`direnv` releases page][direnv-releases], and, for the latest release, download the Windows 64-bit
executable; this is usually called `direnv.windows-amd64.exe`.

For maintainability, create a `direnv` folder within your Git for Windows installation location, e.g.
`C:\Program Files\Git\usr\bin\direnv`, and move the download there. You _may_ need administrator privileges to do this.
Now [set up the symbolic link](#set-up-direnv-symbolic-link).

### Set up `direnv` symbolic link

1. Open the Run dialog box (shortcut: Win + R)
2. Type `cmd` to open the command prompt
3. Create a [symbolic link][git-for-windows-symbolic-links] so that entering the `direnv` command runs the
   `direnv.windows-amd64.exe` executable file.
   ```bash
   mklink direnv <<<FILEPATH TO direnv.windows-amd64.exe>>>
   ```
   where `<<FILEPATH TO direnv.windows-amd64.exe>>>` is the filepath to the `direnv.windows-amd64.exe` executable
   file. Remember, if your filepath contains spaces, you will need to double quote it, for example:
   ```bash
   mklink direnv "C:\Program Files\Git\usr\bin\direnv\direnv.windows-amd64.exe"
   ```

Now you can [add the `direnv` hooks to Git for Windows](#add-direnv-hooks-to-git-bash).

### Add `direnv` hooks to `git-bash`

1. Open `git-bash` — in the Start menu this should be listed in the Git folder as "Git Bash"
2. Create a `.bash_profile`, and add the `direnv` hook to it by entering the following command:
   ```bash
   echo 'eval "$(direnv hook bash)"' >> ~/.bash_profile
   ```
3. Restart `git-bash` by closing it, and opening `git-bash` again
4. Check that `direnv` has been correctly installed by entering `direnv`:
   ```bash
   direnv
   ```
   You should see a list of available `direnv` commands printed out!

## Setting up `Make` in `git-bash`

Follow these [steps][so-ezwinports] to get `Make` installed in `git-bash`:

1. Go to [ezwinports][ezwinports]
2. Download the `make-<<<VERSION>>>-without-guile-w32-bin.zip` file, where `<<<VERSION>>>` is the version of the `Make`
   port
3. Unzip the download
4. Copy all the folders _except_ `share`
5. Paste into the `mingw64` folder of your Git installation, for example at `C:\Program Files\Git\mingw64`. **Do not
   overwrite or replace any files**, only merge in the folders
6. Open `git-bash`, and type `make` — you should see the following message:
   ```bash
   make: *** No targets specified and no makefile found.  Stop.
   ```

To get all the `make` commands in the `Makefile` work, you also need to create a symbolic link to the Windows `more`
command:

1. Open the Run dialog box (shortcut: Win + R)
2. Type `cmd` to open the command prompt
3. Enter the following command:
   ```bash
   mklink more C:\Windows\System32\more.com
   ```

You should now be able to run all the `make` commands within the `Makefile`.

## Other useful instructions

Here are links to other useful instructions for getting this project running on Windows:

- [Using `git-bash` in PyCharm's terminal][so-pycharm-git-bash]
- [Setting up Anaconda for `git-bash`][so-anaconda-git-bash] — note you should `echo` into `~/.bash_profile` **not**
  `~/.profile`

[ezwinports]: https://sourceforge.net/projects/ezwinports/files/
[direnv]: https://github.com/direnv/direnv/
[direnv-issue-343]: https://github.com/direnv/direnv/issues/343#issuecomment-463502726
[direnv-releases]: https://github.com/direnv/direnv/releases
[direnv-source-env]: https://direnv.net/man/direnv-stdlib.1.html#codesourceenv-ltfileordirpathgtcode
[git-for-windows]: https://gitforwindows.org/
[git-for-windows-symbolic-links]: https://github.com/git-for-windows/git/wiki/Symbolic-Links
[microsoft-security-symbolic-links]: https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/create-symbolic-links
[python-dotenv]: https://saurabh-kumar.com/python-dotenv/
[so-anaconda-git-bash]: https://stackoverflow.com/a/56170202
[so-ezwinports]: https://stackoverflow.com/a/43779544
[so-pycharm-git-bash]: https://stackoverflow.com/a/20611422
