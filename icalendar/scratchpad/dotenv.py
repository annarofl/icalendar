# see https://github.com/pedroburon/dotenv
# pip install dotenv
#
# Use this to configure per-team environments, then only need the one
# 'main' app to be available, with different runtime

from dotenv import Dotenv
dotenv = DotEnv('/path/to/.env')
print(dotenv)
print(dotenv['FOO'])
dotenv['FOO'] = "baz"
print(dotenv['FOO'])
del dotenv['FOO']
print(dotenv)
