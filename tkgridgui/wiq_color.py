from __future__ import print_function

"""
Define a color system similar to YIQ called WIQ where W is the
W3 luminance instead of the YIQ grey level.

Relative Luminance    see: https://www.w3.org/WAI/GL/wiki/Relative_luminance
Contrast Ratio WCAG 2 see: https://www.w3.org/WAI/GL/wiki/Contrast_ratio

YIQ: used by composite video signals (linear combinations of RGB)
Y: perceived grey level (0.0 == black, 1.0 == white)
I, Q: color components I=-0.6 to +0.6,  Q=-0.52 to +0.52

WIQ: applies to the WCAG 2 color contrast requirements AA and AAA
W : W3 Luminance
I, Q: color components I=-0.6 to +0.6,  Q=-0.52 to +0.52
"""

import colorsys

def rgb_to_wiq(r, g, b):
    '''r,g,b are fractions (0-1) for red, green, blue'''
    w = w3_luminance(r, g, b) # replace y in yiq with w3_luminance
    i = 0.60*r - 0.28*g - 0.32*b # taken directly from yiq def
    q = 0.21*r - 0.52*g + 0.31*b # taken directly from yiq def
    return (w, i, q)

def wiq_to_rgb(w, i, q, tol=1.0/2560.0):
    """
    WIQ: applies to the WCAG 2 color contrast requirements AA and AAA
    w : W3 Luminance
    i, q: color components as defined by YIQ color model
    
    tol = tolerance on iterative solution (use yiq as basis for iteration)
    """
    y = w
    r, g, b = colorsys.yiq_to_rgb( y, i, q)
    w3lum = w3_luminance(r, g, b)
    
    if w3lum > w:
        ymin = 0.0
        ymax = w
    else:
        ymin = w
        ymax = 1.0
    
    diff = abs(w3lum - w)
    #print('w3lum=%g, y=%g, w=%g, diff=%g'%(w3lum, y, w, diff), '  ymin=%g, ymax=%g'%(ymin, ymax))
    count = 0
    while abs(diff)>tol and count<20:
        count += 1
        y = (ymin + ymax) / 2.0
        r, g, b = colorsys.yiq_to_rgb( y, i, q)
        w3lum = w3_luminance(r, g, b)
        diff = w3lum - w
        
        if diff > 0.0:
            ymax = y
        else:
            ymin = y
    
    # dropped through loop. Check for solution.
    fmin = 0.0
    fmax = 1.0
    adj_str = ''
    if abs(diff)>tol:
        rref,gref,bref = r,g,b
        count = 0
        
        if w3lum > w: # can't lower y any more to achieve low luminance
            # leave r,g,b ratios alone, but start darkening values
            adj_str = 'Lowering r,g,b' + str( (r, g, b) )
            while abs(diff)>tol and count<20:
                count += 1
                f = (fmin + fmax) / 2.0
                r, g, b = f*rref, f*gref, f*bref
                w3lum = w3_luminance(r, g, b)
                diff = w3lum - w
                
                if diff > 0.0:
                    fmax = f
                else:
                    fmin = f
        else: # can't raise y any more to achieve higher luminance
            # start moving r,g,b values higher while maintaining their relative values
            adj_str = 'Raising r,g,b' + str( (r, g, b) )
            while abs(diff)>tol and count<20:
                count += 1
                f = (fmin + fmax) / 2.0
                r, g, b = rref+f*(1.0-rref), gref+f*(1.0-gref), bref+f*(1.0-bref)
                w3lum = w3_luminance(r, g, b)
                diff = w3lum - w
                
                if diff > 0.0:
                    fmax = f
                else:
                    fmin = f
                
            
    if abs(diff)>tol:        
        print('wiq_to_rgb ERROR...', adj_str)
        print('  ... w3lum=%g, y=%g, w=%g, diff=%g'%(w3lum, y, w, diff), '  fmin=%g, fmax=%g'%(fmin, fmax))
        print('  ... (r,g,b) =',(r,g,b))
        
    return (r, g, b)
        

def w3_luminance(r,g,b): # float values of r,g,b
    """Relative Luminance per: https://www.w3.org/WAI/GL/wiki/Relative_luminance"""
    def condition( c ): # c is r,g or b
        if c<0.03928:
            val = c / 12.92
        else:
            val = ((c+0.055)/1.055)**2.4
        return val
            
    return 0.2126*condition(r) + 0.7152*condition(g) + 0.0722*condition(b)

def w3_contrast( webStr_1, webStr_2 ):
    """per WCAG 2  see: https://www.w3.org/WAI/GL/wiki/Contrast_ratio
    
    Relative Luminance per: https://www.w3.org/WAI/GL/wiki/Relative_luminance
    AA  requires 4.5:1 contrast ratio for normal text
    AA  requires   3:1 contrast ratio for large  text
    AAA requires   7:1 contrast ratio for normal text
    AAA requires 4.5:1 contrast ratio for large  text

    Large Text is >=14 point, 18.66px and bold OR >=18 pt, 24px
    """
    L1 = w3_luminance( *hex_to_rgbfloat(webStr_1) )
    L2 = w3_luminance( *hex_to_rgbfloat(webStr_2) )
    
    if L1>L2:
        return (L1 + 0.05) / (L2 + 0.05)
    else:
        return (L2 + 0.05) / (L1 + 0.05)

def hex_to_rgbfloat(hex_str):
    """Returns a tuple representing the given hex string as RGB.
    
    >>> hex_to_rgbfloat('CC0000')
    (204, 0, 0)
    """
    if hex_str.startswith('#'):
        hex_str = hex_str[1:]
    ans_tup = tuple([int(hex_str[i:i + 2], 16) for i in xrange(0, len(hex_str), 2)])
    #print 'for',hex_str,'ans_tup=',ans_tup
    return tuple([round(float(c)/255, 8) for c in ans_tup])


def rgbfloat_to_hex(rgb_float):
    """Converts an rgb tuple to hex string for web.
    
    >>> rgbfloat_to_hex((0.8, 0.0, 0.0))
    '#CC0000'
    """
    rgb = tuple([int(c*255) for c in rgb_float])
    return '#' + ''.join(["%0.2X" % c for c in rgb])

if __name__=="__main__":
    
    print( "hex_to_rgbfloat('#CC0000') =",hex_to_rgbfloat('#CC0000') )

    print( "rgbfloat_to_hex((0.8, 0.0, 0.0)) =", rgbfloat_to_hex((0.8, 0.0, 0.0)) )
    
    print("rgb_to_wiq(0.8, 0.0, 0.0) =", rgb_to_wiq(0.8, 0.0, 0.0))
    
    print()
    #print("Start: wiq_to_rgb(0.12837369224064482, 0.48, 0.168)")
    rgb = wiq_to_rgb(0.12837369224064482, 0.48, 0.168)
    print("wiq_to_rgb(0.12837369224064482, 0.48, 0.168) =", rgb )
    print('Get Hex String of WIQ value above = rgbfloat_to_hex(rgb) =', rgbfloat_to_hex(rgb))
