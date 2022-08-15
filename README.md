# picotick

A simple script that fetches and dumps simple market prices. Uses the [Twelve Data](https://twelvedata.com/) REST API.

Note that the Free plan for Twelve Data does not support indices, but it does support index funds (e.g. SPX)

## Running

```
$ python3 main.py --help
usage: main.py [-h] [--config CONFIG] {fetch,show}

positional arguments:
  {fetch,show}     the action to perform

options:
  -h, --help       show this help message and exit
  --config CONFIG  path to config file
```

Example:
```
$ picotick show
USD/AUD: 1.42155
USD/GBP: 0.82729
AUD/GBP: 0.58164
SPX    : 4267.69000
TSLA   : 915.00000
BTC/USD: 24163.60000
Last fetched 2022-08-15 15:32
```

## Configuration

Follow the example in `config.example.json` and place it somewhere you like. You will need to create a [Twelve Data](https://twelvedata.com/) API key.

## Installation - Linux (systemd)

Put this repo somewhere you like.

Then, edit the example systemd files `picotick.service` and `picotick.timer`. Copy them to `~/.config/systemd/user`.

Finally, you can do

```
systemctl --user enable picotick.timer

systemctl --user start picotick.timer
```

To test if your service works, run
```
systemctl --user start picotick.service
```

## Extra

(Similar to picop, I made this script because I was bored and had a few hours of free time. I also know Twelve has an official Python API but since i'm only using one endpoint it's not gonna be an issue)