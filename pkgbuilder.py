import colorama
from sys import argv, exit

if len(argv) < 2:
    print("You didn't give me the file")
    print("pkgbuilder ./super-version-rel.rpm")
    exit(0)
source = argv[1]
default = source.split('-')
if len(default) == 1:
    default = source.split('_')
for i in default:
    if "i686" in i:
        print(f"{colorama.Fore.RED}Warning! This package is most probably 32bit. It most probably won't work.")
        break
pkgname = ""
pkgver = ""
pkgrel = ""
print(len(default))
if len(default) > 0:
    default[0] = default[0].lstrip("./")
    pkgname = input(f"Package name: {colorama.Style.DIM}(default: {default[0]}) {colorama.Style.NORMAL} >> ")
    if len(pkgname) == 0:
        pkgname = default[0]
else:
    while len(pkgname) == 0:
        pkgname = input(f"Package name: {colorama.Style.DIM}(default: not detected) {colorama.Style.NORMAL} >> ")

if len(default) > 1:
    pkgver = input(f"Package version: {colorama.Style.DIM}(default: {default[1]}) {colorama.Style.NORMAL} >> ")
    if len(pkgver) == 0:
        pkgver = default[1]
else:
    while len(pkgver) == 0:
        pkgver = input(f"Package version: {colorama.Style.DIM}(default: not detected) {colorama.Style.NORMAL} >> ")

if len(default) > 2:
    default = default[2].split('.')
    if default[0].isnumeric():
        pkgrel = input(f"Package release: {colorama.Style.DIM}(default: {default[0]}) {colorama.Style.NORMAL} >> ")
        if len(pkgrel) == 0:
            pkgrel = default[0]
    else:
        while len(pkgrel) == 0:
            pkgrel = input(f"Package release: {colorama.Style.DIM}(default: not detected) {colorama.Style.NORMAL} >> ")
else:
    while len(pkgrel) == 0:
        pkgrel = input(f"Package release: {colorama.Style.DIM}(default: not detected) {colorama.Style.NORMAL} >> ")

pkgdesc = input(f"Package description: {colorama.Style.DIM}(default: {pkgname}) {colorama.Style.NORMAL} >> ")
if len(pkgdesc) == 0:
    pkgdesc = pkgname
    
s = f"pkgname=\"{pkgname}\"\n"
s += f"pkgver=\"{pkgver}\"\n"
s += f"pkgrel=\"{pkgrel}\"\n"
s += f"pkgdesc=\"{pkgdesc}\"\n"
s += "arch=(\"x86_64\")\n\n"
s += f"source=(\"{source.lstrip("./")}\")\n\n"
s += "sha256sums=(\"SKIP\")\n"
s += "package() {\n"
s += "\tfind $srcdir/ -mindepth 1 -maxdepth 1 -type d | xargs cp -r -t \"$pkgdir\"\n"
s += "}"

with open("./PKGBUILD", "w") as f:
    f.write(s)
    
print("Finished generating PKGBUILD")
print("Make sure to run " + colorama.Style.BRIGHT + "$ makepkg" + colorama.Style.NORMAL + " to build it and")
print(f"{colorama.Style.BRIGHT}$ pacman -U {pkgname}-{pkgver}-{pkgrel}-x86_64.pkg.tar.zst{colorama.Style.NORMAL} as root or using sudo to install")