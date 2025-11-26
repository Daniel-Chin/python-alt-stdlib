def english(data):
    (arab,id)=data
    if id>=3:
        id-=3
        arab-=1
    if id==1:
        if arab//10==0:
            return ''
        else:
            if arab%10==0:
                return 'ty'
            else:
                return 'ty-'
    if id==0:
        return   {9:('nin'),\
                  8:('eigh'),\
                  7:('seven'),\
                  6:('six'),\
                  5:('fif'),\
                  4:('for'),\
                  3:('thir'),\
                  2:('twen'),\
                  1:('one'),\
                  0:('')}[arab//10]
    if id==2:
        return   {9:('nine'),\
                  8:('eight'),\
                  7:('seven'),\
                  6:('six'),\
                  5:('five'),\
                  4:('four'),\
                  3:('three'),\
                  2:('two'),\
                  1:('one'),\
                  0:('')}[arab%10]+' '
