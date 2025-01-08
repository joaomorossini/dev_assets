import os
from dotenv import load_dotenv
from textwrap import dedent
from datetime import datetime
from crewai import Agent, Task, Crew
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_community.tools import HumanInputRun
load_dotenv()

# Define LLM
llm = AzureChatOpenAI(
    model="gpt-4o",
)

# Function for getting human input
def get_human_input() -> str:
    print("Your feedback here (Enter 'q' to end.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "q":
            break
        contents.append(line)
    return "\n".join(contents)


human_input_tool = HumanInputRun(input_func=get_human_input)

# Define the Agents
analista_de_edital = Agent(
    role="Analista de Edital",
    goal=(
        "Extrair e categorizar SOMENTE os trechos do edital relevantes para a categoria Aliança Educacional, incluindo, mas não se restringindo prazos, critérios financeiros e condições de participação." 
    ),
    backstory=(
        "Um especialista em editais brasileiros de subvenção econômica para inovação. Detalhista e metódico, extrai com precisão os trechos mais relevantes do edital para que a Cogmo, uma startup brasileira de IA, possa utilizar essas informações para submeter uma proposta."
    ),
    llm=llm,
    temperature=0.4,
    verbose=True,
    allow_delegation=False,
)

analista_de_requisitos = Agent(
    role="Levantador de Requisitos",
    goal=(
        "Identificar em cada trecho do material disponível se algum requisito de participação ou submissão de proposta foi mencionado."
        "Se houver algum requisito, este deve ser categorizado descrito como um item de uma lista de verificação."
    ),
    backstory=(
        "Experiente em processos de subvenção econômica, este agente é especializado em identificar e categorizar as ações e exigências necessárias para participação e submissão de uma proposta"
    ),
    llm=llm,
    temperature=0.2,
    verbose=True,
    allow_delegation=False,
)

supervisor = Agent(
    role="Supervisor",
    goal=(
        "O supervisor é responsável por revisar o trabalho dos agentes anteriores e garantir que todas as informações relevantes tenham sido extraídas e categorizadas corretamente."
        "Ao final, este agente deve compilar um resumo abrangente dos documentos de licitação, incluindo um resumo geral e uma lista de verificação dos requisitos para submissão de proposta pela Cogmo."
        "Use a 'human_input_tool' para obter feedback e tirar dúvidas com o usuário"
    ),
    backstory=(
        "Um líder experiente em processos de subvenção econômica, este agente é especializado em avaliar e compilar informações de editais para garantir que a Cogmo possa submeter propostas de forma eficaz."
    ),
    llm=llm,
    temperature=0.0,
    verbose=True,
    allow_delegation=False,
    tools=[human_input_tool],
)

# Define the tasks
analise_de_edital = Task(
    description=(
        dedent("""
        Analisar o edital abaixo (delimitado por <<<>>>) para identificar, categorizar e extrair as sessões mais relevantes, sob o ponto de vista de uma startup de IA, que deseja submeter uma proposta.
        <<<{edital}>>>
        IMPORTANTE: VALIDAR COM O HUMANO O RESULTADO DA TAREFA ANTES DE PROSSEGUIR.
        """)
    ),
    expected_output=(
        dedent("""
        Uma lista de dicionários Python válidos, cada um contendo uma categoria e o trecho correspondente dos documentos de licitação, exatamente como consta dos originais.
        Os trechos devem ser categorizados em somente uma das categorias a seguir: prazos, financeiro, critérios_avaliacao, exigencias, outros
        Exemplos MERAMENTE ILUSTRATIVOS, delmitados por <<<>>>:
        <<<"[dict(categoria='prazos', trecho='Avaliação das propostas: 30 dias após o encerramento do prazo de submissão.'),
        dict(categoria='financeiro', trecho='O valor total disponível para subvenção é de R$ 1.000.000,00.'),
        dict(categoria='exigencias', trecho='Os documentos necessários para participação são: ...')]">>>
        IMPORTANTE:
        - Os exemplos fornecidos são meramente ilustrativos e não devem ser utilizados como parte do resultado final.
        """)
    ),
    agent=analista_de_edital,
    human_input=True
)

analise_de_requisitos = Task(
    description=(
        dedent("""Analisar: 
        1. Cada trecho do edital levantado pelo agente Analista de Edital e identificar se algum requisito de participação ou submissão de proposta foi mencionado.
        2. O modelo de proposta abaixo (delimitado por <<<>>>) e identificar os requisitos relacionados à construção do documento de proposta.
        <<<# Modelo de Proposta\n\n{modelo_de_proposta}>>>\n
        Os requisitos devem ser descritos como itens acionáveis (contendo verbos no infinitivo) de uma lista de verificação.
        Cada requisito levantado deve ser auto-suficiente e não depender de informações de outros requisitos. Seja específico e inclua todos os detalhes relevantes, mesmo correndo o risco de ser redundante.
        IMPORTANTE: VALIDAR COM O HUMANO O RESULTADO DA TAREFA ANTES DE PROSSEGUIR.
        """)
    ),
    expected_output=
    dedent("""
        Uma lista de dicionários, cada um contendo categoria, origem, transcrição do trecho correspondente e uma lista dos requisitos, quando houver.
        Abaixo, encontram-se exemplos MERAMENTE ILUSTRATIVOS, delimitados por <<<>>>:
        <<<dict(categoria='prazo', origem='edital', trecho='Avaliação das propostas: XX dias após ...', requisitos=[]),
        dict(categoria='financeiro', origem='edital', trecho='O valor total disponível para subvenção é de R$ XX.000.000,00.', requisitos=[]),
        dict(categoria='submissao_da_proposta', origem='modelo_de_proposta', trecho='Os documentos necessários para participação são documento X, documento Y e documento Z', requisitos=['apresentar documento X', 'apresentar documento Y', 'apresentar documento Z'])>>>
    """),
    agent=analista_de_requisitos,
    context=[analise_de_edital],
    human_input=True
)

compilacao_de_resumo = Task(
    description=
        dedent("""
            Verificar se cada um dos requisitos levantados realmente está de acordo com os trechos extraídos dos documentos originais
            e compilar um resumo abrangente dos documentos de licitação, incluindo um resumo geral e uma lista de verificação dos requisitos para submissão de proposta pela Cogmo.
            Sempre que encontrar um requisito que não esteja de acordo com o trecho original, o agente deve solicitar a revisão daquele item ao Analista de Requisitos".
            IMPORTANTE: VALIDAR COM O HUMANO O RESULTADO DA TAREFA ANTES DE PROSSEGUIR.
            """),
    expected_output=
        dedent("""
            Resposta final (Final Answer) dividida em 3 tópicos principais:
               1) GLOSSÁRIO: Contendo apenas expressões ou palavras que demandam conhecimento do contexto do edital para serrem compreendidas.
               2) DESCRITIVO: Breve resumo dos trechos mais relevantes, organizados por tópico
               3) CHECKLIST: Lista de todos os requisitos para submissão da proposta, agrupados por assunto.
            Abaixo, encontra-se um BREVE MODELO (delimitado por <<<>>>) do FORMATO DESEJADO para o resultado final:
            <<<# GLOSSÁRIO
               - Macroentregas: primeiro nível da EAP do projeto, a ser entregue com a proposta
               - Contrapartida financeira: ...
               - Contrapartida econômica: ...

            # DESCRITIVO

            ## Tópico 1
            Resumo das informações relevantes para o tópico 1
            ...
                        
            ## Tópico 2
            Resumo das informações relevantes para o tópico 2
            ...
               
            ## Tópico 3
            ...
            
            ## Outros tópicos
            ...
                        
            # CHECKLIST
            - [ ] Assunto X
                - [ ] Apresentar documento X
                - [ ] Apresentar documento Y
                - [ ] Apresentar documento Z no modelo fornecido nos anexos do edital
            - [ ] Assunto Y
               - [ ] Descrever a startup proponente
                - [ ] Histórico da empresa
                - [ ] Projetos anteriores
            - [ ] Assunto Z
               ...>>>
            EXTREMAMENTE IMPORTANTE:
            - O modelo fornecido é meramente ilustrativo. Seu conteúdo NÃO deve ser utilizado como parte do resultado final.
            - Espera-se que o resultado final seja mais detalhado e completo, de acordo com o edital e o modelo de proposta fornecidos.
            """),
    agent=supervisor,
    output_file = f'summary_{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.md',
    human_input=True,
    context=[analise_de_requisitos]
)

# Assemble the crew
crew = Crew(
    agents=[analista_de_edital, analista_de_requisitos, supervisor],
    tasks=[analise_de_edital, analise_de_requisitos, compilacao_de_resumo],
    verbose=2,
    # memory=True
)

# Read multiple Markdown documents
with open("/Users/morossini/Projects/Prototypes/Cogmo/LicitaBot/tender_summary_crew/docs/edital.md", "r") as file:
    edital = file.read()
with open("/Users/morossini/Projects/Prototypes/Cogmo/LicitaBot/tender_summary_crew/docs/modelo_proposta.md", "r") as file:
    modelo_proposta = file.read()
documents = {"edital": edital, "modelo_de_proposta": modelo_proposta}
print(documents)

result = crew.kickoff(inputs=documents)

summary_path = "/Users/morossini/Projects/Prototypes/Cogmo/LicitaBot/tender_summary_crew/summary.md"

# Check if the file exists, if not, create it
if not os.path.exists(summary_path):
    with open(summary_path, "w") as f:
        pass

# Save the final output
with open(summary_path, "w") as f:
    f.write(str(result))

# Print the result
print("\n==========================================================================")
print(f"Complete results: \n{str(result)}")
print("==========================================================================")
