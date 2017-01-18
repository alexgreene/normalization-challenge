Alex Greene
agreen13@calpoly.edu
516-660-1696


**Seatgeek Section Normalization Challenge**

To start, when reading a provided manifest, I wanted to store it in a way that would make working with it very simple. I decided to store it in a dictionary where the highest level keys are the numerical values associated with given section (ie. Field Level 43, Suite 43, Bleacher Left 43 would all be stored under the key '43'). One of the most consistent things about the test data is the presence of numbers, so I placed the most importance on numbers when designing the manifest.

From the other end, when normalizing a section, we must first try and extract a number from the section name so we have something to lookup in the manifest. Because the Citi Field data is mainly numbers, very little normalization was required to pass most of its tests very quickly. For the Dodger Stadium data, I would focus on one non-working section at a time and diagnose why it was not working. Because of the way my manifest is designed, for each test section provided as input, I can immediately find a set of several possible matching sections (based on number, of course). This made testing much easier! I could print out each possible match along with its respective score that I calculate for it. By comparing the scores I could fine tune them to get results I wanted.

By scores I just mean the measurements for each of my comparison strategies:

 1. similarity ratio provided by SequenceMatcher 
 2. number of words in common 
 3. if their first non-digits are the same

*I enjoyed this challenge and look forward to hearing your feedback. Thank you!*# normalization-challenge
