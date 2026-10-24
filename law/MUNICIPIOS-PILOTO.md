# MUNICÍPIOS — piloto (FILL-PLAN B2c)

Gerado por tools/pilot_municipios.py (ccp-pilot-municipios-0.1) a partir de law/municipios/piloto.json e do store; não editar à mão.

Método (2026-10-24). Para cada município procurámos três registos do seu direito próprio que entram num veredicto de contratação: (1) a norma de controlo interno (NCI); (2) a delegação de competências da câmara no presidente, ou o despacho de delegação/subdelegação em vereadores e dirigentes, que fixa quem autoriza despesa; (3) um regulamento municipal de compras ou de contratação. Onde: pesquisa web restrita ao domínio do município e a diariodarepublica.pt (2.ª série), com o nome do município e do registo; um resultado só conta quando o documento capturado nomeia o município. Cada documento encontrado foi lido por um único GET (3 s entre leituras, nada enviado) e guardado em law/ com sha256. 'Com texto' mede a camada de texto do PDF (>= 500 caracteres por página) ou o texto da página HTML; um PDF digitalizado conta como capturado sem texto.

## Cobertura por município

| município | registos encontrados | capturados | com texto | onde |
|---|---|---|---|---|
| Lisboa | 2 | 2 | 1 | site do município, site do município (Boletim Municipal) |
| Porto | 1 | 1 | 1 | site do município |
| Vila Nova de Gaia | 1 | 1 | 0 | site do município |
| Braga | 0 | 0 | 0 | — |
| Coimbra | 2 | 2 | 2 | site do município (editais) |
| Sintra | 1 | 1 | 0 | DR 2.ª série |
| Loures | 1 | 0 | 0 | site do município |
| Cascais | 2 | 2 | 1 | DR 2.ª série, site do município |
| Funchal | 2 | 2 | 2 | DR 2.ª série, site do município |
| Ponta Delgada | 0 | 0 | 0 | — |

Totais: 12 encontrados, 11 capturados, 7 com texto, em 10 municípios.

## Estimativa para os 308 municípios

- registos por município no piloto: 1.2 encontrados, 1.1 capturados, 0.7 com texto
- estimativa linear para 308: ~370 registos encontrados, ~339 capturáveis, ~216 com texto utilizável sem OCR
- leituras passivas no piloto: 12 (1.2 por município); para 308: ~370 leituras, a 3 s entre páginas, ~1.5 h de captura (15 s por leitura com renderização)

- o que não cobre: a estimativa é linear sobre 10 municípios grandes; municípios pequenos publicam menos no próprio site e mais em editais afixados, pelo que a taxa de 'encontrado' tende a descer
- o tempo conta só as leituras (15 s por leitura, a média das capturas renderizadas desta fase); não conta a pesquisa, que no piloto foi o maior custo: duas a três pesquisas por município, e mesmo assim 3 dos 10 sem registo encontrado
- os PDF da 2.ª série do DR vêm cifrados (/Encrypt): capturados com sha256, mas a camada de texto só se verifica com uma biblioteca PDF, fora do gate (D17)
- o texto de uma delegação raramente está no DR: a 2.ª série publica avisos que a citam; o texto vive no site do município (editais, Boletim Municipal) ou em atas
- nenhum município do piloto publica a NCI na 2.ª série do DR; onde existe é um PDF no site, sem endereço estável
- para usar estes registos num veredicto falta estruturá-los (delegação -> quem autoriza despesa até que valor): fica para a fase 3, com uma fila em DECISIONS antes de qualquer campo de município em norma

## Detalhe por município

### Lisboa
- nci: Deliberação n.º 187/CM/2011 (NCI), 2.º Suplemento ao Boletim Municipal n.º 894, 2011-04-07 — site do município (Boletim Municipal) — https://www.lisboa.pt/fileadmin/transparencia/prevencao_corrupcao/2.__SUP_894__JORGE_.pdf — PDF 80 p., 14572 car. de texto — raw raw:municipio:nci:lisboa-nci-2011
- regulamento: Regulamento do Orçamento do Município de Lisboa (2025) — site do município — https://recrutamento.cm-lisboa.pt/cmlisboa-wirerecruit/uploads/writer_file/document/807/regulamento_do_orcamento_do_municipio_de_lisboa.pdf — PDF 12 p., 97743 car. de texto — raw raw:municipio:regulamento:lisboa-regulamento-orcamento-2025
- delegacao: delegação da câmara no presidente, mandato 2025-2029 (Proposta n.º 593/2025, citada por um documento partidário) — — — não encontrado — não capturado — não encontrada publicada pelo município
- procurado: lisboa.pt / cm-lisboa.pt e diariodarepublica.pt: «norma de controlo interno», «delegação de competências» 2025; o regulamento do orçamento de 2025 diz que a NCI em vigor é a Deliberação n.º 187/CM/2011 (2.º Suplemento ao Boletim Municipal n.º 894)

### Porto
- nci: Norma de Controlo Interno, dezembro de 2024 — site do município — https://www.cm-porto.pt/files/uploads/cms/1%20(1).%20Norma%20de%20Controlo%20Interno — PDF 93 p., 245817 car. de texto — raw raw:municipio:nci:porto-nci-2024
- delegacao: delegação da câmara no presidente, mandato 2025-2029 — — — não encontrado — não capturado — não encontrada
- procurado: cm-porto.pt e diariodarepublica.pt: «norma de controlo interno», «delegação de competências» 2025; os regulamentos de 2025 citam a Ordem de Serviço NUD/232865/2022/CMP como base da delegação

### Vila Nova de Gaia
- nci: Norma de Controlo Interno, revisão 02, 2024-02-05 — site do município — https://www.cm-gaia.pt/fotos/editor2/pcnta/7_nci_2024.pdf — PDF 76 p., 200 car. de texto — raw raw:municipio:nci:gaia-nci-2024
- delegacao: delegação da câmara no presidente, mandato 2025-2029 — — — não encontrado — não capturado — não encontrada
- procurado: cm-gaia.pt / gaia.pt e diariodarepublica.pt: «norma de controlo interno», «delegação de competências» 2025

### Braga
- nci: Norma de Controlo Interno — — — não encontrado — não capturado — não encontrada
- delegacao: delegação da câmara no presidente, mandato 2025-2029 — — — não encontrado — não capturado — não encontrada
- procurado: cm-braga.pt e diariodarepublica.pt: «norma de controlo interno», «delegação de competências» outubro-novembro 2025; os editais de 2025 encontrados com «Braga» eram de outros municípios ou de outro assunto

### Coimbra
- nci: Norma de Controlo Interno (reformulada em 2022, segundo notícia do município) — — — não encontrado — não capturado — documento não encontrado; só a notícia https://www.coimbra.pt/2022/12/cm-coimbra-intensifica-controlo-interno-e-cumprimento-das-disposicoes-legais-aplicaveis-a-autarquia/
- delegacao: Edital n.º 414/2025 (Despacho n.º 27/PR/2025, de 4 de dezembro: delegação no chefe do gabinete de apoio à presidência) — site do município (editais) — https://www.cm-coimbra.pt/wp-content/uploads/2025/12/Edital-N.o-414_2025.pdf — PDF 3 p., 10563 car. de texto — raw raw:municipio:delegacao:coimbra-edital-414-2025
- delegacao: Edital n.º 406/2025 (subdelegação em dirigentes; cita o Despacho n.º 13/PR/2025, de 17 de novembro) — site do município (editais) — https://www.cm-coimbra.pt/wp-content/uploads/2025/12/Edital-N.o-406_2025.pdf — PDF 8 p., 15152 car. de texto — raw raw:municipio:delegacao:coimbra-edital-406-2025
- procurado: cm-coimbra.pt e diariodarepublica.pt: «norma de controlo interno» (só uma notícia de 2022 sobre a reformulação), «delegação de competências» novembro-dezembro 2025

### Sintra
- nci: Norma de Controlo Interno — — — não encontrado — não capturado — não encontrada
- delegacao: Aviso n.º 2033/2026/2 (remete para a delegação e subdelegação de 2025: Despacho n.º 47-P/2025, retificado pelo 53-P/2025) — DR 2.ª série — https://files.diariodarepublica.pt/2s/2026/02/022000000/0066100661.pdf — PDF cifrado (/Encrypt): camada de texto não verificável aqui — raw raw:municipio:delegacao:sintra-aviso-2033-2026 — o conteúdo descrito vem do resumo da pesquisa; o PDF capturado é cifrado e não foi lido aqui
- procurado: cm-sintra.pt e diariodarepublica.pt: «norma de controlo interno», «delegação de competências» novembro 2025; o Aviso n.º 2033/2026/2 remete para o Edital n.º 888/2025 e para os Despachos n.º 47-P/2025 e 53-P/2025

### Loures
- nci: Norma de Controlo Interno — — — não encontrado — não capturado — não encontrada
- delegacao: documento de dezembro de 2025 no site do município (candidato) — site do município — https://www.cm-loures.pt/media/pdf/PDF20251218091537604.pdf — não capturado — não lido: o certificado TLS do site não se verifica a partir daqui; não foi contornado
- procurado: cm-loures.pt e diariodarepublica.pt: «norma de controlo interno», «delegação de competências» 2025

### Cascais
- nci: NCI — Norma de Controlo Interno, versão 3.2 (2022) — site do município — https://www.cascais.pt/sites/default/files/anexos/gerais/new/nci_-_norma_de_controlo_interno_2022_0.pdf — PDF 37 p., 95144 car. de texto — raw raw:municipio:nci:cascais-nci-2022
- delegacao: Aviso n.º 22089/2025/2 (cita a subdelegação do Despacho n.º 7/2025, de 3 de fevereiro) — DR 2.ª série — https://files.diariodarepublica.pt/2s/2025/09/171000000/0023600236.pdf — PDF cifrado (/Encrypt): camada de texto não verificável aqui — raw raw:municipio:delegacao:cascais-aviso-22089-2025 — o conteúdo descrito vem do resumo da pesquisa; o PDF capturado é cifrado e não foi lido aqui
- procurado: cascais.pt e diariodarepublica.pt: «norma de controlo interno», «delegação de competências» 2025

### Funchal
- nci: Norma de Controlo Interno, janeiro de 2025 (regulamentos: 19-12-2024) — site do município — https://cmfdoc.funchal.pt/media/k2/attachments/Norma_De_Controlo_Interno_2025.pdf — PDF 62 p., 174271 car. de texto — raw raw:municipio:nci:funchal-nci-2025
- delegacao: Aviso n.º 6712/2026/2 (consulta pública de um regulamento; cita o Despacho de Delegação e Subdelegação de Competências de 8 de janeiro de 2026, publicitado pelo Edital n.º 19/2026) — DR 2.ª série — https://diariodarepublica.pt/dr/detalhe/aviso/6712-2026-1076923256 — HTML, 34813 car. de texto — raw raw:municipio:delegacao:funchal-aviso-6712-2026 — o despacho e o Edital n.º 19/2026 não foram encontrados; este aviso só os cita
- procurado: cmfdoc.funchal.pt e diariodarepublica.pt: «norma de controlo interno», «delegação e subdelegação de competências» 2026

### Ponta Delgada
- nci: Norma de Controlo Interno — — — não encontrado — não capturado — não encontrada
- delegacao: delegação da câmara no presidente, mandato 2025-2029 — — — não encontrado — não capturado — não encontrada
- procurado: cm-pontadelgada.pt e diariodarepublica.pt: «norma de controlo interno», «delegação de competências» 2025

