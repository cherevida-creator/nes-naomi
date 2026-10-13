## SM64 para Naomi 2: estado del port

### Validado por GitHub Actions

- El overlay modifica, de forma reproducible y fijada por commit, el registro de controladores de Dreamcast-Projects/sm64-port-lat (e4574b577609a51c6b7ca7914d2f25436831eede).
- Player 1 JVS se convierte a entrada N64; diagonales se normalizan y direcciones opuestas se cancelan.
- Los botones Player 1 1–6 se asignan a A, B, Z, C-left, C-right y R; Start se asigna a Start.
- La integración reutiliza el header y la implementación Maple/JVS fijados de DragonMinded/libnaomi (fadc8536d3c115b53277c50dca5d001dfbccc30d) con un puente KallistiOS para mutex e inicialización.
- En la corrida [Actions #34](https://github.com/cherevida-creator/nes-naomi/actions/runs/38364146275) pasaron el test de controles host y la compilación SH-4 de los objetos del controlador y del bridge Maple para Naomi.

### Lo que esta comprobación no cubre

Actions compila esos dos objetos. Todavía no compila el juego completo, no genera un ELF o BIN del juego, no crea un paquete .dat de NetDimm y no prueba el arranque en Naomi 2 ni en un emulador. La ejecución #34 no es una compilación jugable.

Falta integrar y validar el arranque Naomi/KOS del juego completo: temporización y salida de vídeo, audio/AICA, enlace con los módulos upstream y el empaquetado final. El overlay actual añade TARGET_NAOMI sobre el build Dreamcast upstream; esto todavía no demuestra compatibilidad del motor de vídeo/audio ni del juego.

La fuente y los assets originales de SM64 se conservan en el upstream; no se sustituyen gráficos ni audio. La ROM comercial no está en el repositorio y no debe subirse a GitHub ni a Actions. La extracción de assets y el build final deben realizarse localmente con la ROM del usuario.

### Estado de entrega

No hay un BIN/.dat funcional verificado. Para declararlo funcional, hay que compilar el juego completo con la ROM local, validar cabecera y estructura del paquete NetDimm y arrancarlo con éxito en emulador Naomi 2 o hardware Naomi 2.
