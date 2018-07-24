# Gamest Reporter Plugin: Diablo III

This plugin enables [gamest](https://github.com/sopoforic/gamest) to report on
a running game of *Diablo III*.

## Installation

Install with pip:

```
pip install gamest-plugins-diablo-iii
```

## Configuration

The configuration is located in
`%LOCALAPPDATA%\gamest\DiabloIIIReporterPlugin.conf`. The default configuration
is:

```
[DiabloIIIReporterPlugin]
# Your user name from your Battle.Net profile URL. If your Battle.Net user name
# in the launcher is listed as GamestUser#1234, then put GamestUser-1234 here.
#
# user_name = GamestUser-1234

# The ID of the hero whose paragon level you wish to track.
#
# hero_id = 123456789

# How often to send notifications, in milliseconds. The default is once per
# hour.
#
# interval = 3600000

# Send a report when the game is started.
#
# send_begin = True

# Send a report when the game is closed.
#
# send_end = True
```

## License

Copyright (C) 2018  Tracy Poff

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
