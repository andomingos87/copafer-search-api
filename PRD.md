# PRD - Agente de Vendas Copafer (Bertão)
## Visão de Produto

---

## 1. Visão Executiva

### 1.1. O Que É
O **Bertão** é um assistente virtual de vendas que atende clientes da Copafer via WhatsApp, oferecendo uma experiência de compra completa e personalizada, desde a busca de produtos até a finalização do pagamento.

### 1.2. Problema que Resolve
- **Atendimento 24/7**: Clientes podem comprar a qualquer hora, sem depender do horário comercial
- **Busca Inteligente**: Encontra produtos mesmo quando o cliente não sabe o nome exato ou código
- **Jornada Simplificada**: Guia o cliente passo a passo, sem necessidade de navegar por sites ou apps
- **Atendimento Personalizado**: Lembra do histórico do cliente e oferece recomendações relevantes
- **Conversão Otimizada**: Transforma consultas em vendas através de uma experiência conversacional natural

### 1.3. Proposta de Valor
> "Transformar sonhos em realidade, com tudo em um só lugar - agora também via WhatsApp, 24 horas por dia, com um atendimento inteligente e personalizado."

### 1.4. Objetivos de Negócio
- **Aumentar conversão**: Transformar mais consultas em vendas
- **Expandir horário de atendimento**: Atender clientes fora do horário comercial
- **Melhorar experiência**: Oferecer atendimento rápido, personalizado e eficiente
- **Reduzir custos**: Automatizar atendimentos rotineiros, liberando equipe para casos complexos
- **Aumentar ticket médio**: Sugerir produtos complementares e upsell

---

## 2. Personas e Jornadas

### 2.1. Personas Principais

#### Persona 1: Cliente Final (Dona Maria)
- **Perfil**: Pessoa física, primeira compra ou ocasional
- **Necessidades**: 
  - Encontrar produtos para reforma/construção
  - Entender especificações técnicas
  - Saber preço e disponibilidade
  - Comprar com segurança
- **Dores**: 
  - Não conhece nomes técnicos dos produtos
  - Dúvidas sobre quantidade necessária
  - Preocupação com entrega e pagamento

#### Persona 2: Profissional (Pedreiro João)
- **Perfil**: Profissional da construção, compras frequentes
- **Necessidades**:
  - Encontrar produtos rapidamente
  - Saber preço e disponibilidade
  - Comprar em quantidade
  - Receber rápido
- **Dores**:
  - Falta de tempo para navegar sites
  - Precisa de resposta rápida
  - Quer comprar pelo celular

#### Persona 3: Cliente Empresarial (Construtora XYZ)
- **Perfil**: Pessoa jurídica, compras em grande volume
- **Necessidades**:
  - Orçamentos personalizados
  - Condições especiais
  - Nota fiscal com IE
  - Negociação de prazos
- **Dores**:
  - Precisa de atendimento especializado
  - Requer negociação
  - Documentação específica

### 2.2. Jornadas do Cliente

#### Jornada 1: Compra Simples (Produto Único)
1. Cliente busca produto por descrição natural
2. Bertão encontra e apresenta opções
3. Cliente escolhe produto
4. Bertão adiciona ao carrinho e oferece complementos
5. Cliente confirma ou adiciona mais itens
6. Bertão coleta dados de entrega
7. Cliente escolhe frete ou retirada
8. Bertão gera link de pagamento
9. Cliente finaliza compra

#### Jornada 2: Compra com Dúvidas Técnicas
1. Cliente descreve necessidade (ex: "preciso revestir 30m²")
2. Bertão identifica tipo de produto necessário
3. Bertão calcula quantidade necessária (com margem de segurança)
4. Bertão apresenta opções de produtos
5. Cliente escolhe produto
6. Bertão sugere produtos complementares (argamassa, rejunte)
7. Cliente confirma carrinho completo
8. Fluxo de finalização

#### Jornada 3: Consulta de Preço e Disponibilidade
1. Cliente pergunta sobre produto específico
2. Bertão busca e apresenta preço e disponibilidade
3. Cliente decide comprar ou não
4. Se comprar, segue fluxo normal
5. Se não comprar, Bertão oferece alternativas

#### Jornada 4: Acompanhamento de Pedido
1. Cliente pergunta sobre status do pedido
2. Bertão consulta e informa status atual
3. Cliente recebe informações de rastreamento

---

## 3. Funcionalidades Principais

### 3.1. Busca Inteligente de Produtos
**O Que Faz**:
- Entende descrições em linguagem natural
- Busca mesmo com nomes incompletos ou errados
- Sugere alternativas quando produto não encontrado
- Trata sinônimos e termos populares

**Exemplo de Uso**:
- Cliente: "Preciso de cimento para fundação"
- Bertão: Busca e apresenta opções de cimento CP-II, CP-III, etc.

**Valor para o Cliente**: Encontra o que precisa sem precisar saber o nome técnico exato

### 3.2. Recomendação de Produtos Complementares
**O Que Faz**:
- Identifica produtos que geralmente são comprados juntos
- Sugere complementos após adicionar produto ao carrinho
- Oferece buscar produtos relacionados

**Exemplo de Uso**:
- Cliente adiciona piso ao carrinho
- Bertão: "Quer que eu veja o que temos de argamassa e rejunte?"

**Valor para o Cliente**: Não esquece de comprar itens necessários, aumenta qualidade da compra

### 3.3. Cálculo Automático de Quantidades
**O Que Faz**:
- Calcula quantidade necessária baseada em área informada
- Adiciona margem de segurança (15% para perdas)
- Sugere quantidade de caixas necessárias

**Exemplo de Uso**:
- Cliente: "Preciso de piso para 30m²"
- Bertão: "Você vai precisar de X caixas, considerando margem de segurança"

**Valor para o Cliente**: Compra a quantidade certa, evita falta ou excesso

### 3.4. Gerenciamento de Carrinho Intuitivo
**O Que Faz**:
- Adiciona produtos ao carrinho
- Remove ou altera quantidades
- Mostra resumo visual do carrinho
- Mantém carrinho entre conversas

**Exemplo de Uso**:
- Cliente pode pedir para ver o carrinho a qualquer momento
- Bertão mostra resumo formatado com todos os itens e totais

**Valor para o Cliente**: Controle total sobre a compra, transparência nos valores

### 3.5. Cálculo de Frete e Opções de Entrega
**O Que Faz**:
- Calcula frete automaticamente pelo CEP
- Apresenta opções (mais barata e mais rápida)
- Oferece retirada em loja física
- Valida endereço automaticamente

**Exemplo de Uso**:
- Cliente informa CEP
- Bertão: "Opções de frete: PAC (5 dias) - R$ 45 ou SEDEX (2 dias) - R$ 80"

**Valor para o Cliente**: Escolhe a melhor opção de entrega, sabe o custo antes de finalizar

### 3.6. Processamento de Mídia
**O Que Faz**:
- Recebe fotos de produtos e descreve
- Transcreve áudios
- Extrai texto de PDFs
- Usa mídia como contexto para busca

**Exemplo de Uso**:
- Cliente envia foto de um produto
- Bertão: "Vejo que você está interessado em [descrição]. Temos opções similares..."

**Valor para o Cliente**: Pode usar fotos para buscar, mais natural e fácil

### 3.7. Finalização de Pedido Guiada
**O Que Faz**:
- Coleta dados cadastrais de forma natural
- Guia passo a passo até o pagamento
- Gera link de pagamento seguro
- Oferece Pix (rápido) ou Cartão (parcelado)

**Exemplo de Uso**:
- Bertão pergunta dados faltantes de forma conversacional
- Após coletar tudo, gera link de pagamento
- Cliente paga e recebe confirmação

**Valor para o Cliente**: Processo simples e seguro, sem complicações

### 3.8. Atendimento Personalizado
**O Que Faz**:
- Lembra do histórico de compras
- Personaliza recomendações
- Usa nome do cliente
- Mantém contexto da conversa

**Exemplo de Uso**:
- "Oi Maria! Vi que você comprou piso mês passado. Precisa de mais alguma coisa?"

**Valor para o Cliente**: Experiência personalizada, sente-se conhecido

### 3.9. Escalonamento Inteligente
**O Que Faz**:
- Identifica quando precisa de atendimento humano
- Transfere para vendedor especializado
- Mantém contexto da conversa
- Informa prazo de retorno

**Exemplo de Uso**:
- Cliente precisa de orçamento grande volume
- Bertão: "Vou te conectar com nosso time comercial. Eles retornam em breve."

**Valor para o Cliente**: Recebe atendimento adequado para sua necessidade

---

## 4. Experiência do Usuário

### 4.1. Princípios de Design
- **Conversacional**: Fala como um vendedor humano, não como robô
- **Proativo**: Antecipa necessidades e oferece soluções
- **Claro**: Usa linguagem simples, evita jargões técnicos
- **Respeitoso**: Trata cliente com educação e atenção
- **Eficiente**: Resolve rápido, sem enrolação

### 4.2. Tom de Voz
- **Atencioso**: Demonstra interesse genuíno em ajudar
- **Direto**: Vai direto ao ponto, sem rodeios
- **Especialista**: Transmite conhecimento sobre produtos
- **Humano**: Usa linguagem natural, não robótica

### 4.3. Formatação de Mensagens
- **Negrito** para informações importantes (preços, códigos, totais)
- **Itálico** para observações e dicas
- Mensagens curtas e objetivas
- Divisão em múltiplas mensagens quando necessário

### 4.4. Fluxo Natural de Conversa
- Uma pergunta por vez
- Aguarda resposta antes de continuar
- Confirma entendimento
- Oferece ajuda quando necessário

---

## 5. Métricas de Sucesso

### 5.1. Métricas de Conversão
- **Taxa de Conversão**: % de conversas que resultam em venda
  - Meta: > 30%
- **Taxa de Finalização**: % de carrinhos que chegam ao pagamento
  - Meta: > 60%
- **Ticket Médio**: Valor médio por pedido
  - Meta: Aumentar 15% vs. vendas tradicionais
- **Taxa de Upsell**: % de pedidos com produtos complementares
  - Meta: > 40%

### 5.2. Métricas de Atendimento
- **Tempo de Resposta**: Tempo até primeira resposta
  - Meta: < 3 segundos
- **Taxa de Resolução**: % de dúvidas resolvidas sem escalonamento
  - Meta: > 80%
- **Satisfação do Cliente**: NPS ou avaliação
  - Meta: > 8.0/10
- **Taxa de Escalonamento**: % de conversas que precisam de humano
  - Meta: < 20%

### 5.3. Métricas de Engajamento
- **Conversas Atendidas**: Número de conversas por dia/mês
- **Taxa de Retorno**: % de clientes que voltam a comprar
- **Tempo Médio de Conversa**: Duração média das interações
- **Taxa de Abandono**: % de conversas abandonadas

### 5.4. Métricas de Negócio
- **Receita Gerada**: Valor total de vendas via Bertão
- **Custo por Venda**: Custo operacional por venda
- **ROI**: Retorno sobre investimento
- **Crescimento**: Crescimento mês a mês

---

## 6. Regras de Negócio

### 6.1. Regras de Venda
- **Preço Zerado**: Se produto não tem preço, buscar alternativa equivalente
- **Estoque**: Não mostrar quantidade disponível, apenas validar ao adicionar
- **Sinônimos**: Buscar automaticamente variações de nomes
- **Produtos Complementares**: Oferecer após adicionar produto principal

### 6.2. Regras de Pagamento
- **Pix como Padrão**: Oferecer Pix primeiro (aprovação imediata)
- **Cartão Opcional**: Oferecer cartão apenas se cliente solicitar
- **Parcelamento**: Máximo 10x, mínimo R$ 100 por parcela
- **Link de Pagamento**: Gerar apenas após confirmação de todos os dados

### 6.3. Regras de Entrega
- **Endereço Obrigatório**: Mesmo para retirada, precisa de endereço completo
- **CEP Primeiro**: Solicitar CEP antes de número e complemento
- **Opções de Frete**: Mostrar no máximo 2 opções (mais barata e mais rápida)
- **Retirada em Loja**: Disponível em 1 dia útil após confirmação

### 6.4. Regras de Escalonamento
- **PJ Automático**: Transferir automaticamente para time comercial
- **Insatisfação**: Escalonar se cliente demonstrar frustração
- **Negociação**: Escalonar para orçamentos grandes ou condições especiais
- **Dúvidas Técnicas**: Escalonar se exceder conhecimento do agente

---

## 7. Casos de Uso Principais

### 7.1. Caso de Uso 1: Primeira Compra
**Cenário**: Cliente nunca comprou na Copafer, precisa de materiais para reforma

**Fluxo**:
1. Cliente inicia conversa
2. Bertão se apresenta e pergunta como pode ajudar
3. Cliente descreve necessidade
4. Bertão busca produtos e apresenta opções
5. Cliente escolhe produtos
6. Bertão coleta dados cadastrais
7. Cliente escolhe entrega ou retirada
8. Bertão gera link de pagamento
9. Cliente finaliza compra

**Resultado Esperado**: Cliente completa primeira compra com facilidade

### 7.2. Caso de Uso 2: Cliente Recorrente
**Cenário**: Cliente já comprou antes, precisa repor estoque

**Fluxo**:
1. Cliente inicia conversa
2. Bertão reconhece cliente e personaliza atendimento
3. Cliente pede produtos específicos
4. Bertão adiciona ao carrinho (já tem dados cadastrais)
5. Cliente confirma e escolhe entrega
6. Bertão gera link de pagamento
7. Cliente finaliza compra

**Resultado Esperado**: Compra rápida e eficiente, aproveitando dados já cadastrados

### 7.3. Caso de Uso 3: Dúvida Técnica
**Cenário**: Cliente tem dúvida sobre qual produto usar

**Fluxo**:
1. Cliente descreve dúvida ou envia foto
2. Bertão analisa e explica opções
3. Bertão recomenda produto adequado
4. Cliente decide comprar
5. Fluxo normal de compra

**Resultado Esperado**: Cliente recebe orientação técnica e compra produto correto

### 7.4. Caso de Uso 4: Compra Empresarial
**Cenário**: Cliente é pessoa jurídica, precisa de orçamento

**Fluxo**:
1. Cliente informa que é PJ
2. Bertão identifica necessidade de atendimento especializado
3. Bertão coleta informações básicas
4. Bertão escalona para time comercial
5. Time comercial retorna com orçamento

**Resultado Esperado**: Cliente PJ recebe atendimento adequado para suas necessidades

---

## 8. Roadmap de Produto

### 8.1. Fase 1: MVP (Atual)
✅ Busca de produtos
✅ Gerenciamento de carrinho
✅ Cálculo de frete
✅ Finalização de pedido
✅ Processamento de mídia
✅ Escalonamento inteligente

### 8.2. Fase 2: Melhorias de Experiência (Próximos 3 meses)
- [ ] Recomendações personalizadas baseadas em histórico
- [ ] Lembretes de produtos que cliente costuma comprar
- [ ] Programa de fidelidade integrado
- [ ] Notificações de promoções personalizadas
- [ ] Suporte a múltiplos idiomas

### 8.3. Fase 3: Expansão de Funcionalidades (3-6 meses)
- [ ] Acompanhamento de pedido em tempo real
- [ ] Suporte a trocas e devoluções
- [ ] Chat com vendedor humano dentro do WhatsApp
- [ ] Agendamento de entrega
- [ ] Integração com outros canais (Instagram, Facebook)

### 8.4. Fase 4: Inteligência Avançada (6-12 meses)
- [ ] Análise de sentimento em tempo real
- [ ] Previsão de necessidades do cliente
- [ ] Otimização automática de carrinho
- [ ] Recomendações baseadas em IA avançada
- [ ] Integração com assistentes de voz

---

## 9. Riscos e Mitigações

### 9.1. Riscos Técnicos
**Risco**: Falhas em integrações podem interromper atendimento
**Mitigação**: Sistema de fallback e escalonamento automático

**Risco**: Respostas incorretas podem frustrar cliente
**Mitigação**: Validação constante, feedback loop, escalonamento quando necessário

### 9.2. Riscos de Negócio
**Risco**: Clientes podem preferir atendimento humano
**Mitigação**: Escalonamento fácil e rápido, manter opção humana sempre disponível

**Risco**: Taxa de conversão pode ser menor que esperado
**Mitigação**: A/B testing constante, melhorias baseadas em dados

### 9.3. Riscos de Experiência
**Risco**: Cliente pode se sentir "falando com robô"
**Mitigação**: Tom de voz natural, personalização, transparência quando necessário

**Risco**: Processo pode ser muito longo
**Mitigação**: Otimização de fluxos, salvamento de dados, atalhos para clientes recorrentes

---

## 10. Sucesso e Validação

### 10.1. Critérios de Sucesso
- **Conversão**: > 30% das conversas resultam em venda
- **Satisfação**: NPS > 8.0
- **Eficiência**: > 80% das dúvidas resolvidas sem escalonamento
- **Crescimento**: Aumento de 20% em vendas via WhatsApp em 6 meses

### 10.2. Como Validar
- **Testes A/B**: Comparar diferentes abordagens
- **Feedback de Clientes**: Pesquisas e avaliações
- **Análise de Conversas**: Identificar pontos de melhoria
- **Métricas em Tempo Real**: Dashboards e alertas

### 10.3. Iteração Contínua
- Revisão semanal de métricas
- Ajustes mensais baseados em dados
- Melhorias trimestrais baseadas em feedback
- Roadmap revisado a cada 6 meses

---

## 11. Conclusão

O **Bertão** representa uma evolução no atendimento ao cliente da Copafer, oferecendo uma experiência de compra moderna, eficiente e personalizada via WhatsApp. Com foco em conversão, experiência do cliente e escalabilidade, o produto está posicionado para se tornar o principal canal de vendas da empresa.

**Próximos Passos**:
1. Monitorar métricas de MVP
2. Coletar feedback de clientes
3. Priorizar melhorias baseadas em dados
4. Expandir funcionalidades conforme roadmap

---

**Versão**: 1.0  
**Data**: Janeiro 2025  
**Status**: Em Produção (MVP)

