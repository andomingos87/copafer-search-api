# Guia Completo: Túneis VPN, WireGuard e Conexão com Redis na Fly.io

## 📚 Índice

1. [O que é um Túnel?](#o-que-é-um-túnel)
2. [O que é WireGuard?](#o-que-é-wireguard)
3. [Como Funciona o WireGuard?](#como-funciona-o-wireguard)
4. [O Arquivo de Configuração (.conf)](#o-arquivo-de-configuração-conf)
5. [Caso Prático: Redis na Fly.io](#caso-prático-redis-na-flyio)
6. [Conceitos de Rede](#conceitos-de-rede)
7. [Segurança e Boas Práticas](#segurança-e-boas-práticas)
8. [Troubleshooting](#troubleshooting)

---

## O que é um Túnel?

### Definição Simples

Um **túnel** é uma conexão segura entre dois pontos na internet que permite que dados trafeguem de forma protegida, como se estivessem passando por um "canal privado" dentro da internet pública.

### Analogia do Mundo Real

Imagine que você precisa enviar uma carta confidencial para um amigo em outra cidade:

- **Sem túnel**: Você coloca a carta em um envelope comum e envia pelo correio público. Qualquer pessoa pode interceptar e ler.
- **Com túnel**: Você coloca a carta em um envelope à prova de violação, coloca dentro de um cofre, e envia por um serviço de segurança privada. Mesmo que alguém intercepte, não consegue ler o conteúdo.

### Túneis em Computação

Em computação, um túnel funciona de forma similar:

```
┌─────────────┐                    ┌─────────────┐
│  Seu PC     │                    │  Servidor   │
│ (localhost) │                    │  (Fly.io)   │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │  ┌──────────────────────────┐   │
       │  │   Internet Pública       │   │
       │  │  (potencialmente         │   │
       │  │   insegura)              │   │
       │  └──────────────────────────┘   │
       │                                  │
       └────────── Túnel VPN ─────────────┘
              (conexão criptografada)
```

### Tipos de Túneis

1. **VPN Túnel**: Conecta seu computador a uma rede privada remota
2. **SSH Túnel**: Cria um túnel através de uma conexão SSH
3. **TLS/SSL Túnel**: Criptografa dados usando TLS/SSL
4. **WireGuard Túnel**: Protocolo moderno de VPN (o que estamos usando)

---

## O que é WireGuard?

### Definição

**WireGuard** é um protocolo de VPN (Virtual Private Network) moderno, rápido e seguro. Foi criado em 2015 por Jason A. Donenfeld e se tornou muito popular por ser:

- ⚡ **Rápido**: Mais rápido que OpenVPN e IPSec
- 🔒 **Seguro**: Usa criptografia de última geração
- 🎯 **Simples**: Código pequeno e fácil de auditar
- 🔧 **Fácil de configurar**: Arquivo de configuração simples

### Por que WireGuard é Especial?

#### 1. Código Minimalista

- OpenVPN: ~600.000 linhas de código
- IPSec: ~400.000 linhas de código
- **WireGuard: ~4.000 linhas de código**

Menos código = menos bugs = mais segurança!

#### 2. Criptografia Moderna

WireGuard usa algoritmos de criptografia de última geração:

- **Curve25519**: Para troca de chaves
- **ChaCha20**: Para criptografia simétrica
- **Poly1305**: Para autenticação
- **BLAKE2s**: Para hash

#### 3. Performance

WireGuard é significativamente mais rápido que outras VPNs porque:

- Usa criptografia mais eficiente
- Tem menos overhead (sobrecarga)
- Implementação otimizada

### Comparação com Outras VPNs

| Característica | WireGuard | OpenVPN | IPSec |
|---------------|-----------|---------|-------|
| Velocidade | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Segurança | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Facilidade | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ |
| Código | 4K linhas | 600K linhas | 400K linhas |

---

## Como Funciona o WireGuard?

### Arquitetura Básica

WireGuard cria uma **interface de rede virtual** no seu sistema operacional. Essa interface funciona como uma "ponte" entre seu computador e a rede remota.

```
┌─────────────────────────────────────────────────┐
│           Seu Computador                        │
│                                                 │
│  ┌──────────────┐         ┌─────────────────┐  │
│  │  Aplicação   │         │  Interface      │  │
│  │  (Python)    │────────▶│  WireGuard     │  │
│  └──────────────┘         │  (wg0)         │  │
│                            └────────┬────────┘  │
│                                     │           │
│                            ┌────────▼────────┐  │
│                            │  Internet       │  │
│                            └─────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Componentes Principais

#### 1. **Interface (Peer Local)**

- Representa **seu computador** na rede WireGuard
- Tem uma **chave privada** (PrivateKey)
- Recebe um **endereço IP** na rede privada

#### 2. **Peer (Par Remoto)**

- Representa o **servidor** (Fly.io no nosso caso)
- Tem uma **chave pública** (PublicKey)
- Define quais **IPs** podem ser acessados através dele

#### 3. **Handshake (Aperto de Mãos)**

Quando você se conecta, o WireGuard faz um "handshake" criptográfico:

1. Seu computador envia uma mensagem criptografada com a chave pública do servidor
2. O servidor verifica e responde
3. Ambos estabelecem uma "sessão" criptografada
4. Dados podem trafegar de forma segura

### Fluxo de Dados

```
1. Aplicação Python tenta conectar ao Redis
   ↓
2. Sistema operacional vê que o IP está na rede privada
   ↓
3. Roteia o tráfego para a interface WireGuard
   ↓
4. WireGuard criptografa os dados
   ↓
5. Dados trafegam pela internet pública (criptografados)
   ↓
6. Servidor WireGuard na Fly.io recebe e descriptografa
   ↓
7. Dados são entregues ao Redis na rede privada
   ↓
8. Resposta segue o caminho inverso
```

---

## O Arquivo de Configuração (.conf)

### Estrutura do Arquivo

O arquivo `wireguard-fly.conf` que criamos tem esta estrutura:

```ini
[Interface]
PrivateKey = rVPo/iMBf3kKICt9UqZP0v034M4qlow+94fIdBoRnlo=
Address = fdaa:32:cea7:a7b:8cfe:0:a:302/120
DNS = fdaa:32:cea7::3

[Peer]
PublicKey = q+cTUCrE9NekeuZEF/gCYxr2wNBjvYgGoqYwV1logEI=
AllowedIPs = fdaa:32:cea7::/48
Endpoint = iad2.gateway.6pn.dev:51820
PersistentKeepalive = 15
```

### Seção [Interface]

Define a configuração do **seu computador** (o cliente):

#### `PrivateKey`
```ini
PrivateKey = rVPo/iMBf3kKICt9UqZP0v034M4qlow+94fIdBoRnlo=
```

- **O que é**: Sua chave privada (secreta!)
- **Função**: Usada para criptografar dados que você envia
- **Segurança**: ⚠️ **NUNCA compartilhe esta chave!** É como sua senha pessoal
- **Formato**: String base64 de 44 caracteres

#### `Address`
```ini
Address = fdaa:32:cea7:a7b:8cfe:0:a:302/120
```

- **O que é**: O endereço IP que seu computador receberá na rede privada da Fly.io
- **Formato**: Endereço IPv6 com máscara de sub-rede (`/120`)
- **Explicação**:
  - `fdaa:32:cea7:a7b:8cfe:0:a:302` = Seu IP na rede privada
  - `/120` = Máscara de sub-rede (define o tamanho da rede)
- **Analogia**: É como receber um número de telefone interno na empresa

#### `DNS`
```ini
DNS = fdaa:32:cea7::3
```

- **O que é**: Servidor DNS da Fly.io
- **Função**: Resolve nomes de host da rede privada (como `fly-fragrant-resonance-5825.upstash.io`)
- **Por que é importante**: Sem isso, você não consegue resolver nomes de host privados

### Seção [Peer]

Define a configuração do **servidor** (Fly.io):

#### `PublicKey`
```ini
PublicKey = q+cTUCrE9NekeuZEF/gCYxr2wNBjvYgGoqYwV1logEI=
```

- **O que é**: Chave pública do servidor WireGuard da Fly.io
- **Função**: Usada para criptografar dados que você envia ao servidor
- **Segurança**: ✅ Pode ser compartilhada publicamente (é pública mesmo!)
- **Formato**: String base64 de 44 caracteres

#### `AllowedIPs`
```ini
AllowedIPs = fdaa:32:cea7::/48
```

- **O que é**: Define quais endereços IP devem passar pelo túnel WireGuard
- **Formato**: CIDR (notação de rede)
- **Explicação**:
  - `fdaa:32:cea7::/48` significa: "todos os IPs que começam com `fdaa:32:cea7`"
  - Isso inclui todos os serviços da Fly.io na região GRU
- **Função**: Diz ao sistema operacional: "quando você quiser acessar um IP que começa com `fdaa:32:cea7`, use o WireGuard"

#### `Endpoint`
```ini
Endpoint = iad2.gateway.6pn.dev:51820
```

- **O que é**: Endereço do servidor WireGuard da Fly.io
- **Formato**: `hostname:porta`
- **Explicação**:
  - `iad2.gateway.6pn.dev` = Servidor na região IAD (Washington, EUA)
  - `51820` = Porta padrão do WireGuard (UDP)
- **Função**: É para onde seu computador se conecta para estabelecer o túnel

#### `PersistentKeepalive`
```ini
PersistentKeepalive = 15
```

- **O que é**: Intervalo (em segundos) para enviar pacotes "keepalive"
- **Função**: Mantém a conexão ativa mesmo quando não há tráfego
- **Por que é importante**: Alguns roteadores/firewalls fecham conexões inativas
- **Valor**: 15 segundos = a cada 15 segundos, envia um pequeno pacote para manter a conexão viva

### Visualização Completa

```
┌─────────────────────────────────────────────────────────┐
│  [Interface] - Seu Computador                           │
│  ┌───────────────────────────────────────────────────┐ │
│  │ PrivateKey: Sua chave secreta                     │ │
│  │ Address: fdaa:32:cea7:a7b:8cfe:0:a:302/120        │ │
│  │         ↑ Seu IP na rede privada                   │ │
│  │ DNS: fdaa:32:cea7::3                               │ │
│  │      ↑ Servidor DNS da Fly.io                      │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                        ↕ Túnel Criptografado
┌─────────────────────────────────────────────────────────┐
│  [Peer] - Servidor Fly.io                               │
│  ┌───────────────────────────────────────────────────┐ │
│  │ PublicKey: Chave pública do servidor               │ │
│  │ AllowedIPs: fdaa:32:cea7::/48                     │ │
│  │            ↑ Todos os IPs da Fly.io GRU            │ │
│  │ Endpoint: iad2.gateway.6pn.dev:51820               │ │
│  │          ↑ Servidor WireGuard                       │ │
│  │ PersistentKeepalive: 15                            │ │
│  │                    ↑ Mantém conexão viva            │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Caso Prático: Redis na Fly.io

### O Problema

Você tem um Redis Upstash rodando na Fly.io:

```
Redis: fly-fragrant-resonance-5825.upstash.io
IP: fdaa:32:cea7:0:1::2
Rede: Privada (só acessível dentro da Fly.io)
```

**Problema**: Como acessar esse Redis do seu computador local?

### Solução: WireGuard

#### Passo 1: Criar o Túnel

```bash
flyctl wireguard create cuboai gru wireguard-local-redis wireguard-fly.conf
```

**O que acontece**:
1. Fly.io cria um "peer" WireGuard para você
2. Gera uma chave privada para seu computador
3. Atribui um IP na rede privada da Fly.io
4. Salva tudo no arquivo `.conf`

#### Passo 2: Importar no WireGuard

1. Abra o aplicativo WireGuard no Windows
2. Clique em "Import tunnel(s) from file"
3. Selecione `wireguard-fly.conf`
4. Clique em "Activate"

**O que acontece**:
- WireGuard cria uma interface de rede virtual
- Estabelece conexão com o servidor da Fly.io
- Seu computador agora "faz parte" da rede privada da Fly.io

#### Passo 3: Configurar o .env

```env
REDIS_HOST=fdaa:32:cea7:0:1::2
REDIS_PORT=6379
REDIS_PASSWORD=05d65280d95f439ea18203d1616473e5
REDIS_USER=default
REDIS_SSL=false
```

**Por que IPv6 direto?**
- O DNS da Fly.io (`fdaa:32:cea7::3`) pode não estar funcionando no Windows
- Usar o IP diretamente é mais confiável

#### Passo 4: Testar Conexão

```bash
python test_redis_connection.py
```

**O que acontece**:

```
1. Python tenta conectar ao fdaa:32:cea7:0:1::2:6379
   ↓
2. Sistema operacional vê que o IP começa com fdaa:32:cea7
   ↓
3. Roteia para a interface WireGuard (por causa do AllowedIPs)
   ↓
4. WireGuard criptografa e envia para iad2.gateway.6pn.dev:51820
   ↓
5. Servidor WireGuard da Fly.io recebe e descriptografa
   ↓
6. Entrega o pacote ao Redis na rede privada
   ↓
7. Redis responde
   ↓
8. Resposta segue o caminho inverso (criptografada)
   ↓
9. Seu computador recebe e descriptografa
   ↓
10. Python recebe a resposta do Redis ✅
```

### Diagrama Completo

```
┌─────────────────────────────────────────────────────────────┐
│  Seu Computador (Windows)                                    │
│                                                              │
│  ┌──────────────┐                                           │
│  │ Python App   │                                           │
│  │              │                                           │
│  │ redis.Redis( │                                           │
│  │   host='fdaa │                                           │
│  │   :32:cea7:0 │                                           │
│  │   :1::2'     │                                           │
│  │ )            │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│  ┌──────▼──────────────────────────────────────────────┐   │
│  │ Sistema Operacional                                  │   │
│  │ "IP fdaa:32:cea7:0:1::2 está em AllowedIPs"         │   │
│  │ "Roteie para interface WireGuard"                    │   │
│  └──────┬──────────────────────────────────────────────┘   │
│         │                                                    │
│  ┌──────▼──────────────────────────────────────────────┐   │
│  │ Interface WireGuard (wg0)                            │   │
│  │ - Criptografa com PrivateKey                         │   │
│  │ - Adiciona cabeçalho WireGuard                       │   │
│  └──────┬──────────────────────────────────────────────┘   │
└─────────┼──────────────────────────────────────────────────┘
          │
          │ Internet Pública (Criptografado)
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│  Servidor WireGuard Fly.io                                   │
│  (iad2.gateway.6pn.dev:51820)                              │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ - Recebe pacote criptografado                        │   │
│  │ - Verifica com PublicKey                             │   │
│  │ - Descriptografa                                     │   │
│  │ - Remove cabeçalho WireGuard                         │   │
│  └──────┬───────────────────────────────────────────────┘   │
│         │                                                    │
│  ┌──────▼──────────────────────────────────────────────┐   │
│  │ Rede Privada Fly.io (fdaa:32:cea7::/48)            │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │ Redis Upstash                                │   │   │
│  │  │ fdaa:32:cea7:0:1::2:6379                     │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Conceitos de Rede

### IPv6 vs IPv4

#### IPv4 (Versão Antiga)
```
Formato: 192.168.1.1
Exemplo: 127.0.0.1 (localhost)
Tamanho: 32 bits = ~4 bilhões de endereços
```

#### IPv6 (Versão Nova)
```
Formato: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
Exemplo: fdaa:32:cea7:0:1::2
Tamanho: 128 bits = 340 undecilhões de endereços!
```

**Por que IPv6?**
- IPv4 está esgotando (já acabou na verdade!)
- IPv6 permite muito mais dispositivos
- Fly.io usa IPv6 para sua rede privada

### CIDR (Notação de Rede)

CIDR significa "Classless Inter-Domain Routing". É uma forma de representar um intervalo de IPs.

#### Exemplos

```
fdaa:32:cea7::/48

Significa: Todos os IPs que começam com fdaa:32:cea7

Inclui:
- fdaa:32:cea7:0:1::2 (Redis)
- fdaa:32:cea7:a7b:8cfe:0:a:302 (Seu PC)
- fdaa:32:cea7::3 (DNS)
- ... e muitos outros
```

```
192.168.1.0/24

Significa: Todos os IPs de 192.168.1.0 até 192.168.1.255

Inclui:
- 192.168.1.1
- 192.168.1.2
- ...
- 192.168.1.255
```

### DNS (Domain Name System)

DNS converte nomes (como `google.com`) em IPs (como `142.250.191.14`).

**No nosso caso**:
```
fly-fragrant-resonance-5825.upstash.io → fdaa:32:cea7:0:1::2
```

**Por que precisamos do DNS da Fly.io?**
- O DNS público da internet não conhece os nomes privados da Fly.io
- O DNS da Fly.io (`fdaa:32:cea7::3`) conhece todos os serviços privados

---

## Segurança e Boas Práticas

### 🔒 Segurança do WireGuard

#### 1. Chaves

- **PrivateKey**: ⚠️ **NUNCA compartilhe!** É como sua senha pessoal
- **PublicKey**: ✅ Pode ser pública, é usada para identificar você

#### 2. Criptografia

WireGuard usa criptografia de última geração:
- **Curve25519**: Impossível de quebrar com tecnologia atual
- **ChaCha20**: Criptografia simétrica rápida e segura
- **Poly1305**: Garante que dados não foram alterados

#### 3. Autenticação

- Cada conexão precisa de chaves válidas
- Não há senhas fracas ou vulneráveis
- Chaves são geradas criptograficamente seguras

### ✅ Boas Práticas

#### 1. Proteger o Arquivo .conf

```bash
# No Linux/Mac
chmod 600 wireguard-fly.conf

# No Windows
# Clique com botão direito > Propriedades > Segurança
# Remova permissões de leitura para outros usuários
```

#### 2. Não Commitar no Git

Adicione ao `.gitignore`:
```
wireguard-fly.conf
*.conf
```

#### 3. Rotacionar Chaves

Se suspeitar que sua chave foi comprometida:
```bash
# Remove o peer antigo
flyctl wireguard remove cuboai wireguard-local-redis

# Cria um novo
flyctl wireguard create cuboai gru wireguard-local-redis-new wireguard-fly.conf
```

#### 4. Usar Túneis Específicos

- Crie túneis separados para diferentes propósitos
- Não compartilhe túneis entre equipes sem necessidade

### ⚠️ Avisos Importantes

1. **PrivateKey é Secreta**: Se alguém tiver sua PrivateKey, pode se passar por você
2. **Endpoint Público**: O endpoint do WireGuard é público, mas só funciona com chaves válidas
3. **AllowedIPs**: Configure corretamente para não vazar tráfego

---

## Troubleshooting

### Problema: "Connection refused" ou "Connection timeout"

**Possíveis causas**:
1. WireGuard não está ativo
2. Túnel expirou ou foi removido
3. Firewall bloqueando porta 51820

**Soluções**:
```bash
# Verificar se WireGuard está ativo
wg show

# Verificar túneis na Fly.io
flyctl wireguard list cuboai

# Recriar túnel se necessário
flyctl wireguard create cuboai gru wireguard-local-redis wireguard-fly.conf
```

### Problema: "DNS resolution failed"

**Possíveis causas**:
1. DNS da Fly.io não está configurado
2. WireGuard não está roteando DNS corretamente

**Soluções**:
- Use o IP diretamente ao invés do hostname
- Verifique se `DNS = fdaa:32:cea7::3` está no arquivo .conf

### Problema: "Cannot reach Redis"

**Possíveis causas**:
1. IP do Redis mudou
2. AllowedIPs não inclui o IP do Redis
3. Redis está em outra região

**Soluções**:
```bash
# Verificar status do Redis
flyctl redis status fragrant-resonance-5825

# Verificar IP atual
# Use o IP diretamente no .env
```

### Problema: Conexão lenta

**Possíveis causas**:
1. Endpoint muito distante (ex: IAD quando você está no Brasil)
2. Latência de rede

**Soluções**:
- Crie túnel na região mais próxima (GRU para Brasil)
- Verifique se `PersistentKeepalive` está configurado

### Comandos Úteis

```bash
# Listar túneis WireGuard
flyctl wireguard list cuboai

# Ver status de um túnel
flyctl wireguard status cuboai wireguard-local-redis

# Remover um túnel
flyctl wireguard remove cuboai wireguard-local-redis

# Verificar conexão WireGuard local
wg show

# Testar conectividade
ping fdaa:32:cea7::3
```

---

## Resumo

### O que aprendemos:

1. **Túnel**: Conexão segura entre dois pontos na internet
2. **WireGuard**: Protocolo VPN moderno, rápido e seguro
3. **Arquivo .conf**: Configuração que define como conectar ao túnel
4. **Caso prático**: Como usar WireGuard para acessar Redis privado na Fly.io

### Conceitos-chave:

- **Interface**: Seu computador na rede WireGuard
- **Peer**: Servidor remoto (Fly.io)
- **PrivateKey**: Sua chave secreta (nunca compartilhe!)
- **PublicKey**: Chave pública do servidor
- **AllowedIPs**: Define quais IPs passam pelo túnel
- **Endpoint**: Endereço do servidor WireGuard

### Próximos Passos:

1. ✅ Entender como túneis funcionam
2. ✅ Compreender WireGuard
3. ✅ Saber ler arquivos .conf
4. ✅ Aplicar no caso do Redis na Fly.io
5. 🎯 Praticar criando e gerenciando túneis

---

## Referências

- [Documentação Oficial do WireGuard](https://www.wireguard.com/)
- [WireGuard Protocol Explanation](https://www.wireguard.com/protocol/)
- [Fly.io WireGuard Documentation](https://fly.io/docs/reference/private-networking/)
- [RFC 4193 - Unique Local IPv6 Unicast Addresses](https://tools.ietf.org/html/rfc4193)

---

**Documento criado em**: 2025-01-28  
**Autor**: Assistente AI  
**Versão**: 1.0

