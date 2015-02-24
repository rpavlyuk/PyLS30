'''
Created on Feb 22, 2015

@author: rpavlyuk
'''

from LS30Util import Config
import json

'''
Format integer into 3-digit hex number
'''
def hex3(n):
    return "0x%s"%("00000000%x"%(n&0xffffffff))[-3:]

'''
Format integer into 3-digit hex number and substitute hex-digits with LS-30 ones
'''
def hex3_encoded(n):
    
    hex_str = hex3(n)
    
    hexCodesFile = open(Config.getCodeTableHex())
    hexCodesJSON = json.load(hexCodesFile)
    
    new_hex_str = ""
    
    for hex_chr in hex_str:
        if str(hex_chr) != 'x':
            new_hex_chr = hexCodesJSON[str(hex_chr)]
        else:
            new_hex_chr = hex_chr
        new_hex_str += str(new_hex_chr)
        
    return new_hex_str


'''
Format integer into 2-digit hex number
'''
def hex2(n):
    return "0x%s"%("00000000%x"%(n&0xffffffff))[-2:]

'''
Format integer into 3-digit hex number and substitute hex-digits with LS-30 ones
'''
def hex2_encoded(n):
    
    hex_str = hex2(n)
    
    hexCodesFile = open(Config.getCodeTableHex())
    hexCodesJSON = json.load(hexCodesFile)
    
    new_hex_str = ""
    
    for hex_chr in hex_str:
        if str(hex_chr) != 'x':
            new_hex_chr = hexCodesJSON[str(hex_chr)]
        else:
            new_hex_chr = hex_chr
        new_hex_str += str(new_hex_chr)
        
    return new_hex_str
        
        
    
    