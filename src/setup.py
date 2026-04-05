from setuptools import setup
import setup_translate

pkg = 'Extensions.PermanentClock'
setup(name='enigma2-plugin-extensions-permanentclock',
       version='3.0',
       description='Shows the clock permanent on the screen',
       package_dir={pkg: 'PermanentClock'},
       packages=[pkg],
       package_data={pkg: ['images/*.png', '*.png', '*.xml', 'locale/*/LC_MESSAGES/*.mo', '*.info', '*.txt', 'trad/*.png']},
       cmdclass=setup_translate.cmdclass,  # for translation
      )
