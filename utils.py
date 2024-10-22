from os import sep
import hashlib

def correct_path(path):
  return path.replace("/", sep)

def encrypt(text):
  return hashlib.md5(text.encode()).hexdigest()