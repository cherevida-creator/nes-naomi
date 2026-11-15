/* SM64's 512-byte EEPROM image in Naomi battery-backed mainboard SRAM.
 * Two independent CRC records; no VMU, no savestates, no BIOS EEPROM writes.
 * Physical-board power-cycle validation remains mandatory. */
#include <stdint.h>
#include <string.h>
#define SAVE_BYTES 512u
#define SLOT_BYTES 1024u
#define SRAM_BASE ((volatile uint8_t *)0xa0204000u)
#define MAGIC 0x34364d53u
static uint8_t image[SAVE_BYTES];
static uint32_t generation;
static int loaded, active=-1;
volatile uint32_t sm64_save_commits, sm64_save_errors, sm64_save_loaded;
static uint32_t crc32(const uint8_t *p,unsigned n) {
    uint32_t c=~0u;
    while(n--) {c^=*p++;for(unsigned i=0;i<8;i++)c=(c>>1)^((0u-(c&1))&0xedb88320u);}
    return ~c;
}
static uint32_t get32(volatile uint8_t *p) {
    return (uint32_t)p[0]|(uint32_t)p[1]<<8|(uint32_t)p[2]<<16|(uint32_t)p[3]<<24;
}
static void put32(volatile uint8_t *p,uint32_t v) {
    for(unsigned i=0;i<4;i++)p[i]=(uint8_t)(v>>(i*8));
}
static int valid(int bank,uint8_t *dst,uint32_t *gen) {
    volatile uint8_t *p=SRAM_BASE+bank*SLOT_BYTES;
    if(get32(p)!=MAGIC || get32(p+4)!=0x00010200u)return 0;
    for(unsigned i=0;i<SAVE_BYTES;i++)dst[i]=p[16+i];
    if(crc32(dst,SAVE_BYTES)!=get32(p+12))return 0;
    *gen=get32(p+8);return 1;
}
static void load(void) {
    uint8_t a[SAVE_BYTES],b[SAVE_BYTES];uint32_t ga=0,gb=0;
    int va=valid(0,a,&ga),vb=valid(1,b,&gb);
    if(va||vb){
        active=vb&&(!va||(int32_t)(gb-ga)>0)?1:0;
        memcpy(image,active?b:a,SAVE_BYTES);generation=active?gb:ga;
        sm64_save_loaded=1;
    }else memset(image,0,SAVE_BYTES);
    loaded=1;
}
int sm64_naomi_save_read(unsigned offset,void *dst,unsigned n) {
    if(offset>SAVE_BYTES || n>SAVE_BYTES-offset)return -1;
    if(!loaded)load();
    memcpy(dst,image+offset,n);return 0;
}
int sm64_naomi_save_write(unsigned offset,const void *src,unsigned n) {
    if(offset>SAVE_BYTES || n>SAVE_BYTES-offset)return -1;
    if(!loaded)load();
    memcpy(image+offset,src,n);
    int next=active==0?1:0;uint32_t gen=generation+1;
    volatile uint8_t *p=SRAM_BASE+next*SLOT_BYTES;
    put32(p,0);put32(p+4,0x00010200u);put32(p+8,gen);
    for(unsigned i=0;i<SAVE_BYTES;i++)p[16+i]=image[i];
    put32(p+12,crc32(image,SAVE_BYTES));
    /* SH-4 uncached volatile stores are ordered for this byte SRAM region. */
    put32(p,MAGIC);
    uint8_t verify[SAVE_BYTES];uint32_t got=0;
    if(!valid(next,verify,&got)||got!=gen||memcmp(verify,image,SAVE_BYTES)){
        sm64_save_errors++;return -1;
    }
    generation=gen;active=next;sm64_save_commits++;return 0;
}