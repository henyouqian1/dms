from struct import *

def readBlob(io):
	p = io.read(4)
	size = unpack('i', p)[0]
	b = io.read(size)
	return b, size
	
def readUtf8(io):
	p = io.read(4)
	size = unpack('i', p)[0]
	str = io.read(size)
	return str
    
def readChar(io):
	p = io.read(1)
	v = unpack('c', p)[0]
	return v

def readShort(io):
	p = io.read(2)
	v = unpack('h', p)[0]
	return v
	
def readInt(io):
	p = io.read(4)
	v = unpack('i', p)[0]
	return v
	
def readFloat(io):
	p = io.read(4)
	v = unpack('f', p)[0]
	return v

def writeChar(io, n):
	msg = pack('c', n)
	io.write(msg)
	
def writeShort(io, n):
	msg = pack('h', n)
	io.write(msg)
	
def writeInt(io, n):
	msg = pack('i', n)
	io.write(msg)
    
def writeFloat(io, n):
	msg = pack('f', n)
	io.write(msg)

def writeBlob(io, b, size):
	writeInt(io, size)
	fmt = "%is" % size
	msg = pack(fmt, b)
	io.write(msg)

def writeUtf8(io, str):
	io.write(str)
	io.write('\0')

def writeWString(io, uStr):
	s = uStr.encode('utf-8')
	io.write(s)
	io.write('\0')