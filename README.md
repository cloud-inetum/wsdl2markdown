# WSDL to Markdown Documentation Generator

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Ferramenta para gerar documentação completa em Markdown a partir de arquivos WSDL (Web Service Description Language). Ideal para documentar APIs SOAP de forma clara, estruturada e profissional.

## 🎯 Características

- ✅ **Extração completa** de informações do WSDL
- ✅ **Documentação automática** de todas as operações
- ✅ **Exemplos SOAP** gerados automaticamente
- ✅ **Tabelas formatadas** para parâmetros e tipos
- ✅ **Suporte a SOAP 1.1 e 1.2**
- ✅ **Parsing de tipos XSD** complexos
- ✅ **Saída em Markdown** pronta para publicação
- ✅ **Integração com VS Code**

## 📋 Requisitos

- Python 3.6 ou superior
- Biblioteca `lxml`

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/cloud-inetum/wsdl2markdown.git
cd wsdl2markdown
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install lxml
```

## 💻 Uso

### Uso Básico

```bash
# Gera arquivo .md com mesmo nome do WSDL
python wsdl2md.py meu-servico.wsdl

# Especifica arquivo de saída
python wsdl2md.py meu-servico.wsdl documentacao-api.md
```

### Exemplos

```bash
# Exemplo com Calculator Service
python wsdl2md.py examples/calculator.wsdl

# Gerar com nome customizado
python wsdl2md.py examples/calculator.wsdl docs/calculator-api.md
```

## 📖 Exemplo de Saída

O script gera documentação estruturada incluindo:

- **Visão Geral**: Nome do serviço, namespace, descrição
- **Endpoints**: URLs SOAP 1.1 e 1.2
- **Operações**: Todas as operações com:
  - Descrição
  - SOAPAction
  - Parâmetros de entrada (tabela)
  - Parâmetros de saída (tabela)
  - Exemplos de requisição SOAP
  - Exemplos de resposta SOAP
- **Tipos de Dados**: Definições XSD em formato tabular

### Preview do Markdown Gerado

```markdown
# Documentação da API SOAP: Calculator

## 📋 Visão Geral

**Nome do Serviço:** `Calculator`  
**Namespace:** `http://tempuri.org/`

## 🌐 Endpoints

### SOAP 1.1
```
http://www.dneonline.com/calculator.asmx
```

## 🔧 Operações

### Add
**SOAPAction:** `http://tempuri.org/Add`

#### 📥 Requisição (Input)
| Parâmetro | Tipo | Elemento |
|-----------|------|----------|
| `intA` | `int` | - |
| `intB` | `int` | - |

...
```

## 🔧 Integração com VS Code

### Task Automática

Crie `.vscode/tasks.json` no seu workspace:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Gerar Documentação Markdown do WSDL",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/wsdl2md.py",
        "${file}",
        "${fileDirname}/${fileBasenameNoExtension}.md"
      ],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "shared"
      }
    }
  ]
}
```

**Como usar:**
1. Abra o arquivo WSDL no VS Code
2. Pressione `Ctrl+Shift+B` (Windows/Linux) ou `Cmd+Shift+B` (Mac)
3. A documentação será gerada automaticamente

## 🧪 WSDLs Públicos para Teste

Você pode testar com estes WSDLs públicos:

### Calculator Service
```bash
curl "http://www.dneonline.com/calculator.asmx?WSDL" -o calculator.wsdl
python wsdl2md.py calculator.wsdl
```

### Number Conversion Service
```bash
curl "https://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL" -o numberconversion.wsdl
python wsdl2md.py numberconversion.wsdl
```

### Country Info Service
```bash
curl "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL" -o countryinfo.wsdl
python wsdl2md.py countryinfo.wsdl
```

## 📁 Estrutura do Projeto

```
wsdl2markdown/
├── wsdl2md.py              # Script principal
├── requirements.txt         # Dependências Python
├── README.md               # Documentação
├── LICENSE                 # Licença MIT
├── .gitignore             # Arquivos ignorados
├── CHANGELOG.md           # Histórico de versões
├── CONTRIBUTING.md        # Guia de contribuição
├── examples/              # Exemplos de WSDL
│   └── .gitkeep
├── .vscode/               # Configuração VS Code
│   └── tasks.json
└── docs/                  # Documentação gerada
    └── .gitkeep
```

## 🛠️ Desenvolvimento

### Estrutura do Código

O script é dividido em duas classes principais:

- **`WSDLParser`**: Responsável por parsear o arquivo WSDL e extrair informações
  - `get_service_info()`: Informações básicas do serviço
  - `get_endpoints()`: URLs dos endpoints SOAP
  - `get_operations()`: Lista de operações com detalhes
  - `get_types()`: Definições de tipos XSD

- **`MarkdownGenerator`**: Gera o documento Markdown formatado
  - `_generate_header()`: Cabeçalho do documento
  - `_generate_overview()`: Visão geral
  - `_generate_operations()`: Seção de operações
  - `_generate_types()`: Tipos de dados

### Executar Testes

```bash
# Testar com WSDL público
curl "http://www.dneonline.com/calculator.asmx?WSDL" -o calculator.wsdl
python wsdl2md.py calculator.wsdl

# Verificar saída
cat calculator.md
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📝 Roadmap

- [ ] Suporte a URLs diretas (baixar WSDL automaticamente)
- [ ] Exportação para HTML e PDF
- [ ] Temas customizáveis para Markdown
- [ ] Suporte a autenticação WS-Security
- [ ] CLI interativo
- [ ] Docker image
- [ ] GitHub Action para CI/CD

## 🐛 Reportar Problemas

Encontrou um bug? [Abra uma issue](https://github.com/cloud-inetum/wsdl2markdown/issues)

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **INETUM Cloud Solutions** - [@cloud-inetum](https://github.com/cloud-inetum)

## 🙏 Agradecimentos

- Comunidade Python
- Desenvolvedores da biblioteca lxml
- Todos os contribuidores

---

**Feito com ❤️ para a comunidade de desenvolvedores**

[![GitHub stars](https://img.shields.io/github/stars/cloud-inetum/wsdl2markdown?style=social)](https://github.com/cloud-inetum/wsdl2markdown)
[![GitHub forks](https://img.shields.io/github/forks/cloud-inetum/wsdl2markdown?style=social)](https://github.com/cloud-inetum/wsdl2markdown/fork)
