## SM64 para Naomi 2: estado del port

### Integración y controles

- El port parte de Dreamcast-Projects/sm64-port-lat (e4574b577609a51c6b7ca7914d2f25436831eede) y conserva su código, gráficos, niveles, música y efectos de sonido.
- Player 1 JVS se traduce a entrada N64; las diagonales se normalizan y las direcciones opuestas se cancelan. Botones JVS 1–6: A, B, Z, C-left, C-right y R; Start: Start.
- La ruta Naomi se selecciona antes que la Dreamcast cuando ambas macros están definidas. El puente Maple/JVS usa la integración fijada de DragonMinded/libnaomi (fadc8536d3c115b53277c50dca5d001dfbccc30d) y KallistiOS.
- La ejecución [Actions #45](https://github.com/cherevida-creator/nes-naomi/actions/runs/40323173443) pasó los tests de controles/prioridad Naomi y compiló los objetos SH-4 del controlador y el puente KallistiOS. No compila ni enlaza el juego completo.

### Paquete candidato y diagnóstico

El BIN recibido mide 12.549.084 bytes y `rominfo` reconoce una imagen Naomi 1, con una sección de carga y punto de entrada `0x8c020000`. Esto valida la cabecera y la estructura del contenedor, pero no que el payload sea un build Naomi 2 que arranque.

Cambiar la etiqueta del encabezado a Naomi 2 no altera el payload. Al probar el candidato con la selección Naomi 2 de Flycast, el usuario reportó `Fatal: SH4 exception when blocked`; por tanto, cambiar la cabecera no corrige el fallo. El origen exacto de la excepción todavía no está localizado.

La ROM base y los assets extraídos se usan solo localmente; no se suben a GitHub ni se pasan a Actions. La compilación completa del juego para Naomi 2 y el arranque sin excepciones aún no están verificados.

### Límite de verificación

El diagnóstico de controles es un programa independiente de libnaomi: muestra el estado JVS y sirve para comprobar Player 1, pero no contiene SM64. El BIN de Mario falla al ejecutarse en Flycast y no se ha probado en hardware Naomi 2. Por tanto, no se declara funcional el port de Mario. Tampoco se ha probado la ruta real de carga por NetDIMM en una máquina.

El registro Flycast más reciente reconoce `Super Mario 64` y selecciona el BIOS Naomi 2. Solo informa de que no encuentra `epr-23607c.ic27`; no contiene `Fatal: SH4 exception when blocked` ni registros de excepción. Por tanto, este archivo no permite atribuir el fallo del juego a una excepción SH-4. Flycast se cierra limpiamente en el propio registro.

El BIN candidato declara su sección y punto de entrada en `0x8c020000`; el Makefile de libnaomi usa por defecto `0x0c021000` en sus ejemplos. Es una diferencia que merece verificarse al integrar el cargador Naomi con el ejecutable KOS: `0x8c...` es un alias P1 de RAM física `0x0c...`, así que comparar solo los números no demuestra por sí mismo que el encabezado sea inválido ni identifica la causa del error 01. Cambiar la etiqueta `NAOMI` por `Naomi2` tampoco corrige el payload. Hace falta generar el paquete con direcciones coherentes y arrancarlo en Flycast para confirmar o descartar esta hipótesis.

En el entorno de trabajo actual no están instalados Docker, `sh-elf-gcc` ni KallistiOS (`KOS_BASE`). Al intentar reconstruir el upstream con `make TARGET_DC=1`, Make termina en `Makefile:952: /Makefile.rules: No such file or directory`. Así que aquí no se ha regenerado un BIN de Mario corregido.

Para cerrar esa validación hay que localizar y corregir la excepción SH-4, compilar el juego completo para Naomi 2 y comprobar vídeo, audio AICA y controles en Flycast o hardware. Hasta entonces, trátese como candidato experimental, no como entrega funcional.
