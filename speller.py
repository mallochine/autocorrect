#!/usr/bin/env python

# This is pretty heavily inspired by Norvig's spell corrector:
# http://www.norvig.com/spell-correct.html

import os
import collections
import sys
import re

# def words(text): return re.findall('[a-z]+', text)
# Norvig's regex '[a-z]+' here doesn't quite work, because it ignores symbols
# like ',' which are actually quite important in the shell world.
def words(text): return re.split(';| |\n', text)

def train(features):
  model = collections.defaultdict(lambda: 1)
  for f in features:
    if f.startswith('#'):
      continue
    model[f] += 1
  return model

NWORDS = train(words(file(os.environ['HISTFILE']).read()))
alphabet = '|abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def edits1(word):
  splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
  deletes    = [a + b[1:] for a, b in splits if b]
  transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
  replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
  inserts    = [a + c + b     for a, b in splits for c in alphabet]
  # TODO: also generate 'compgen' for inserts.
  return set(deletes + transposes + replaces + inserts)

def known(words): return set(w for w in words if w in NWORDS)

def correct(cmd):
  # Don't consider commands 1 characters or less.
  if len(cmd) <= 1: return cmd


  # XXX: Norvig's previous command. Removed edits2. We generally don't care
  # about edit distance of 2.
  # candidates = known([cmd]) or known(edits1(cmd)) or known_edits2(cmd) or [cmd]
  candidates = known([cmd]) | known(edits1(cmd)) | set([cmd])
  return max(candidates, key=NWORDS.get)

def main():
  if len(sys.argv) < 2:
    print "Need a string as argument."
    return
  cmd = sys.argv[1]
  result = ""
  for word in cmd.split():
    result += correct(word) + " "
  print result[:-1]

if __name__ == "__main__":
  main()
