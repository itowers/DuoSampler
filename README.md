# DuoSampler

Sampler e beat maker para o iPhone Duo (PWA, Web Audio, um único `index.html`). Protótipo.

## Recursos
- Pads 4×4 em quatro modos: DRUM, KEYS, CHORD e FX (15 efeitos de performance, segurando o pad).
- Looper de 4 faixas de notas: contagem de 1 compasso no REC, overdub em camadas com feedback, UNDO/REDO, ×2, mute no compasso e BPM LOOP (o primeiro loop define o BPM).
- Efeitos por loop, todos ao mesmo tempo: drive, crush, filtro DJ, delay, reverb e pan.
- Mix master: DUCK pelo bumbo, filtro DJ, DUST e limitador sempre ligado.
- Biblioteca sintetizada: 12 kits de bateria e 48 sons em 6 categorias.
- Acordes: 7 graus do tom, joystick de 8 variações que trava, strum, arp (divisão, ordem, alcance), inversão e oitava.
- Sampler: microfone ou arquivo; cortar, reverso, fatiar em grade ou por ataques.
- Sequencer de 16 passos com swing.
- Latência de gravação calibrável (CFG › CALIBRAR).
- Projeto e samples salvos no aparelho (IndexedDB); exportar/importar backup `.json`.

## Instalar
Abra o endereço do GitHub Pages no Safari → Compartilhar → Adicionar à Tela de Início. O microfone exige HTTPS.

## Teste
`python3 testes/smoke.py index.html` (Playwright + Chrome): simula toques e microfone e falha se houver erro de JavaScript. Não mede timing nem áudio.
