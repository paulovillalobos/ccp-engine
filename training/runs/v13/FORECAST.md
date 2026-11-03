# v13 forecast, committed before v13 answers (D67)

Made on 2026-11-03, before v13 was trained, in answer to Paulo's «so is this training going to make AMALIA … very pro in this
domain?», and kept unchanged here. v13 is graded against it: tools/measure_rule_readings_v13.py on data-v13's measured sets
(protocol 0.4, v13 decoding with --quotes text) and round 9 of the rules factory (FROUNDS[9], the real law).

| measure | v12 (measured, protocol 0.3) | v13 forecast (0.4 + quote grammar) | Reader B (0.4, BEFORE) |
|---|---|---|---|
| sealed articles settled | 55.2 % | 75–85 % | 89.6 % |
| dev «não tipável» answered right (of 25) | 2 | 18–23 | 24 |
| dev answers the checker refuses (of 104) | 46 | 5–15 | 0 |
| dev answers quoting words that are not in the text | 11 | 0 (the grammar forbids them) | — |
| real law, round 9: valid readings (of 12) | 1 (round 8) | 6–10 | answering |
| real law, round 9: rules settled with Reader B (of 12) | 0 (round 8) | 4–8 | — |

The bar set for a showcase («wow»): on the real law at least 10 of 12 readings valid, at least 8 of 12 settled with Reader B
blind, and no invented quote. v13 reaches it only at the top of its range; the expected path is v14, trained on round 9's
real-law errors.

The Reader B column was measured after the forecast (training/runs/v13/BEFORE): under the protocol 0.4 Reader B went from 81.2 %
to 89.6 % on sealed and from 20 dev misses to 6, which the forecast assumed for the prompt fixes (15 of Reader B's 20 misses were
the prompt's or the checker's). v12's reading of the same sets with the protocol 0.4 and the grammar is in BEFORE beside it.
