import os

class FilePart:
 """A view of a part of a file. Can be used like a regular file"""
 def __init__(self, file, offset=0, size=-1):
  if size < 0:
   file.seek(0, os.SEEK_END)
   size = file.tell() - offset
  self.file = file
  self.offset = offset
  self.size = size
  self.pos = 0

 def seek(self, pos, ref=os.SEEK_SET):
  if ref == os.SEEK_SET:
   self.pos = pos
  elif ref == os.SEEK_CUR:
   self.pos += pos
  elif ref == os.SEEK_END:
   self.pos = self.size + pos
  pos = min(max(pos, 0), self.size)

 def tell(self):
  return self.pos

 def read(self, size=-1):
  if size < 0:
   size = self.size
  self.file.seek(self.offset + self.pos)
  data = self.file.read(min(size, self.size - self.pos))
  self.pos += len(data)
  return data


class ChunkedFile:
 def __init__(self, generateChunks, size=-1):
  self._generateChunks = generateChunks
  self._size = size
  self.reset()

 def reset(self):
  self._chunks = None
  self._pos = 0
  self._buffer = ''

 def read(self, n=-1):
  if self._chunks == None:
   self._chunks = self._generateChunks()

  try:
   while n < 0 or len(self._buffer) < n:
    self._buffer += next(self._chunks)
  except StopIteration:
   if self._size >= 0 and self._pos + len(self._buffer) < self._size:
    raise Exception('Not enough bytes returned')
  if self._size >= 0 and self._pos + len(self._buffer) > self._size:
   raise Exception('Too many bytes returned')

  contents = self._buffer if n < 0 else self._buffer[:n]
  self._pos += len(contents)
  self._buffer = self._buffer[len(contents):]
  return contents

 def tell(self):
  return self._pos
