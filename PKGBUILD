# Maintainer: q4t <qatoqatt@gmail.com>
pkgname=prayer-lockscreen
pkgver=0.1.0
pkgrel=1
pkgdesc="Overlay prayer times on KDE Plasma lock screen wallpaper"
arch=('any')
url="https://github.com/q4t/prayer-lockscreen"
license=('MIT')
depends=('python' 'python-pillow' 'python-pyqt6' 'kde-cli-tools')
makedepends=('python-build' 'python-installer' 'python-setuptools' 'python-wheel')
options=(!strip)
source=()

build() {
    cd "$startdir"
    python -m build --wheel --no-isolation
}

package() {
    cd "$startdir"
    python -m installer --destdir="$pkgdir" dist/*.whl

    install -Dm644 arch/prayer-lockscreen.service \
        "$pkgdir/usr/lib/systemd/user/prayer-lockscreen.service"
    install -Dm644 arch/prayer-lockscreen.timer \
        "$pkgdir/usr/lib/systemd/user/prayer-lockscreen.timer"

    install -Dm644 config/config.json \
        "$pkgdir/usr/share/prayer-lockscreen/config.json"

    # KDE System Settings module
    install -Dm644 prayer-lockscreen-settings.desktop \
        "$pkgdir/usr/share/kservices6/prayer-lockscreen-settings.desktop"
    install -Dm644 prayer-lockscreen-settings.desktop \
        "$pkgdir/usr/share/kservices5/prayer-lockscreen-settings.desktop"
}
