# Super Mario 64 para Naomi 2

La compilación del port usa la revisión fijada de Dreamcast-Projects/sm64-port-lat y un baserom US local. La ROM se lee desde `SM64_BASEROM`; nunca se copia al repositorio.

## Compilar

Requisitos: KallistiOS con toolchain SH-4, CMake, Git, Python 3 y una ROM US de Super Mario 64 obtenida legalmente.

```sh
source /ruta/a/kos/environ.sh
export SM64_BASEROM=/ruta/privada/baserom.us.z64
bash tools/build_sm64_naomi2.sh
```

La compilación fija `KOS_SUBARCH=naomi` y fuerza el linker a usar `LOAD_OFFSET=0x8c020000`, incluso si el entorno de KOS se cargó antes con las opciones de Dreamcast. Se detiene si el ELF de SH-4 no empieza en esa dirección. Luego construye `mario64-naomi2.bin` y comprueba que la cabecera Naomi declara la misma dirección de carga y el mismo punto de entrada que el ELF.

El script descarga GLdc en el commit `f06c72ff145d5354467739f26264160a996e3a2d`, aplica la integración de JVS Player 1 y usa la salida de audio KOS. Joystick arcade se mapea a la palanca N64; botones 1–6 a A, B, Z, C-left, C-right y R; Player 1 Start a Start.

La ROM base y los assets generados quedan fuera del repositorio.

## Verificación

Las comprobaciones de compilación y metadatos prueban que la imagen SH-4 se construyó con el formato y las direcciones esperadas. No prueban por sí solas ejecución, vídeo, audio ni controles en Naomi 2. El BIN solo se considerará funcional tras iniciar el juego en Flycast o hardware y verificar esos componentes.

Upstream: Dreamcast-Projects/sm64-port-lat, commit `e4574b577609a51c6b7ca7914d2f25436831eede`.
