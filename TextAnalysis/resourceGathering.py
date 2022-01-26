import requests
from bs4 import BeautifulSoup
from googlesearch import search

test_dict = {'spike neuron': ['https://en.wikipedia.org/wiki/Spiking_neural_network#History', 'https://www.frontiersin.org/articles/10.3389/fnins.2020.00425/full', 'https://www.frontiersin.org/articles/10.3389/fnins.2018.00774/full', 'https://en.wikipedia.org/wiki/Spiking_neural_network', 'https://www.researchgate.net/figure/Comparison-of-deep-spiking-neural-networks-SNNs-to-conventional-deep-neural-networks_fig1_328504662']}

# will be replaced by output from other files
answer = "spike neuron"

# search google for the topic parsed from the user's question in the other files


def get_resources(ans):
    links = [""]
    values = {"": 0}
    # retrieves the links
    if ans not in test_dict:
        for j in search(ans, tld="co.in", num=5, stop=5, pause=2):
            # opens each webpage and extracts the main body contents
            req = requests.get(j)
            webpage = req.text
            soup = BeautifulSoup(webpage, "html.parser")
            body = str(soup.find("h1"))
            stripped = body[body.find(">")+1:len(body)-5]
            # counts how times the input appears in the body - currently always returns 0 for some reason
            values[j] = stripped.count(ans)
            # orders the links in the array by how many times the input appears
            for i in links:
                if values.get(i) <= values.get(j):
                    links = links[:links.index(i)] + [j] + links[links.index(i):]
                    break
        test_dict[ans] = links[:len(links)-1]
    return (test_dict.get(ans))


# store the keywords from the question - will need to change so persists between users
# get_resources(answer)
# print(test_dict)

# works for the most part, not sure why it doesn't find any instance of the input in the text though
