# Growth of every issue body

Source: every saved version of each issue body (`step2/raw-all/`), by `scripts/growth.py`. "At first PR" is the body as it stood when the first PR for the issue opened. Stub drafts of 10 words or fewer, such as "Draft. Filled in next.", are skipped.

| kind | n | median first version | median at first PR | median final | median growth before work (x) |
|---|---|---|---|---|---|
| devloop | 17 | 299 | 356 | 424 | 1.0 |
| eval | 17 | 702 | 918 | 972 | 1.3 |
| feature | 46 | 383.0 | 808.0 | 808.0 | 1.4 |
| fix | 19 | 327 | 347 | 347 | 1.0 |
| recording | 9 | 362 | 438 | 438 | 1.0 |
| spike | 13 | 446 | 705 | 705 | 1.1 |
| all | 121 | 361 | 561 | 578 | 1.1 |

Largest growth before work: [(156, 437, 3378), (60, 254, 2794), (77, 156, 2568), (53, 383, 2769), (209, 840, 3213), (66, 170, 1924), (55, 307, 1484), (64, 151, 1328)]
Issues that at least doubled before work: 27 of 121
Issues that grew after their first PR: [(266, 1035, 2740), (209, 3213, 7042), (76, 1016, 2452), (177, 918, 1092), (75, 199, 1164), (63, 183, 226), (129, 1194, 1763)]
