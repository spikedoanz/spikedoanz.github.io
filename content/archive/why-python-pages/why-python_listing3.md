```
Listing 3. Metaclass Function
def copy_instance(toclass, fromdict):
# Initialize a class object of given type from a conformant dictionary.
    class_sig = toclass.__dict__.keys(); class_sig.sort()
    dict_keys = fromdict.keys(); dict_keys.sort()
    common = intersect(class_sig, dict_keys)
    if 'typemap' in class_sig:
    class_sig.remove('typemap')
    if tuple(class_sig) != tuple(dict_keys):
        print "Conformability error"
#       print "Class signature: " + `class_sig`
#       print "Dictionary keys: " + `dict_keys`
        print "Not matched in class signature: " + `setdiff(class_sig, common)`
        print "Not matched in dictionary keys: " + `setdiff(dict_keys, common)`
        sys.exit(1)
    else:
    for x in dict_keys:
        setattr(toclass, x, fromdict[x])
```
