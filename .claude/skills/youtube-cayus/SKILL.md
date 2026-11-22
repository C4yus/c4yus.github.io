---
name: youtube-cayus
description: "Kit de YouTube para os canais do João (Relaxing with Cayus e Waddle Hop Pals): títulos, descrições, tags, capítulos, miniaturas, Shorts, ideias, calendário, leitura de estatísticas e análise de concorrentes, a partir de dados que o João cola ou de capturas do YouTube Studio, sem APIs. Usar para 'título para o vídeo', 'descrição', 'tags', 'SEO do YouTube', 'ideias de vídeos', 'porque é que este vídeo não teve vistas', 'Shorts', 'miniatura'."
---

# YouTube Cayus

Responder ao João em PT-PT, curto; títulos, descrições e tags em inglês.
Sem APIs, sem chaves, sem yt-dlp, sem serviços pagos: trabalha com o que o João cola (texto, números, capturas do YouTube Studio) e com o conhecimento abaixo. A produção e o agendamento estão nas skills `relaxing-with-cayus` e `kids-shorts-channel`: ler a do canal antes de escrever.

## Canais
| Canal | Formato | Público | Cuidado principal |
|---|---|---|---|
| Relaxing with Cayus | 1 hora de natureza/fogueira + Short | adultos: dormir, estudar, relaxar | promessa honesta (sem "cura a insónia") |
| Waddle Hop Pals | Shorts de canções e danças | crianças | "Made for kids" SEMPRE ligado |

**Made for kids (Waddle Hop Pals):** com esta marca o YouTube desliga comentários, sino de notificações, cartões e ecrãs finais, mini-player e anúncios personalizados. Não prometer nada disso nos textos. Nada de pedir dados às crianças, nada de "comenta em baixo". Confirmar regras na Ajuda do YouTube quando houver dúvida.

## 1. Pacote de publicação (o pedido mais comum)
Pedir/usar: assunto do vídeo, duração, palavra-chave principal, o que se ouve/vê. Entregar pronto a colar:

**TÍTULOS (3):** pesquisa (palavra-chave à frente) · descoberta (emoção/curiosidade) · híbrido (recomendado). Contar caracteres; o gancho nos primeiros 40–45 (corte no telemóvel). Shorts: 4–6 palavras, 20–40 caracteres.
**DESCRIÇÃO:** palavra-chave nas primeiras 25 palavras; as primeiras 2 linhas (≈125 caracteres) vendem; para o canal de relaxamento: para que serve (dormir, estudar, meditar), o que se ouve, duração; capítulos se fizer sentido (começam em 0:00, mínimo 3); link para o outro vídeo/playlist; 3–5 hashtags no fim (não no título).
**TAGS:** 10–15, separadas por vírgulas, total < 500 caracteres; da mais específica à mais larga.
**MINIATURA:** brief (ver 2). Texto da miniatura nunca repete o título.
**DEFINIÇÕES:** público (made for kids ou não), categoria, idioma, dia/hora sugeridos com porquê.
**CHECKLIST:** palavra-chave no título (40 primeiros caracteres) e na descrição (25 primeiras palavras) · miniatura própria · hashtags no corpo · sem promessas médicas · made for kids certo.

## 2. Miniaturas
- Pensar no telemóvel: 70%+ das vistas; ver a miniatura a ~320px de largura antes de aprovar. Ficheiro 1280x720 (16:9), < 2 MB.
- **Relaxing with Cayus:** a paisagem/fogo é a estrela; luz quente, uma só cena, contraste alto; texto curto ou nenhum (ex.: "1 HOUR", "RAIN"); coerência entre vídeos (mesma posição de texto, mesma família de cores).
- **Waddle Hop Pals:** personagens grandes e expressivos, cores vivas, 1–3 palavras no máximo, nada assustador.
- Regras gerais: um foco claro, duas cores dominantes, nada importante no canto inferior direito (lá fica a duração), sem iscos enganosos.
- Para gerar a imagem no Gemini à mão: skill `prompts-redes-cayus` (miniatura) e `gemini-pedidos-precisos`.

## 3. Shorts
- O algoritmo testa num grupo pequeno e alarga se as pessoas não deslizarem nos primeiros segundos: o 1.º segundo tem de prender (movimento, som, personagem). A taxa de "deslizar" pesa mais do que o clique.
- Um Short pode arrancar até ao 4.º dia: não apagar cedo.
- 3–5 hashtags; os primeiros 125 caracteres da descrição aparecem nas pré-visualizações.
- Do vídeo longo para Short: o momento mais bonito/calmo em 9:16, com texto mínimo e link (ou "vídeo relacionado") para a versão de 1 hora.
- Música com Content ID pode bloquear Shorts de 1–3 min: usar só som próprio ou com licença.

## 4. Ler estatísticas (do Studio, coladas pelo João)
| Sinal | Saudável | Se estiver mal |
|---|---|---|
| CTR das impressões | 4–8% e estável | miniatura/título: testar outra miniatura (Studio tem teste A/B de miniaturas e títulos) |
| Retenção média (vídeo de 1 h) | o que importa é o tempo absoluto e quem volta | abertura mais bonita nos 30 s iniciais; capítulos |
| Vistas do Short / "visto vs. deslizado" | > 70% a ver | primeiro segundo mais forte |
| Origem do tráfego | pesquisa + navegação a subir | títulos de pesquisa vs. de descoberta |
É normal o CTR descer à medida que o vídeo chega a público mais frio. Comparar sempre com a média do próprio canal, não com números de blogs. Dizer o que é observado (números do João), o que é calculado e o que é palpite.

## 5. Ideias e calendário
- Ideias a partir do que já funciona no canal (os 3 vídeos com mais vistas/retenção) e de pesquisas que o João vê no YouTube (sugestões da barra de pesquisa, vídeos de concorrentes que ele cola).
- Para cada ideia: título de trabalho, palavra-chave, porque deve resultar, esforço (gravação existente ou nova).
- Calendário: ritmo que o João aguenta (ex.: 1 vídeo longo + 3 Shorts por semana), a mesma hora, séries com nome.

## 6. Concorrentes
O João cola títulos, vistas e datas (ou capturas). Tirar padrões: duração, palavras nos títulos, estilo de miniatura, frequência. Nunca copiar miniaturas, músicas ou gravações de outros.

Baseada nos guias da skill claude-youtube de AgriciDaniel (MIT), reescrita sem scripts, sem a API do YouTube e sem DataForSEO/NanoBanana (serviços externos e pagos).
