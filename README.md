# Check

[![Build Status](https://travis-ci.org/bcho/check.svg)](https://travis-ci.org/bcho/check)

Check your server like a boss.



## Usage

```bash
$ check -c config.json
```


## Config.json

```json
{
  "in_charge": [
    {
      "name": "Travis Bickle",
      "email": "travis.bickle@example.com"
    },
    {
      "name": "Besty",
      "email": "besty@example.com"
    }
  ],
  "reporters": {
    "email": {
      "crendential": {
        "username": "watchmen@example.com",
        "password": "watchmen-passw0rd",
        "smtp": "smtp.example.com:587"
      },
      "formats": {
        "short": "Site {site['name']} is down!",
        "long": "Your site {site['name']} is down since {happened_at}!"
      }
    },
    "cli": {
      "formats": {
        "short": "Site {site['name']} is down!",
        "long": "Check time: {happened_at}"
      }
    }
  },
  "sites": [
    {
      "name": "My Cool Site",
      "url": "http://cool.example.com"
    },
    {
      "name": "Goole is Down",
      "url": "https://google.com"
    }
  ]
}
```

### `in_charge`

Specify list of people you want to notify when a incident happened here.

##### Fields:

| name | description | required? |
|:------:|:-------------:|:-----------:|
| name | alias name | yes |
| email | receiver's email address | no |

- `email`: If user's `email` is provided, they will receive a warning email for the incident.


### `reporters`

Enabled report generators. Each generator can customize the `incident report` format.


##### Report Format Fields

| name | description | required? |
|:------:|:-------------:|:-----------:|
| short | summarize report | yes |
| long | detailed report | yes |

Each `incident report` will contain:

- site name
- site url
- incident happened time string, format is [ISO8601][iso8601].

```python
incident_report = {
    'site': {
      'name': 'test',
      'url': 'http://test.domain'
    },
    'happened_at': '2014-11-01T15:42:00.000000+00:00'
}
```


[iso8601]: http://en.wikipedia.org/wiki/ISO_8601

#### Email Handler

If you want to use email handler, you should provide email sender's crendential
settings.

##### Fields:

| name | description | required? |
|:------:|:-------------:|:-----------:|
| username | login name | yes |
| password | login password | yes |
| smtp | smtp server | yes |


### `sites`

List of sites you want to monitor.

##### Fields:

| name | description | required? |
|:------:|:-------------:|:-----------:|
| url | site's url | yes |
| name | alias name | no, defaults to `url`|
