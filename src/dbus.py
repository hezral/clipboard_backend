# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>
import subprocess
import ast

app_command = ("gdbus call -e -d org.gnome.Shell -o /org/gnome/Shell -m org.gnome.Shell.Eval global.get_window_actors\(\)[`gdbus call -e -d org.gnome.Shell -o /org/gnome/Shell -m org.gnome.Shell.Eval global.get_window_actors\(\).findIndex\(a\=\>a.meta_window.has_focus\(\)===true\) | cut -d\"'\" -f 2`].get_meta_window\(\).get_wm_class\(\)")
app_process = subprocess.Popen(app_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
app_retval = app_process.stdout.read()
app_retcode = app_process.wait()

app_tuple_string = app_retval.decode('utf-8').strip()
# We now have a string that looks like:
# (true, "\"Qur'an App"\")

app_tuple_string = app_tuple_string.replace("(true", "(True")
app_tuple_string = app_tuple_string.replace("(false", "(False")
# We now have a string that looks like a python tuple:
# (True, "\"Qur'an App"\")

app_tuple = ast.literal_eval(app_tuple_string)
app = app_tuple[1]
# We now have a string with quotes in it that looks like:
# "Qur'an App"

app = ast.literal_eval(app)
# We now have a string that looks like:
# Qur'an App

print(app)