import requests
from random import sample, seed


def getRandomTickets(secret, vrf_height, tickets_amount, bought_tickets_amount):
    try:
        req = requests.get('https://nodes.swop.fi/blocks/height')
        if req.status_code != 200:
            raise requests.exceptions.RequestException('Status code ' + str(req.status_code))
    except requests.exceptions.RequestException as e:
        print('Can\'t connect to node ' + e.response)
        raise e
    height = req.json()['height']
    if height <= int(vrf_height):
        raise BaseException('Block height can\'t be bigger than blockchain height')
    try:
        req = requests.get('https://nodes.swop.fi/blocks/at/' + vrf_height)
        if req.status_code != 200:
            raise requests.exceptions.RequestException('Status code ' + str(req.status_code))
    except requests.exceptions.RequestException as e:
        print('Can\'t get block at height ' + vrf_height)
        raise e
    vrf = req.json()["VRF"]
    seed(vrf + secret)
    win_tickets = sample(range(1, bought_tickets_amount + 1), tickets_amount)
    return win_tickets


print("To start please input params:")
print("Secret word:")
secret = input()
print("VRF height:")
vrf_height = input()
print("Launchpad tickets amount:")
tickets_amount = int(input())
print("Bought tickets amount:")
bought_tickets_amount = int(input())

tickets = getRandomTickets(secret, vrf_height, tickets_amount, bought_tickets_amount)
print(",".join(map(str, tickets)))
