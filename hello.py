import json
header_tags = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
metacritic_tags = {'class': "sc-b0901df4-0 bXIOoL metacritic-score-box"}
awards_tags = {'class' : 'ipc-metadata-list-summary-item__t'}
boxoffice_tags = {'data-testid' : 'title-boxoffice-budget', 'class' : 'ipc-metadata-list-item__list-content-item'}
grossworldwide_tags = {'data-testid' : 'title-boxoffice-cumulativeworldwidegross', 'class' : 'ipc-metadata-list-item__list-content-item'}

tags_list = [header_tags, metacritic_tags,  awards_tags, boxoffice_tags, grossworldwide_tags ]

with open("awards.json", "w") as json_file:
    for d in tags_list:
        json_file.write(json.dumps(d) + "\n")