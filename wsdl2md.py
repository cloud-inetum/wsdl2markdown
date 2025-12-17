#!/usr/bin/env python3
"""
WSDL to Markdown Documentation Generator
Gera documentação completa em Markdown a partir de um arquivo WSDL.

Uso: python wsdl2md.py <arquivo.wsdl> [saida.md]
"""

import sys
import os
from lxml import etree
from datetime import datetime

class WSDLParser:
    def __init__(self, wsdl_path):
        self.tree = etree.parse(wsdl_path)
        self.root = self.tree.getroot()
        self.ns = {
            'wsdl': 'http://schemas.xmlsoap.org/wsdl/',
            'soap': 'http://schemas.xmlsoap.org/wsdl/soap/',
            'soap12': 'http://schemas.xmlsoap.org/wsdl/soap12/',
            'xsd': 'http://www.w3.org/2001/XMLSchema',
            'tns': self.root.get('targetNamespace', '')
        }
    
    def get_service_info(self):
        """Extrai informações básicas do serviço"""
        return {
            'name': self.root.get('name', 'Unknown Service'),
            'target_namespace': self.root.get('targetNamespace', ''),
            'documentation': self._get_documentation(self.root)
        }
    
    def get_endpoints(self):
        """Extrai endpoints SOAP"""
        endpoints = []
        
        # SOAP 1.1
        for addr in self.root.findall('.//soap:address', self.ns):
            endpoints.append({
                'version': 'SOAP 1.1',
                'location': addr.get('location', '')
            })
        
        # SOAP 1.2
        for addr in self.root.findall('.//soap12:address', self.ns):
            endpoints.append({
                'version': 'SOAP 1.2',
                'location': addr.get('location', '')
            })
        
        return endpoints
    
    def get_operations(self):
        """Extrai todas as operações com detalhes"""
        operations = []
        
        for port_type in self.root.findall('.//wsdl:portType', self.ns):
            for op in port_type.findall('wsdl:operation', self.ns):
                op_name = op.get('name')
                
                # Buscar binding correspondente
                binding_info = self._get_binding_info(op_name)
                
                # Buscar mensagens de entrada/saída
                input_msg = self._get_message_info(op.find('wsdl:input', self.ns))
                output_msg = self._get_message_info(op.find('wsdl:output', self.ns))
                
                operations.append({
                    'name': op_name,
                    'documentation': self._get_documentation(op),
                    'soap_action': binding_info.get('soap_action', ''),
                    'input': input_msg,
                    'output': output_msg
                })
        
        return operations
    
    def get_types(self):
        """Extrai definições de tipos (XSD)"""
        types = []
        
        for schema in self.root.findall('.//xsd:schema', self.ns):
            for complex_type in schema.findall('.//xsd:complexType', self.ns):
                type_name = complex_type.get('name')
                if type_name:
                    elements = self._parse_complex_type(complex_type)
                    types.append({
                        'name': type_name,
                        'elements': elements
                    })
        
        return types
    
    def _get_documentation(self, element):
        """Extrai documentação de um elemento"""
        doc = element.find('wsdl:documentation', self.ns)
        return doc.text.strip() if doc is not None and doc.text else ''
    
    def _get_binding_info(self, operation_name):
        """Busca informações de binding para uma operação"""
        for binding in self.root.findall('.//wsdl:binding', self.ns):
            for op in binding.findall('wsdl:operation', self.ns):
                if op.get('name') == operation_name:
                    soap_op = op.find('soap:operation', self.ns)
                    if soap_op is not None:
                        return {'soap_action': soap_op.get('soapAction', '')}
        return {}
    
    def _get_message_info(self, io_element):
        """Extrai informações de mensagem (input/output)"""
        if io_element is None:
            return None
        
        msg_name = io_element.get('message', '').split(':')[-1]
        
        for message in self.root.findall('.//wsdl:message', self.ns):
            if message.get('name') == msg_name:
                parts = []
                for part in message.findall('wsdl:part', self.ns):
                    parts.append({
                        'name': part.get('name'),
                        'element': part.get('element', '').split(':')[-1],
                        'type': part.get('type', '').split(':')[-1]
                    })
                return {
                    'message_name': msg_name,
                    'parts': parts
                }
        
        return None
    
    def _parse_complex_type(self, complex_type):
        """Parseia elementos de um complexType"""
        elements = []
        
        for element in complex_type.findall('.//xsd:element', self.ns):
            elements.append({
                'name': element.get('name'),
                'type': element.get('type', '').split(':')[-1],
                'min_occurs': element.get('minOccurs', '1'),
                'max_occurs': element.get('maxOccurs', '1')
            })
        
        return elements


class MarkdownGenerator:
    def __init__(self, parser):
        self.parser = parser
    
    def generate(self):
        """Gera o documento Markdown completo"""
        md = []
        
        # Cabeçalho
        md.append(self._generate_header())
        
        # Visão Geral
        md.append(self._generate_overview())
        
        # Endpoints
        md.append(self._generate_endpoints())
        
        # Operações
        md.append(self._generate_operations())
        
        # Tipos de Dados
        md.append(self._generate_types())
        
        # Rodapé
        md.append(self._generate_footer())
        
        return '\n\n'.join(md)
    
    def _generate_header(self):
        service_info = self.parser.get_service_info()
        return f"""# Documentação da API SOAP: {service_info['name']}

> Documentação gerada automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

---"""
    
    def _generate_overview(self):
        service_info = self.parser.get_service_info()
        
        doc = service_info['documentation']
        doc_section = f"\n**Descrição:** {doc}\n" if doc else ""
        
        return f"""## 📋 Visão Geral

**Nome do Serviço:** `{service_info['name']}`  
**Namespace:** `{service_info['target_namespace']}`{doc_section}"""
    
    def _generate_endpoints(self):
        endpoints = self.parser.get_endpoints()
        
        if not endpoints:
            return "## 🌐 Endpoints\n\n*Nenhum endpoint encontrado*"
        
        md = ["## 🌐 Endpoints\n"]
        
        for endpoint in endpoints:
            md.append(f"### {endpoint['version']}")
            md.append(f"```\n{endpoint['location']}\n```")
        
        return '\n\n'.join(md)
    
    def _generate_operations(self):
        operations = self.parser.get_operations()
        
        if not operations:
            return "## 🔧 Operações\n\n*Nenhuma operação encontrada*"
        
        md = ["## 🔧 Operações\n"]
        
        for op in operations:
            md.append(f"### {op['name']}")
            
            if op['documentation']:
                md.append(f"**Descrição:** {op['documentation']}\n")
            
            if op['soap_action']:
                md.append(f"**SOAPAction:** `{op['soap_action']}`\n")
            
            # Input
            if op['input']:
                md.append("#### 📥 Requisição (Input)")
                md.append(self._format_message(op['input']))
                md.append(self._generate_soap_example(op['name'], op['input'], 'request'))
            
            # Output
            if op['output']:
                md.append("#### 📤 Resposta (Output)")
                md.append(self._format_message(op['output']))
                md.append(self._generate_soap_example(op['name'], op['output'], 'response'))
            
            md.append("---")
        
        return '\n\n'.join(md)
    
    def _format_message(self, message):
        """Formata informações de mensagem como tabela"""
        if not message['parts']:
            return "*Sem parâmetros*"
        
        table = ["| Parâmetro | Tipo | Elemento |", "|-----------|------|----------|"]
        
        for part in message['parts']:
            param = part['name']
            ptype = part['type'] or '-'
            element = part['element'] or '-'
            table.append(f"| `{param}` | `{ptype}` | `{element}` |")
        
        return '\n'.join(table)
    
    def _generate_soap_example(self, op_name, message, msg_type):
        """Gera exemplo de SOAP envelope"""
        if msg_type == 'request':
            body_content = f"<{op_name}>\n"
            if message['parts']:
                for part in message['parts']:
                    body_content += f"         <{part['name']}>valor_exemplo</{part['name']}>\n"
            body_content += f"      </{op_name}>"
        else:
            body_content = f"<{op_name}Response>\n"
            if message['parts']:
                for part in message['parts']:
                    body_content += f"         <{part['name']}>valor_retornado</{part['name']}>\n"
            body_content += f"      </{op_name}Response>"
        
        example = f"""```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Header/>
   <soapenv:Body>
      {body_content}
   </soapenv:Body>
</soapenv:Envelope>
```"""
        
        return example
    
    def _generate_types(self):
        types = self.parser.get_types()
        
        if not types:
            return "## 📦 Tipos de Dados\n\n*Nenhum tipo complexo encontrado*"
        
        md = ["## 📦 Tipos de Dados (XSD)\n"]
        
        for dtype in types:
            md.append(f"### {dtype['name']}")
            
            if dtype['elements']:
                table = ["| Campo | Tipo | Min | Max |", "|-------|------|-----|-----|"]
                for elem in dtype['elements']:
                    table.append(f"| `{elem['name']}` | `{elem['type']}` | {elem['min_occurs']} | {elem['max_occurs']} |")
                md.append('\n'.join(table))
            else:
                md.append("*Sem elementos definidos*")
            
            md.append("")
        
        return '\n\n'.join(md)
    
    def _generate_footer(self):
        return """---

## 📚 Informações Adicionais

### Como Usar

1. Importe o WSDL em sua ferramenta favorita (SOAP UI, Postman, etc.)
2. Configure o endpoint apropriado
3. Utilize os exemplos de requisição como base
4. Consulte os tipos de dados para estruturar corretamente os payloads

### Ferramentas Recomendadas

- **SOAP UI**: [https://www.soapui.org/](https://www.soapui.org/)
- **Postman**: [https://www.postman.com/](https://www.postman.com/)
- **cURL**: Para testes via linha de comando

---

*Documentação gerada automaticamente a partir do WSDL*"""


def main():
    if len(sys.argv) < 2:
        print("Uso: python wsdl2md.py <arquivo.wsdl> [saida.md]")
        sys.exit(1)
    
    wsdl_file = sys.argv[1]
    
    if not os.path.exists(wsdl_file):
        print(f"❌ Erro: Arquivo '{wsdl_file}' não encontrado!")
        sys.exit(1)
    
    # Define arquivo de saída
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = os.path.splitext(wsdl_file)[0] + '.md'
    
    try:
        print(f"📄 Parseando WSDL: {wsdl_file}")
        parser = WSDLParser(wsdl_file)
        
        print(f"📝 Gerando documentação Markdown...")
        generator = MarkdownGenerator(parser)
        markdown_content = generator.generate()
        
        print(f"💾 Salvando em: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Documentação gerada com sucesso!")
        print(f"📂 Arquivo: {output_file}")
        
    except etree.XMLSyntaxError as e:
        print(f"❌ Erro ao parsear XML: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
