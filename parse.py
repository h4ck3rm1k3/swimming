#.contenttext > hr:nth-child(17)
#.//*[@id='centercolumn']/div[3]/div[2]/p[5]/strong
#.more_info>strong
import glob

from lxml import etree

parser = etree.HTMLParser()
import re

def rec(y, indent="\t\t"):
    #print indent +"REC:",etree.tostring(y, pretty_print=True, method="html")
    #print indent + "Childtag:'%s'" % y.tag
    #print indent + "Childtext:'%s'" % y.text

    if y.text:
        m = re.match(r"(.+\@.+)",y.text)
        if m :
            print y.text, m.groups()

    for z in y :
        rec(z,indent + "\t")
    
def proc(y1):
    z = 0    
    state =0

    for y in y1:
        s = etree.tostring(y, pretty_print=True, method="html").rstrip()
        
#        print "CHECK", s
        if s=='<!-- CONTENT START -->':
            state=1           
            continue
        elif s=='<!-- CONTENT END -->':
            return 
        elif re.match(r'<p><strong>\d+\) <span onclick=\"location\.href',s):
            #print "Begin \'%s\'" % s
            state = "BEGIN"
        elif s.startswith('<script type="text/javascript">'):
            continue
        elif s.startswith('<p class="more_info"><strong>Record Last Updated:'):
            state="LASTUPDATE"
        elif s.startswith('<p class="more_info"><a href="placswimmod.php'):
            state="MOD"
            continue
        elif s.startswith('<p class="more_info">&#160;</p>'):
            state="MOAR"
        elif s.startswith('<hr>'):
            state="FIN"
            continue
        elif s.startswith('<p class="more_info"><strong>WebSite: </strong>'):
            state="WEBSITE"
        else:
            #print "\tOTHER",s
            pass

        a = 0 
        for c in y:

            #print "Child4:",etree.tostring(c, pretty_print=True, method="html")
            #print "Check4",c.tag, c.text

            if c.tag == 'strong':
                if a == 0 :                    
                    for d in c :
                        if d.tag == 'span':
                            #for e in d:
                            #print "\t\tLocation:",d.text
                            rec(d)
                        else:
                            rec(d)
                    rec(c)
                else:
                    rec(c)
            else:
                rec(c)

            a = a + 1               
        z = z +1 

def scan():
    for x in glob.glob("data2/FINKSBURG_MD"):
        #print "FILE",x
        f = open(x)
        l = ""
        #tree = etree.parse(f)
        tree   = etree.parse(f, parser)
        #for y in f.readlines():
        #    l = l + y
        f.close()
        r = tree.xpath(".//*[@id=\'centercolumn\']/div/div[@class='contenttext']")
        for y in r:
            proc(y)

scan()


