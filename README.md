# HTTP Log Monitoring Console App

## Acceptance Criteria

Create a simple console program that monitors HTTP traffic on your machine:

* Consume an actively written-to w3c-formatted HTTP access log (https://en.wikipedia.org/wiki/Common_Log_Format)
* Every 10s, display in the console the sections of the web site with the most hits (a section is defined as being what's before the second '/' in a URL. i.e. the section for "http://my.site.com/pages/create' is "http://my.site.com/pages"), as well as interesting summary statistics on the traffic as a whole.
* Make sure a user can keep the console app running and monitor traffic on their machine
* Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = {value}, triggered at {time}”
* Whenever the total traffic drops again below that value on average for the past 2 minutes, add another message detailing when the alert recovered
* Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons.
* Write a test for the alerting logic
* Explain how you’d improve on this application design

## Requirements

* Python3 & pip3 installed
* Minimal terminal size 145x25

## Install

```
make install
```

## Usage

```
usage: http-monitor [-h] [--file FILE] [--threshold THRESHOLD]
    [--section_expiration SECTION_EXPIRATION]
    [--section_refresh SECTION_REFRESH]

# e.g: http-monitor --file access.log --threshold 100 --section-expiration 120 --section-refresh=10
```

```
usage: http-generator [-h] [--file FILE] [--per_second PER_SECOND]

# e.g: http-generator --file access.log --per-second=100
```

## Code Structure

    ├── bin
    │   ├── http-generator
    │   └── http-monitor
    ├── src
    │   ├── monitoring
    │   │   ├── __init__.py
    │   │   ├── parser.py
    │   │   └── traffic.py
    │   ├── utils
    │   │   ├── __init__.py
    │   │   └── topic.py
    │   ├── widgets
    │   │   ├── __init__.py
    │   │   ├── alert.py
    │   │   ├── section.py
    │   │   └── stat.py
    │   ├── __init__.py
    │   ├── alert.py
    │   └── entry.py
    ├── tests
    │   └── monitoring
    │       ├── test_logparser.py
    │       └── test_traffic.py
    ├── .editorconfig
    ├── .gitattributes
    ├── .gitignore
    ├── LICENSE.txt
    ├── Makefile
    ├── README.md
    ├── requirements.txt
    └── setup.py

## License

This package is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).
