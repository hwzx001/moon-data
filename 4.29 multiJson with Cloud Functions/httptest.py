import requests
def getmyurl(url):
    try:
        #headers=headers,timeout=10
        page = requests.get(url=url,timeout=10).text
    except Exception as e:
        return str(e)
    else:
        return str(page)
def hello_test(request):

    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return getmyurl(request.args.get('message'))
    elif request_json and 'message' in request_json:
        return getmyurl(request_json['message'])
    else:
        return f'Hello World!'

def getweb(url):
    return getmyurl('https://us-central1-project-moon-271201.cloudfunctions.net/function-test?message='+str(url))


if __name__ == "__main__":
    print(getweb('https://colourpop.com/products.json'))
    #https://colourpop.com/products.json