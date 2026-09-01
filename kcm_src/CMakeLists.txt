kcmutils_add_qml_kcm(kcm_prayerlockscreen)

target_sources(kcm_prayerlockscreen PRIVATE
   prayerlockscreen.cpp
   prayerlockscreen.h
)

target_link_libraries(kcm_prayerlockscreen PRIVATE
    Qt::Quick
    KF6::CoreAddons
    KF6::KCMUtils
    KF6::I18n
)
