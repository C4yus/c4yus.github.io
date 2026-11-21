# Skills: pesquisa e instalação (21 nov 2026)

Pesquisa feita por 5 agentes, uma categoria cada. Só entraram skills grátis, sem API paga.
As 8 escolhidas foram lidas antes de entrar aqui (scripts, ligações à rede, caracteres escondidos, instruções suspeitas).

## Instaladas em `.claude/skills/` (versão fixa, revista)

| Pacote | Skills | Origem (commit) | Notas da revisão |
|---|---|---|---|
| Superpowers | verification-before-completion, systematic-debugging, brainstorming, writing-plans, executing-plans | github.com/obra/superpowers (22f0b46), MIT | Só texto e scripts locais. Ficaram de fora as que mexem em worktrees/ramos e a using-superpowers (obriga a ver skills em todas as mensagens). |
| webapp-testing | webapp-testing | github.com/anthropics/skills (e4bb5d9), Apache-2.0 | Oficial da Anthropic. Playwright local. |
| Impeccable | impeccable | github.com/pbakaus/impeccable (b49177d), Apache-2.0 | Descarrega um programa das releases do GitHub do autor na 1.ª utilização. Telemetria anónima DESLIGADA em `.impeccable/config.json`. Pede direções visuais a impeccable.style (pode falhar na nuvem, não faz mal). |
| web-quality-skills | accessibility, web-quality-audit, core-web-vitals, performance, best-practices, seo | github.com/addyosmani/web-quality-skills (afa8da9), MIT | Só texto e um script local de análise. |
| kdp-coloring-book | kdp-coloring-book | github.com/CarlosCaPe/octorato (0a28f79), MIT | O passo da arte chama uma ferramenta "imagegen": em vez disso usamos as imagens que o João faz no Gemini. Predefinição de tamanho é 8,5x8,5: os nossos livros são 8,5x11. |
| kindle-cover | kindle-cover | github.com/nikmcfly/kindle-cover-skill (954eb8e), MIT (no README) | Script local (reportlab + Pillow). |
| claude-youtube | claude-youtube | github.com/AgriciDaniel/claude-youtube (84c3fa6), MIT | Funciona sem chaves (dados colados ou capturas do Studio). Ignorar DataForSEO (pago). Não trata "made for kids": isso fica na skill kids-shorts-channel. |
| social-media-skills | youtube-thumbnail, gemini-carousel, quote-post, graphic-designer | github.com/charlie947/social-media-skills (10ca79c), MIT | Só escrevem pedidos para colar no Gemini à mão. Ficou de fora reels-scripting (usa Apify e API do Gemini). |

Para atualizar uma skill: voltar a descarregar, ler o que mudou, e só depois substituir a pasta.

## Lista completa (11 por categoria)

### Design de sites
1. Impeccable — github.com/pbakaus/impeccable ✅ instalada
2. web-quality-skills — github.com/addyosmani/web-quality-skills ✅ instalada
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
1. social-media-skills — github.com/charlie947/social-media-skills ✅ instalada (4 skills)
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
1. claude-youtube — github.com/AgriciDaniel/claude-youtube ✅ instalada
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
1. kdp-coloring-book — github.com/CarlosCaPe/octorato (skills/kdp-coloring-book) ✅ instalada
2. kdp-cover-checker — github.com/hoanghd218/aws-kdp (.claude/skills/kdp-cover-checker), sem licença
3. kindle-cover — github.com/nikmcfly/kindle-cover-skill ✅ instalada
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
4. web-quality-skills — github.com/addyosmani/web-quality-skills ✅ instalada
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
