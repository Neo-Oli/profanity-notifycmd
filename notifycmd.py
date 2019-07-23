#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Executes a command when a message is received
"""

import prof
from subprocess import Popen
import time
from sys import platform

def secure(string):
    string=string.replace('\\','\\\\')
    string=string.replace("\"","\\\"")
    string=string.replace("$","\$")
    string=string.replace("`","\`")
    return string

def notifycmd(sender,message):
    command = prof.settings_string_get("notifycmd", "command", "")
    # replace markers with complex strings first to avoid "%%mittens"=>"(%%)mittens"=>"(%m)ittens"=>"<message>ittens" but rather do "(%%)mittens"=>"%mittens"
    command = command.replace("%%","{percentreplace}")
    command = command.replace("%s","${senderreplace}")
    command = command.replace("%m","${messagereplace}")


    command = command.replace("{percentreplace}","%")
    command = "set -f;senderreplace=\"{}\";messagereplace=\"{}\";{}".format(secure(sender),secure(message),command)
    p = Popen(['sh', '-c', command])

def prof_post_chat_message_display(barejid, resource, message):
    enabled = prof.settings_string_get("notifycmd", "enabled", "on")
    current_recipient = prof.get_current_recipient()
    if enabled == "on" or (enabled == "active" and current_recipient == barejid):
        notifycmd(barejid, message)
    return message


def prof_post_room_message_display(barejid, nick, message):
    enabled = prof.settings_string_get("notifycmd", "enabled", "on")
    rooms = prof.settings_string_get("notifycmd", "rooms", "mention")
    current_muc = prof.get_current_muc()
    mynick = prof.get_room_nick(barejid)
    # Don't notify for ones own messages
    if nick != mynick:
        if rooms == "on":
            if enabled == "on":
                notifycmd(nick + " in " + barejid, message)
            elif enabled == "active" and current_muc == barejid:
                notifycmd(nick, message)
        elif rooms == "mention":
            if mynick in message:
                if enabled == "on":
                    notifycmd(nick, message)
                elif enabled == "active" and current_muc == barejid:
                    notifycmd(nick, message)
    return message


def prof_post_priv_message_display(barejid, nick, message):
    if enabled:
        notifycmd(nick,message)

    return message


def _cmd_notifycmd(arg1=None, arg2=None):
    if arg1 == "on":
        prof.settings_string_set("notifycmd", "enabled", "on")
        prof.cons_show("Notifycmd plugin enabled")
    elif arg1 == "off":
        prof.settings_string_set("notifycmd", "enabled", "off")
        prof.cons_show("Notifycmd plugin disabled")
    elif arg1 == "active":
        prof.settings_string_set("notifycmd", "enabled", "active")
        prof.cons_show("Notifycmd plugin enabled for active window only")
    elif arg1 == "command":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/notifycmd")
        else:
            prof.settings_string_set("notifycmd", "command", arg2)
            prof.cons_show("notifycmd plugin command set to: " + arg2)
    elif arg1 == "rooms":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/notifycmd")
        else:
            prof.settings_string_set("notifycmd", "rooms", arg2)
            prof.cons_show("notifycmd plugin notifications for rooms set to: " + arg2)
    else:
        enabled = prof.settings_string_get("notifycmd", "enabled", "on")
        rooms = prof.settings_string_get("notifycmd", "rooms", "mention")
        command = prof.settings_string_get("notifycmd", "command", "")
        prof.cons_show("Notifycmd plugin settings:")
        prof.cons_show("enabled : " + enabled)
        prof.cons_show("command : " + command)
        prof.cons_show("rooms : " + rooms)

def prof_init(version, status, account_name, fulljid):
    synopsis = [
        "/notifycmd on|off|active",
        "/notifycmd command <command>",
        "/notifycmd rooms on|off|mention"
    ]
    description = "Executes a command when a message is received"
    args = [
        [ "on|off",      "Enable/disable notifycmd for all windows" ],
        [ "active",      "Enable notifycmd for active window only" ],
        [ "command <args>",    "Set command to execute. Replaces %s with sender, %m with message and %% with literal %." ],
        [ "rooms <args>",    "Setting for multi-user rooms. Set to 'on', 'off' or 'mention'. If set to mention it will only run it your nick was mentioned." ]
    ]
    examples = []

    prof.register_command("/notifycmd", 0, 2, synopsis, description, args, examples, _cmd_notifycmd)
    prof.completer_add("/notifycmd", [ "on", "off","active","command","rooms" ])
    prof.completer_add("/notifycmd rooms", [ "on", "off", "mention" ])
