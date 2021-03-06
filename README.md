pygen
============================

Command line tool that creates a skeleton Python script of the functions, arguments and return values as specified by a User

## Installation Instructions

* Symlink the generate.py file to an executable called pygen

``` console
sudo ln -s /Path/to/pygen/generate.py /usr/local/bin/pygen
```
Make sure you add the full path to the ``` generate.py ``` when symlinking the executable to the script

* Make the pygen file an executable

``` console
chmod +x /usr/local/bin/pygen
```

In the command line type ``` pygen --help ``` or ``` pygen -h``` for more info

## Example Output

The command: ``` pygen tester -f one two -c cube -i random ```  
will output this:  
![Terminal](https://raw.github.com/cjrieck/pygen/master/img/terminal.png)
And will result in a file that looks like this:
![Sublime Text](https://raw.github.com/cjrieck/pygen/master/img/sublime.png)
