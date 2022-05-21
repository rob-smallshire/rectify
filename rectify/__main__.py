import os
import sys

path = os.path.dirname(__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)


from rectify.cli import main


sys.exit(main())

