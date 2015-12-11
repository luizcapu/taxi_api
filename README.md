taxi_api
============

== GOALS (Brazilian Portuguese)

Objetivo

Implementar o backend de um aplicativo de smartphone que mostra um mapa com os taxistas ativos da 99Taxis. O sistema deve assumir que tem diversos taxistas cadastrados e permitir atualizar o status desses taxistas, consultar status deles e encontrar taxistas em uma dada área. Toda comunicação deve ser feita com JSON.

Endpoints:

1. Grava a posição atual e estado de um taxista.
1. Parâmetros:
1. latitude
2. longitude
3. driverId (id único de taxista no sistema)
4. driverAvailable: true/false. Representa se o taxista está disponível ou não para corridas.
2. Resposta:
1. Apenas status code HTTP
3. Exemplo:
1. POST /drivers/8475/status '{"latitude":-23.60810717,"

2. Lista os taxistas ativos dentro de uma retângulo geográfico. 
1. Parâmetros:
1. sw: Ponto extremo sul, extremo oeste do retângulo, no formato "latitude,longitude". Ex: -23.612474,-46.702746
2. ne: Ponto extremo norte, extremo leste do retângulo, no formato "latitude,longitude". Ex: -23.589548,-46.673392
2. Resposta: Um array em formato json, de um objeto com atributos:
1. latitude
2. longitude
3. driverId (id único de taxista no sistema)
4. driverAvailable: true/false. Representa se o taxista está disponível ou não para corridas. Neste endpoint retorna sempre true.
3. Exemplo:
GET /drivers/inArea?sw=-23.612474,
[{"latitude":-23.60810717,"

3. Estado de um taxista. Recebe o id de um taxista e retorna os dados dele:
1. Parâmetros:
1. driverId
2. Resposta:
1. latitude
2. longitude
3. driverId (id único de taxista no sistema)
4. driverAvailable: true/false. Representa se o taxista está disponível ou não para corridas.
3. Exemplo:
1. GET /drivers/73456/status
'{"latitude":-23.60810717,"

Objetivos Bonus:

1. Subir a aplicação "na nuvem" e enviar o link para testarmos os endpoints.
2. Descrever algoritmo ótimo de procura dos taxistas.
3. Autenticação nos endpoints, explicando a solução.
4. Criar outros endpoints que possibilitem a mesma funcionalidade mas com outro fluxo.
5. Endpoint Cria taxista:
1. Parâmetros:
1. name
2. carPlate: placa do carro
2. Resposta:
1. Apenas status code HTTP
3. Exemplos:
1. POST /drivers 
'{"name":"Pedro","carPlate":"

=== INSTALLATION

1) Be sure your environment is read to run Python applications (https://www.python.org/about/gettingstarted/)

2) Recommended use of virtual environment (Brazilian Portuguese reference: https://osantana.me/ambiente-isolado-para-python-com-virtualenv/)

3) Run install.sh file found at the root of the project

=== HELP OUTPUT

```
usage: url_gather.py [-h] [-u URL] [-d DEPTH] [-w WORKERS]
                     [-ae ACCEPTABLE_ERRORS] [-o OUT] [-cf COLLECTOR_FILE]
                     [-cc COLLECTOR_CLASS]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Initial URL to gather
  -d DEPTH, --depth DEPTH
                        Gathering depth
  -w WORKERS, --workers WORKERS
                        Number of parallel workers
  -ae ACCEPTABLE_ERRORS, --acceptable_errors ACCEPTABLE_ERRORS
                        Max acceptable errors to continue execution
                        (-1=disabled)
  -o OUT, --out OUT     Folder to save output files
  -cf COLLECTOR_FILE, --collector_file COLLECTOR_FILE
                        Path to custom .py file to act as collector
  -cc COLLECTOR_CLASS, --collector_class COLLECTOR_CLASS
                        Class name of custom collector
```


=== USAGE EXAMPLE

```
cd url_gather
python url_gather.py -u http://g1.globo.com/ -d 1 -w 5 -o /tmp/
```

USING A CUSTOM COLLECTOR

```
python url_gather.py -u http://g1.globo.com/ -cf ./collectors/test_custom_collector.py -cc TestCustomCollector
```

=== IMPORTANT

Your custom collector code MUST OBEY the collector interface BUT MUST NOT INHERIT from it.

Collector interface can be found at [ROOT]/url_gather/collectors/collector_interface.py

