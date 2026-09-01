cmake_minimum_required(VERSION 3.21)
project(kcm_prayerlockscreen LANGUAGES CXX)

find_package(ECM 6.0 REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH})

include(KDEInstallDirs)
include(KDECompilerSettings NO_POLICY_SCOPE)
include(KDECMakeSettings)

find_package(Qt6 6.6 REQUIRED COMPONENTS Quick Qml)
find_package(KF6 6.0 REQUIRED COMPONENTS KCMUtils CoreAddons I18n)

kcmutils_add_qml_kcm(kcm_prayerlockscreen SOURCES prayerlockscreen.h prayerlockscreen.cpp)
target_link_libraries(kcm_prayerlockscreen PRIVATE
    KF6::KCMUtils
    KF6::CoreAddons
    KF6::I18n
    Qt6::Quick
)
