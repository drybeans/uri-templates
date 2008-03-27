import re
lines = file("draft-gregorio-uritemplate-02.txt", "r").readlines()

vars_regex = re.compile(r"^\s*\|")
vars_txt = [[w.strip() for w in l.strip().split('|')][1:3] for l in lines if vars_regex.search(l)]
vars = {}
for (key, value) in vars_txt:
    if value and "[" == value[0]:
        vars[key] = eval(value) 
    else:
        vars[key] = eval('u"""%s"""' % value) 

begin = [i for (i, line) in enumerate(lines) if line.startswith("   ----") > 0][0]

got_template = False
template = ""
expansion = ""
tests = []
for index in range(begin+1, len(lines)):
    if lines[index].startswith("   ----"):
        break
    if lines[index].startswith("   "):
        line = lines[index].strip()
        if (line):
            if got_template:
                expansion = line
                got_template = False
                tests.append((template, expansion))
            else:
                template = line
                got_template = True 

if __name__ == "__main__":
    import unittest
    from work.template_parser import URITemplate  
    
    class Test(unittest.TestCase):
        def test(self):
            for (template, expected) in tests:
                t = URITemplate(template)
                expanded = t.sub(vars)
                self.assertEqual(expanded, expected)

    unittest.main()

