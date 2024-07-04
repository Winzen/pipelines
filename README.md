<p align="center">
    <a href="https://basedosdados.org">
        <img src="https://basedosdados.org/favicon.ico">
    </a>
</p>

<p align="center">
    <em>Universalizando o acesso a dados de qualidade.</em>
</p>

# Pipelines

Esse repositório contém fluxos de captura e subida de dados no datalake da Base dos Dados.

---

## Configuração de ambiente para desenvolvimento

### Requisitos

-   Um editor de texto (recomendado VS Code)
-   Python 3.10.x
-   `pip`
-   (Opcional, mas recomendado) Um ambiente virtual para desenvolvimento (`miniconda`, `virtualenv` ou similares)

### Procedimentos

-   #### Clonar esse repositório

    ```
    git clone https://github.com/basedosdados/pipelines
    ```
- #### Instalar o WSL 2 - Ubuntu (Apenas Usuarios windows)
  
    * Se você usa o windows é essencial Instalar o WSL 2 - Ubuntu
    * Siga esse [passo a passo](https://learn.microsoft.com/pt-br/windows/wsl/install)
      
- #### Comando para instalar dependencias:

```bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev
``` 

  
* Caso seu sistema não reconheça `R` como um comando interno, instale pacote [`R-base`][r-base]:

```bash
sudo apt -y install r-base
```
- #### Instalar o pyenv 

  É importante instalar o pyenv para garantir que a versão de python é padrão. Escrevemos uma versão resumida mas recomendamos [esse material](https://realpython.com/intro-to-pyenv/) e [esse](https://gist.github.com/luzfcb/ef29561ff81e81e348ab7d6824e14404) para mais informações. 
    
    * Comando para instalar o pyenv:
 
      ```bash
        curl https://pyenv.run | bash
      ```
       * **ATENÇÃO: leia atentamente os avisos depois desse comando, existe um passo a passo essencial para que o pyenv funcione**
    
    * Comando para ver lista de versões do pyenv:
 
      ```bash
        pyenv install --list
      ```
      
    * Comando para instalar a versão padrão de desenvolvimento: 
 
      ```bash
        pyenv install -v 3.10.14
      ```
      
    * Comando para definir essa versão como versão global: 

      ```bash
        pyenv global 3.10.14
      ```

- #### Criar o ambiente virtual dentro do repositório
    
    * Comando para criar o ambiente:
        ```bash
        python -m venv .venv
        ```     
    * Comando para ativar o ambiente:
        ```bash
        source .venv/bin/activate
        ```  
    * Certifique-se que a versão do python está correta com:
        ```bash
        python -V
        ```
- #### Atualizar o `pip` 

    É muito importante garantir que a versão está atualizada na venv antes de instalar o `poetry`
    * Comando para atualizar o `pip`: 
       ```bash
        python -m pip install --upgrade pip
        ```

-   #### No seu ambiente de desenvolvimento, instalar [poetry](https://python-poetry.org/) para gerenciamento de dependências

    ```bash
    pip install poetry
    ```

-   #### Instalar as dependências para desenvolvimento

    ```bash
    poetry install
    ```
    
-   **Pronto! Seu ambiente está configurado para desenvolvimento.**

---

## Como desenvolver

### Estrutura de diretorios

```
datasets/                    # diretório raiz para o órgão
|-- projeto1/                # diretório de projeto
|-- |-- __init__.py          # vazio
|-- |-- constants.py         # valores constantes para o projeto
|-- |-- flows.py             # declaração dos flows
|-- |-- schedules.py         # declaração dos schedules
|-- |-- tasks.py             # declaração das tasks
|-- |-- utils.py             # funções auxiliares para o projeto
...
|-- __init__.py              # importa todos os flows de todos os projetos
|-- constants.py             # valores constantes para o órgão
|-- flows.py                 # declaração de flows genéricos do órgão
|-- schedules.py             # declaração de schedules genéricos do órgão
|-- tasks.py                 # declaração de tasks genéricas do órgão
|-- utils.py                 # funções auxiliares para o órgão

...

utils/
|-- __init__.py
|-- flow1/
|-- |-- __init__.py
|-- |-- flows.py
|-- |-- tasks.py
|-- |-- utils.py
|-- flows.py                 # declaração de flows genéricos
|-- tasks.py                 # declaração de tasks genéricas
|-- utils.py                 # funções auxiliares

constants.py                 # valores constantes para todos os órgãos

```

### Adicionando órgãos e projetos

O script `manage.py` é responsável por criar e listar projetos desse repositório. Para usá-lo, no entanto, você deve instalar as dependências:

```
poetry install --with=dev
```

Você pode obter mais informações sobre os comandos com

```
python manage.py --help
```

O comando `add-agency` permite que você adicione um novo órgão a partir do template padrão. Para fazê-lo, basta executar

```
python manage.py add-agency nome-do-orgao
```

Isso irá criar um novo diretório com o nome `nome-do-orgao` em `pipelines/` com o template padrão, já adaptado ao nome do órgão. O nome do órgão deve estar em [snake case](https://en.wikipedia.org/wiki/Snake_case) e deve ser único. Qualquer conflito com um projeto já existente será reportado.

Para listar os órgão existentes e nomes reservados, basta fazer

```
python manage.py list-projects
```

Em seguida, leia com anteção os comentários em cada um dos arquivos do seu projeto, de modo a evitar conflitos e erros.
Links para a documentação do Prefect também encontram-se nos comentários.

Caso o órgão para o qual você desenvolverá um projeto já exista, basta fazer

```
python manage.py add-project datasets nome-do-projeto
```

Onde `nome-projeto`

### Adicionando dependências para execução

-   Requisitos de pipelines devem ser adicionados com

```
poetry add <package>
```

### Como testar uma pipeline localmente

Escolha a pipeline que deseja executar (exemplo `pipelines.rj_escritorio.test_pipeline.flows.flow`)

```py
from pipelines.utils.utils import run_local
from pipelines.datasets.test_pipeline.flows import flow

run_local(flow, parameters = {"param": "val"})
```

### Como testar uma pipeline na nuvem

1. Faça a cópia do arquivo `.env.example` para um novo arquivo nomeado `.env`:

    ```
    cp .env.example .env
    ```

-   Substitua os valores das seguintes variáveis pelos seus respectivos valores:

    -   `GOOGLE_APPLICATION_CREDENTIALS`: Path para um arquivo JSON com as credenciais da API do Google Cloud
        de uma conta de serviço com acesso de escrita ao bucket `basedosdados-dev` no Google Cloud Storage.
    -   `VAULT_TOKEN`: deve ter o valor do token do órgão para o qual você está desenvolvendo. Caso não saiba o token, entre em contato.

-   Carregue as variáveis de ambiente do arquivo `.env`:

    ```sh
    source .env
    ```

-   Também, garanta que o arquivo `$HOME/.prefect/auth.toml` exista e tenha um conteúdo semelhante ao seguinte:

    ```toml
    ["prefect.basedosdados.org"]
    api_key = "<sua-api-key>"
    tenant_id = "<tenant-id>"
    ```

    -   O valor da chave `tenant_id` pode ser coletada atráves da seguinte URL: https://prefect.basedosdados.org/default/api. Devendo ser executado a seguinte query:

        ```graphql
        query {
            tenant {
                id
            }
        }
        ```

*   Em seguida, tenha certeza que você já tem acesso à UI do Prefect, tanto para realizar a submissão da run, como para acompanhá-la durante o processo de execução.

1. Crie o arquivo `test.py` com a pipeline que deseja executar e adicione a função `run_cloud` com os parâmetros necessários:

    ```py
    from pipelines.utils.utils import run_cloud
    from pipelines.[secretaria].[pipeline].flows import flow # Complete com as infos da sua pipeline

    run_cloud(
        flow,               # O flow que você deseja executar
        labels=[
            "example",      # Label para identificar o agente que irá executar a pipeline (ex: basedosdados-dev)
        ],
        parameters = {
            "param": "val", # Parâmetros que serão passados para a pipeline (opcional)
        }
    )
    ```

2. Rode a pipeline com:

    ```sh
    python test.py
    ```

-   A saída deverá se assemelhar ao exemplo abaixo:

    ```
    [2022-02-19 12:22:57-0300] INFO - prefect.GCS | Uploading xxxxxxxx-development/2022-02-19t15-22-57-694759-00-00 to basedosdados-dev
    Flow URL: http://localhost:8080/default/flow/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    └── ID: xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    └── Project: main
    └── Labels: []
    Run submitted, please check it at:
    https://prefect.basedosdados.org/flow-run/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ```

-   (Opcional, mas recomendado) Quando acabar de desenvolver sua pipeline, delete todas as versões da mesma pela UI do Prefect.

  <-- Referecias -->

  [r-base]: https://www.r-project.org/
