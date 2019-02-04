from pathlib import Path
import sys

savedir = Path('e:/temp') / 'gary'


def _mk_save_dir():    
    newdir = Path(savedir) / 'Apps' / 'icalendar'

    if not newdir.exists():
        newdir.mkdir(parents=True)
        
    return newdir


def _write_file():
    filename = 'foo'
    newfile = _mk_save_dir() / filename
    print(newfile)
    print(type(newfile))
    newfile.write_text('gary')
    print('saved:%s' % newfile)


def main(argv):
    _write_file()
    
if __name__ == '__main__':
    main(sys.argv)
