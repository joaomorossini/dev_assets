import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import AzureChatOpenAI

load_dotenv()

azure_llm = AzureChatOpenAI(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY"),
    model="gpt-4o",
)

analista_de_edital = Agent(
    role="Analista de Edital",
    goal=(
        "Extrair e categorizar os trechos mais relevantes do edital, incluindo, mas não se restringindo prazos, critérios financeiros e condições de participação."
    ),
    backstory=(
        "Um especialista em editais brasileiros de subvenção econômica para inovação. Detalhista e metódico, extrai com precisão os trechos mais relevantes do edital para que a Cogmo, uma startup brasileira de IA, possa utilizar essas informações para submeter uma proposta."
    ),
    llm=azure_llm,
    temperature=0.4,
    verbose=True,
    allow_delegation=False,
)

analista_de_requisitos = Agent(
    role="Levantador de Requisitos",
    goal=(
        "Identificar em cada trecho do material preparado pelo Analista de Edital se algum requisito de participação ou submissão de proposta foi mencionado."
        "Se houver algum requisito, este deve ser categorizado descrito como um item de uma lista de verificação."
    ),
    backstory=(
        "Experiente em processos de subvenção econômica, este agente é especializado em identificar e categorizar requisitos de participação e submissão de propostas."
    ),
    llm=azure_llm,
    temperature=0.2,
    verbose=True,
    allow_delegation=False,
)

supervisor = Agent(
    role="Supervisor",
    goal=(
        "O supervisor é responsável por revisar o trabalho dos agentes anteriores e garantir que todas as informações relevantes tenham sido extraídas e categorizadas corretamente."
        "Ao final, este agente deve compilar um resumo abrangente dos documentos de licitação, incluindo um resumo geral e uma lista de verificação dos requisitos para submissão de proposta pela Cogmo."
    ),
    backstory=(
        "Um líder experiente em processos de subvenção econômica, este agente é especializado em avaliar e compilar informações de editais para garantir que a Cogmo possa submeter propostas de forma eficaz."
    ),
    llm=azure_llm,
    temperature=0.0,
    verbose=True,
    allow_delegation=True,
)

# Define the tasks
analise_de_edital = Task(
    description=(
        "Analisar o edital fornecido para identificar, categorizar e extrair as sessões mais relevantes, sob o ponto de vista de uma startup de IA, que deseja submeter uma proposta."
    ),
    expected_output=(
        """
        Uma lista de dicionários, cada um contendo uma categoria e o trecho correspondente dos documentos de licitação, exatamente como consta dos originais.
        Os trechos devem ser categorizados em somente uma das categorias a seguir: prazos, financeiro, documentacao, solucao_proposta, critérios_avaliacao, condicoes_participacao, outros
        Exemplo: [
            {'categoria': 'prazos', 'trecho': 'Avaliação das propostas: 30 dias após o encerramento do prazo de submissão.'},
            {'categoria': 'financeiro', 'trecho': 'O valor total disponível para subvenção é de R$ 1.000.000,00.'},
            {'categoria': 'documentacao', 'trecho': 'Os documentos necessários para participação são: ...'}
        ]
        """
    ),
    agent=analista_de_edital
)

analise_de_requisitos = Task(
    description=(
        "Analisar cada trecho do edital levantado pelo agente Analista de Edital e identificar se algum requisito de participação ou submissão de proposta foi mencionado."
    ),
    expected_output="""
        Uma lista de dicionários, cada um contendo uma categoria, a transcrição do trecho do edital e uma lista dos requisitos, se houver.
        
        Exemplo: [
            {'categoria': 'prazo', 'trecho': 'Avaliação das propostas: 30 dias após o encerramento do prazo de submissão.', 'requisitos': []},
            {'categoria': 'financeiro', 'trecho': 'O valor total disponível para subvenção é de R$ 1.000.000,00.', 'requisitos': []},
            {'categoria': 'documentacao', 'trecho': 'Os documentos necessários para participação são certidão negativa de débitos, contrato social e proposta, de acordo com o modelo fornecido', 'requisitos': ['apresentar certidão negativa de débitos', 'apresentar contrato social', 'apresentar proposta no modelo fornecido']}
        ]
    """,
    agent=analista_de_requisitos
)

compilacao_de_resumo = Task(
    description="""
        Verificar se cada um dos requisitos levantados realmente está de acordo com os trechos extraídos dos documentos originais
        e compilar um resumo abrangente dos documentos de licitação, incluindo um resumo geral e uma lista de verificação dos requisitos para submissão de proposta pela Cogmo.
        Sempre que encontrar um requisito que não esteja de acordo com o trecho original, o agente deve solicitar a revisão daquele item ao Analista de Requisitos".
        """,
    expected_output="""
        Um arquivo em formato markdown, contendo um resumo dos trechos mais relevantes, organizados por tópico, e uma lista de verificação de todos os requisitos para submissão de uma proposta pela Cogmo, a startup de IA para qual este trabalho está sendo realizado.
        Exemplo:
        ```markdown
        # Resumo do Edital
                       
        ## Prazos
        - Data limite para submissão das propostas: DD/MM/AAAA
        - Avaliação das propostas: 30 dias após o encerramento do prazo de submissão.
        ...
                       
        ## Financeiro
        - O valor total disponível para subvenção é de R$ X.000.000,00.
        - As startups participantes devem dar uma contrapartida de 0,0Y do valor total do projeto.
        ...
                       
        # Checklist
        - [ ] Apresentar certidão negativa de débitos
        - [ ] Apresentar contrato social
        - [ ] Apresentar proposta no modelo fornecido
        ...
            
        ...            
        ```
        """,
    agent=supervisor,
    output_file="summary.md"
)

# Assemble the crew
crew = Crew(
    agents=[analista_de_edital, analista_de_requisitos, supervisor],
    tasks=[analise_de_edital, analise_de_requisitos, compilacao_de_resumo],
    verbose=2,
    memory=True
)

# Read multiple Markdown documents
with open("/Users/morossini/Projects/Prototypes/Cogmo/LicitaBot/tender_summary_crew/docs/edital.md", "r") as file:
    edital = file.read()
documents = {"edital": edital}

result = crew.kickoff(inputs=documents)

summary_path = "/Users/morossini/Projects/Prototypes/Cogmo/LicitaBot/tender_summary_crew/summary.md"

# Check if the file exists, if not, create it
if not os.path.exists(summary_path):
    with open(summary_path, "w") as f:
        pass

# Save the final output
with open(summary_path, "w") as f:
    f.write(result)

# Print the result
print(f"\n\nComplete results: \n{str(result)}\n\n")


# if __name__ == "__main__":
#     print(documents)