inp = open('haproxy.cfg', 'r')
outp = open('haproxy.cfg.new', 'w')

for line in inp.readlines():
    if line.startswith('listen '):
        _, name, binding = line.split()
        outp.write('frontend %s-frontend\n' % name)
        outp.write('    bind %s\n' % binding)
        outp.write('    default_backend %s-backend\n' % name)
        outp.write('\n')
        outp.write('backend %s-backend\n' % name)
    else:
        outp.write(line)

inp.close()
outp.close()
