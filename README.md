## Wikipedia Scrapper

Given two english wikipedia pages url, it looks for a path between the two, through clickable links.
It implements a BFS algorithm.

#### Instruction to run

``` python pathFinder.py url1 url2 ```

#### Real Example

``` python pathFinder.py https://en.wikipedia.org/wiki/Mahatma_Gandhi https://en.wikipedia.org/wiki/United_States ```

It output the text of the clickable links path. The complexity of the implemented algorithm makes it performs poorly if more than two clicks needed.
