#!/usr/bin/env python3

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import enum
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Tuple

class Mode(enum.Enum):
    local = 'local'
    cross = 'cross'


def is_unix(os: str) -> bool:
    return os in ['linux']


def is_mac(os: str) -> bool:
    return os in ['darwin']


def is_windows(os: str) -> bool:
    return os in ['windows']


def get_cargo_artifact_name(os: str, arch: str) -> str:
    if is_unix(os):
        return f"libopendaljni.so"
    elif is_mac(os):
        return f"libopendaljni.dylib"
    elif is_windows(os):
        return f"opendaljni.dll"
    raise Exception(f"unsupported platform {os}@{arch}")


def get_jni_library_name(os: str, arch: str) -> str:
    if is_unix(os):
        return f"libopendaljni-linux-{arch}.so"
    elif is_mac(os):
        return f"libopendaljni-osx-{arch}.dylib"
    elif is_windows(os):
        return f"libopendaljni-win-{arch}.dll"
    raise Exception(f"unsupported platform {os}@{arch}")


def normalize(os: str, arch: str) -> Tuple[str, str]:
    os = os.lower()
    arch = arch.lower()

    if arch == 'arm64':
        return (os, 'aarch64')
    if arch == 'amd64':
        return (os, 'x86_64')

    return (os, arch)


if __name__ == '__main__':
    binding_root = Path(__file__).parent.parent
    opendal_root = binding_root.parent.parent

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('mode', type=Mode, default=Mode.local, choices=list(Mode))
    args = parser.parse_args()

    if args.mode != Mode.cross:
        subprocess.run([
            'cargo', 'build', '--color=always', '--release',
        ], cwd=binding_root)

        (os, arch) = normalize(platform.system(), platform.machine())

        src = opendal_root / 'target' / 'release' / get_cargo_artifact_name(os, arch)
        dst = binding_root / 'target' / 'classes' / 'native' / get_jni_library_name(os, arch)
        dst.parent.mkdir(exist_ok=True, parents=True)
        shutil.copy2(src, dst)
    else:  # cross

        pass
