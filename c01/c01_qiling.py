# Written with Python 3.8 on WSL
from qiling import *
from qiling.const import QL_VERBOSE

from qiling.os.windows.api import *
from qiling.os.windows.fncc import *

# Override the generic ReadFile hook that comes with Qiling

# BOOL ReadFile(
#   HANDLE       hFile,
#   LPVOID       lpBuffer,
#   DWORD        nNumberOfBytesToRead,
#   LPDWORD      lpNumberOfBytesRead,
#   LPOVERLAPPED lpOverlapped
# );
@winsdkapi(cc=STDCALL, params={
    'hFile'                : HANDLE,
    'lpBuffer'             : LPVOID,
    'nNumberOfBytesToRead' : DWORD,
    'lpNumberOfBytesRead'  : LPDWORD,
    'lpOverlapped'         : LPOVERLAPPED
})
def my_ReadFile(ql: Qiling, address: int, params):
    hFile = params["hFile"]
    lpBuffer = params["lpBuffer"]
    nNumberOfBytesToRead = params["nNumberOfBytesToRead"]
    lpNumberOfBytesRead = params["lpNumberOfBytesRead"]

    ql.log.debug("Mocking input")
    xorbytes = ql.mem.read(0x402140, 0x18)
    data = ''
    for x in xorbytes:
        data += chr(x^0x7d)
    data = bytes(data, 'ascii') + b"\x00"
    print(data)
    ql.mem.write(lpBuffer, data)
    ql.mem.write(lpNumberOfBytesRead, ql.pack(len(data)))
    return 1

# Since there's no proper ExitProcess procedure, stop emulation at the end of the EXE.
def stop(ql:Qiling):
    ql.emu_stop()

def my_sandbox(path, rootfs):
    ql = Qiling(path, rootfs, verbose=QL_VERBOSE.DEFAULT, profile='windows.ql')
    ql.set_api("ReadFile", my_ReadFile)
    ql.hook_address(stop, 0x401094)
    ql.run()

if __name__ == '__main__':
    my_sandbox(["./i_am_happy_you_are_to_playing_the_flareon_challenge.exe"], "/mnt/c/tools/qiling/examples/rootfs/x86_windows")