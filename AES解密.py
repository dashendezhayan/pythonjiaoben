from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import binascii,base64

def en_code(text,key,iv):             #加密
    cipher=AES.new(key,AES.MODE_CBC,iv)
    padtext = pad(text, 16, style='pkcs7')  # 对数据进行填充

    cipherText = cipher.encrypt(padtext)
    return cipherText

def de_code(text,key,iv):             #解密
    decrypter = AES.new(key, AES.MODE_CBC, iv)
    plaintext = decrypter.decrypt(text)
    unpadtext = unpad(plaintext, 16, 'pkcs7')

    #print('plaintext',binascii.b2a_hex(plaintext),plaintext[-1])
    print(unpadtext)
    return unpadtext
    # print(plaintext)
    # return plaintext
    #return binascii.b2a_hex(plaintext)
key=b'797864576F375A31424361324269664D'
iv=b'424361324269664D'
# key=b'42644f344d537878517033326b507754'
# iv=b'517033326b507754'
# key=b'54'
# iv=b'517033326b507754'

#cipher=AES.new(newkey,AES.MODE_CBC,iv)
while True:
    mode=input('请输入模式（0：解密，1：加密）：')
    text=input("请输入数据：")
    text=text.replace(' ','')

    text = bytes.fromhex(text)

    print('转换数据',text,len(text))
    if mode=='0':
        de_text=de_code(text,key,iv)
        print(de_text)
        print("解密后数据为：",binascii.b2a_hex(de_text).decode())
    elif mode=='1':
        en_text=en_code(text,key,iv)
        print("加密后数据为：",binascii.b2a_hex(en_text).decode())
    else:
        print("请输入正确的数字！")
    print(' ')




# text=b'\x00\x01\x02\x03'
# padtext=pad(text,16,style='pkcs7')    #对数据进行填充
# cipherText=cipher.encrypt(padtext)
# print('填充后的待加密数据：',padtext)
# print('加密数据：',binascii.b2a_hex(cipherText).decode())
#
# decrypter=AES.new(key,AES.MODE_CBC,iv)
# plaintext=decrypter.decrypt(cipherText)
# unpadtext=unpad(plaintext,16,'pkcs7')     #因为解密后不会对数据填充的部分删减，所以需要unpad
# print('解密后未处理的数据',plaintext)
# print('解密后数据',unpadtext)