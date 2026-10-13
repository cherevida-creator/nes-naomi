#ifndef SM64_NAOMI_MAPLE_KOS_COMPAT_H
#define SM64_NAOMI_MAPLE_KOS_COMPAT_H

/* KOS bindings for libnaomi's Naomi JVS-over-Maple protocol driver. */
#include <kos.h>
#include <stdlib.h>

#define UNCACHED_MIRROR 0xA0000000u
#define PHYSICAL_MASK   0x0FFFFFFFu
#define RAM_BASE        0x0C000000u
#define RAM_SIZE        0x02000000u
#define mutex_free      mutex_destroy

/* libnaomi returns nonzero on success; KOS mutex_trylock returns zero. */
static inline int sm64_naomi_mutex_try_lock(mutex_t *mutex)
{
    return mutex_trylock(mutex) == 0;
}
#define mutex_try_lock sm64_naomi_mutex_try_lock

static inline void sm64_naomi_maple_invariant(const char *where,
                                               const char *reason)
{
    (void)where;
    (void)reason;
    abort();
}
#define _irq_display_invariant sm64_naomi_maple_invariant

void _maple_init(void);

#endif
