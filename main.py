import argparse
import datetime
import requests
import os
import json

TWELVE_ENDPOINT = "https://api.twelvedata.com/price?symbol={0}&apikey={1}"

class SymbolData:
    def __init__(self, config):
        self.symbols = config["symbols"]
        self.apikey = config["apikey"]
        self.error = True
        self.error_msg = "Symbols not fetched yet :("
        self.results = {}
        self.fetch_time = "never"
        self.cached = "Cache not fetched :("
    
    def fetch(self):
        query = TWELVE_ENDPOINT.format(",".join(self.symbols), self.apikey)
        response = requests.get(query)
        self.fetch_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if response.status_code != 200:
            self.msg = response.text
        else:
            self.error = False
            self.results = {}
            for symbol, result in response.json().items():
                self.results[symbol] = result["price"]
    
    def load_cache(self, cache_file):
        if not os.path.exists(cache_file):
            self.error_msg = "Cached output not found! Please run fetch first."
        with open(cache_file, "r") as f:
            self.cached = f.read().strip()
            self.error = False
            
    def show(self):
        if self.error:
            return self.error_msg
        elif self.results:
            outputs = []
            for symbol in self.symbols:
                outputs.append(f"{symbol:7}: {self.results[symbol]}")
            outputs.append(f"Last fetched {self.fetch_time}")
            return "\n".join(outputs)
        else:
            return self.cached

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path to config file", default=os.path.expanduser("~/.config/picotick/config.json"))
    parser.add_argument("action", help="the action to perform", choices=["fetch", "show"], default="show")

    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)

    data = SymbolData(config)

    if args.action == "fetch":
        data.fetch()
        with open(config["output"], "w") as f:
            f.write(data.show())
            f.write("\n")
    elif args.action == "show":
        data.load_cache(config["output"])

    print(data.show())

if __name__ == "__main__":
    main()