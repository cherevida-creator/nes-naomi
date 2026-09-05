# NES Naomi

Port de un emulador NES para Sega Naomi pensado para NetDIMM/PiForce.

## Objetivo
- Salida fija de libnaomi actual: 640x480p @ 60 Hz (31 kHz VGA).
- NES 256x240 escalada pixel-perfect x2 a 512x480, centrada con 64 px a cada lado.
- JVS: joystick = cruceta, B1 = NES B, B2 = NES A, START = Start, SERVICE = Select, B3 = volver al menu.
- Audio APU 44.1 kHz por ring buffer AICA.
- Carpeta `roms/` empaquetada como ROMFS.
- Nucleo: PeakRacing/nes, Apache-2.0, fijado al commit 69e433da8bd1eaf993659991f30b4989b77dad2c.
- SDK: DragonMinded/libnaomi, fijado al commit fb6f6e3f42885ddb845977392fad8f5a9bfa7ad5.

## ROMs
Copia tus `.nes` en `roms/` antes de compilar. No se incluyen ROMs comerciales.

## Construccion
1. `tools/bootstrap.sh`
2. Instala/construye el toolchain de libnaomi siguiendo el README oficial de `vendor/libnaomi`.
3. `tools/build.sh`
4. Resultado: `nes_naomi.bin`

## NetDIMM/PiForce
Copia `nes_naomi.bin` al directorio de imagenes que uses con PiForce y envialo al NetDIMM como cualquier otro binario Naomi.

## Nota sobre `roms/`
El NetDIMM no expone la carpeta de la Raspberry como un filesystem al programa Naomi. Por eso `roms/` queda integrada en el ROMFS del `.bin`; cambiar juegos requiere recompilar el binario.
