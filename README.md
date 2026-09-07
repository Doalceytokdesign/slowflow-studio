# Slow Flow Studio — Infraestrutura n8n & Local Setup

Infraestrutura local automatizada para orquestração de workflows, automações de IA e captura de leads do **Slow Flow Studio** utilizando Docker e Docker Compose.

---

## 🚀 Como Subir o n8n Localmente

Certifique-se de que o **Docker Desktop** está em execução na sua máquina.

### 1. Iniciar o Container em Segundo Plano
No terminal, dentro da pasta raiz do projeto (`SlowFlow_Studio`), execute:

```bash
docker compose up -d
```

### 2. Acessar o Painel de Controle
Abra o navegador e acesse:

👉 **[http://localhost:5678](http://localhost:5678)**

> No primeiro acesso, crie sua conta de proprietário (Nome, E-mail e Senha) para liberar o canvas de automação.

---

## ⚡ Integração com o Webhook de Leads (WhatsApp)

O frontend do Slow Flow Studio já está preparado para enviar os dados dos leads diretamente para o n8n via telemetria assíncrona (`navigator.sendBeacon` / `fetch keepalive`).

### Configurando o Workflow no n8n:
1. No painel do n8n, crie um novo workflow (**"Add workflow"**).
2. Adicione o trigger **Webhook**:
   - **HTTP Method:** `POST`
   - **Path:** `webhook/leads-whatsapp`
   - **Respond:** `Immediately` com status `200`
3. Salve e ative o workflow (**Active: ON**).
4. Ao clicar em qualquer botão de contato no site (`Iniciar Projeto Web`, `Construir Minha Marca`, `Falar com um Especialista` ou `Rodapé`), o n8n receberá o payload com:
   - Identificação do botão (`cta_label`)
   - Número de destino (`target_whatsapp`)
   - URL de conversão e página
   - Dados de campanha (`utm_source`, `utm_campaign`, etc.)
   - Tipo de dispositivo (`mobile` / `desktop`) e timestamp

---

## 🛠️ Comandos Úteis do Docker

| Ação | Comando |
| :--- | :--- |
| **Iniciar containers** | `docker compose up -d` |
| **Verificar status** | `docker compose ps` |
| **Ver logs em tempo real** | `docker compose logs -f n8n` |
| **Pausar o n8n** | `docker compose stop` |
| **Reiniciar o container** | `docker compose restart` |
| **Parar e remover container** *(dados seguros no volume)* | `docker compose down` |
| **Atualizar para a última versão** | `docker compose pull && docker compose up -d` |

---

## 💾 Persistência de Dados

Todos os seus fluxos, credenciais, configurações e histórico de execuções ficam salvos no volume Docker nomeado `slowflow_n8n_data`, mapeado diretamente para `/home/node/.n8n`.

Mesmo que o container seja reiniciado, atualizado ou removido via `docker compose down`, **seus dados e credenciais permanecem 100% preservados**.

---

## ⚙️ Configurações Opcionais (.env)

Caso queira customizar portas, fuso horário ou URLs de webhook para túneis externos (ngrok / cloudflare):

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```
2. Edite as variáveis no arquivo `.env` gerado.
