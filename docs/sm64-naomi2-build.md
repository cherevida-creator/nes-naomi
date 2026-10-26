# Super Mario 64 para Naomi 2

## Qué contiene el port

El ejecutable parte de `Dreamcast-Projects/sm64-port-lat` fijado en `e4574b577609a51c6b7ca7914d2f25436831eede`. Conserva los recursos extraídos de la ROM original, incluidos gráficos, niveles, música y efectos. La adaptación selecciona el controlador JVS de Player 1: joystick para el stick N64, botones arcade 1–6 para A/B/Z/C-left/C-right/R y botón Start para Start.

## Compilación completa

Se compiló el juego completo con KallistiOS 2.2.1 y GCC SH-4 15.1.0 para la subarquitectura Naomi. Para repetir la compilación, instala KallistiOS, coloca una ROM base propia como `baserom.us.z64` en la raíz del repositorio (o indica `SM64_BASEROM`) y ejecuta:

```bash
export KOS_SUBARCH=naomi
source /opt/toolchains/dc/kos/environ.sh
bash tools/build_sm64_naomi2.sh
```

El script fija las revisiones de SM64 y libnaomi, aplica el overlay del controlador, compila el ELF/RAW completo y crea `mario64-naomi2.bin` con `naomibintool` como plataforma `Naomi2`. La ROM base y los recursos comerciales permanecen locales y no se suben al repositorio.

## Estado del BIN generado

El paquete local fue releído por `naomibintool`: declara `Naomi2`, contiene el título `Super Mario 64`, tiene un segmento de 12.498.372 bytes cargado en `0x8c020000` y punto de entrada `0x8c020000`. Su SHA-256 actual es `54df927ed4019dedfd5857924805d0782362a9241b19d69ddb097384c27c988e`.

Esto confirma que se compiló y empaquetó el juego completo; no confirma que Flycast o una placa Naomi 2 lo hayan arrancado. El registro aportado reconoce el juego y selecciona Naomi 2, y advierte que no encuentra la revisión `epr-23607c.ic27`. Flycast también acepta la revisión `epr-23607b.ic27`, que aparece en la captura del archivo del usuario, buscando las ROMs por CRC; por eso el aviso sobre la revisión `c` no demuestra que el BIOS impida el arranque. No tenemos aquí los bytes de ese archivo para repetir el arranque. El BIN se mantiene como **compilado, arranque pendiente de verificar**, no como funcional.

## CI y comprobación pendiente

La GitHub Action existente comprueba la integración de controles y compila el puente SH-4; no contiene una ROM base ni produce el juego completo. No se añade la ROM ni los recursos comerciales a GitHub. Para cerrar la verificación hay que arrancar este BIN recién generado en Flycast o una placa Naomi 2 y confirmar vídeo, audio y controles de Player 1. La carga real por NetDIMM tampoco se ha verificado.
