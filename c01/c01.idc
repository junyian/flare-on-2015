#include <idc.idc>

static main()
{
    auto addr=0x402140;
    auto i;
    auto c;
    for(i=0;i<0x18;i++){
        c = byte(addr+i)^0x7D;
        msg(c);
    }
}