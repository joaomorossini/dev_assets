# Como criar uma nova instância do NOVObot cobrador

Por: João Morossini
Atualizado em: 23/01/2025, às 15h

Para utilizar o NOVObot cobrador com mais de um número de whatsapp é necessário

# Passo a Passo

1. Criar uma nova caixa de entrada no CRM
2. Duplicar e renomear as seguintes automações no N8n:
   - Automação "Configurar NOVObot_cobrador"
   - Automação "Trigger - Novobot whatsapp - cobrança de inadimplentes"
   - Automação "Controle de sessao do atendimento Humano"
3. Em todas as automações, alterar o nome desejado para a nova instância da Evolution API. A instância padrão é "NOVObot_cobrador". As instâncias adicionais devem ser nomeadas "Novobot_cobrador_2", "Novobot_cobrador_3", etc.
4. Executar a nova automação "Configurar NOVObot_cobrador" com o novo nome da instância.
5. Acessar a Evolution API, clicar na nova instância recém criada, gerar QR code e escanear com o novo número de whatsapp.
6. Na nova instância da Evolution API, certifique-se de que o nome da inbox no CRM (Chatwoot) está correto.
   - Menu "Integrations" -> Chatwoot -> "Name Inbox"
7. Criar nova versão da coleção do Postman, com gatilhos para o novo webhook. Isso é necessário porque nesse método básico de criação de nova instância, cada uma delas tem um webhook diferente.

# Recomendações

- Na base de dados dos filiados do NOVO, associar cada filiado a uma instância específica do cobrador, para que o filiado seja atendido sempre pelo mesmo número de whatsapp.
- No futuro, caso o Partido NOVO decida utilizar vários números para o cobrador, será necessário rever esse processo para torná-lo mais automático e simples.
