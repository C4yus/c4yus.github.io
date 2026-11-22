# Skills: pesquisa e instalação (21 nov 2026)

Pesquisa feita por 5 agentes, uma categoria cada. Só entraram skills grátis, sem API paga.
As 8 escolhidas foram lidas antes de entrar aqui (scripts, ligações à rede, caracteres escondidos, instruções suspeitas).

## Regra (João, 22 nov 2026)
Nenhuma skill pode enviar dados para fora. Se for boa mas enviar, escreve-se uma versão nossa, só local. Na dúvida, escreve-se sempre a nossa. Detalhes na skill `regras-skills-cayus`.

## Instaladas em `.claude/skills/` (12)

### As nossas (escritas de raiz, só locais)
| Skill | Para quê | Baseada em | Porque não ficou a original |
|---|---|---|---|
| regras-skills-cayus | a regra acima e como verificar uma skill | — | — |
| design-cayus | desenhar, criticar e polir o site | Impeccable (pbakaus, Apache-2.0) | telemetria, catálogo online em impeccable.style, descarrega um programa |
| qualidade-web-local | velocidade, CWV, imagens, SEO técnico; script `medir_pagina.py` (Playwright local) | web-quality-skills (addyosmani, MIT) | recomenda CrUX/PageSpeed (envia o endereço à Google) |
| youtube-cayus | títulos, descrições, tags, miniaturas, Shorts, estatísticas | claude-youtube (AgriciDaniel, MIT) | API do YouTube, yt-dlp, DataForSEO e NanoBanana (pagos/externos) |
| prompts-redes-cayus | prompts para colar no Gemini à mão: miniaturas, carrosséis, posts | social-media-skills (charlie947, MIT) | instruções para ligar serviços; uma parte usa Apify e API do Gemini |
| kdp-montar-livro | limpar páginas, PDF do interior e capa KDP (3 scripts, testados) | kdp-coloring-book (CarlosCaPe, MIT) + kindle-cover (nikmcfly, MIT) | a primeira gera imagens por API |

### De terceiros, mantidas como estão (só texto e scripts locais, lidas linha a linha)
| Skill | Origem (commit) |
|---|---|
| verification-before-completion, systematic-debugging, brainstorming, writing-plans, executing-plans | github.com/obra/superpowers (22f0b46), MIT. O brainstorming tem um servidor só em 127.0.0.1. |
| webapp-testing | github.com/anthropics/skills (e4bb5d9), Apache-2.0. Playwright em localhost. |

Para atualizar uma skill de terceiros: descarregar, ler o que mudou, aplicar a regra e só depois substituir.

## Lista completa (11 por categoria)

### Design de sites
1. Impeccable — github.com/pbakaus/impeccable ➜ substituída por design-cayus (envia dados)
2. web-quality-skills — github.com/addyosmani/web-quality-skills ➜ substituída por qualidade-web-local
3. web-design-guidelines — github.com/vercel-labs/agent-skills (skills/web-design-guidelines)
4. Taste Skill — github.com/Leonxlnx/taste-skill
5. UI UX Pro Max — github.com/nextlevelbuilder/ui-ux-pro-max-skill
6. Marketing Skills — github.com/coreyhaines31/marketingskills
7. Chrome DevTools MCP — github.com/ChromeDevTools/chrome-devtools-mcp
8. make-interfaces-feel-better — github.com/jakubkrehel/make-interfaces-feel-better
9. Modern Web Guidance — github.com/GoogleChrome/modern-web-guidance
10. Claude SEO — github.com/AgriciDaniel/claude-seo
11. webapp-testing — github.com/anthropics/skills (skills/webapp-testing) ✅ instalada

### Imagens
1. social-media-skills — github.com/charlie947/social-media-skills ➜ substituída por prompts-redes-cayus
2. nano-banana-prompt-generator — github.com/maciejdzierzek/nano-banana-prompt-generator
3. design-assets / image-processing — github.com/jezweb/claude-skills (plugins/design-assets)
4. web-asset-generator — github.com/alonw0/web-asset-generator
5. instagram-carousel — github.com/marcolang/marketing-skills
6. design-assets / color-palette — github.com/jezweb/claude-skills
7. logo-designer-skill — github.com/neonwatty/logo-designer-skill
8. image-prompt (gist) — gist.github.com/kousen/f7c66a70cefe90b12c8b5285688a0016
9. processing-images — github.com/oaustegard/claude-skills (processing-images)
10. ColoringBookAISkill — github.com/johnnybpena1989/ColoringBookAISkill (nova, sem uso provado)
11. image-optimization — github.com/secondsky/claude-skills

### YouTube
1. claude-youtube — github.com/AgriciDaniel/claude-youtube ➜ substituída por youtube-cayus
2. ffmpeg-skill — github.com/kajisho5/ffmpeg-skill
3. youtube-skills — github.com/sergebulaev/youtube-skills
4. Remotion Skills — github.com/remotion-dev/skills
5. youtube-uploader — github.com/aviz85/claude-skills-library (skills/youtube-uploader)
6. YouTube plugin — github.com/JCodesMore/youtube-for-ai-agents
7. youtube-full — github.com/alirezarezvani/claude-skills (marketing-skill/skills/youtube-full)
8. claude-video — github.com/AgriciDaniel/claude-video
9. youtube-transcript — github.com/michalparkola/tapestry-skills-for-claude-code
10. claude-code-video-toolkit — github.com/digitalsamba/claude-code-video-toolkit (partes pagas)
11. faster-whisper — github.com/theplasmak/faster-whisper
- NÃO usar: TubeAlfred (só 50 créditos grátis por 14 dias, depois pago).

### Livros de colorir / KDP
1. kdp-coloring-book — github.com/CarlosCaPe/octorato ➜ substituída por kdp-montar-livro
2. kdp-cover-checker — github.com/hoanghd218/aws-kdp (.claude/skills/kdp-cover-checker), sem licença
3. kindle-cover — github.com/nikmcfly/kindle-cover-skill ➜ juntada em kdp-montar-livro
4. kdp-book-builder + kdp-image-reviewer — github.com/hoanghd218/aws-kdp, sem licença
5. Image Production — github.com/danielrosehill/Claude-Image-Production-Plugin
6. Ask KDP Kings — github.com/cdeistopened/kdp-kings-wiki, sem licença
7. kdp-keyword-optimizer — github.com/cdeistopened/skill-stack
8. amazon-category-research — github.com/cdeistopened/skill-stack
9. kdp-aplus-content — github.com/rawveg/skillsforge-marketplace
10. pinterest-posts — github.com/kostja94/marketing-skills
11. Amazon-Skills — github.com/nexscope-ai/Amazon-Skills

### Código
1. Superpowers — github.com/obra/superpowers ✅ instalada (5 skills)
2. webapp-testing — github.com/anthropics/skills ✅ instalada
3. playwright-cli — github.com/microsoft/playwright-cli
4. web-quality-skills — github.com/addyosmani/web-quality-skills ➜ substituída por qualidade-web-local
5. hookify — github.com/anthropics/claude-plugins-official (plugins/hookify)
6. agent-skills — github.com/addyosmani/agent-skills
7. Chrome DevTools MCP — github.com/ChromeDevTools/chrome-devtools-mcp
8. web-design-guidelines — github.com/vercel-labs/agent-skills
9. pr-review-toolkit — github.com/anthropics/claude-plugins-official (plugins/pr-review-toolkit)
10. mattpocock-skills — github.com/mattpocock/skills
11. security-guidance — github.com/anthropics/claude-plugins-official (plugins/security-guidance), gasta limite do plano

## Cuidados
- Há sobreposições (Superpowers / agent-skills / mattpocock; várias de browser). Não instalar tudo.
- Ler sempre o SKILL.md e os scripts antes de instalar uma skill de terceiros.
- A skill própria `prova-antes-de-entregar` e a `verification-before-completion` fazem o mesmo: usar uma de cada vez.
