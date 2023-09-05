from modules.capsolverGen import capsolver
from modules.capmonsterGen import capmonster

print("[+] 1. CapSolver\n[+] 2. Capmonster")
option = int(input("[+] What service would like to gen a key for?: "))


if option == 1:
    capsolver()
else:
    capmonster()


