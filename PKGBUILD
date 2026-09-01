# Maintainer: q4t <qatoqatt@gmail.com>
pkgname=prayer-lockscreen
pkgver=0.1.0
pkgrel=1
pkgdesc="Overlay prayer times on KDE Plasma lock screen wallpaper"
arch=('any')
url="https://github.com/q4t/prayer-lockscreen"
license=('MIT')
depends=('python' 'python-pillow' 'python-pyqt6' 'kde-cli-tools')
makedepends=('python-build' 'python-installer' 'python-setuptools' 'python-wheel'
             'extra-cmake-modules' 'qt6-base' 'kcmutils' 'kirigami' 'ki18n')
options=(!strip)
source=()

build() {
    cd "$startdir"

    # Build Python wheel
    python -m build --wheel --no-isolation

    # Build KCM
    rm -rf kcm_build
    mkdir -p kcm_build/ui
    cp kcm_src/CMakeLists.txt kcm_build/
    cp kcm_src/*.cpp kcm_src/*.h kcm_src/*.json kcm_build/
    cp kcm_src/ui/*.qml kcm_build/ui/
    cd kcm_build
    cmake -B build/ -DCMAKE_INSTALL_PREFIX=/usr
    cmake --build build/
    cd "$startdir"
}

package() {
    cd "$startdir"

    # Install Python package
    python -m installer --destdir="$pkgdir" dist/*.whl

    # Install systemd units
    install -Dm644 arch/prayer-lockscreen.service \
        "$pkgdir/usr/lib/systemd/user/prayer-lockscreen.service"
    install -Dm644 arch/prayer-lockscreen.timer \
        "$pkgdir/usr/lib/systemd/user/prayer-lockscreen.timer"

    # Install default config
    install -Dm644 config/config.json \
        "$pkgdir/usr/share/prayer-lockscreen/config.json"

    # Install KCM plugin
    install -Dm644 kcm_build/build/bin/plasma/kcms/systemsettings/kcm_prayerlockscreen.so \
        "$pkgdir/usr/lib/qt6/plugins/plasma/kcms/systemsettings/kcm_prayerlockscreen.so"

    # Install KCM desktop file
    install -Dm644 kcm_build/build/kcm_prayerlockscreen.desktop \
        "$pkgdir/usr/share/applications/kcm_prayerlockscreen.desktop"

    # Cleanup
    rm -rf kcm_build
}
