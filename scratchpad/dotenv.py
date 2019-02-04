# see https://github.com/pedroburon/dotenv
# pip install dotenv
#
# Use this to configure per-team environments, then only need the one
# 'main' app to be available, with different runtime

from dotenv import Dotenv
env = DotEnv('/path/to/.env')
print(env)
print(env['FOO'])
env['FOO'] = "baz"
print(env['FOO'])
del env['FOO']
print(env)
