"""Report the __DATA/__bss layout of an arm64 Mach-O executable and whether stone.free_blocks
falls where the file has nonzero bytes (the bytes the crashed process saw in place of zeros)."""
import struct
import sys

def parse(path):
    b = open(path, "rb").read()
    magic, _cpu, _sub, _ft, ncmds, _sz, _fl, _res = struct.unpack_from("<IiiIIIII", b, 0)
    assert magic == 0xFEEDFACF, hex(magic)
    off = 32
    segs, sects, symtab = {}, {}, None
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", b, off)
        if cmd == 0x19:  # LC_SEGMENT_64
            name = b[off + 8:off + 24].rstrip(b"\0").decode()
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", b, off + 24)
            nsects = struct.unpack_from("<I", b, off + 64)[0]
            segs[name] = (vmaddr, vmsize, fileoff, filesize)
            s = off + 72
            for _ in range(nsects):
                sname = b[s:s + 16].rstrip(b"\0").decode()
                addr, size = struct.unpack_from("<QQ", b, s + 32)
                sects[sname] = (addr, size)
                s += 80
        elif cmd == 0x2:  # LC_SYMTAB
            symtab = struct.unpack_from("<IIII", b, off + 8)
        off += cmdsize
    syms = {}
    if symtab:
        symoff, nsyms, stroff, _strsize = symtab
        for i in range(nsyms):
            strx, _t, _s, _d, value = struct.unpack_from("<IBBHQ", b, symoff + 16 * i)
            end = b.index(b"\0", stroff + strx)
            syms[b[stroff + strx:end].decode()] = value
    return b, segs, sects, syms

def report(path):
    b, segs, sects, syms = parse(path)
    vmaddr, vmsize, fileoff, filesize = segs["__DATA"]
    bss_addr, bss_size = sects["__bss"]
    fb = syms["stone.free_blocks"]
    rel = fb - vmaddr
    fo = fileoff + rel
    window = b[fo:fo + 128]  # free list heads for the first 16 size classes
    past = rel >= filesize
    dirty = past and any(window)
    print(f"{path}: file {len(b)}  __DATA filesize {filesize:#x} vmsize {vmsize:#x}  "
          f"__bss {bss_addr - vmaddr:#x}..{bss_addr - vmaddr + bss_size:#x}  "
          f"free_blocks at {rel:#x} -> file offset {fo:#x} "
          f"({'past EOF' if fo >= len(b) else 'in file'})  "
          f"{'CRASH EXPECTED' if dirty else 'ok'}")
    return dirty

if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
