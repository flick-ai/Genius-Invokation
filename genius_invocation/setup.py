from setuptools import setup,find_packages
setup(name='genius',
      version='0.0.1',
      description='Genius-Invocation',
      author='Bluixe',
      author_email='1q20943033@gmail.com',
      requires=['loguru'], # 定义依赖哪些模块
      packages=find_packages(), # 系统自动从当前目录开始找包
      # 如果有的包不用打包，则只能指定需要打包的文件
      #packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
      license='apache 3.0')