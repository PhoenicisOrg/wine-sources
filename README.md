Alternative Wine sources for Phoenicis

[![Build Status](https://travis-ci.com/PhoenicisOrg/wine-sources.svg?branch=master)](https://travis-ci.com/PhoenicisOrg/wine-sources)

### How to use it
Create/update your `config.properties` (usually in `~/.Phoenicis`) with `webservice.wine.url = <json-url>`.

If Phoenicis does not show the correct versions, delete the cached `~/.Phoenicis/engines/wine/availableVersions.json`.

### Available Wine sources
* Lutris (Linux): https://github.com/PhoenicisOrg/wine-sources/master/lutris-linux.json
* WineHQ (OSX): https://github.com/PhoenicisOrg/wine-sources/master/winehq-macosx.json

### How it works
* Python scripts read the available versions from the download websites
* Travis runs the python scripts once a day to ensure that the .json files are up-to-date
