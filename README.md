# Otimização de Rotas de Resposta a Riscos Agroclimáticos via Dados Orbitais
**Global Solution 2026**
**Disciplina:** Dynamic Programming
---

## 👥 Integrantes do Grupo
* **Caio Costa Beraldo** - RM560775
* **Icaro Henrique De Souza Calixto** - RM560278
* **Pietro Brandalise De Andrade** - RM560142
* **Victor Kenzo Mikado** - RM560057

---

## 📝 Descrição do Projeto
Este projeto apresenta uma plataforma de software inteligente focada na Região Norte do Brasil (Estado do Amazonas) para otimizar rotas de resposta logística e ajuda humanitária frente a desastres agroclimáticos (cheias e vazantes históricas). 

A aplicação conecta a Economia Espacial a desafios terrestres críticos, utilizando dados de sensoriamento remoto de agências como NASA, ESA e INPE, cruzados com alertas meteorológicos reais do INMET e de Plataformas de Coleta de Dados (PCDs) do CEMADEN. O sistema calcula caminhos de custo mínimo ponderados por risco entre os 44 municípios da base real do Amazonas, contornando os vazios de conectividade móvel mapeados na infraestrutura de telecomunicações tradicional.

### 🌐 Alinhamento com as ODS da ONU
* **ODS 2 (Fome Zero e Agricultura Sustentável):** Proteção do escoamento agrícola de pequenas cooperativas ribeirinhas contra inundações repentinas.
* **ODS 9 (Indústria, Inovação e Infraestrutura):** Modelagem matemática para mitigar falhas físicas de logística e comunicação na Amazônia.
* **ODS 11 (Cidades e Comunidades Sustentáveis):** Resiliência para assentamentos humanos vulneráveis e isolados.
* **ODS 13 (Ação Contra a Mudança Global do Clima):** Mecanismos de adaptação a eventos climáticos severos intensificados pelo aquecimento global.

---

## 🛠️ Abordagens Algorítmicas Implementadas

### 1. Força Bruta Exaustiva (brute_force.py)
Utiliza Busca em Profundidade (DFS) para varrer exaustivamente todas as combinações de trajetórias viáveis da origem até o destino geográfico real.
* **Complexidade Temporal:** O(2^(N+M)) (Crescimento Exponencial).
* **Otimização:** Inclusão de poda algorítmica (pruning) baseada no melhor custo global para interromper ramificações ineficientes.

### 2. Programação Dinâmica (dynamic_programming.py)
Garante a resolução do problema reutilizando subproblemas idênticos sobrepostos e mantendo a estabilidade assintótica. Implementa:
* **Bottom-Up (Tabulação):** Preenchimento iterativo da tabela de decisões a partir do caso base. Complexidade de O(N x M) em tempo e espaço.
* **Top-Down (Memoização):** Abordagem recursiva com estrutura de cache para impedir recomputações desnecessárias.
* **Inovação Aplicada:** Suporte a grades geoespaciais reais truncadas (matriz 7x7 para os 44 municípios reais do Amazonas), forçando a parada na coordenada exata do destino final (6, 1) e isolando células excedentes como obstáculos (infinito).

### 3. Simulação Estocástica de Monte Carlo (monte_carlo.py)
Modela a volatilidade meteorológica executando 1000 iterações da Programação Dinâmica. O risco de cada município é perturbado dinamicamente utilizando amostragem estatística baseada na Distribuição Beta (parâmetros alpha e beta), utilizando a probabilidade histórica do cenário, gerando intervalos de confiança científicos para prever cenários de pior e melhor caso.

---

##  Estrutura do Repositório

├── data/
│   └── raw/
│       ├── data_loader.py          # Script de carregamento de dados geográficos
│       ├── municipios_dados.csv    # Dados reais dos 44 municípios do Amazonas
│       └── coordenadas.csv         # Coordenadas e custos de infraestrutura
├── outputs/                         # Gráficos e relatórios visuais salvos em alta definição
├── brute_force.py                  # Algoritmo de Busca Exaustiva com DFS
├── dynamic_programming.py          # Estruturas Top-Down e Bottom-Up (DP)
├── monte_carlo.py                  # Simulação Estocástica de Riscos
├── scenarios.py                    # Gerador de matrizes sintéticas para estresse
├── visualizations.py               # Renderização de gráficos usando Matplotlib/Numpy
├── performance_monitor.py          # Benchmark de tempo e monitor de RAM (tracemalloc)
└── generate_reports.py             # Script unificado de execução da pipeline

Como Executar a Solução
1. Pré-requisitos
Certifique-se de possuir o Python 3.10 ou superior instalado na máquina, juntamente com as seguintes bibliotecas:
pip install numpy matplotlib
2. Gerar Todos os Relatórios e Artefatos Visuais
Para rodar a pipeline de testes, validar os dados reais do Amazonas, computar o custo ótimo (125.85), rodar a simulação de Monte Carlo e exportar as curvas de desempenho, execute no terminal:
python generate_reports.py
Após o término da execução, os seguintes gráficos serão salvos automaticamente na pasta outputs/:

dp_heatmap.png: Mapa de calor com os custos acumulados da Programação Dinâmica.

histogram.png e boxplot.png: Distribuição de dispersão estatística de Monte Carlo.

scalability.png: Curva assintótica de tempo de execução (em milissegundos) para comprovar a eficiência da DP.

memory_usage.png: Perfil de consumo de memória RAM coletado via tracemalloc.

Decisões de Projeto e Resultados
Tratamento de Dados Incompletos: Implementação de máscaras bidimensionais (utilizando numpy) no script de visualização, garantindo que as áreas sem municípios mapeados na matriz estrutural do Amazonas sejam plotadas como áreas bloqueadas (exibindo "inf" em vermelho no gráfico) sem distorcer as escalas cromáticas de cor.

Eficiência Comprovada: O monitoramento de desempenho empírico validou que a Programação Dinâmica Bottom-Up mantém a execução na casa dos milissegundos mesmo para grades densas (como matrizes 50x50), provando sua prontidão para operação em servidores de resposta ágil da Defesa Civil.
