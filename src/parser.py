# -*- coding: utf-8 -*-


from bitstring import BitStream, BitArray

class Type:
  def __init__(self, name, bits):
    self.name = name
    self.bits = bits
  
  def parse(self, data):
    "Implement this"

  def toXML(self, indent):
    "Implement this"

class PrimitiveType(Type):
  def __init__(self, type, name, bits):
    Type.__init__(self, name, bits)
    self.type = type
  def toXML(self, indent):
    attributes = {}
    
    if len(self.name) > 0:
      attributes['name'] = self.name
    
    attributes['type'] = self.type

    return '<primitive %s />' % (' '.join(map(lambda (n, v): '%s="%s"' % (n, v), attributes.iteritems())),)

class int8(PrimitiveType):
  def __init__(self, name = ''):
    PrimitiveType.__init__(self, 'Int8', name, 8)
  def parse(self, data):
    return (self.name, data.stream.read('int:8'))
    
class uint8(PrimitiveType):
  def __init__(self, name = ''):
    PrimitiveType.__init__(self, 'UInt8', name, 8)
  def parse(self, data):
    return (self.name, data.stream.read('uint:8'))
    

class array(Type):
  def __init__(self, name, inner_type, length):
    Type.__init__(self, name, length * inner_type.bits )
    self.name = name
    self.length = length
    self.inner_type = inner_type
  def parse(self, data):
    result = []
    for idx in range(0,self.length):
      result.append(self.inner_type.parse(data))
    return (self.name, result);
  def toXML(self, indent):
    self_indentation =  (indent)*'\t'
    internal_indentation =  (indent + 1)*'\t'
    
    return '<array name="%s" length="%s">\n%s%s\n%s</array>' \
      % (self.name, self.length, internal_indentation, self.inner_type.toXML(indent + 1), self_indentation)



class struct(Type):
  def __init__(self, name, inner_types):
    bits = 0
    for t in inner_types:
      bits = bits + t.bits
    Type.__init__(self, name, bits )
    
    self.inner_types = inner_types
  def parse(self, data):
    result = []
    for type in self.inner_types:
      result.append(type.parse(data))
    return result;
  def toXML(self, indent):
    self_indentation =  (indent)*'\t'
    internal_indentation =  (indent + 1)*'\t'
    
    return '<struct name="%s">\n%s%s\n%s</struct>' \
      % (self.name, internal_indentation, ('\n' + internal_indentation).join(map(lambda x: x.toXML(indent+1), self.inner_types)), self_indentation)




s = struct('complex', [uint8('size'), array('fourBytes', int8(), 4)]);

class Data:
  def __init__(self):
    self.stream = BitStream(bytes='31234')
  

data = Data()


print s.toXML(0)

print s.parse(data)










