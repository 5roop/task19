# task19
Extracting non-textuals from ParlaMint-{HR,BA,RS}

## 2022-11-17T09:06:33

Idea: open a component file. For every utterance, reconstruct segments into full utterance. Extract non-textual elements. Reconstruct and renumber the component.

All the targets: moved to [](000_triggers.txt).

The RegEx patterns have been written and sequenced in proper order.

To discuss:
* I have the option of not splitting on sentences this time. Should I go for unsplit utterances? -> ask Tomaž! Yes, do not split.

To add:
* (NASTAVAK NAKON STANKE U 9,45 SATI)

## 2022-11-22T10:21:03

As of now the component-level fixer works marvelously. Next step: running it on all the datasets.

## 2022-11-22T13:54:58

I found a few more bugs, but it was finally sucessfully ran on all the three branches. Now I'll research if the add common content was done correctly.