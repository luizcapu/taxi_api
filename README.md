taxi_api
============

** Objetivos

[Descrição dos Objetivos](docs/goals.pdf)


=== INSTALAÇÃO

Entre na pasta raiz do projeto e execute ./first_install.sh

A instalação automatizada foi testada em Ubuntu 14.04 LTS. Para rodar em outras distribuições talvez sejam necessárias adaptações no instalador.

=== ATUALIZAÇÕES

Para atualizar somente o código fonte após alguma alteração, entre na pasta raiz e execute ./install.sh

Se estiver usando virtualenv (recomendado) não esqueça de ativá-la antes de rodar o install.


=== HELP OUTPUT

```
usage: server.py [-h] [-e ENV]

optional arguments:
  -h, --help         show this help message and exit
  -e ENV, --env ENV  Environment to run (prod|test). Default: test
```


=== EXEMPLO DE USO

```
./taxi_api/server.py -e prod
```

=== APLICAÇÃO NA NUVEM

Uma instância do servidor está rodando no seguinte endereço: http://ec2-54-213-3-150.us-west-2.compute.amazonaws.com:5000

As documentações podem ser acessadas em: http://ec2-54-213-3-150.us-west-2.compute.amazonaws.com:5000/api/spec.html#!/spec/


=== ALGORITMO ÓTIMO DE PROCURA DOS TAXISTAS

[Descrição Textual](docs/driver_search_algo.pdf)

[Esboço Implementação](taxi_api/helpers/driver_finder.py)

=== AUTENTICAÇÃO NOS ENDPOINTS




=== CRIAR OUTROS ENDPOINTS

