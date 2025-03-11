O diagrama de arquitetura descreve a interação entre diferentes componentes e serviços utilizados no projeto NOVObot. A arquitetura é dividida em duas partes principais: "cobrador-wpp" e "chat-site".

Descrição Detalhada:
Requisição de Cobrança (webhook):

Inicia o fluxo para o agente cobrador, enviando uma requisição para o CogmoFlow.
CogmoFlow:

Serve como ponto central para processar as requisições tanto do cobrador quanto do chat do site.
No caso do cobrador, interage com a API não oficial do WhatsApp (Evolution) para enviar mensagens.
Para ambos os casos, se comunica com o CRM Cogmo.
WhatsApp API (Evolution):

Utilizada pelo CogmoFlow na parte de cobrança para enviar mensagens via WhatsApp.
CRM Cogmo:

Centraliza as informações dos usuários e gerencia as interações tanto para cobranças quanto para atendimento no site.
Interage com um atendente humano quando necessário.
Cogmo-AI:

Responsável por fornecer inteligência artificial às interações, tanto no contexto de cobrança quanto no chat do site.
Atendente Novo:

Um componente humano que pode intervir nas conversas gerenciadas pelo CRM Cogmo quando necessário.
Base de Dados:

Armazena informações relevantes utilizadas pelos diferentes componentes da arquitetura.
Portainer:

Ferramenta utilizada para gerenciar os containers onde os serviços estão hospedados.
Integração com Aplicativos Móveis e Site (novo.org.br):

O fluxo permite interação através de aplicativos móveis e diretamente pelo site novo.org.br, utilizando o CogmoFlow como intermediário.
Tradução para Mermaid:
Mermaid
graph TD;
subgraph cobrador-wpp
A[Requisição de Cobrança] --> B[CogmoFlow]
B --> C[WhatsApp API (Evolution)]
B --> D[CRM Cogmo]
D --> E[Cogmo-AI]
D --> F[Atendente Novo]
end

    subgraph chat-site
        G[novo.org.br] --> H[CogmoFlow]
        H --> I[CRM Cogmo]
        I --> J[Cogmo-AI]
    end

    K[Base de Dados] --- D
    L[Portainer] --- B

Este diagrama em Mermaid representa visualmente a mesma estrutura apresentada na imagem original, destacando as conexões entre os componentes principais da arquitetura do projeto NOVObot.
