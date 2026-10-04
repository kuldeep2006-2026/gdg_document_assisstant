# Evaluation results (retriever: tfidf, top-k: 3)


## Config A: words 100/20 (11 chunks, threshold 0.1)

| # | Question | Best score | Evidence retrieved? | Answer (start) |
|---|---|---|---|---|
| 1 | What are the opening hours of the Student Support Desk? | 0.31 | yes | (retrieval-only mode, best passage) GDG-USAR Student Handbook Sample s |
| 2 | Who should I contact about fee payment issues? | 0.25 | yes | (retrieval-only mode, best passage) correct university office for comm |
| 3 | Do all workshops provide certificates? | 0.21 | yes | (retrieval-only mode, best passage) desk can guide students to the app |
| 4 | What should a project README contain? | 0.26 | yes | (retrieval-only mode, best passage) desk can guide students to the app |
| 5 | What does AI_USAGE.md need to state? | 0.20 | yes | (retrieval-only mode, best passage) reason for the final choice. If AI |
| 6 | Does registering for an event guarantee entry? | 0.25 | yes | (retrieval-only mode, best passage) but it does not replace the requir |
| 7 | Can the Student Support Desk approve attendance exempti | 0.37 | yes | (retrieval-only mode, best passage) in removal from the activity. Phot |
| 8 | My learning portal is broken and I also want a fee refu | 0.23 | yes | (retrieval-only mode, best passage) correct university office for comm |
| 9 | What is the date of the next GDG event? | 0.12 | n/a (should refuse): ANSWERED | (retrieval-only mode, best passage) For fee payment issues, they shoul |
| 10 | Who is the current community lead? | 0.25 | n/a (should refuse): ANSWERED | (retrieval-only mode, best passage) sample handbook does not specify t |
| 11 | What is the capital of France? | 0.00 | n/a (should refuse): refused | I could not find this in the document. |

Evidence hit rate: 8/8 | Unanswerable refused: 1/3

## Config B: words 300/60 (4 chunks, threshold 0.1)

| # | Question | Best score | Evidence retrieved? | Answer (start) |
|---|---|---|---|---|
| 1 | What are the opening hours of the Student Support Desk? | 0.22 | yes | (retrieval-only mode, best passage) GDG-USAR Student Handbook Sample s |
| 2 | Who should I contact about fee payment issues? | 0.15 | yes | (retrieval-only mode, best passage) GDG-USAR Student Handbook Sample s |
| 3 | Do all workshops provide certificates? | 0.15 | yes | (retrieval-only mode, best passage) in removal from the activity. Phot |
| 4 | What should a project README contain? | 0.16 | yes | (retrieval-only mode, best passage) in removal from the activity. Phot |
| 5 | What does AI_USAGE.md need to state? | 0.14 | yes | (retrieval-only mode, best passage) 4. Project Submissions For communi |
| 6 | Does registering for an event guarantee entry? | 0.15 | yes | (retrieval-only mode, best passage) 4. Project Submissions For communi |
| 7 | Can the Student Support Desk approve attendance exempti | 0.29 | yes | (retrieval-only mode, best passage) in removal from the activity. Phot |
| 8 | My learning portal is broken and I also want a fee refu | 0.15 | yes | (retrieval-only mode, best passage) GDG-USAR Student Handbook Sample s |
| 9 | What is the date of the next GDG event? | 0.10 | n/a (should refuse): refused | I could not find this in the document. |
| 10 | Who is the current community lead? | 0.16 | n/a (should refuse): ANSWERED | (retrieval-only mode, best passage) in removal from the activity. Phot |
| 11 | What is the capital of France? | 0.00 | n/a (should refuse): refused | I could not find this in the document. |

Evidence hit rate: 8/8 | Unanswerable refused: 2/3

## Config C: by section (8 chunks, threshold 0.1)

| # | Question | Best score | Evidence retrieved? | Answer (start) |
|---|---|---|---|---|
| 1 | What are the opening hours of the Student Support Desk? | 0.29 | yes | (retrieval-only mode, best passage) 1. Student Support Desk The Studen |
| 2 | Who should I contact about fee payment issues? | 0.25 | yes | (retrieval-only mode, best passage) 1. Student Support Desk The Studen |
| 3 | Do all workshops provide certificates? | 0.20 | yes | (retrieval-only mode, best passage) 6. Frequently Asked Questions Can  |
| 4 | What should a project README contain? | 0.21 | yes | (retrieval-only mode, best passage) 6. Frequently Asked Questions Can  |
| 5 | What does AI_USAGE.md need to state? | 0.17 | yes | (retrieval-only mode, best passage) 4. Project Submissions For communi |
| 6 | Does registering for an event guarantee entry? | 0.24 | yes | (retrieval-only mode, best passage) 5. Event Registration and Conduct  |
| 7 | Can the Student Support Desk approve attendance exempti | 0.37 | yes | (retrieval-only mode, best passage) 6. Frequently Asked Questions Can  |
| 8 | My learning portal is broken and I also want a fee refu | 0.23 | yes | (retrieval-only mode, best passage) 1. Student Support Desk The Studen |
| 9 | What is the date of the next GDG event? | 0.11 | n/a (should refuse): ANSWERED | (retrieval-only mode, best passage) 7. Information Not Specified Here  |
| 10 | Who is the current community lead? | 0.26 | n/a (should refuse): ANSWERED | (retrieval-only mode, best passage) 7. Information Not Specified Here  |
| 11 | What is the capital of France? | 0.00 | n/a (should refuse): refused | I could not find this in the document. |

Evidence hit rate: 8/8 | Unanswerable refused: 1/3
