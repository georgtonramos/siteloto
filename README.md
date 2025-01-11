# Site Lotofácil - Análise e Ferramentas

Este projeto é um site desenvolvido em Flask (Python) que oferece várias ferramentas para análise de resultados da Lotofácil.

## Funcionalidades

*   **Verificar Números:** Analisa uma sequência de números e fornece estatísticas como: quantidade de pares, ímpares, primos, números de Fibonacci, múltiplos de 3 e a soma dos números. Além disso, verifica se a sequência atende a critérios específicos (como a quantidade de pares/ímpares estar entre 7 e 9, por exemplo).
*   **Verificar Números Faltantes:** Dada uma sequência de 15 números, identifica quais números entre 1 e 25 estão faltando.
*   **Verificar Sorteio:** Verifica se uma sequência de 15 números já foi sorteada na Lotofácil e, em caso afirmativo, em qual concurso.
*   **Gerar Combinações:** Gera combinações aleatórias de números com base em parâmetros definidos pelo usuário (quantidade de combinações, números por combinação e uma lista de números para combinar), evitando sequências longas de números consecutivos.

## Tecnologias Utilizadas

*   **Python (Flask):** Framework web para o backend.
*   **Pandas:** Biblioteca para manipulação e análise de dados (usada para carregar e processar os resultados da Lotofácil).
*   **HTML, CSS, JavaScript:** Frontend do site.
*   **Gunicorn:** Servidor WSGI para deploy.
*   **Nginx:** Servidor web reverso.
*   **Let's Encrypt (Certbot):** Para HTTPS.

## Estrutura do Projeto

site_lotofacil/
├── app.py          # Arquivo principal da aplicação Flask
├── routes.py       # Rotas da aplicação
├── utils.py        # Funções auxiliares
├── lotofacil.py    # Funções relacionadas à Lotofácil
├── templates/      # Templates HTML
│   ├── home.html
│   ├── index.html
│   ├── gerar_combinacoes.html
│   ├── verificar_numeros.html
│   └── verificar_sorteio.html
├── static/
│   └── styles.css  # Arquivo CSS
└── requirements.txt # Dependências do projeto

## Como executar

1.  **Clone o repositório:**
    ```bash
    git clone <URL_do_repositorio>
    ```
2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    ```
3.  **Ative o ambiente virtual:**
    *   Linux/macOS: `source venv/bin/activate`
    *   Windows: `venv\Scripts\activate`
4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configure o arquivo `app.py`:**
    *   Certifique-se de que o caminho para o arquivo `LotoV7.xlsx` esteja correto na variável `file_path`.
6.  **Execute a aplicação:**
    ```bash
    flask run
    ```

## Deploy

O projeto está configurado para deploy em um servidor Ubuntu 22.04 usando Gunicorn como servidor WSGI e Nginx como servidor web reverso. O HTTPS é configurado usando o Let's Encrypt (Certbot).

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

[MIT License](LICENSE) ```

Este README fornece uma boa introdução ao seu projeto. Ele explica o que é o projeto, como executá-lo e como contribuir. Você pode adaptá-lo e adicionar mais informações conforme necessário.