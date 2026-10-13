## SM64 para Naomi 2: estado del port

### Integración y controles

- El port parte de Dreamcast-Projects/sm64-port-lat (e4574b577609a51c6b7ca7914d2f25436831eede) y conserva su código, gráficos, niveles, música y efectos de sonido.
- Player 1 JVS se traduce a entrada N64; las diagonales se normalizan y las direcciones opuestas se cancelan. Botones JVS 1–6: A, B, Z, C-left, C-right y R; Start: Start.
- La ruta Naomi se selecciona antes que la Dreamcast cuando ambas macros están definidas. El puente Maple/JVS usa la integración fijada de DragonMinded/libnaomi (fadc8536d3c115b53277c50dca5d001dfbccc30d) y KallistiOS.
- Las ejecuciones [Actions #39](https://github.com/cherevida-creator/nes-naomi/actions/runs/38372940558) y [#40](https://github.com/cherevida-creator/nes-naomi/actions/runs/38372946496) pasaron los tests de controles/prioridad Naomi y compilaron los objetos SH-4 del controlador y el puente KallistiOS.

### Compilación local y paquete candidato

Se compiló localmente el toolchain SH-4, KallistiOS para Naomi, GLdc, libAL y el juego completo con los assets extraídos de la ROM del usuario. El ELF resultante es SH-4 y se empaquetó como una imagen ROM Naomi con makerom. rominfo reconoce el encabezado, la sección de programa y su dirección de carga/entrada. La imagen candidata mide 12.549.084 bytes.

La ROM comercial y los assets extraídos permanecen locales; no se suben a GitHub ni se pasan a Actions. Actions valida la integración y el código del controlador, pero no reproduce el build completo porque necesita esa ROM privada.

### Límite de verificación

El BIN candidato no se ha arrancado en hardware Naomi 2 ni en un emulador Naomi 2 con BIOS. Por tanto, se verificaron la compilación, la arquitectura SH-4 y la estructura de la imagen ROM, pero no se declara el BIN funcional. Tampoco se ha probado la ruta real de carga por NetDIMM en una máquina.

Para cerrar esa validación falta arrancar esta imagen en Flycast/Naomi o hardware Naomi 2 con BIOS apropiada, y comprobar vídeo, audio AICA y controles durante el juego. No hay un emulador o BIOS Naomi disponible en el entorno de compilación actual. Hasta esa prueba, trátese como candidato experimental, no como entrega funcional.
