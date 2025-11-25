import samples.Utils as Utils
from unicorn import Unicorn, UnicornConst, Arm64Const

ARM64_CODE=Utils.hexToBytes("ab0500b8af054038")
ARM64_CODE_EB=ARM64_CODE;
ARM64_MRS_CODE=Utils.hexToBytes("62d03bd5")
ARM64_PAC_CODE=Utils.hexToBytes("e123c1da")
ADDRESS=0x10000

def hook_block(uc, address, size, user_data):
    print(">>> Tracing basic block at 0x%x, block size = 0x%x\n" % (address, size))

def hook_code(uc, address, size, user_data):
     print(">>> Tracing instruction at 0x%x, instruction size = 0x%x\n" % (address, size))

def main():
    x11=0x12345678
    x13=0x10000 + 0x8
    x15=0x33
    print("Emulate ARM64 code\n")
    uc = Unicorn(UnicornConst.UC_ARCH_ARM64, UnicornConst.UC_MODE_ARM)
    uc.mem_map(ADDRESS, 2 * 1024 * 1024, UnicornConst.UC_PROT_ALL)
    uc.mem_write(ADDRESS, ARM64_CODE)
    uc.reg_write(Arm64Const.UC_ARM64_REG_X11, x11)
    uc.reg_write(Arm64Const.UC_ARM64_REG_X13, x13)
    uc.reg_write(Arm64Const.UC_ARM64_REG_X15, x15)
    uc.hook_add(hook_block, 1, 0 , None)
    uc.hook_add(hook_code, ADDRESS, ADDRESS, None)
    uc.emu_start(ADDRESS, ADDRESS + len(ARM64_CODE), 0, 0)
    print(">>> Emulation done. Below is the CPU context\n")
    print(">>> As little endian, X15 should be 0x78:\n")
    print(">>> X15 = 0x%x\n" % (uc.reg_read(Arm64Const.UC_ARM64_REG_X15),))

main()

