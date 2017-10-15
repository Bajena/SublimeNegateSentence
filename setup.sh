#!/bin/bash
username=`id -un`
repo_url="https://raw.githubusercontent.com/Bajena/SublimeNegateSentence/master"
settings_url="$repo_url/NegateSentence"
packages_path="/Users/$username/Library/Application Support/Sublime Text 3/Packages/User"
settings_path="$packages_path/NegateSentence"

mkdir $settings_path

wget "$repo_url/negatesentence.py" -O "$packages_path/negatesentence.py"
wget "$settings_url/Default (OSX).sublime-keymap" -O "/Users/$username/Library/Application Support/Sublime Text 3/Packages/User/NegateSentence/Default (OSX).sublime-keymap"
wget "$settings_url/Default (Windows).sublime-keymap" -O "$settings_path/Default (Windows).sublime-keymap"
wget "$settings_url/Default (Linux).sublime-keymap" -O "$settings_path/Default (Linux).sublime-keymap"
wget "$settings_url/Default.sublime-commands" -O "$settings_path/Default.sublime-commands"
wget "$settings_url/Main.sublime-menu" -O "$settings_path/Main.sublime-menu"
