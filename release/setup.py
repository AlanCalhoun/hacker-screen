"""Install / wheel build — app source lives in ../app/src, assets in ../app/assets."""

from pathlib import Path
import shutil

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py

APP_ROOT = Path(__file__).resolve().parent.parent / "app"


class BuildPy(build_py):
    def run(self) -> None:
        super().run()
        src = APP_ROOT / "assets"
        if not src.is_dir():
            return
        dst = Path(self.build_lib) / "hacker_screen" / "assets"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst, dirs_exist_ok=True)


setup(
    package_dir={"": "../app/src"},
    packages=find_packages("../app/src"),
    cmdclass={"build_py": BuildPy},
)
