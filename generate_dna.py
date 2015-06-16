#!/usr/bin/python
# encoding: utf-8

import sys
import re

from workflow import Workflow, ICON_WEB, web


__version__ = '0.2'



dna_dict = {"A":"T", 
            "T":"A",
            "a":"t",
            "t":"a",
            "G":"C",
            "C":"G",
            "g":"c",
            "c":"g",
            "N":"N",
            "n":"n"}

def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`

    # Your imports here if you want to catch import errors
    import random

    # Get args from Workflow as normalized Unicode
    args = wf.args
    args[0] = args[0][:-1].replace("\n","")
    if args[0].isdigit():
        dna_len = int(args[0])
        if dna_len <= 1000:
            dna = ''.join(random.choice("ATCG") for _ in range(dna_len))
            # Add an item to Alfred feedback
            wf.add_item(u'Random DNA Uppercase', dna, arg=dna, valid=True, icon="dna.icns")
            wf.add_item(u'Random DNA Lowercase', dna.lower(), arg=dna.lower(), valid=True, icon="dna.icns")
    elif re.match("^[ATCG]+$", args[0]):
        from translate import translate
        complement = ''.join([dna_dict[x] for x in args[0]])
        wf.add_item(u'Complement', complement, arg=complement, valid=True, icon="dna.icns")
        wf.add_item(u'Reverse Complement', complement[::-1], arg=complement, valid=True, icon="dna.icns")
        
        rna = args[0].replace("T","U").replace("t","u")
        wf.add_item(u'RNA',rna, arg=rna, valid=True, icon="dna.icns")
        
        protein = translate(args[0])
        wf.add_item(u'Protein',protein, arg=protein, valid=True, icon="dna.icns")
        
        freq = '; '.join(["%s: %s" % (x,args[0].upper().count(x)) for x in ["A","T","C","G", "N"]])
        n_free = args[0].replace("N","")
        AT_freq = round((args[0].count("A")*1.0 + args[0].count("T"))/len(n_free)*100,2)
        GC_freq = round((args[0].count("G")*1.0 + args[0].count("C"))/len(n_free)*100,2)
        log.debug(AT_freq)
        freq += " | AT: {AT_freq}% ; GC: {GC_freq}%;".format(**locals())
        freq += " | Length: " + str(len(n_free))
        wf.add_item(u'Composition', freq)
    else:
        wf.add_item(u'Error', "String contains non-base characters", icon="dna.icns")

    # Send output to Alfred
    #log.debug(wf.send_feedback())
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'danielecook/seq-utilities',
        'version': __version__,
        'frequency': 7
        })
    if wf.update_available:
        # Download new version and tell Alfred to install it
        wf.start_update()
    log = wf.logger
    sys.exit(wf.run(main))

