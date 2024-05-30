## Usando o Flake8, Black e o isort como Boas Práticas

Este README demonstra como integrar o Flake8, Black e o isort em seu projeto Python para garantir código limpo, consistente e de alta qualidade.

### 1. Introdução

O Flake8, Black e o isort são ferramentas essenciais para um desenvolvimento Python eficaz. Eles ajudam a:

* **Flake8**: Verificar erros de estilo e código, garantindo conformidade com as PEP8 e outras diretrizes.
* **Black**: Formatar automaticamente o código Python, garantindo consistência de estilo.
* **isort**: Organizar as importações do seu código, seguindo as melhores práticas e simplificando a leitura.

### 2. Instalação

Utilize o `pip` para instalar as ferramentas:

```bash
pip install flake8 black isort
```

### 3. Configuração

#### 3.1 Arquivo `.flake8`

Crie um arquivo chamado `.flake8` na raiz do seu projeto com as seguintes configurações (opcional):

```
[flake8]
ignore = E501,W503,E203
max-line-length = 120
```

* `ignore`: Ignora avisos específicos (consulte a documentação do Flake8 para a lista completa de códigos).
* `max-line-length`: Define o comprimento máximo da linha (padrão: 79).

#### 3.2 Arquivo `.isort.cfg`

Crie um arquivo chamado `.isort.cfg` na raiz do seu projeto com as seguintes configurações (opcional):

```
[isort]
profile = black
line_length = 120
multi_line_output = 3
```

* `profile = black`: Usa as configurações do Black para a ordenação de importações.
* `line_length`: Define o comprimento máximo da linha (padrão: 79).
* `multi_line_output`: Define como as importações são formatadas em múltiplas linhas (consulte a documentação do isort para mais detalhes).

#### 3.3 Arquivo `pyproject.toml`

Crie um arquivo chamado `pyproject.toml` na raiz do seu projeto com as seguintes configurações:

```toml
[tool.black]
line-length = 120

[tool.isort]
profile = black
line_length = 120
multi_line_output = 3
```

### 4. Integração

#### 4.1 Linha de Comando

Use os seguintes comandos para executar as ferramentas:

* **Flake8**: `flake8 .` - Analisa todos os arquivos Python na raiz do projeto.
* **Black**: `black .` - Formata todos os arquivos Python na raiz do projeto.
* **isort**: `isort .` - Organiza as importações de todos os arquivos Python na raiz do projeto.

#### 4.2 IDEs

A maioria das IDEs integradas, como PyCharm, VS Code e Sublime Text, oferece suporte direto ao Flake8, Black e isort. Configure suas preferências para que as ferramentas sejam executadas automaticamente durante a edição ou salvamento dos arquivos.

#### 4.3 Git Hooks

Para automatizar a verificação do código antes do commit, configure Git Hooks. Adicione os seguintes scripts ao diretório `.git/hooks`:

* **pre-commit**:
   ```bash
   #!/bin/bash
   flake8 .
   black .
   isort .
   ```

Este script verifica o código antes de cada commit, garantindo que ele atenda aos padrões de estilo e organização.

### 5. Conclusão

Usar o Flake8, Black e isort em seu projeto Python garante um código consistente, limpo e de alta qualidade. Integração com sua IDE e Git Hooks automatizam o processo de verificação e formatação, simplificando o desenvolvimento e promovendo boas práticas.

