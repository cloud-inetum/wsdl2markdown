# Guia de Contribuição

Obrigado por considerar contribuir com o **WSDL to Markdown**! 🎉

## Como Contribuir

### 1. Reportar Bugs

Se você encontrou um bug, por favor:
- Verifique se já não existe uma [issue](https://github.com/cloud-inetum/wsdl2markdown/issues) sobre o problema
- Abra uma nova issue incluindo:
  - Descrição clara do problema
  - Passos para reproduzir
  - Comportamento esperado vs. comportamento atual
  - Ambiente (SO, versão do Python, etc.)
  - Arquivo WSDL de exemplo (se possível)

### 2. Sugerir Melhorias

Para sugerir novas funcionalidades:
- Abra uma issue com a tag `enhancement`
- Descreva claramente a funcionalidade
- Explique por que seria útil
- Se possível, sugira uma implementação

### 3. Contribuir com Código

#### Setup do Ambiente

```bash
# 1. Fork o repositório
# 2. Clone seu fork
git clone https://github.com/SEU-USUARIO/wsdl2markdown.git
cd wsdl2markdown

# 3. Crie uma branch para sua feature
git checkout -b feature/minha-feature

# 4. Instale dependências
pip install -r requirements.txt
```

#### Padrões de Código

- Use **Python 3.6+**
- Siga o **PEP 8**
- Adicione **docstrings** para funções e classes
- Mantenha o código **legível** e **documentado**
- Escreva **testes** quando aplicável

#### Commit

Use mensagens de commit claras e descritivas:

```bash
git commit -m "Add: Suporte para WSDL com autenticação WS-Security"
git commit -m "Fix: Correção no parsing de tipos XSD complexos"
git commit -m "Docs: Atualiza README com novos exemplos"
```

Prefixos recomendados:
- `Add:` - Nova funcionalidade
- `Fix:` - Correção de bug
- `Docs:` - Documentação
- `Refactor:` - Refatoração de código
- `Test:` - Adição ou modificação de testes

#### Pull Request

1. Faça push da sua branch:
```bash
git push origin feature/minha-feature
```

2. Abra um Pull Request no GitHub
3. Descreva suas mudanças claramente
4. Referencie issues relacionadas (se houver)
5. Aguarde review

### 4. Melhorar Documentação

Contribuições para documentação são sempre bem-vindas:
- Corrigir erros de digitação
- Melhorar explicações
- Adicionar exemplos
- Traduzir documentação

## Código de Conduta

- Seja respeitoso e inclusivo
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros

## Dúvidas?

Se tiver dúvidas, abra uma [issue](https://github.com/cloud-inetum/wsdl2markdown/issues) ou entre em contato.

---

**Obrigado por contribuir! 🚀**