'''
For an NYU person, convert their netID to profile.  
'''
import webbrowser
from interactive import inputChin

# MAGIC = 'https://globalhome.nyu.edu/group/people/profile?user=%s'
MAGIC = 'https://globalhome.nyu.edu/people/search/%s'

def netid2profile(netid):
    webbrowser.open(MAGIC % netid, new=2)

if __name__ == '__main__':
    print(__doc__)
    netid = inputChin('netid = ', 'mc7214')
    netid2profile(netid)
