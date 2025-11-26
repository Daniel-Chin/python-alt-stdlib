'''
Translate markdown .md file to html file.  
Note: to work on WordPress, avoid level one header (# Title).  
A lot of markdown features are not implemented!  
'''
import argparse
import re
import sys
from itertools import cycle

FONT_SIZE = (20, 36, 24, 18, 16, 14, 13, 13, 13)

class Translator:
    def __init__(self):
        self.code_block_started = False
    
    def translateLine(self, src):
        s = self.handleCode(src.rstrip())
        if self.code_block_started:
            tag = '%s<br />'
            s = s.replace(' ' * 2, '&nbsp;' * 2)
        else:
            n_hash = 0
            while s.startswith('#'):
                n_hash += 1
                s = s[1:]
            tag = self.n_hash2Tag(n_hash)
            s = self.handleLinks(s)
            s += '&nbsp;'
        return tag % s
    
    def n_hash2Tag(self, n_hash):
        styles = []
        styles.append('font-size: %dpt;' % FONT_SIZE[n_hash])
        # styles.append('line-height: 1.2;')
        if n_hash >= 1:
            styles.append('margin-top: 0;')
            styles.append('padding-top: 2pt;')
            styles.append('padding-bottom: 2pt;')
            styles.append('margin-bottom: 0;')
            styles.append('font-weight: bold;')
        style = 'style="%s"' % ' '.join(styles)
        if n_hash == 0:
            tag = f'<span {style}>%s</span><br />'
        if n_hash >= 1:
            tag = f'<h{n_hash} {style}>%s</h{n_hash}>'
            if n_hash in (1, 2):
                tag += '<hr />'
        return tag
    
    def handleLinks(self, s):
        # before[text](link)after
        try:
            while '](' in s:
                left, right = s.split('](', 1)
                brack_pos = left.rfind('[')
                before = left[:brack_pos]
                text = left[brack_pos + 1:]
                link, after = right.split(')', 1)
                s = '%s<a href="%s">%s</a>%s' % (before, link, text, after)
        except Exception as e:
            print(e, 'illegal line:', s)
        return s
    
    def handleCode(self, s):
        backticks = [x.end() for x in re.finditer('```', s)]
        if backticks:
            if len(backticks) >= 2:
                print('Error: two "```"s in one line. ')
                print('Problem line:', s)
                sys.exit(1)
            if self.code_block_started:
                s = s.replace('```', '</code>')
            else:
                language = s[backticks[0]:].strip()
                if language:
                    tag = '<code language="%s">' % language
                else:
                    tag = '<code>'
                s = s[:backticks[0] - 3] + tag
            self.code_block_started = not self.code_block_started
        if '`' in s:    # code segment
            parts = s.split('`')
            if len(parts) % 2 == 0:
                print('Error: odd number of ` in one line. ')
                print('Problem line:', s)
                sys.exit(1)
            s = ''.join([x + y for x, y in zip(parts[:-1], cycle(['<code>', '</code>']))]) + parts[-1]
        return s

def main():
    args = parseArgs()
    with open(args.output, 'w') as html:
        def write(*args, **kw):
            print(*args, file = html, **kw)
        # write('<!DOCTYPE html>')
        write('<html><body>')
        try:
            with open(args.input, 'r', encoding = 'utf-8') as md:
                translator = Translator()
                for line in md:
                    write(translator.translateLine(line))
        except FileNotFoundError:
            print('Please run python -m md2html -h')
            return
        write('</body></html>')
    print('Done. Written to', args.output)

def parseArgs():
    parser = argparse.ArgumentParser(description = 'Convert markdown to html', epilog = __doc__)
    parser.add_argument('--input', '-i', type = str, default = 'src.md', help = 'input markdown file. Default: src.md')
    parser.add_argument('--output', '-o', type = str, default = 'build.html', help = 'output html file. Default: build.html')
    return parser.parse_args()

if __name__ == '__main__':
    main()
    sys.exit(0)
