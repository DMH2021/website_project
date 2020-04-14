import requests


OPEN_WEATHER_KEY = "e002e4a56551adbd797f982bf7bca49f"
IP_STACK_KEY = "a3b000865bedf19ce2aaa5e6c61cfc1a"

def main():
    resp = requests.get("http://api.ipstack.com/check?access_key=%s" % IP_STACK_KEY)
    result = resp.json()
    print("I see you are in %s, %s" % (result['city'], result['region_name']))
    resp = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s" % (result['latitude'], result['longitude'], OPEN_WEATHER_KEY))
    result = resp.json()
    desc = result['weather'][0]['description']
    if 'rain' in desc:
        print("Sorry about the %s" % desc)
    else:
        print("I see it is %s" % desc)
if __name__=="__main__":
    main()