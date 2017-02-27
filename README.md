# profanity-notifycmd
Plugin for Profanity to launch a custom shell command when a message is received



## Requirements



## Installation

1. Download the script

2. Launch Profanity

3. Install the plugin with the following command

```
/plugins install ~/profanity-notifycmd/notifycmd.py

```

## Configuration

### Turn the plugin on

`/notifycmd on`

### Turn the plugin off

`/notifycmd off`

### Only notify for the currently active window

`/notifycmd active`

### Enable/Disable notifications for all messages in rooms

`/notifycmd rooms on|off`

### Set command to exectue

`/notifycmd command <command>`

Set command to execute. You can use the following markers:

 * %s -> sender
 * %m -> message
 * %% -> literal %

Warning: For security reasons all quotes (') get replaced by ’. You should put all your markers in single quotes. Without doing this you're potentially vulnerable to remote code execution. 

### Command Examples

#### Android notifications for Termux
You'll need [Termux:API](https://play.google.com/store/apps/details?id=com.termux.api) and the termux-api package (`apt install termux-api`).

```
/notifycmd command termux-notification -t 'Profanity: %s says:' -c '%m' --vibrate 500,100,500
```
![Screenshot](screenshot.png)

#### Send an Email as a notification

```
/notifycmd plugin command set to: echo '%m' | mutt -s 'New message from %s' name@domain.tld
```

