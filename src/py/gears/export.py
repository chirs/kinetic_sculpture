# http://jamesgregson.blogspot.com/2012/05/python-involute-spur-gear-script.html

def export_svg( px, py, filename, scale=1.0 ):
    """write output as svg, for laser-cutters, graphic design, etc.
    """
    out = open( filename, 'w' )
    
    minx = min( px )
    maxx = max( px )
    miny = min( py )
    maxy = max( py )
    cenx = (minx + maxx)/2.0
    ceny = (miny + maxy)/2.0
    sx = ( maxx - cenx )*1.1
    sy = ( maxy - ceny )*1.1
    
    minx = scale*(cenx - sx)
    maxx = scale*(cenx + sx)
    miny = scale*(ceny - sy)
    maxy = scale*(ceny + sy)
    
    out.write('<?xml version="1.0" standalone="no" ?>\n' )
    out.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
    out.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" x="%fpx" y="%fpx" width="%fpx" height="%fpx">\n' % (minx, miny, maxx-minx, maxy-miny) )
    out.write('<polyline style="fill:none;stroke:black;stroke-width:1" points="' );
    
    for i in range( 0, len(px) ):
        out.write( '%f,%f ' % ( scale*(px[i]+sx), scale*(py[i]+sy) ) )
    
    out.write('" />\n' ) 
    out.write('</svg>\n')
    out.close()

def export_dxf(px, py, filename, scale=1.0):
    """
    write output as dxf profile in x-y plane, for use with OpenSCAD
    """
    out = open( filename, 'w' )
    out.write('  0\n')
    out.write('SECTION\n')
    out.write('  2\n')
    out.write('HEADER\n')
    out.write('999\n')
    out.write('%s by gears.py\n' % filename )
    out.write('999\n')
    out.write('contact james.gregson@gmail.com for gears.py details\n')
    out.write('  0\n')
    out.write('ENDSEC\n')
    out.write('  0\n')
    out.write('SECTION\n')
    out.write('  2\n')
    out.write('TABLES\n')
    out.write('  0\n')
    out.write('ENDSEC\n')
    out.write('  0\n')
    out.write('SECTION\n')
    out.write('  2\n')
    out.write('BLOCKS\n')
    out.write('  0\n')
    out.write('ENDSEC\n')
    out.write('  0\n')
    out.write('SECTION\n')
    out.write('  2\n')
    out.write('ENTITIES\n')
    
    for i in range( 0, len(px)-1 ):
        out.write('  0\n')
        out.write('LINE\n')
        out.write('  8\n')
        out.write('  2\n')
        out.write(' 62\n')
        out.write('  4\n')
        out.write(' 10\n')
        out.write('%f\n' % (scale*px[i]))
        out.write(' 20\n')
        out.write('%f\n' % (scale*py[i]))
        out.write(' 30\n')
        out.write('0.0\n')
        out.write(' 11\n')
        out.write('%f\n' % (scale*px[i+1]))
        out.write(' 21\n')
        out.write('%f\n' % (scale*py[i+1]))
        out.write(' 31\n')
        out.write('0.0\n')
    
    
    out.write('  0\n')
    out.write('ENDSEC\n')
    out.write('  0\n')
    out.write('EOF\n')
    out.close()
